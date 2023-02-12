# coding=utf-8
from locust import HttpLocust, TaskSet, task
import base64
import json
import random
import requests


USE_IRON_GATE = "true"  # string

USE_API_GATEWAY = False  # boolean
API_GATEWAY = "http://gateway-staging.shopback.com.tw"

# Login variable
EMAIL = "andy.li@shopback.com"  # 2464051
PASSWORD = "abcd1234"
COUNTRY = "TW"
DOMAIN = "www.shopback.com.tw"

# Without login
ACCOUNT_ID = 2461721  # andy.test@shopback.com

HEADERS = {
    "Content-Type": "application/json",
    "X-Shopback-Agent": "sbiosagent/1.0",
    "X-Shopback-Key": "q452R0g0muV3OXP8VoE7q3wshmm2rdI3",
    "X-Shopback-Store-Service": USE_IRON_GATE,
    "X-Shopback-Country": COUNTRY,
    "x-Shopback-domain": DOMAIN
}

keywords = ["二手書", "the", "二手", "書店", "二手書店", "a", "A", ".", "2", "的", "時尚", "女", "1/1", "小", "收納", "包", "3", "S", "s", "6*6尺蓆", "6*6尺藤席", "6", "兒童", "日本", "to", "Notebook", "運動", "二手書 書店", "手機", "學生", "notebook", "購物", "運動", "動", "To", "書", "T", "寶", "大", "多功能", "男", "生活", "618", "10/10", "台灣", "上衣", "便宜生活", "二手書包怡寶", "書寶", "書寶二手書", "防水", "免運", "可", "韓國", "架", "套裝", "8", "尺", "短袖", "寶寶", "100", "黑色", "版", "精品", "充電", "玻璃", "gift", "Ff手機殼", "Y1915手機殼", "手機殼", "橋村手機殼", "iphora 手機殼", "casetifyxr手機殼", "9*9", "book", "Book", "便攜", "錶", "Pornhub t恤", "貼", "背包", "BOOK", "7", "家居", "髮", "玩具", "i", "7-", "禮物", "I", "iphone", "iPhone", "Iphone", "apple iphone", "IPhone", "特價", "女新款", "廚房", "戶外", "m", "辦公", "T恤", "外套", "米漿T恤", "鹦鹉T恤", "電腦", "sousou手機殼", "Agu手機殼", "AUG手機殼", "紅墨水手機殼", "手機殼snobby", "paris 手機殼", "Uga 手機殼", "設計", "透氣", "t恤", "Bossini T恤", "&M", "lives t恤", "祖國 T恤", "12", "折疊", "汽車", "男士", "不銹鋼", "鞋", "墊", "長袖", "置物架", "全", "保護殼", "褲", "飾品", "北歐", "IPHONE", "iphone ", "寵物", "usb", "Usb", "咖啡", "on", "On", "led", "LED", "ON", "復古", "Zebar 復古", "大容量", "公司貨", "保護套", "L", "櫃", "居家", "l", "免", "台灣製", "電動", "機", "洋裝", "白", "牛仔", "三星", "samsung", "Samsung", "samsung三星", "潮", "長", "沙發", "USB", "Life", "C", "life", "成人", "c", "my", "無", "蘋果", "3c", "燈", "防曬", "Led", "3C", "國際牌", "組合", "保護貼", "台灣製造淨新", "裙", "台灣製造壁貼", "夾腿器台灣製", "生活館", "11", "收納盒", "健身", "氣質", "an", "米", "短袖t恤", "高", "金", "快速出貨", "收納架", "嬰兒", "Pro", "新", "超", "短褲", "背心", "寬", "陶瓷", "工具", "性感", "便宜生活館", "高腰", "支架", "衣服", "防曬防曬", "耳環", "電子書", "手機保護殼", "顯瘦", "女裝", "收納架 架", "化妝", "FZ10002 保護貼", "微奈米保護貼", "保護貼 A8plue", "i678保護貼", "襯衫", "AN", "Planner", "Hode 保護貼", "宿舍", "蘋果蘋果", "杯", "中", "振興", "E", "連身", "生日", "e", "收納置物架", "床頭", "春秋", "原廠", "床", "內衣", "手工", "不鏽鋼", "浴室", "送", "椅", "T1", "v", "帆布", "V", "24", "D+", "粉", "D", "綠", "B", "好", "水晶", "短袖上衣", "情侶", "螢幕", "小說", "長褲", "環保", "E&e", "g", "An", "恤上衣", "玫瑰", "保溫", "oppopro玻璃貼", "玻璃貼", "舒適", "whyand1/2", "貓", "D ", "清新", "辦公室", "耳機", "電池", "no", "智慧", "d", "懶人", "太陽", "雙", "拖鞋", "Iphone殼", "50", "G", "防摔殼", "b", "德國", "收納櫃", "no!no!", "全自動", "櫃 收納", "褲子", "貼紙", "DVD", "涼鞋", "壁掛", "架子", "DIY", "no no", "No No", "旅攝b&b", "Diy", "配件", "DVd", "有", "No", "收納櫃 ", "Shiado B&B", "Iphone手機", "三星galaxy", "samsung三星galaxy", "阿志小舖", "皇兒小舖", "Iphone 手機", "內褲", "iphone手機", "iphone 手機", "F", "f", "衣", "少女", "iphone 7puer手機殼", "t恤 上衣", "三星samsung galaxy", "玻璃貼玻璃", "迪士尼", "紅色", "Galaxy", "男休閒", "幼兒", "家", "清潔", "皮革", "便攜式", "米蘭", "love", "項鍊", "吊帶", "灰", "拼接", "超薄", "大碼", "抗菌", "上衣 女", "日式", "休閒鞋", "kids", "bagcom後背包", "Baby", "遮陽", "玻璃保護貼", "led燈", "women", "Hoke one one", "免運費", "女休閒", "和", "asus", "asus華碩", "貓咪", "床墊", "Asus", "電視", "後背包", "Chone後背包", "It", "sony", "world", "it", "Usb充電", "Aneno後背包", "Alleno後背包", "抽", "Sony", "美", "砂金項鍊", "運費", "棉麻", "One", "收納袋", "HOW", "水果", "項鍊項鍊", "手錶", "眼鏡", "沙灘", "Nesun 手錶", "布", "女鞋", "+0", "愛", "北港項鍊", "吧台玩具兒童", "背包後背包", ",內褲", "卡斯特後背包", "衣櫃", "ｆ", "Sarah 後背包", "車", "女 上衣", "上衣女", "Holle後背包", "Bagstationz 後背包", "Ellcom  後背包", "含，", "台灣製造", "麵", "預購", "手機保護套", "防摔手機殼", "asus華碩 pchome", "華碩", "無痕", "K", "Thormhill後背包", "k", "索尼", "iphone手機殼", "水壺", "ASUS", "ASUS ", "SONY", "露天 後背包", "iphone 手機殼", "sony索尼", "連身裙", "Iphone手機殼", "Aldo後背包", "cartt後背包", "Apple", "apple", "Iphone CR手機殼", "恤短袖上衣", "水杯", "家具", "apple ", "APPLE", "輪轂 手錶", "輪轂手錶", "華碩asus", "oshen 手錶", "筆記", "噴霧", "自動家用", "廚房收納", "線", "蝴蝶結", "保濕", "童裝", "學習", "三星手機", "抽屜", "牛仔褲", "s.f.s 鎖", "s.f.s 智能鎖", "風扇", "birthday", "旋轉", "loewe 手錶", "帽", "圓形", "銀", "NO.71809027", "3m", "3M", "長袖上衣", "椅子", "裙子", "Or", "ONE", "how", "one", "black", "s.", "保護貼玻璃貼 i7+ 黑滿版 10D", "保護貼玻璃貼 i7+ 黑滿版", "行李", "水", "鋁合金", "洗衣", "桌", "手機支架", "保護貼玻璃貼", "kitty", "登山", "情人節", "娃娃", "狗狗", "max", "餐桌", "Led 燈", "U", "u", "女短袖", "APPLE ", "logo", "夏天", "捲捲車包", "夏裝", "收納包", "本", "尺雙人", "多功能收納", "小清新", "螢幕貼", "P90.2", "刺繡", "禮盒", "防塵", "LED燈", "Best", "女運動", "包包", "文具", "電器", "鋼化保護貼", "day", "毛巾", "w", "防水防摔手機殼ipone6", "手機殼ipone6防摔防水", "XQ小舖", "自行車", "#14", "免打孔", "戒指", "note", "design", "帽子", "相機", "餐具", "健康", "遊戲", "DE", "r", "交換禮物", "18", "筆", "best", "整理收納", "拉兒小舖", "記憶", "流行", "手機殼防摔殼", "NOTE", "日", "防水防摔手機殼ipone", "優惠", "shop", "盤", "攝影", "露營", "samsung手機", "匿名2 二手", "珍珠", "收納箱", "三星手機手機", "CD", "Shop", "情人節禮物", "車用", "Note", "收納 刀具箱", "花", "牛仔褲牛仔", "Uv", "鋼化玻璃貼", "短袖上衣t恤", "衣櫥", "iphone 7", "iphone7", "平板", "精", "IPhone 7", "平板電腦", "傳輸", "紫", "音樂", "平板筆電", "襪", "狗", "日本製", "小米", "iphone保護殼", "衣架", "BE", "氣墊", "Iphone保護殼", "W", "Cd", "防摔保護殼", "cd", "Loka one one", "行動", "精華", "as", "夏", "de", "展示", "黃金", "24h", "批發", "厚底", "蛋糕", "鞋櫃", "收納箱-收納箱", "書桌", "斜背包", "媽媽", "LA", "la", "螢幕保護貼", "Sousou收納箱", "蘋果手機", "蘋果 蘋果手機", "R", "運動鞋", "手鍊", "三", "筆記本", "收納箱收納", "鞋子", "Kitty", "廁所", "碗", "AS", "leggings for women", "排汗", "Hello", "香水", "餐廳", "沐浴", "連衣裙", "腕錶", "La", "2手書", "杯子", "男時尚", "空氣", "買", "大尺碼", "聖誕", "戒指便宜", "Airpods2 二手", "充電器", "單開收納箱", "襪子", "GUCCL斜背包", "軟蟲收納包", "Nike", "NIKE", "nike", "鈦", "食品", "可折疊", "KITTY", "單肩包", "oppo", "Oppo", "OPPO", "雜貨", "All", "跟鞋", "按摩", "手機殼三星", "吋手機", "手套", "隱形", "熊", "平板 電腦", "睡衣", "正韓", "馬", "As", "英文", "抱枕", "Q", "茶", "行李箱", "廚房置物架", "傳輸線", "義大利", "ALL", "iphone 11", "Nike ", "Iphone 11", "小學生", "Iphone11", "iphone11", "法國", "iPhone 11", "廚房架", "iphone plus", "美容", "喇叭", "烘焙", "保護殼iphone", "精油", "perfect", "雪紡", "便宜衣架", "playbpu斜背包", "鋼化玻璃貼 貼", "坐墊", "英國", "打底衫", "mini", "蝦皮", "纖維+", "連身洋裝", "優雅", "hello kitty-", "SHOP", "科學", "靠背", "Hello Kitty", "空調", "girl", "V領", "糖果", "SHop", "枕頭", "H", "涼", "植物", "游泳", " 蝦皮", "蝦皮  ", "華為huawei", "三層", "湯米斜背包", "h", "斜背包Cugg", "斜背包Cuggi", "牙刷", "棒", "書包", "台北", "枕套", "H&H", "廚房 置物架", "兩用被", "代購", "adidas", "愛迪達", "Adidas", "t恤 女基督教", "t恤 女", "旗艦店", "POLO", "H:", "switch手鍊", "family", "H H", "天絲", "iphone 8", "xiaomi", "音響", "手機皮套", "機車", "幸福", "xs", "耐吉", "耐吉nike", "地墊", "單", "外套女", "腰", "茶几", "生日禮物", "學", "充電式", "鑰匙", "蝦皮蝦皮", "蝦皮 ", "小包", "air", "蝦皮˙", "蝦皮，", "xiaomi小米", "滿", "手機蘋果", "化妝收納", "尺床墊", "Iphone 7", "蝦皮'", "兒童家用", "時尚款", " 小米", "iphone xs", "中大尺碼", "收納化妝", "雨傘", "過濾", "枕頭枕頭", "公仔", "go", "Go", "雙人加大", "y", "小實 兩用被", "無袖", "Xiaomi", "鉛筆", "Iphone xs", "Perfect", "素帽t長袖", "軍 外套 女", "密碼", "茶幾", "手環", "Girl", "外套 女", "手機套", "皮帶", "Polo", "模型", "25", "三星手機殼", "三星samsung手機殼", "手提包", "冰絲涼外套 女", "Htc", "冰絲涼感外套 女", "休閒褲", "HTC", "Air", "洗澡", "愛買", "huawei華為", "餐椅", "samsung 手機殼", "床包組", "天使", "日本 日本製", "女 外套", "充電線", "推薦", "美甲", "木質", "紫外線", "男鞋", "完美", "polo", "huawei", "背帶", "兒童 成人", "廚房收納置物架", "Xr", "A4", "華為", "全密封床包組", "床包組 床", "睡衣 ", "瑜伽", "hello kitty", "n", "檸檬", "禮品", "休閒短褲", "孕婦", "Ipad", "ipad", "A字", "酒店", "浪漫", "pink", "PINK", "IPad", "旅遊", "連身 洋裝", "美式", "Dot", "兩件套", "鍋", "HELLO KITTY 皂模", "洗髮", "長裙", "真空", "fun", "純銀鍊", "皮", "軟殼手機殼", "七分", "iphone11pormix", "Iphone11pro256G", "親子", "冰箱", "廚房收納架", "Pink pink", "樂", "特大+", "Overdig iphone11", "Iphone11減光", "Iphone11 MWVE", "酷比扣iphone11", "IPHONE11", "床包組bts", "house", "襯衫 上衣", "arno iphone11", "IPhone 11", "智能", "保護貼 鋼化玻璃貼", "P", "招財", "小物", "鏡頭", "錢包", "折疊便攜", "iphone x", "17", "冷氣", "Fun", "馬桶", "防水包", "dot", "經濟型", "抽屜收納", "收納抽屜", "藍芽", "面膜", "連身裙 洋裝", "零食", "便當", "This", "天誅/女飾品", "購物中心", "柏麗塔嘉", "推車", "指甲", "泳衣", "books", "蝦皮24h", "Y", "Books", "冰絲", "空壓殼", "Travel", "西裝", "防潑水", "Go!", "GO!", "洋裝連身裙", "電影", "透明殼", "GO", "收納 抽屜", "南紡", "南紡購物中心", "犬", "iPad", "短裙", "無鋼圈", "腳踏", "運動", "日本", "手機", "學生", "T", "t", "書", "台灣", "10", "生活", "寶", "生活]", "大", "多功能", "創意", "in", "男", "防水", "上衣", "書寶二手書", "免運", "書寶", "架", "短袖", "玻璃", "韓國", "精品", "風", "出貨", "7", "套裝", "尺", "7-", "Unicron手機殼", "𝖬𝖮𝖬𝖮", "𝖬𝖮𝖪𝖮", "電子", "Ibiopen手機殼", "美國", "酷冷T恤", "T恤", "戶外", "12", "玩具", "小型", "設計", "髮", "家居", "Gift", "gift", "禮物", "m", "不銹鋼", "置物架", "鞋", "旅行", "復古", "保護殼", "飾品", "寵物", "居家", "咖啡", "USB", "usb", "L", "白", "機", "牛仔", "用", "秋比短袖T", "生活館", "保護套", "led", "大容量", "LED", "11", "超", "台灣製", "櫃", "潮", "samsung", "三星", "samsung三星", "洋裝", "公司貨", "Samsung", "3c", "高", "蘋果", "中", "C", "電子書", "防曬", "成人", "無", "蘋果蘋果", "衛生", "燈", "保護貼", "vivolite 保護貼", "Samung保護貼", "百搭韓版", "收納盒", "顯瘦", "國際牌", "嬰兒", "my", "米", "benk 保護貼", "健身", "金", "收納架", "杯", "背心", "短褲", "收納架 架", "皮套", "DIY", "情侶", "衣服", "V", "耳環", "性感", "v", "水晶", "最便宜的衣服", "短袖上衣", "手機保護殼", "襯衫", "女裝", "女裝 ", "床", "Life", "床頭", "30", "生日", "收納置物架", "50", "小說", "浴室", "內衣", "D+", "棉", "24", "不鏽鋼", "e", "春秋", "下", "e&e", "B", "螢幕", "藍色", "g", "E", "Iphone手機", "iphone 手機", "玻璃貼", "好", "長褲", "b", "清潔", "G", "德國", "On", "g-shockxbaby-g", "玻璃貼玻璃", "d+", "D", "d", "貓", "彈力", "zebra玻璃貼", "恤上衣", "被", "B&b", "電池", "no", "拖鞋", "辦公室", "love", "耳機", "no no", "純銀", "預購", "No no", "動物", "防摔殼", "大碼", "架子", "涼鞋", "收納櫃", "全自動", "壁掛", "gregory 2020 女", "gregory 女 2020", "皮革", "DVD", "家樂福 收納櫃", "滑托收納櫃", "astoria s.r.l.", "振興", "samsung galaxy", "三星galaxy", "samsung三星galaxy", "貼紙", "平底", "褲子", "三星samsung galaxy", "遮陽", "美", "內褲", "無痕", "衣", "台灣製造", "運費", "海錨手機殼iphone", "Iphone手機殼", "iphone手機殼", "F", "f", "Iphone 手機殼", "家", "皇兒小舖", "迪士尼", "便攜式", "男休閒", "愛", "手機防", "it", "沙灘", "How", "how", "歐爸小舖", "Forzen項鍊", "項鍊", "阿志小舖", "娃娃", "獨家", "吊帶", "帽", "頻譜項鍊", "代購", "led燈", "玻璃保護貼", "asus", "ASUS", "asus華碩", "Asus", "休閒鞋", "項鍊項鍊", "電視", "華碩", "後背包", "palladium後背包", "李焰 後背包", "Sony", "長袖上衣", "sony", "襪", "床墊", "SONY", "保護貼玻璃貼", "華碩asus", "Jonas後背包", "女休閒", "收納袋", "Led燈", "女鞋", "usb充電", "眼鏡", "遊戲", "Temi後背包", "sony索尼", "刺繡", "麵", "布", "手錶", "枕", "水果", "頻果手錶", "Gamin手錶", "車", "andriod 手錶", "文化", "夏天", "洗衣", "免運費", "衣櫃", "韓國三星手錶", "bastwin手錶", "珍珠", "Theodora手錶", "優惠", "風扇", "連身裙", "one", "水壺", "手機殼防摔殼", "手機殼 防摔", "apple", "Apple", "APPLE", "aPPLE", "防塵", "roots連身裙", "root連身裙", "英文", "防摔手機殼", "電器", "手機保護套", "禮盒", "登山", "samsungs206.2", "車用", "恤短袖上衣", "花", "K", "k", "跑步", "NO.B146", "水杯", "健康", "旋轉", "廚房收納", "噴霧", "家具", "三星手機手機", "椅子", "抽屜", "三星手機", "蝴蝶結", "童裝", "狗", "卡", "牛仔褲", "保濕", "正韓", "粉紅", "18+", "桌", "3M", "手機支架", "Cover", "手機三星", "3m", "流行", "裙子", "18", "水", "kitty", "女短袖", "餐桌", "u", "U", "餐桌餐桌", "鋁合金", "情人節", "黃金", "包包", "多功能收納", "文具", "UV", "毛巾", "note", "收納包", "One", "氣墊", "女運動", "day", "螢幕貼", "尺雙人", "免打孔", "自行車", "小清新", "w", "W", "三", "女款", "鋼化保護貼", "餐具", "戒指", "相機", "媽媽", "XS", "帽子", "限量", "露營", "收納箱", "收納箱-收納箱", "台灣現貨", "SHOP", "筆", "手套", "S.pellec", "平板", "平板電腦", "四季", "xs", "airbook 螢幕保護", "小米", "iphone 7", "椅座收納箱", "Sousou收納箱", "廁所", "7/8 GQ", "7/8 Gq", "音樂", "鋼化玻璃貼", "shop", "Shop", "衣架", "apple iphone 7", "iphone保護殼", "情人節禮物", "日本製", "7 8", "衣櫥", "蛋糕", "衣架衣架", "防摔保護殼", "紫", "抱枕", "iphone 7便宜", "螢幕保護貼", "到", "香水", "書桌", "運動鞋", "紙", "lucys手鍊", "DE", "筆記本", "襪子", "連衣裙", "鞋櫃", "手鍊", "大尺碼", "日本 日本製", "蘋果 蘋果手機", "充電器", "As", "碗", "鞋子", "蘋果手機", "24h", "涼", "生日禮物", "食品", "xiaomi", "斜背包", "空調", "男時尚", "La", "餐廳", "單肩包", "Nike", "nike", "吋手機", "按摩"]
category_ids = [10, 542, 67, 5, 8, 29, 6, 7, 54, 34, 4, 33, 1, 32, 11, 50, 63, 30, 14, 207, 59, 58, 55, 235, 27, 208, 51, 9, 2, 53, 248, 18, 66, 45, 25, 28, 476, 430, 472, 12, 390, 87, 249, 245, 42, 433, 38, 355, 61, 210, 40, 518, 458, 388, 204, 387, 206, 217, 41, 68, 459, 222, 39, 109, 81, 389, 209, 534, 24, 57, 300, 252, 539, 250, 37, 244, 221, 266, 71, 242, 477, 396, 36, 78, 397, 213, 35, 238, 432, 442, 282, 88, 270, 260, 16, 44, 75, 236, 43, 298, 90, 73, 52, 254, 47, 169, 3, 317, 522, 321, 515, 56, 232, 462, 400, 299, 423, 31, 362, 23, 296, 286, 391, 496, 95, 428, 251, 346, 495, 404, 79, 46, 358, 319, 436, 403, 216, 280, 460, 26, 365, 519, 203, 211, 381, 475, 70, 354, 220, 241, 333, 541, 49, 240, 429, 112, 167, 437, 538, 364, 308, 399, 490, 316, 392, 370, 528, 434, 420, 366, 243, 360, 347, 353, 395]
brand_ids = [62, 111, 58, 1, 61, 37, 43, 31, 81, 119, 36, 72, 34, 159, 97, 44, 45, 25, 19, 98, 56, 120, 106, 21, 66, 14, 52, 3, 15, 23, 4, 198, 85, 59, 47, 29, 125, 39, 41, 9, 75, 82, 48, 22, 26, 104, 17, 10, 160, 54, 24]
sorts = ['lp', 'hp', 'hb']


def login(email, password):
    url = "{}/members/sign-in".format(API_GATEWAY)
    payload = json.dumps({
        "email": email,
        "password": password,
        "client_user_agent": "test"
    })
    response = requests.request("POST", url, headers=HEADERS, data=payload)
    if response.status_code == 200:
        if 'auth' in response.json():
            return response.json()['auth']['access_token']
    print('Cant to get token {}'.format(response.json()))
    exit(1)


def generate_jwt_token(account_id):
    authorization_content = json.dumps({
        "uuid": "479c94048a8e410694ea24fc17302906",
        "iss": DOMAIN,
        "issuedAt": 1577477107.184,
        "iat": 1577477107,
        "exp": 1578773107,
        "id": account_id
    })
    return base64.b64encode(authorization_content.encode('utf-8')).decode('utf-8')


def get_search_url(page_type):
    page = 1
    size_per_page = 20
    include_non_affiliate_store = True
    sort = random.choice(sorts)
    url = "/search/product?page={}&sizePerPage={}&pageType={}&sort={}&includeNonAffiliateStore={}".format(
        page, size_per_page, page_type, sort, include_non_affiliate_store
    )
    if USE_API_GATEWAY is True:
        url = '/orca' + url
    if page_type == 'product':
        keyword = random.choice(keywords)
        url = url + "&name={}".format(keyword)
    elif page_type == 'category':
        category_id = random.choice(category_ids)
        url = url + "&categoryIds[]={}".format(category_id)
    elif page_type == 'brand':
        brand_id = random.choice(brand_ids)
        url = url + "&brandIds[]={}".format(brand_id)
    print(url)
    return url


class UserBehavior(TaskSet):
    if USE_API_GATEWAY is True:
        token = login(EMAIL, PASSWORD)
    else:
        token = generate_jwt_token(ACCOUNT_ID)
    print('Token: ', token)
    HEADERS['Authorization'] = 'JWT {}'.format(token)

    # url = API_GATEWAY + get_search_url('product')
    # req = requests.request('GET', url, headers=HEADERS)
    # print(req.text)

    @task(1)
    def search_product(self):
        url = get_search_url('product')
        self.client.get(url, headers=HEADERS, name="/orca/search/product - product")

    @task(1)
    def search_category(self):
        url = get_search_url('category')
        self.client.get(url, headers=HEADERS, name="/orca/search/product - category")

    @task(1)
    def search_brand(self):
        url = get_search_url('brand')
        self.client.get(url, headers=HEADERS, name="/orca/search/product - brand")


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 3000
    max_wait = 5000
