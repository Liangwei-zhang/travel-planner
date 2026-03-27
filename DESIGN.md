# 旅遊規劃師 (Travel Planner) - 詳細設計模式

## 一、系統架構總覽

```
Telegram 用戶 (輸入城市名稱)
        │
        ▼ HTTPS (Telegram Bot API)
┌─────────────────────────────────────┐
│         應用層 (Application)         │
│  ┌───────────┐ ┌─────────────┐      │
│  │ 消息路由器 │ │ 命令處理器  │      │
│  │ (Router)  │ │ (/start)    │      │
│  └───────────┘ └─────────────┘      │
│        │            │               │
│        ▼            ▼               │
│  ┌─────────────────────────────┐   │
│  │   目的地匹配引擎 (Matching)   │   │
│  │ 精確匹配 → 模糊匹配 → Fallback│   │
│  └─────────────────────────────┘   │
│        │                            │
│        ▼                            │
│  ┌─────────────────────────────┐   │
│  │  旅遊規劃生成器 (Generator)    │   │
│  └─────────────────────────────┘   │
│        │                            │
│        ▼                            │
│  ┌─────────────────────────────┐   │
│  │    目的地數據庫 (DESTINATION) │   │
│  └─────────────────────────────┘   │
└─────────────────────────────────────┘
```

## 二、使用的設計模式

### 1. 事件循環模式 (Event Loop / Polling Pattern)

**用途：** Bot 持續監聽 Telegram 伺服器的新訊息

- **JavaScript (bot.js)** - 手動實現 Long Polling
- **Python (bot.py)** - 使用框架 `run_polling()`

### 2. 數據倉庫模式 (Repository Pattern)

**用途：** 集中管理所有旅遊目的地的結構化資料

```javascript
const DESTINATION_DB = {
  "東京": {
    country: "日本",
    currency: "日幣 (JPY)",
    budget_daily: { budget: "...", mid: "...", luxury: "..." },
    best_season: "3-5月 (春季)、9-11月 (秋季)",
    attractions: [...],
    food: [...],
    transport: [...],
    accommodation: [...],
    customs: [...],
    safety: "..."
  }
};
```

### 3. 責任鏈模式 (Chain of Responsibility)

**用途：** 目的地匹配 — 依序嘗試不同匹配策略

```
用戶輸入 "東京"
     │
     ▼ 命中
精確匹配 DB[destination] ──→ 生成詳細規劃
     │
     ▼ 未命中
模糊匹配 includes() / toLowerCase() ──→ 生成詳細規劃
     │
     ▼ 未命中
通用模板 (Fallback) ──→ 生成通用規劃
```

### 4. 模板方法模式 (Template Method Pattern)

**用途：** 旅遊規劃輸出有統一的格式模板

- **詳細模板** (generatePlanFromDB)：資料庫有資料時使用
- **通用模板** (generateGenericPlan)：無資料時使用

### 5. 守衛模式 (Guard / Access Control Pattern)

**用途：** 限制只有特定使用者能觸發 Bot

```javascript
if (String(chatId) === OWNER_ID) {
  await handleMessage(update.message);
}
```

### 6. 適配器模式 (Adapter Pattern)

**用途：** 封裝原生模組，提供統一的 Telegram API 介面

### 7. 策略模式 (Strategy Pattern)

**用途：** Python 版本對未知目的地有兩種處理策略

## 三、雙版本架構對比

| 維度 | bot.js (JavaScript) | bot.py (Python) |
|------|---------------------|------------------|
| 框架 | 無框架（原生 https） | python-telegram-bot |
| 城市數量 | 9 個（完整） | 3 個 |
| 權限控制 | ✅ OWNER_ID 守衛 | ❌ 無 |
| 模糊匹配 | ✅ | ❌ |
| Fallback | ✅ 通用模板 | ❌ |

## 四、現存問題與改進建議

| # | 問題 | 嚴重度 | 狀態 |
|---|------|--------|------|
| 1 | Bot Token 硬編碼 | 高 | ⏳ 待修復 |
| 2 | bot.py 語法錯誤 | 高 | ⏳ 待修復 |
| 3 | 資料與邏輯耦合 | 中 | ⏳ 待重構 |
| 4 | JS/Python 資料不同步 | 中 | ⏳ 待統一 |
| 5 | 無單元測試 | 中 | ⏳ 待添加 |
| 6 | 無日誌系統 | 低 | ⏳ 可選 |
| 7 | 無 i18n 機制 | 低 | ⏳ 可選 |

## 五、重構後的目標架構

```
travel-planner/
├── data/
│   └── destinations.json    # 統一數據源
├── src/
│   ├── bot.js              # Bot 入口
│   ├── matcher.js          # 目的地匹配引擎
│   ├── generator.js        # 旅遊規劃生成器
│   └── telegram.js         # Telegram API 封裝
├── tests/
│   └── matcher.test.js     # 單元測試
├── .env.example
├── package.json
├── SPEC.md
└── README.md
```

## 六、設計原則

- **單一職責原則 (SRP)**：每個模組只負責一件事
- **依賴反轉 (DIP)**：匹配引擎和生成器可被獨立替換
- **開放封閉原則 (OCP)**：新增城市只需修改 destinations.json，不動程式碼