# Changelog

## v1.0.2 — Compatibility Update

### Plugin
- **[Loader]** Updated `AscensionLoader.lua` to properly handle the split-loading architecture for improved memory usage during database loading.

## v1.0.1 — Database Split

### Database
- **[Performance]** Split monolithic database files into smaller chunks to resolve memory allocation errors.
- **[Architecture]** Adopted the split-loading architecture to reduce initial memory footprint and load times.

### Plugin
- **[Loader]** Updated `AscensionLoader.lua` to dynamically inject `addonTable` populated by split files.

## v1.0.0 — Initial Release

### Database

- **[Quests]** Initial Ascension custom quest database (`AscensionQuestDB.lua`).
- **[NPCs]** Initial Ascension NPC database with spawn coordinates (`AscensionNpcDB.lua`).
- **[Objects]** Initial Ascension object database (`AscensionObjectDB.lua`).
- **[Items]** Initial Ascension item database (`AscensionItemDB.lua`).
- **[Zones]** Added UI map ID mappings and zone table overrides for Ascension-specific zones.

### Plugin

- **[Loader]** `AscensionLoader.lua` registers all database tables with Questie-X via `QuestiePluginAPI`.
- **[TOC]** `Questie-X-AscensionDB.toc` declares `Questie-X` as a hard dependency — plugin will not load without the core addon present.
