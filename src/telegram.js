/**
 * Telegram API 包裝器
 * 負責所有與 Telegram Bot API 的互動
 */

const https = require('https');

class TelegramClient {
  constructor(botToken) {
    this.botToken = botToken;
  }

  /**
   * 發送 API 請求
   * @param {string} method - Telegram API 方法名
   * @param {object} params - 請求參數
   * @returns {Promise<object>} API 回應結果
   */
  async request(method, params = {}) {
    return new Promise((resolve, reject) => {
      const data = JSON.stringify(params);
      const options = {
        hostname: 'api.telegram.org',
        path: `/bot${this.botToken}/${method}`,
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

  /**
   * 發送文字訊息
   * @param {string|number} chatId - 聊天 ID
   * @param {string} text - 訊息內容
   * @param {object} options - 額外選項 (parse_mode, reply_to_message_id, etc.)
   */
  async sendMessage(chatId, text, options = {}) {
    const params = {
      chat_id: chatId,
      text: text,
      parse_mode: options.parse_mode || 'Markdown',
      ...options
    };
    return this.request('sendMessage', params);
  }

  /**
   * 取得 updates
   * @param {object} options - 選項 (offset, timeout, allowed_updates)
   */
  async getUpdates(options = {}) {
    return this.request('getUpdates', {
      offset: options.offset,
      timeout: options.timeout || 30,
      allowed_updates: options.allowed_updates || ['message']
    });
  }

  /**
   * 取得 bot 資訊
   */
  async getMe() {
    return this.request('getMe');
  }
}

module.exports = TelegramClient;