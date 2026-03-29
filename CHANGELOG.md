# Changelog

## v1.0.3 — Initialization Stability and Visibility Fix

### Plugin
- **[Fix]** Database compilation is now deferred to **Stage 3** on WotLK/Ascension clients. This ensures the compilation progress log is fully visible in the chat frame after login.
- **[Fix]** Resolved Stage 2 initialization crash by ensuring `l10n` and `QuestieCorrections` are initialized during deferred flow.
- **[Fix]** Fixed "bad argument #1 to 'pairs' (table expected, got nil)" in `zoneDB.lua` by initializing `QuestPointers` as an empty table in the dummy block.
- **[Stability]** Implemented comprehensive dummy handles and pointers in `QuestieDB.lua` to prevent downstream crashes while the database is being compiled.
- **[Fix]** Added guarded `QuestieDB:Initialize()` call in Stage 3 to ensure handles are properly set up after late compilation.

## v1.0.2 — Injection and Newline Fixes

### Database
- **[Fix]** Fixed hidden literal newline characters (`\\n`) in the rechunking script that were causing all split files to load as a single comment block.
- **[Fix]** Corrected database injection casing in `AscensionLoader.lua` to match `QuestiePluginAPI` requirements (`QUEST`, `NPC`, `OBJECT`, `ITEM`).
- **[Fix]** Restored `InjectUiMapData` call to ensure zone boundary data is correctly loaded.

## v1.0.1 — Architecture Update

### Database
- **[Performance]** Split monolithic database files into smaller chunks to resolve memory allocation errors.
- **[Architecture]** Adopted the split-loading architecture (like WotLKDB) to reduce initial memory footprint and load times.

### Plugin
- **[Loader]** Updated `AscensionLoader.lua` to dynamically inject `addonTable` populated by split files.

## v1.0.0 — Initial Release

### Database
- **[Quests]** Initial Ascension quest loading.

### Plugin
- **[Core]** Created Questie-X-AscensionDB.
