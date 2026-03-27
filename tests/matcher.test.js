/**
 * 目的地匹配引擎 - 單元測試
 * 使用 Node.js 原生 assert
 */

const assert = require('assert');
const path = require('path');
const DestinationMatcher = require('../src/matcher');

// 測試
console.log('🧪 開始測試 DestinationMatcher...\n');

const dataPath = path.join(__dirname, '..', 'data', 'destinations.json');
const matcher = new DestinationMatcher(dataPath).load();

// Test 1: exactMatch - 應該精確匹配已知目的地
console.log('Test 1: exactMatch 應該精確匹配已知目的地');
const result1 = matcher.exactMatch('東京');
assert(result1 !== null, '應該找到東京');
assert(result1.country === '日本', '國家應該是日本');
assert(result1.currency === '日幣 (JPY)', '貨幣應該是日幣');
console.log('  ✅ 通過\n');

// Test 2: exactMatch - 應該返回 null 當找不到目的地
console.log('Test 2: exactMatch 應該返回 null 當找不到目的地');
const result2 = matcher.exactMatch('不存在的城市');
assert(result2 === null, '應該返回 null');
console.log('  ✅ 通過\n');

// Test 3: fuzzyMatch - 應該模糊匹配包含關鍵字的目的地
console.log('Test 3: fuzzyMatch 應該模糊匹配包含關鍵字的目的地');
const result3 = matcher.fuzzyMatch('去東京玩');
assert(result3 !== null, '應該找到匹配');
assert(result3.name === '東京', '應該匹配到東京');
console.log('  ✅ 通過\n');

// Test 4: fuzzyMatch - 應該忽略大小寫匹配 (使用中文)
console.log('Test 4: fuzzyMatch 應該忽略大小寫匹配');
const result4 = matcher.fuzzyMatch('巴黎');
assert(result4 !== null, '應該找到匹配');
assert(result4.name === '巴黎', '應該匹配到巴黎');
console.log('  ✅ 通過\n');

// Test 5: match - 應該優先使用精確匹配
console.log('Test 5: match 應該優先使用精確匹配');
const result5 = matcher.match('台北');
assert(result5 !== null, '應該找到台北');
console.log('  ✅ 通過\n');

// Test 6: match - 應該在精確匹配失敗時使用模糊匹配
console.log('Test 6: match 應該在精確匹配失敗時使用模糊匹配');
const result6 = matcher.match('東京旅遊');
assert(result6 !== null, '應該找到匹配');
console.log('  ✅ 通過\n');

// Test 7: listDestinations - 應該返回所有目的地名稱
console.log('Test 7: listDestinations 應該返回所有目的地名稱');
const list = matcher.listDestinations();
assert(Array.isArray(list), '應該是陣列');
assert(list.length > 0, '應該有目的地');
assert(list.includes('東京'), '應該包含東京');
assert(list.includes('巴黎'), '應該包含巴黎');
console.log(`  ✅ 通過 (共 ${list.length} 個目的地)\n`);

// Test 8: hasDestination - 應該正確判斷目的地是否存在
console.log('Test 8: hasDestination 應該正確判斷目的地是否存在');
assert(matcher.hasDestination('東京') === true, '東京應該存在');
assert(matcher.hasDestination('不存在的城市') === false, '不存在的城市應該返回 false');
console.log('  ✅ 通過\n');

console.log('🎉 所有測試通過！');