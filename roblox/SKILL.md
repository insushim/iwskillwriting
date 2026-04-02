# Roblox Development Skill

> 로블록스 게임 개발 전문가 - Lua 스크립팅, UI, 게임 시스템

## Triggers
- "로블록스", "Roblox", "루아", "Lua"
- "로블록스 게임", "로블록스 스크립트"
- "Roblox Studio", "로벅스"

## Capabilities

### 1. Lua Scripting
```lua
-- Server Script (ServerScriptService)
local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

Players.PlayerAdded:Connect(function(player)
    local leaderstats = Instance.new("Folder")
    leaderstats.Name = "leaderstats"
    leaderstats.Parent = player

    local coins = Instance.new("IntValue")
    coins.Name = "Coins"
    coins.Value = 0
    coins.Parent = leaderstats
end)
```

### 2. Client-Server Communication
```lua
-- RemoteEvent 패턴
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local RemoteEvent = ReplicatedStorage:WaitForChild("MyEvent")

-- Server
RemoteEvent.OnServerEvent:Connect(function(player, data)
    print(player.Name .. " sent: " .. tostring(data))
end)

-- Client
RemoteEvent:FireServer({action = "buy", item = "sword"})
```

### 3. UI Development
```lua
-- ScreenGui 생성
local Players = game:GetService("Players")
local player = Players.LocalPlayer
local playerGui = player:WaitForChild("PlayerGui")

local screenGui = Instance.new("ScreenGui")
screenGui.Parent = playerGui

local frame = Instance.new("Frame")
frame.Size = UDim2.new(0.3, 0, 0.2, 0)
frame.Position = UDim2.new(0.35, 0, 0.4, 0)
frame.BackgroundColor3 = Color3.fromRGB(45, 45, 45)
frame.Parent = screenGui
```

### 4. Game Systems

#### Combat System
```lua
local CombatSystem = {}

function CombatSystem.Attack(attacker, target, damage)
    if not target:FindFirstChild("Humanoid") then return end

    local humanoid = target.Humanoid
    humanoid:TakeDamage(damage)

    -- 히트 이펙트
    local hitEffect = ReplicatedStorage.Effects.Hit:Clone()
    hitEffect.Parent = target.PrimaryPart
    game:GetService("Debris"):AddItem(hitEffect, 1)
end

return CombatSystem
```

#### Economy System
```lua
local DataStoreService = game:GetService("DataStoreService")
local playerDataStore = DataStoreService:GetDataStore("PlayerData")

local Economy = {}

function Economy.GetBalance(player)
    local success, data = pcall(function()
        return playerDataStore:GetAsync("coins_" .. player.UserId)
    end)
    return success and data or 0
end

function Economy.AddCoins(player, amount)
    local currentBalance = Economy.GetBalance(player)
    local newBalance = currentBalance + amount

    pcall(function()
        playerDataStore:SetAsync("coins_" .. player.UserId, newBalance)
    end)

    player.leaderstats.Coins.Value = newBalance
end

return Economy
```

### 5. Physics & Animation
```lua
-- Tween 애니메이션
local TweenService = game:GetService("TweenService")

local part = workspace.MyPart
local tweenInfo = TweenInfo.new(
    2,                   -- 시간
    Enum.EasingStyle.Quad,
    Enum.EasingDirection.Out,
    0,                   -- 반복
    false,               -- 역방향
    0                    -- 딜레이
)

local goal = {Position = Vector3.new(0, 10, 0)}
local tween = TweenService:Create(part, tweenInfo, goal)
tween:Play()
```

## Game Templates

### Obby (장애물 게임)
```lua
-- 체크포인트 시스템
local Checkpoints = workspace:WaitForChild("Checkpoints")

for i, checkpoint in ipairs(Checkpoints:GetChildren()) do
    checkpoint.Touched:Connect(function(hit)
        local player = game.Players:GetPlayerFromCharacter(hit.Parent)
        if player then
            player:SetAttribute("Checkpoint", i)
        end
    end)
end
```

### Tycoon
```lua
-- 드롭퍼 시스템
local Dropper = {}

function Dropper.new(position, value, interval)
    local self = setmetatable({}, {__index = Dropper})
    self.Position = position
    self.Value = value
    self.Interval = interval
    return self
end

function Dropper:Start()
    while true do
        local drop = Instance.new("Part")
        drop.Size = Vector3.new(1, 1, 1)
        drop.Position = self.Position
        drop.Parent = workspace.Drops
        drop:SetAttribute("Value", self.Value)
        wait(self.Interval)
    end
end

return Dropper
```

## Best Practices
1. FilteringEnabled (서버 권한)
2. DataStore 에러 핸들링
3. 메모리 관리 (Debris 사용)
4. 모듈화된 코드 구조
5. 최적화 (RenderStepped 최소화)

## Publishing Checklist
- [ ] 게임 아이콘/썸네일
- [ ] 게임 설명
- [ ] 소셜 링크
- [ ] 게임패스/개발자 상품
- [ ] 그룹 게임 설정
