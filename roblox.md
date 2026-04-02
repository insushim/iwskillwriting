---
description: 로블록스 게임 개발. "로블록스", "Roblox", "루아", "Lua", "Roblox Studio" 트리거.
---

# Roblox 게임 개발

## 개발 환경
- Roblox Studio 설치: https://create.roblox.com/
- 언어: Lua / Luau

## 프로젝트 구조
```
game/
├── Workspace/              # 3D 오브젝트
├── ServerScriptService/    # 서버 스크립트 (보안)
├── ServerStorage/          # 서버 전용 에셋
├── ReplicatedStorage/      # 공유 모듈/에셋
├── ReplicatedFirst/        # 로딩 시 최우선 실행
├── StarterGui/             # UI
├── StarterPack/            # 시작 도구
├── StarterPlayer/
│   ├── StarterCharacterScripts/
│   └── StarterPlayerScripts/
└── SoundService/           # 오디오
```

## 핵심 스크립트 템플릿

### 서버 스크립트 (ServerScriptService)
```lua
-- GameManager.lua
local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local GameManager = {}
GameManager.PlayerData = {}

function GameManager:Init()
    Players.PlayerAdded:Connect(function(player)
        self:OnPlayerJoin(player)
    end)

    Players.PlayerRemoving:Connect(function(player)
        self:OnPlayerLeave(player)
    end)
end

function GameManager:OnPlayerJoin(player)
    print(player.Name .. " joined!")
    self.PlayerData[player.UserId] = {
        Coins = 0,
        Level = 1,
        Experience = 0
    }

    -- 리더보드 설정
    local leaderstats = Instance.new("Folder")
    leaderstats.Name = "leaderstats"
    leaderstats.Parent = player

    local coins = Instance.new("IntValue")
    coins.Name = "Coins"
    coins.Value = 0
    coins.Parent = leaderstats
end

function GameManager:OnPlayerLeave(player)
    -- 데이터 저장
    self.PlayerData[player.UserId] = nil
end

return GameManager
```

### 클라이언트 스크립트 (StarterPlayerScripts)
```lua
-- PlayerController.lua
local Players = game:GetService("Players")
local UserInputService = game:GetService("UserInputService")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local player = Players.LocalPlayer
local character = player.Character or player.CharacterAdded:Wait()

-- 입력 처리
UserInputService.InputBegan:Connect(function(input, gameProcessed)
    if gameProcessed then return end

    if input.KeyCode == Enum.KeyCode.E then
        -- E키 상호작용
        print("Interact pressed")
    end
end)

-- 캐릭터 리스폰 처리
player.CharacterAdded:Connect(function(char)
    character = char
    print("Character respawned")
end)
```

### RemoteEvent 통신
```lua
-- 서버 (ServerScriptService)
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local CoinEvent = Instance.new("RemoteEvent")
CoinEvent.Name = "CoinEvent"
CoinEvent.Parent = ReplicatedStorage

CoinEvent.OnServerEvent:Connect(function(player, action, amount)
    if action == "collect" then
        local leaderstats = player:FindFirstChild("leaderstats")
        if leaderstats then
            leaderstats.Coins.Value += amount
        end
    end
end)

-- 클라이언트
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local CoinEvent = ReplicatedStorage:WaitForChild("CoinEvent")

-- 코인 수집 시
CoinEvent:FireServer("collect", 10)
```

### 데이터 저장 (DataStoreService)
```lua
local DataStoreService = game:GetService("DataStoreService")
local PlayerDataStore = DataStoreService:GetDataStore("PlayerData")

local function SaveData(player)
    local data = {
        Coins = player.leaderstats.Coins.Value,
        Level = 1
    }

    local success, err = pcall(function()
        PlayerDataStore:SetAsync(player.UserId, data)
    end)

    if not success then
        warn("Failed to save data: " .. err)
    end
end

local function LoadData(player)
    local success, data = pcall(function()
        return PlayerDataStore:GetAsync(player.UserId)
    end)

    if success and data then
        player.leaderstats.Coins.Value = data.Coins or 0
    end
end
```

### UI 스크립트 (StarterGui)
```lua
-- ShopGui.lua (LocalScript)
local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local player = Players.LocalPlayer
local gui = script.Parent

local shopFrame = gui:WaitForChild("ShopFrame")
local buyButton = shopFrame:WaitForChild("BuyButton")
local closeButton = shopFrame:WaitForChild("CloseButton")

buyButton.MouseButton1Click:Connect(function()
    local PurchaseEvent = ReplicatedStorage:WaitForChild("PurchaseEvent")
    PurchaseEvent:FireServer("sword", 100)
end)

closeButton.MouseButton1Click:Connect(function()
    shopFrame.Visible = false
end)
```

## 일반적인 패턴

### 모듈 스크립트
```lua
-- ReplicatedStorage/Modules/Utils.lua
local Utils = {}

function Utils.FormatNumber(num)
    if num >= 1000000 then
        return string.format("%.1fM", num / 1000000)
    elseif num >= 1000 then
        return string.format("%.1fK", num / 1000)
    end
    return tostring(num)
end

function Utils.Lerp(a, b, t)
    return a + (b - a) * t
end

return Utils
```

### 터치 파트 (Coin 수집)
```lua
local coin = script.Parent
local debounce = {}

coin.Touched:Connect(function(hit)
    local player = game.Players:GetPlayerFromCharacter(hit.Parent)
    if player and not debounce[player] then
        debounce[player] = true

        -- 코인 수집
        player.leaderstats.Coins.Value += 1
        coin:Destroy()
    end
end)
```

## 테스트
1. Roblox Studio에서 F5 (플레이 테스트)
2. 멀티플레이어: Test > Start (2 Players)

$ARGUMENTS
