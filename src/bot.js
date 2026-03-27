#!/usr/bin/env node
/**
 * Travel Planner (旅遊規劃師) - Telegram Bot 主入口
 * 使用 Long Polling API，直接使用 HTTP 請求
 */

const path = require('path');
const TelegramClient = require('./src/telegram');
const DestinationMatcher = require('./src/matcher');
const PlanGenerator = require('./src/generator');

// 配置 - 從環境變數讀取
const BOT_TOKEN = process.env.TELEGRAM_BOT_TOKEN || process.env.BOT_TOKEN;
const OWNER_ID = process.env.OWNER_ID || '6390423676';

// 驗證必要的環境變數
if (!BOT_TOKEN) {
  console.error('❌ 錯誤：請設定 TELEGRAM_BOT_TOKEN 環境變數');
  console.error('   請建立 .env 檔案或設定環境變數');
  process.exit(1);
}

// 初始化模組
const dataPath = path.join(__dirname, 'data', 'destinations.json');
const telegram = new TelegramClient(BOT_TOKEN);
const matcher = new DestinationMatcher(dataPath).load();
const generator = new PlanGenerator();

// 追蹤更新 ID
let lastUpdateId = 0;

// 處理訊息
async function handleMessage(message) {
  const chatId = message.chat.id;
  const text = message.text || '';
  const messageId = message.message_id;

  // 忽略命令
  if (text.startsWith('/')) {
    // 處理 /start 命令
    if (text === '/start') {
      await telegram.sendMessage(chatId, generator.generateWelcome());
    }
    return;
  }

  const destination = text.trim();
  
  // 顯示規劃中的訊息
  await telegram.sendMessage(chatId, generator.generatePlanning(destination));

  try {
    let plan;
    
    // 使用 matcher 查找目的地
    const match = matcher.match(destination);
    
    if (match) {
      plan = generator.generateFromDB(match.name, match.data);
    } else {
      plan = generator.generateGeneric(destination);
    }

    await telegram.sendMessage(chatId, plan);
  } catch (error) {
    console.error('Error:', error);
    await telegram.sendMessage(chatId, generator.generateError(destination));
  }
}

// 主迴圈 - Long Polling
async function startPolling() {
  console.log('🌍 旅遊規劃師 Bot 啟動中 (Long Polling)...');
  
  while (true) {
    try {
      const updates = await telegram.getUpdates({
        offset: lastUpdateId + 1,
        timeout: 30
      });

      for (const update of updates) {
        lastUpdateId = update.update_id;
        
        if (update.message) {
          const chatId = update.message.chat.id;
          
          // 只處理 Owner 的訊息
          if (String(chatId) === OWNER_ID || chatId.toString() === OWNER_ID) {
            console.log(`📩 收到來自 ${update.message.chat.first_name} 的訊息: ${update.message.text}`);
            await handleMessage(update.message);
          } else {
            console.log(`📩 忽略來自 ${chatId} 的訊息`);
          }
        }
      }
    } catch (error) {
      console.error('Polling error:', error.message);
      await new Promise(resolve => setTimeout(resolve, 5000)); // 等待 5 秒後重試
    }
  }
}

// 啟動
startPolling().catch(console.error);