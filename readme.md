# AI 英語教練 / AI English Coach

這是一個使用 Google Gemini Pro API 的 AI 英語教練專案。它可以幫助你提升英語能力,並保存對話歷史供日後回顧。

This is an AI English Coach project using Google Gemini Pro API. It helps you improve your English skills and saves conversation history for later review.

## 先備條件 / Prerequisites

在開始之前，請確保您已具備：
Before getting started, make sure you have:

- Google Gemini API 金鑰 / Google Gemini API key
  - 前往 [Google AI Studio](https://makersuite.google.com/app/apikey) 申請
  - Visit [Google AI Studio](https://makersuite.google.com/app/apikey) to apply
- Python 開發環境 / Python development environment
  - 建議使用 VSCode 或 Cursor 等編輯器
  - Recommended editors: VSCode or Cursor
  - 需要安裝 Python 擴充功能
  - Python extension needs to be installed

## 功能特點 / Features

- 智能對話 / Intelligent Conversation
- 對話歷史保存 / Conversation History Saving
- 網頁查看歷史記錄 / Web Interface for History Viewing
- 即時語言糾正 / Real-time Language Correction
- 詳細的學習建議 / Detailed Learning Suggestions

## 安裝步驟 / Installation Steps

### 1. 下載專案 / Download Project
```bash
# 使用 Git 複製專案 / Clone the project using Git
git clone [專案網址 / project URL]

# 進入專案目錄 / Enter project directory
cd [專案目錄名稱 / project directory]
```

### 2. 設定 Python 環境 / Set up Python Environment
```bash
# 建議使用虛擬環境 / It's recommended to use a virtual environment
python -m venv venv

# Windows 啟動虛擬環境 / Activate virtual environment on Windows
venv\Scripts\activate

# macOS/Linux 啟動虛擬環境 / Activate virtual environment on macOS/Linux
source venv/bin/activate
```

### 3. 安裝所需套件 / Install Required Packages
```bash
# 安裝所有依賴套件 / Install all dependencies
pip install -r requirements.txt
```

### 4. 設定 API 金鑰 / Configure API Key
在 `english_coach.py` 中設定 Google API 金鑰 / Set up Google API key in `english_coach.py`:
   - 找到以下程式碼 / Find this code:
   ```python
   api_key = "在此處填入您的 Google API 金鑰"
   ```
   - 將您的 API 金鑰填入引號中 / Put your API key in the quotes

### 5. 確認安裝 / Verify Installation
```bash
# 測試程式是否能正常運行 / Test if the program runs correctly
python english_coach.py
```

## 使用方法 / Usage

1. 啟動程式 / Start the Program:
使用 vscode 或 cursor 等編輯器的 terminal 或 單純的 terminal，透過專案目錄啟動程式。
```bash
python english_coach.py
```

2. 查看對話歷史 / View Conversation History:
   - 啟動本地伺服器 / Start Local Server:
   ```bash
   python -m http.server 8000
   ```
   - 在瀏覽器中開啟 / Open in Browser:
   ```
   http://localhost:8000/view_history.html
   ```

## 使用提示 / Usage Tips

- 建議使用英文進行對話以獲得最佳學習效果
- It's recommended to use English for the best learning experience
- 可以請教練檢查語法、詢問用法或進行對話練習
- You can ask the coach to check grammar, inquire about usage, or practice conversation
- 輸入 'quit' 結束對話
- Type 'quit' to end the conversation

## 注意事項 / Important Notes

- 需要有效的 Google Gemini API 金鑰
- A valid Google Gemini API key is required
- 確保網路連線正常
- Ensure stable internet connection
- 對話歷史將自動保存在 chat_history.json 檔案中
- Conversation history is automatically saved in chat_history.json
- 使用瀏覽器查看歷史記錄時需要啟動本地伺服器
- Local server must be running to view history in browser

## 未來展望 / Future Plans

我們計畫加入以下功能：
We plan to add the following features:

- 可視化界面 / Visual Interface
  - 網頁應用程式 / Web Application
  - 手機 App / Mobile App
  - 桌面應用程式 / Desktop Application

- 進階功能 / Advanced Features
  - 語音辨識與對話 / Speech Recognition and Conversation
  - 即時發音評分 / Real-time Pronunciation Scoring
  - 個人化學習計劃 / Personalized Learning Plans
  - 學習進度追蹤 / Learning Progress Tracking
  - 多語言支援 / Multi-language Support

- 社群功能 / Community Features
  - 學習者社群 / Learner Community
  - 經驗分享平台 / Experience Sharing Platform
  - 學習夥伴配對 / Learning Partner Matching

歡迎貢獻想法與代碼！
Contributions and ideas are welcome!

