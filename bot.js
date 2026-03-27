#!/usr/bin/env node
/**
 * Travel Planner (旅遊規劃師) - 使用 Telegram Long Polling API
 * 不依賴 Telegraf 庫，直接使用 HTTP 請求
 */

const https = require('https');

// 配置
const BOT_TOKEN = '8585851488:AAFT7326kF79zgT-yVK6EEbxvic-MLTr1pg';
const OWNER_ID = '6390423676';

// 預設目的地數據庫
const DESTINATION_DB = {
  "東京": {
    country: "日本",
    currency: "日幣 (JPY)",
    budget_daily: {
      budget: "NT$3,000-4,000",
      mid: "NT$4,000-6,000",
      luxury: "NT$6,000+"
    },
    best_season: "3-5月 (春季)、9-11月 (秋季)",
    attractions: [
      "淺草寺 - 東京最古老的佛教寺廟",
      "東京晴空塔 - 俯瞰全市景色",
      "新宿御苑 - 皇家公園",
      "築地市場 - 海鮮美食天堂",
      "秋葉原 - 動漫與電器聖地",
      "澀谷十字路口 - 世界最繁忙交叉口",
      "明治神宮 - 都市中的森林神社",
      "東京迪士尼樂園 - 夢幻王國"
    ],
    food: [
      "壽司 - 築地市場新鮮壽司",
      "拉麵 - 一蘭拉麵、豚骨拉麵",
      "天婦羅 - 炸蝦、炸蔬菜",
      "燒肉 - 敘敘苑、烤肉",
      "便當 - 鐵路便當",
      "抹茶甜點 - 抹茶冰淇淋、蛋糕"
    ],
    transport: [
      "地鐵 - JR線、都營地下鐵",
      "計程車 - 較昂貴但方便",
      "巴士 - 觀光循環巴士"
    ],
    accommodation: [
      "新宿 - 交通樞紐，購物方便",
      "澀谷 - 年輕時尚區",
      "淺草 - 傳統文化區",
      "上野 - 博物館與公園區"
    ],
    customs: [
      "進室內需脫鞋",
      "自動販賣機前不可飲食",
      "排隊秩序很重要",
      "電車上避免講電話"
    ],
    safety: "東京是非常安全的城市，但仍需注意扒竊"
  },
  "巴黎": {
    country: "法國",
    currency: "歐元 (EUR)",
    budget_daily: {
      budget: "NT$4,000-6,000",
      mid: "NT$6,000-10,000",
      luxury: "NT$10,000+"
    },
    best_season: "4-6月、9-11月",
    attractions: [
      "艾菲爾鐵塔 - 巴黎地標",
      "羅浮宮 - 世界最大博物館",
      "聖母院 - 哥德式建築經典",
      "香榭麗舍大道 - 購物天堂",
      "蒙馬特高地 - 藝術家廣場",
      "凡爾賽宮 - 奢華宮殿",
      "奧塞博物館 - 印象派收藏"
    ],
    food: [
      "法式可麗餅 - 經典街頭美食",
      "馬卡龍 - Ladurée 甜點",
      "法式洋蔥湯 - 傳統湯品",
      "紅酒燉牛肉 - 經典法菜",
      "可頌麵包 - 早餐必備",
      "法式蝸牛 - 特色料理"
    ],
    transport: [
      "地鐵 - 涵蓋全市",
      "RER - 郊區交通",
      "計程車 - Uber 普及"
    ],
    accommodation: [
      "香榭麗舍 - 高檔購物區",
      "瑪黑區 - 藝術時尚區",
      "蒙帕納斯 - 藝術家區",
      "拉丁區 - 學生區，經濟實惠"
    ],
    customs: [
      "見面需行貼面禮",
      "進入餐廳需打招呼",
      "小費通常是消費的10%",
      "下午1-3點是午餐時間"
    ],
    safety: "小心扒手，尤其在觀光區"
  },
  "台北": {
    country: "台灣",
    currency: "新台幣 (TWD)",
    budget_daily: {
      budget: "NT$2,000-3,000",
      mid: "NT$3,000-5,000",
      luxury: "NT$5,000+"
    },
    best_season: "3-5月、10-12月",
    attractions: [
      "台北101 - 世界最高綠建築",
      "故宮博物院 - 中華文化寶藏",
      "士林夜市 - 最大的夜市",
      "龍山寺 - 傳統廟宇",
      "陽明山國家公園 - 溫泉與自然",
      "淡水老街 - 河岸風光",
      "信義商圈 - 購物與夜景"
    ],
    food: [
      "珍珠奶茶 - 台灣發源地",
      "蚵仔煎 - 夜市經典",
      "牛肉麵 - 紅燒、清燉",
      "小籠包 - 鼎泰豐",
      "滷肉飯 - 國民美食",
      "挫冰 - 水果冰品"
    ],
    transport: [
      "捷運 - 便捷的軌道交通",
      "UBike - YouBike 租借",
      "計程車 - 隨處可見"
    ],
    accommodation: [
      "信義區 - 最繁華商圈",
      "中山區 - 購物與美食",
      "大安區 - 文青區",
      "西門町 - 年輕潮流區"
    ],
    customs: [
      "乘捷運需排隊",
      "博愛座讓給有需要的人",
      "餐廳收取10%服務費",
      "很多場所禁止吸菸"
    ],
    safety: "台北非常安全，適合獨旅"
  },
  "倫敦": {
    country: "英國",
    currency: "英鎊 (GBP)",
    budget_daily: {
      budget: "NT$4,000-6,000",
      mid: "NT$6,000-9,000",
      luxury: "NT$9,000+"
    },
    best_season: "5-9月",
    attractions: [
      "大笨鐘 - 倫敦標誌",
      "白金漢宮 - 英國皇室宮殿",
      "大英博物館 - 世界級博物館",
      "塔橋 - 倫敦標誌性橋樑",
      "倫敦眼 - 摩天輪",
      "海德公園 - 皇家公園",
      "西敏寺 - 歷史教堂"
    ],
    food: [
      "炸魚薯條 - 英國經典",
      "英式早茶 - 必嘗體驗",
      "牧羊人派 - 傳統料理",
      "牛排腰子派 - 特色美食",
      "印度咖哩 - 倫敦特色"
    ],
    transport: [
      "地鐵 - 全球最古老的地下鐵",
      "公車 - 觀光好選擇",
      "計程車 - 黑色計程車"
    ],
    accommodation: [
      "肯辛頓 - 博物館區",
      "蘇荷區 - 夜生活區",
      "Covent Garden - 藝術區",
      "國王十字 - 交通樞紐"
    ],
    customs: [
      "排隊很重要",
      "請說謝謝 (Please/Thank you)",
      "小費約10-15%",
      "自來水可直接飲用"
    ],
    safety: "大型城市需注意扒手"
  },
  "紐約": {
    country: "美國",
    currency: "美元 (USD)",
    budget_daily: {
      budget: "NT$5,000-8,000",
      mid: "NT$8,000-15,000",
      luxury: "NT$15,000+"
    },
    best_season: "4-6月、9-11月",
    attractions: [
      "自由女神像 - 紐約地標",
      "時代廣場 - 世界十字路口",
      "中央公園 - 都市綠洲",
      "帝國大廈 - 曼哈頓天際線",
      "大都會博物館 - 世界級藝術",
      "自由塔 - 新地標",
      "布魯克林大橋"
    ],
    food: [
      "熱狗 - 街頭經典",
      "漢堡 - 特色美式料理",
      "紐約披薩 - 薄餅特色",
      "貝果 - 猶太美食",
      "肋排 - BBQ 餐廳"
    ],
    transport: [
      "地鐵 - 24小時營運",
      "計程車 - 黃色計程車",
      "Uber/Lyft - 共乘服務"
    ],
    accommodation: [
      "曼哈頓 - 市中心",
      "布魯克林 - 藝術區",
      "時代廣場 - 劇院區",
      "蘇荷區 - 購物區"
    ],
    customs: [
      "小費文化很重要 (15-20%)",
      "自來水可飲用",
      "Driving 靠右",
      "公共場所不可吸菸"
    ],
    safety: "需注意市區安全，夜晚避免偏僻地區"
  },
  "首爾": {
    country: "韓國",
    currency: "韓圜 (KRW)",
    budget_daily: {
      budget: "NT$2,500-4,000",
      mid: "NT$4,000-6,000",
      luxury: "NT$6,000+"
    },
    best_season: "3-5月、9-11月",
    attractions: [
      "景福宮 - 韓國故宮",
      "明洞 - 購物天堂",
      "弘大 - 年輕文化區",
      "南山首爾塔 - 俯瞰全景",
      "北村韓屋村 - 傳統聚落",
      "仁寺洞 - 傳統藝術街",
      "東門市場 - 傳統市場"
    ],
    food: [
      "烤肉 - 韓式燒肉",
      "拌飯 - 韓式石鍋拌飯",
      "辣炒年糕 - 經典街頭小吃",
      "參雞湯 - 養生料理",
      "炸雞 - 韓式炸雞",
      "豆腐鍋 - 韓式火鍋"
    ],
    transport: [
      "地鐵 - 便捷覆蓋廣",
      "計程車 - 方便但貴",
      "公車 - 觀光路線"
    ],
    accommodation: [
      "明洞 - 購物與交通",
      "弘大 - 年輕潮流區",
      "江南 - 高檔區",
      "仁寺洞 - 文化區"
    ],
    customs: [
      "長輩優先",
      "喝酒要轉身",
      "脫鞋進入室內",
      "不可倒酒給長輩"
    ],
    safety: "首爾非常安全"
  },
  "新加坡": {
    country: "新加坡",
    currency: "新加坡幣 (SGD)",
    budget_daily: {
      budget: "NT$3,000-5,000",
      mid: "NT$5,000-8,000",
      luxury: "NT$8,000+"
    },
    best_season: "全年適宜",
    attractions: [
      "魚尾獅公園 - 新加坡地標",
      "濱海灣花園 - 超級樹",
      "聖淘沙 - 度假島嶼",
      "牛車水 - 華人區",
      "小印度 - 印度文化區",
      "克拉碼頭 - 夜生活"
    ],
    food: [
      "海南雞飯 - 國民美食",
      "辣椒螃蟹 - 特色料理",
      "肉骨茶 - 馬來西亞華人料理",
      "咖椰吐司 - 早餐經典",
      "拉茶 - 印度奶茶"
    ],
    transport: [
      "地鐵 - MRT便捷",
      "計程車 - 較昂貴",
      "公車 - 完善網絡"
    ],
    accommodation: [
      " Marina Bay - 濱海灣區",
      "烏節路 - 購物區",
      "牛車水 - 文化區",
      "聖淘沙 - 度假區"
    ],
    customs: [
      "嚴禁隨地吐痰",
      "禁菸區多",
      "小心罰款",
      "多元文化尊重"
    ],
    safety: "非常安全的城市"
  },
  "香港": {
    country: "香港",
    currency: "港幣 (HKD)",
    budget_daily: {
      budget: "NT$2,500-4,000",
      mid: "NT$4,000-6,000",
      luxury: "NT$6,000+"
    },
    best_season: "10-12月",
    attractions: [
      "維多利亞港 - 世界三大夜景",
      "太平山頂 - 俯瞰全港",
      "迪士尼樂園 - 童話王國",
      "海洋公園 - 海洋主題樂園",
      "星光大道 - 明星手印",
      "旺角 - 購物與美食",
      "中環 - 金融中心"
    ],
    food: [
      "港式奶茶 - 經典飲品",
      "蛋撻 - 必嘗甜點",
      "雲吞麵 - 經典麵食",
      "燒臘 - 叉燒、燒鴨",
      "火鍋 - 港式火鍋",
      "魚蛋 - 街頭經典"
    ],
    transport: [
      "港鐵 - MTR便捷",
      "巴士 - 覆蓋廣泛",
      "計程車 - 紅的/綠的"
    ],
    accommodation: [
      "尖沙咀 - 購物與景點",
      "中環 - 商務區",
      "銅鑼灣 - 購物區",
      "旺角 - 平民區"
    ],
    customs: [
      "排隊很重要",
      "粵語為主",
      "小費隨意",
      "八達通卡必備"
    ],
    safety: "非常安全的城市"
  },
  "大阪": {
    country: "日本",
    currency: "日幣 (JPY)",
    budget_daily: {
      budget: "NT$3,000-4,500",
      mid: "NT$4,500-7,000",
      luxury: "NT$7,000+"
    },
    best_season: "3-5月、9-11月",
    attractions: [
      "道頓堀 - 美食天堂",
      "通天閣 - 大阪地標",
      "大阪城 - 歷史古城",
      "環球影城 - 電影主題樂園",
      "天王寺 - 新世界",
      "阿倍野 Harukas - 日本最高摩天大樓",
      "大阪港 - 海遊館"
    ],
    food: [
      "章魚燒 - 大阪名物",
      "大阪燒 - 庶民美食",
      "串炸 - 特色料理",
      "蟹料理 - 蟹道樂",
      "拉麵 - 當地口味",
      "甜的零食 - 使用好人參"
    ],
    transport: [
      "地鐵 - 便捷",
      "JR - 城市間移動",
      "計程車 - 便利"
    ],
    accommodation: [
      "難波 - 交通樞紐",
      "心齋橋 - 購物區",
      "天王寺 - 方便",
      "大阪站 - 商務區"
    ],
    customs: [
      "進屋脫鞋",
      "小心走在自行車道上",
      "很多餐廳只收現金",
      "熱情推銷要小心"
    ],
    safety: "大阪很安全"
  }
};

// 追蹤更新 ID
let lastUpdateId = 0;

// Telegram API 請求輔助函數
function telegramRequest(method, params = {}) {
  return new Promise((resolve, reject) => {
    const data = JSON.stringify(params);
    const options = {
      hostname: 'api.telegram.org',
      path: `/bot${BOT_TOKEN}/${method}`,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(data)
      }
    };

    const req = https.request(options, (res) => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        try {
          const json = JSON.parse(body);
          if (json.ok) resolve(json.result);
          else reject(new Error(json.description));
        } catch (e) {
          reject(e);
        }
      });
    });

    req.on('error', reject);
    req.write(data);
    req.end();
  });
}

// 發送訊息
async function sendMessage(chatId, text, replyToMessageId = null) {
  const params = {
    chat_id: chatId,
    text: text,
    parse_mode: 'Markdown'
  };
  if (replyToMessageId) {
    params.reply_to_message_id = replyToMessageId;
  }
  return telegramRequest('sendMessage', params);
}

// 生成旅遊規劃
function generatePlanFromDB(destination, data) {
  const attractions = data.attractions.map(a => `  • ${a}`).join('\n');
  const food = data.food.map(f => `  • ${f}`).join('\n');
  const transport = data.transport.map(t => `  • ${t}`).join('\n');
  const accommodation = data.accommodation.map(a => `  • ${a}`).join('\n');
  const customs = data.customs.map(c => `  • ${c}`).join('\n');

  return `🎯 *${destination}* 旅遊規劃

📍 【景點推薦】
${attractions}

🍜 【當地美食】
${food}

💰 【預算估算】(每日)
  • 經濟型：${data.budget_daily.budget}
  • 中檔：${data.budget_daily.mid}
  • 豪華：${data.budget_daily.luxury}

🚗 【交通指南】
${transport}

🏨 【住宿推薦】
${accommodation}

🌤️ 【最佳旅遊季節】
  ${data.best_season}

⚠️ 【當地習俗與安全】
${customs}

💵 當地貨幣：${data.currency}

---
💡 資料僅供參考，實際費用可能有所不同。`;
}

function generateGenericPlan(destination) {
  return `🎯 *${destination}* 旅遊規劃

🌍 歡迎來到 ${destination}！

📍 【熱門景點】
  • 市中心廣場
  • 國家博物館
  • 歷史古蹟
  • 當地市場

🍜 【當地美食】
  • 特色料理 1
  • 特色料理 2
  • 街頭小吃

💰 【預算估算】(每日)
  • 經濟型：NT$2,000-3,000
  • 中檔：NT$3,000-5,000
  • 豪華：NT$5,000+

🚗 【交通指南】
  • 機場交通
  • 公共交通
  • 計程車/共乘

🏨 【住宿推薦】
  • 市中心飯店
  • 經濟型住宿
  • 特色民宿

⚠️ 【實用提示】
  • 提前預訂機票與住宿
  • 兌換當地貨幣
  • 注意保管隨身物品

---
💡 想知道更詳細的資訊嗎？嘗試輸入「東京」、「巴黎」、「台北」等熱門城市！`;
}

// 處理訊息
async function handleMessage(message) {
  const chatId = message.chat.id;
  const text = message.text || '';
  const messageId = message.message_id;

  // 忽略命令
  if (text.startsWith('/')) {
    // 處理 /start 命令
    if (text === '/start') {
      const welcomeText = `🌍 歡迎使用旅遊規劃師！

我是你的私人旅遊助理，可以幫你規劃行程。

📝 使用方式：
直接輸入你想去的城市名稱，我會為你提供：

• 景點推薦
• 當地美食
• 行程規劃
• 預算估算
• 交通指南
• 住宿建議
• 天氣與提示
• 當地習俗與安全

🎯 試試輸入：「東京」、「巴黎」或「台北」`;
      await sendMessage(chatId, welcomeText);
    }
    return;
  }

  const destination = text.trim();
  
  // 顯示規劃中的訊息
  const planningMsg = await sendMessage(chatId, `🔍 正在為你規劃 ${destination} 的行程...`);

  try {
    let plan;
    
    // 檢查資料庫 - 精確匹配
    if (DESTINATION_DB[destination]) {
      plan = generatePlanFromDB(destination, DESTINATION_DB[destination]);
    } else {
      // 嘗試模糊匹配
      const keys = Object.keys(DESTINATION_DB);
      const found = keys.find(k => 
        destination.includes(k) || 
        k.includes(destination) ||
        k.toLowerCase() === destination.toLowerCase()
      );
      
      if (found) {
        plan = generatePlanFromDB(found, DESTINATION_DB[found]);
      } else {
        plan = generateGenericPlan(destination);
      }
    }

    await sendMessage(chatId, plan);
  } catch (error) {
    console.error('Error:', error);
    await sendMessage(chatId, `❌ 抱歉，無法處理這個目的地: ${destination}\n請稍後再試或嘗試其他城市。`);
  }
}

// 主迴圈 - Long Polling
async function startPolling() {
  console.log('🌍 旅遊規劃師 Bot 啟動中 (Long Polling)...');
  
  while (true) {
    try {
      const updates = await telegramRequest('getUpdates', {
        offset: lastUpdateId + 1,
        timeout: 30,
        allowed_updates: ['message']
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
