# 🌏 旅遊規劃師 (Travel Planner)

Telegram Bot - 輸入目的地，獲得完整旅遊計畫！

## ✨ 功能特點

- 📍 **景點推薦** - 熱門景點 + 隱藏版景點
- 🍜 **當地美食** - 必吃餐廳 + 街頭小吃
- 💰 **預算估算** - 經濟型/中檔/豪華
- 🚗 **交通指南** - 機場交通 + 當地出行
- 🏨 **住宿推薦** - 各價位飯店民宿
- 🌤️ **天氣資訊** - 最佳旅遊季節
- ⚠️ **安全提示** - 當地習俗 + 注意事項

## 🚀 快速開始

### 安裝依賴

```bash
cd travel-planner
npm install
```

### 配置

```bash
cp .env.example .env
# 編輯 .env 填入你的 Telegram Bot Token
```

### 運行

```bash
# 生產環境
npm start

# 開發環境
npm run dev
```

## 📱 使用方式

在 Telegram 輸入城市名稱即可獲得旅遊規劃！

```
範例：
- 東京
- 巴黎
- 台北
- 倫敦
- 紐約
```

## 🌎 支援城市

東京、巴黎、台北、倫敦、紐約、首爾、新加坡、香港、大坂

## 📁 項目結構

```
travel-planner/
├── bot.js          # Bot 主程式
├── package.json    # Node.js 配置
├── SPEC.md         # 項目規格
└── .env.example   # 環境變量範例
```

## 🛠️ 技術栈

- Node.js
- grammy (Telegram Bot Framework)

## 📝 License

MIT