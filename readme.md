# 英語教練 AI 助手

這是一個使用 LangChain 和 Google Gemini Pro 建立的英語教練 AI 助手。它可以幫助您提升英語能力，並且會記住對話歷史，提供連貫的學習體驗。

## 功能特點

- 智能英語教練對話
- 記憶對話歷史
- 自定義教學提示
- 互動式學習體驗
- 使用免費的 Google Gemini Pro API

## 安裝步驟

1. 安裝所需套件：
```bash
pip install -r requirements.txt
```

2. 設定 API 金鑰：
打開 `english_coach.py`，找到以下程式碼：
```python
# 設定您的 Google API 金鑰
GOOGLE_API_KEY = "在此處填入您的 Google API 金鑰"
```
將您的 API 金鑰填入引號中即可。

3. 運行程式：
```bash
python english_coach.py
```

## 申請 Google API 金鑰步驟

1. 訪問 Google AI Studio (https://makersuite.google.com/app/apikey)
2. 登入您的 Google 帳戶
3. 點擊 "Get API key"
4. 創建一個新的 API 金鑰或使用現有的金鑰
5. 複製您的 API 金鑰
6. 將金鑰填入 `english_coach.py` 中的指定位置

## 使用方式

1. 啟動程式後，直接用英文或中文與 AI 教練對話
2. 教練會記住對話內容，提供更有針對性的回應
3. 輸入 'quit' 結束對話

## 注意事項

- 需要有效的 Google Gemini API 金鑰（免費使用）
- 建議使用英文進行對話以獲得最佳學習效果
- 對話歷史會在程式重啟後清除
- Google Gemini API 每分鐘有請求限制，但對於一般學習用途已經足夠
