from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv
import google.generativeai as genai

# 載入 .env 檔案
load_dotenv()

# 設定 API 金鑰（請將您的 API 金鑰填入下方）
GOOGLE_API_KEY = "在此處填入您的 Google API 金鑰"

# 如果環境變數中沒有 API 金鑰，就使用上面設定的金鑰
if not os.getenv('GOOGLE_API_KEY'):
    os.environ['GOOGLE_API_KEY'] = GOOGLE_API_KEY

# 配置 Google Gemini
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

class EnglishCoach:
    def __init__(self):
        # 初始化語言模型
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-pro",
            temperature=0.7,
            convert_system_message_to_human=True,
            google_api_key=os.getenv('GOOGLE_API_KEY')  # 直接傳入 API 金鑰
        )
        
        # 創建對話記憶
        self.memory = ConversationBufferMemory()
        
        # 定義提示模板
        template = """You are a professional English language coach. Your role is to help students improve their English skills.
Please provide detailed feedback on grammar, vocabulary, and pronunciation when appropriate.
Always encourage the student and maintain a positive, supportive attitude.
        
Current conversation:
{history}

Student: {input}
Coach: """
        
        self.prompt = PromptTemplate(
            input_variables=["history", "input"],
            template=template
        )
        
        # 創建對話鏈
        self.conversation = ConversationChain(
            llm=self.llm,
            memory=self.memory,
            prompt=self.prompt,
            verbose=True
        )
    
    def chat(self, user_input: str) -> str:
        """處理使用者輸入並返回教練的回應"""
        try:
            response = self.conversation.predict(input=user_input)
            return response
        except Exception as e:
            return f"發生錯誤：{str(e)}\n請確認您的 API 金鑰是否正確設定。"

def main():
    # 檢查 API 金鑰是否已設定
    if not os.getenv('GOOGLE_API_KEY') or os.getenv('GOOGLE_API_KEY') == "在此處填入您的 Google API 金鑰":
        print("錯誤：請先在程式碼中設定您的 Google API 金鑰！")
        return

    # 初始化英語教練
    coach = EnglishCoach()
    
    print("歡迎使用英語教練！(輸入 'quit' 來結束對話)")
    print("提示：建議使用英文進行對話以獲得最佳學習效果")
    
    while True:
        user_input = input("\n你: ")
        if user_input.lower() == 'quit':
            break
            
        response = coach.chat(user_input)
        print("\n教練:", response)

if __name__ == "__main__":
    main() 