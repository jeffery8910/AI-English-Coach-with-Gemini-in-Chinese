from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
import os
import json
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai

def setup_api_key():
    """設定並驗證 API 金鑰"""
    # 載入 .env 檔案
    load_dotenv()
    
    # 設定 API 金鑰
    api_key = "AIzaSyCwTD1tu5nS7kgEhsUgaAQjH7pzlTadRX4"
    
    # 確保 API 金鑰是有效的格式
    if not isinstance(api_key, str) or not api_key.strip():
        raise ValueError("API 金鑰格式無效")
    
    # 設定環境變數
    os.environ['GOOGLE_API_KEY'] = api_key.strip()
    
    try:
        # 配置 Google Gemini
        genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
        return True
    except Exception as e:
        print(f"API 金鑰設定錯誤：{str(e)}")
        return False

class EnglishCoach:
    def __init__(self):
        # 確保 API 已正確設定
        if not setup_api_key():
            raise RuntimeError("無法初始化 API 設定")
            
        # 初始化語言模型
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-pro",
            temperature=0.7,
            google_api_key=os.getenv('GOOGLE_API_KEY')
        )
        
        # 定義角色提示詞
        self.role_prompt = """You are a professional English language coach. 
Your role is to help students improve their English skills.
Please provide detailed feedback on grammar, vocabulary, and pronunciation when appropriate.
Always encourage the student and maintain a positive, supportive attitude.
When correcting mistakes, first acknowledge what was done well, then provide corrections.
For each correction, explain the rule or reason behind it.
End each response with a small encouragement or practice suggestion."""
        
        # 創建提示模板
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", self.role_prompt),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}")
        ])
        
        # 創建對話鏈
        self.chain = self.prompt | self.llm
        
        # 初始化對話歷史
        self.message_history = []
        
        # 載入之前的對話歷史
        self.load_history()
    
    def load_history(self):
        """載入歷史對話記錄"""
        try:
            if os.path.exists('chat_history.json'):
                with open('chat_history.json', 'r', encoding='utf-8') as f:
                    history = json.load(f)
                    # 將JSON數據轉換回消息對象
                    for msg in history:
                        if msg['type'] == 'human':
                            self.message_history.append(HumanMessage(content=msg['content']))
                        elif msg['type'] == 'ai':
                            self.message_history.append(AIMessage(content=msg['content']))
        except Exception as e:
            print(f"載入歷史記錄時發生錯誤：{str(e)}")
    
    def save_history(self):
        """儲存對話歷史到JSON檔案"""
        try:
            # 將消息對象轉換為可序列化的字典
            history = []
            for msg in self.message_history:
                msg_dict = {
                    'type': 'human' if isinstance(msg, HumanMessage) else 'ai',
                    'content': msg.content,
                    'timestamp': datetime.now().isoformat()
                }
                history.append(msg_dict)
            
            # 儲存到檔案
            with open('chat_history.json', 'w', encoding='utf-8') as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"儲存歷史記錄時發生錯誤：{str(e)}")
    
    def chat(self, user_input: str) -> str:
        """處理使用者輸入並返回教練的回應"""
        try:
            if not user_input.strip():
                return "請輸入一些內容讓我幫您檢查或回答。"
            
            # 添加新的訊息到歷史記錄
            self.message_history.append(HumanMessage(content=user_input))
            
            # 使用新的方式處理對話
            response = self.chain.invoke({
                "history": self.message_history,
                "input": user_input
            })
            
            # 將 AI 的回應添加到歷史記錄
            self.message_history.append(AIMessage(content=response.content))
            
            # 儲存更新後的歷史記錄
            self.save_history()
            
            return response.content
            
        except Exception as e:
            error_msg = str(e)
            if "API key not available" in error_msg:
                return "錯誤：API 金鑰無效或未正確設定。"
            elif "model not found" in error_msg:
                return "錯誤：無法存取 Gemini 模型，請確認您的 API 金鑰權限。"
            else:
                return f"發生錯誤：{error_msg}"

def main():
    try:
        # 初始化英語教練
        coach = EnglishCoach()
        
        print("歡迎使用英語教練！(輸入 'quit' 來結束對話)")
        print("提示：建議使用英文進行對話以獲得最佳學習效果")
        print("您可以：")
        print("1. 請教練檢查您的英文語法")
        print("2. 詢問英文用法相關問題")
        print("3. 練習英文對話")
        print("\n對話歷史將被儲存在 chat_history.json 檔案中")
        
        while True:
            user_input = input("\n你: ")
            if user_input.lower() == 'quit':
                break
                
            response = coach.chat(user_input)
            print("\n教練:", response)
    except Exception as e:
        print(f"程式初始化錯誤：{str(e)}")
        print("請確認：")
        print("1. API 金鑰是否正確")
        print("2. 網路連線是否正常")
        print("3. 是否已安裝所有必要套件")

if __name__ == "__main__":
    main() 