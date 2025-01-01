from langchain.llms import GooglePalm
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv
import google.generativeai as genai

def 設定API金鑰(api_key: str) -> bool:
    """直接設定 API 金鑰"""
    try:
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(f'GOOGLE_API_KEY={api_key}')
        return True
    except Exception:
        return False

# 設定您的 Google API 金鑰
GOOGLE_API_KEY = "在此處填入您的 Google API 金鑰"
設定API金鑰(GOOGLE_API_KEY)

# Load environment variables
load_dotenv()

# Configure Google Gemini
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

class EnglishCoach:
    def __init__(self):
        # Initialize the language model
        self.llm = GooglePalm(
            temperature=0.7,
            model_name="models/text-bison-001"
        )
        
        # Create a conversation memory
        self.memory = ConversationBufferMemory()
        
        # Define the prompt template for the English coach
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
        
        # Create the conversation chain
        self.conversation = ConversationChain(
            llm=self.llm,
            memory=self.memory,
            prompt=self.prompt,
            verbose=True
        )
    
    def chat(self, user_input: str) -> str:
        """
        Process user input and return coach's response
        """
        response = self.conversation.predict(input=user_input)
        return response

def main():
    # Initialize the English coach
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