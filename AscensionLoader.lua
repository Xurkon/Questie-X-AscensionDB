local addonName, addonTable = ...
print("|cFF5EBAF3Questie|r|cFFDAFAFD-X|r [AscensionLoader] Loading...")

-- Ascension-X Loader
local function registerAndInject()
    if not QuestieLoader then
        return false
    end

    ---@type QuestiePluginAPI
    local QuestiePluginAPI = QuestieLoader:ImportModule("QuestiePluginAPI")
    if not QuestiePluginAPI then
        return false
    end

    local realmName = GetRealmName() or ""
    -- Broaden the check to match QuestieServer.lua logic
    local isAscension = _G.IsAscensionServer or realmName:find("Ascension") or realmName:find("Area 52") or
                      realmName:find("Al'ar") or realmName:find("Thrall") or realmName:find("Elune") or
                      realmName:find("Bronzebeard") or realmName:find("Rexxar") or realmName:find("Grizzly Hills")

    if not isAscension then 
        return true -- Not on Ascension, skip but don't retry
    end

    local plugin = QuestiePluginAPI:RegisterPlugin("Ascension")
    if not plugin then return true end -- Already registered or error

    print("|cFF5EBAF3Questie|r|cFFDAFAFD-X|r [AscensionLoader] Plugin registered, injecting data...")

    if addonTable.zoneSort or addonTable.uiMapIdToAreaId then
        plugin:InjectZoneTables(addonTable)
    end

    if addonTable.uiMapData then
        print("[AscensionLoader] Using addonTable.uiMapData")
        plugin:InjectUiMapData(addonTable)
    elseif AscensionUiMapData and AscensionUiMapData.uiMapData then
        print("[AscensionLoader] Using AscensionUiMapData.uiMapData with " .. tostring(AscensionUiMapData.uiMapData and "data" or "nil"))
        plugin:InjectUiMapData(AscensionUiMapData)
    else
        print("[AscensionLoader] No uiMapData found - addonTable.uiMapData=" .. tostring(addonTable.uiMapData) .. " AscensionUiMapData=" .. tostring(AscensionUiMapData))
    end

    -- Inject the data into Questie-X
    if addonTable.npcData then
        plugin:InjectDatabase("NPC", addonTable.npcData)
    end
    if addonTable.questData then
        plugin:InjectDatabase("QUEST", addonTable.questData)
    end
    if addonTable.objectData then
        plugin:InjectDatabase("OBJECT", addonTable.objectData)
    end
    if addonTable.itemData then
        plugin:InjectDatabase("ITEM", addonTable.itemData)
    end

    _G.AscensionDB = addonTable

    print("|cFF5EBAF3Questie|r|cFFDAFAFD-X|r [AscensionLoader] Data injection complete.")
    plugin:FinishLoading("Ascension")
    return true
end

-- Try registering immediately
if not registerAndInject() then
    -- Fallback: Register at PLAYER_LOGIN if QuestieLoader wasn't ready
    local frame = CreateFrame("Frame")
    frame:RegisterEvent("PLAYER_LOGIN")
    frame:SetScript("OnEvent", function(self)
        self:UnregisterEvent("PLAYER_LOGIN")
        registerAndInject()
    end)
end
