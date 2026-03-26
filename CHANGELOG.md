# Changelog

## v1.0.2 — Syntax Fix

### Database
- **[Fix]** Fixed syntax error in `Bronzebeard/Split/AscensionNpcDB_2.lua` (missing closing `}` at end of NPC entry for ID 3287) that caused Lua parse errors on load.

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
