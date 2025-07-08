--[[

  Trait & Profession Factory Stubs
  --------------------------------
  This file mocks the game’s TraitFactory, ProfessionFactory, and other globals
  so that MainCreationMethods.lua can run outside of the game.

  It allows extracting traits and professions.

]]

-- No-op and fallback helpers
local function noop(...) end
local function dummytbl()
    return setmetatable({}, { __index = function(_, _) return noop end })
end

-- Game environment globals
getText = function(id) return id end
ZombRand = function(_, _) return 0 end
isClient, isServer = noop, noop

-- Server options stub
local so = { getBoolean = function(_, _) return false end }
function getServerOptions() return so end

-- Perk-related globals
Perks = setmetatable({}, {
    __index = function(t, k) t[k] = k ; return k end
})

PerkFactory = {
    getPerkName = function(p) return tostring(p) end
}

-- Stub: passes tables through unchanged
function transformIntoKahluaTable(t) return t or {} end

-- Other stubs and placeholders
ObservationFactory = setmetatable({}, { __index = function() return noop end })
doTailorRecipes = noop
doMetalWorkerRecipes = noop

-- Factories
TraitFactory = {}
ProfessionFactory = {}

-- Stub event system
Events = setmetatable({}, {
    __index = function(t, k)
        local ev = { Add = noop, Remove = noop }
        rawset(t, k, ev)
        return ev
    end
})

-- TraitFactory mock
TraitFactory._traits = {}
TraitFactory._mutualExclusive = {}

local function new_trait(id, name, cost, desc, isFree)
    local self = {
        id = id,
        name = name,
        cost = cost,
        desc = desc,
        isFree = isFree or false,
        xpBoosts = {},
        recipes = {},
        freeTraits = {},

        addXPBoost = function(s, perk, lvl)
            table.insert(s.xpBoosts, { perk = tostring(perk), level = lvl })
        end,

        getFreeRecipes = function(s)
            return { add = function(_, recipe)
                table.insert(s.recipes, recipe)
            end }
        end,

        addFreeTrait = function(s, tr)
            table.insert(s.freeTraits, tr)
        end,

        getXPBoostMap = function(s)
            local m = {}
            for _, v in ipairs(s.xpBoosts) do m[v.perk] = v.level end
            return m
        end
    }
    return setmetatable(self, { __index = self })
end

function TraitFactory.addTrait(id, name, cost, desc, isFree)
    local t = new_trait(id, name, cost, desc, isFree)
    TraitFactory._traits[id] = t
    return t
end

TraitFactory.setMutualExclusive = function(a, b)
    table.insert(TraitFactory._mutualExclusive, { a, b })
end

-- Simulates empty Java-style list
function TraitFactory.getTraits()
    return {
        size = function() return 0 end,
        get = function() return nil end
    }
end

TraitFactory.sortList = noop

-- ProfessionFactory mock
ProfessionFactory._profs = {}

local function new_prof(id, name, icon, cost)
    local self = {
        id = id,
        name = name,
        icon = icon,
        cost = cost,
        xpBoosts = {},
        recipes = {},
        freeTraits = {},

        addXPBoost = function(s, perk, lvl)
            table.insert(s.xpBoosts, { perk = tostring(perk), level = lvl })
        end,

        getFreeRecipes = function(s)
            return { add = function(_, recipe)
                table.insert(s.recipes, recipe)
            end }
        end,

        addFreeTrait = function(s, tr)
            table.insert(s.freeTraits, tr)
        end
    }
    return setmetatable(self, { __index = self })
end

function ProfessionFactory.addProfession(id, name, icon, cost)
    local p = new_prof(id, name, icon, cost)
    ProfessionFactory._profs[id] = p
    return p
end

function ProfessionFactory.getProfessions()
    return {
        size = function() return 0 end,
        get = function() return nil end
    }
end
