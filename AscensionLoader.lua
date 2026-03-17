
local frame = CreateFrame("Frame")
frame:RegisterEvent("PLAYER_LOGIN")
frame:SetScript("OnEvent", function(self)
    self:UnregisterEvent("PLAYER_LOGIN")

    local realmName = GetRealmName() or ""
    if not (_G.IsAscensionServer or realmName == "Elune" or realmName == "Area 52" or realmName == "Bronzebeard" or realmName == "Rexxar" or realmName == "Grizzly Hills") then return end

    if not QuestieLoader then
        return
    end

    ---@type QuestiePluginAPI
    local QuestiePluginAPI = QuestieLoader:ImportModule("QuestiePluginAPI")

    if not QuestiePluginAPI then
        Questie:Debug(Questie.DEBUG_CRITICAL, "[AscensionLoader] QuestiePluginAPI module not found — Ascension data will not load.")
        return
    end

    ---@type table
    local AscensionDB = _G.AscensionDB or {}

    local plugin = QuestiePluginAPI:RegisterPlugin("Ascension")
    if not plugin then return end

    print("|cFF5EBAF3Questie|r|cFFDAFAFD-X|r [AscensionLoader] Plugin registered, injecting data...")
    Questie:Debug(Questie.DEBUG_DEVELOP, "[AscensionLoader] Registering Ascension plugin...")

    if AscensionZoneTables then
        Questie:Debug(Questie.DEBUG_DEVELOP, "[AscensionLoader] Injecting zone tables...")
        plugin:InjectZoneTables(AscensionZoneTables)
    end

    if AscensionUiMapData then
        Questie:Debug(Questie.DEBUG_DEVELOP, "[AscensionLoader] Injecting UI map data...")
        plugin:InjectUiMapData(AscensionUiMapData)
    end

    if AscensionDB.npcData then
        Questie:Debug(Questie.DEBUG_DEVELOP, "[AscensionLoader] Injecting NPC data...")
        plugin:InjectDatabase("NPC", AscensionDB.npcData)
    end
    if AscensionDB.objectData then
        Questie:Debug(Questie.DEBUG_DEVELOP, "[AscensionLoader] Injecting Object data...")
        plugin:InjectDatabase("OBJECT", AscensionDB.objectData)
    end
    if AscensionDB.itemData then
        Questie:Debug(Questie.DEBUG_DEVELOP, "[AscensionLoader] Injecting Item data...")
        plugin:InjectDatabase("ITEM", AscensionDB.itemData)
    end
    if AscensionDB.questData then
        Questie:Debug(Questie.DEBUG_DEVELOP, "[AscensionLoader] Injecting Quest data...")
        plugin:InjectDatabase("QUEST", AscensionDB.questData)
    end

    plugin:FinishLoading()
end)
