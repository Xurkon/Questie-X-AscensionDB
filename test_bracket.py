import re

content = open("C:\\Users\\kance\\Documents\\GitHub\\Questie-X-AscensionDB\\Bronzebeard\\AscensionNpcDB.lua", "r", encoding="utf-8").read()
pattern = re.compile(r'([\w\.]+)\s*=\s*(?:[\w\.]+\s*or\s*)?\{')

match = None
for m in pattern.finditer(content):
    if "npcData" in m.group(1):
        match = m
        break

if match:
    start_idx = match.end()
    end_idx = start_idx
    bracket_count = 1
    
    while end_idx < len(content) and bracket_count > 0:
        c = content[end_idx]
        
        # ignore strings and comments
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
            if bracket_count == 0:
                print(f"Bracket count hit 0 at index {end_idx}")
                print(f"Context: {content[end_idx-50:end_idx+50]}")
            
        end_idx += 1
        
    print(f"Ended at {end_idx}, char: {content[max(0,end_idx-10):min(len(content),end_idx+10)]}")
