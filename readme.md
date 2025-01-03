# AI 英語教練 / AI English Coach

這是一個使用 Google Gemini Pro API 的 AI 英語教練專案，提供圖形化介面，幫助你提升英語能力並保存對話歷史供日後回顧。

This is an AI English Coach project using Google Gemini Pro API with a graphical user interface. It helps you improve your English skills and saves conversation history for later review.

## 先備條件 / Prerequisites

在開始之前，請確保您已具備：
Before getting started, make sure you have:

- Google Gemini API 金鑰 / Google Gemini API key
  - 前往 [Google AI Studio](https://makersuite.google.com/app/apikey) 申請
  - Visit [Google AI Studio](https://makersuite.google.com/app/apikey) to apply
- Python 開發環境 / Python development environment
  - 建議使用 Python 3.8 或更高版本
  - Python 3.8 or higher is recommended

## 功能特點 / Features

- 圖形化使用者介面 / Graphical User Interface
- 智能對話 / Intelligent Conversation
- 對話歷史保存與搜尋 / Conversation History Saving and Searching
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

## 使用方法 / Usage

1. 啟動程式 / Start the Program:
```bash
python english_coach_gui.py
```

2. 設定 API 金鑰 / Set up API Key:
   - 在程式視窗中輸入您的 Google API 金鑰
   - Enter your Google API key in the program window
   - 點擊「設定」按鈕保存
   - Click the "Set" button to save

3. 開始對話 / Start Conversation:
   - 在輸入框中輸入英文訊息
   - Type English messages in the input box
   - 按下「發送」按鈕或按 Enter 鍵發送
   - Press the "Send" button or hit Enter to send

4. 查看歷史記錄 / View History:
   - 切換到「歷史記錄」標籤頁
   - Switch to the "History" tab
   - 使用搜尋功能尋找特定對話
   - Use the search function to find specific conversations

## 使用提示 / Usage Tips

- 建議使用英文進行對話以獲得最佳學習效果
- It's recommended to use English for the best learning experience
- 可以請教練檢查語法、詢問用法或進行對話練習
- You can ask the coach to check grammar, inquire about usage, or practice conversation
- 對話歷史會自動保存，可隨時在歷史記錄標籤頁查看
- Conversation history is automatically saved and can be viewed in the History tab

## 注意事項 / Important Notes

- 需要有效的 Google Gemini API 金鑰
- A valid Google Gemini API key is required
- 確保網路連線正常
- Ensure stable internet connection
- 對話歷史將自動保存在 chat_history.json 檔案中
- Conversation history is automatically saved in chat_history.json

## 未來展望 / Future Plans

我們計畫加入以下功能：
We plan to add the following features:

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

