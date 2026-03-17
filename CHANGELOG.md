# Changelog

## v1.0.0 — Initial Release

### Database

- **[Quests]** Initial Ascension custom quest database (`AscensionQuestDB.lua`).
- **[NPCs]** Initial Ascension NPC database with spawn coordinates (`AscensionNpcDB.lua`).
- **[Objects]** Initial Ascension object database (`AscensionObjectDB.lua`).
- **[Items]** Initial Ascension item database (`AscensionItemDB.lua`).
- **[Zones]** Added UI map ID mappings and zone table overrides for Ascension-specific zones.

### Plugin

- **[Loader]** `AscensionLoader.lua` registers all database tables with Questie-X via `QuestiePluginAPI`.
- **[TOC]** `Questie-Ascension.toc` declares `Questie-X` as a hard dependency — plugin will not load without the core addon present.
