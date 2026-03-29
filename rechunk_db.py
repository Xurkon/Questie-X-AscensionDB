import os
import re
import math

# Target database files
db_files = [
    r"Bronzebeard\AscensionItemDB.lua",
    r"Bronzebeard\AscensionNpcDB.lua",
    r"Bronzebeard\AscensionObjectDB.lua",
    r"Bronzebeard\AscensionQuestDB.lua",
    r"Zones\AscensionUiMapData.lua",
    r"Zones\AscensionZoneTables.lua"
]

LINES_PER_FILE = 5000

for file_path in db_files:
    if not os.path.exists(file_path):
        print(f"Skipping {file_path}, does not exist.")
        continue
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    pattern = re.compile(r'([\w\.]+)\s*=\s*(?:[\w\.]+\s*or\s*)?\{')
    
    # Track the tables we find
    tables_found = {}
    
    for match in pattern.finditer(content):
        # Determine base table name (e.g. AscensionDB.npcData -> npcData, AscensionZoneTables.uiMapIdToAreaId -> uiMapIdToAreaId)
        table_name = match.group(1).split('.')[-1]
        
        # We only care about root tables like npcData, itemData, uiMapData, etc.
        # AscensionDB itself isn't needed
        if table_name in ["AscensionDB", "AscensionZoneTables", "AscensionItemDB", "AscensionNpcDB", "AscensionObjectDB", "AscensionQuestDB", "AscensionUiMapData"]:
            continue
            
        start_idx = match.end()
        end_idx = start_idx
        bracket_count = 1
        
        while end_idx < len(content) and bracket_count > 0:
            c = content[end_idx]
            
            # Context-aware string/comment parsing
            if c == '"' or c == "'":
                quote = c
                end_idx += 1
                while end_idx < len(content):
                    if content[end_idx] == quote and content[end_idx-1] != '\\':
                        break
                    end_idx += 1
            elif content[end_idx:end_idx+2] == '--':
                while end_idx < len(content) and content[end_idx] != '\n':
                    end_idx += 1
            elif c == '{':
                bracket_count += 1
            elif c == '}':
                bracket_count -= 1
            
            end_idx += 1
            
        table_content = content[start_idx:end_idx-1].strip()
        
        if len(table_content) > 0:
            tables_found[table_name] = table_content
            print(f"[{file_path}] Found table: {table_name} (Length: {len(table_content)})")

    # If we found relevant tables, split them
    if tables_found:
        base_dir = os.path.dirname(file_path)
        split_dir = os.path.join(base_dir, "Split")
        os.makedirs(split_dir, exist_ok=True)
        
        # Clean old split files for this DB
        base_name = os.path.basename(file_path).replace(".lua", "")
        for f in os.listdir(split_dir):
            if f.startswith(base_name) and f.endswith(".lua"):
                os.remove(os.path.join(split_dir, f))
        
        file_index = 1
        current_chunk = []
        current_lines_count = 0
        depth = 0
        
        # Group tables into chunks
        # Because different tables might be parallel (e.g. uiMapData and zoneSort), we shouldn't mix them into the SAME variables in one huge data block easily.
        # Actually it's easier to write one table at a time into the file chunks.
        
        # The original code had an indentation error here, implying a missing loop.
        # Assuming the intent was to process each found table separately.
        for t_name, t_content in tables_found.items():
            lines = t_content.splitlines()

            chunk_state = {
                "file_index": 1,
                "current_chunk": [],
                "current_lines_count": 0,
                "depth": 0
            }
            
            def write_chunk(state):
                if len(state["current_chunk"]) == 0:
                    return
                chunk_file = os.path.join(split_dir, f"{base_name}_{t_name}_{state['file_index']}.lua") # Added t_name to filename
                with open(chunk_file, 'w', encoding='utf-8') as out:
                    out.write("-- AUTO GENERATED FILE! DO NOT EDIT!\n")
                    out.write("local _, addonTable = ...\n\n")
                    out.write(f"addonTable.{t_name} = addonTable.{t_name} or {{}}\n\n")
                    out.write("local data = {\n")
                    out.write("\n".join(state["current_chunk"]))
                    out.write("\n}\n\n")
                    out.write(f"for k, v in pairs(data) do addonTable.{t_name}[k] = v end\n")
                
                print(f"Generated {chunk_file} with {state['current_lines_count']} lines")
                state["file_index"] += 1
                state["current_chunk"] = []
                state["current_lines_count"] = 0
            
            for line in lines:
                chunk_state["current_chunk"].append(line)
                chunk_state["current_lines_count"] += 1
                
                i = 0
                while i < len(line):
                    c = line[i]
                    if c == '"' or c == "'":
                        q = c
                        i += 1
                        while i < len(line):
                            if line[i] == q and line[i-1] != '\\':
                                break
                            i += 1
                    elif line[i:i+2] == '--':
                        break
                    elif c == '{': chunk_state["depth"] += 1
                    elif c == '}': chunk_state["depth"] -= 1
                    i += 1
                
                if chunk_state["depth"] == 0 and chunk_state["current_lines_count"] >= LINES_PER_FILE:
                    write_chunk(chunk_state)
            
            write_chunk(chunk_state)

print("Chunking complete.")
