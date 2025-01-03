import os
import json
import customtkinter as ctk
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
import threading
import webbrowser
from pathlib import Path

class EnglishCoachGUI:
    def __init__(self):
        self.setup_window()
        self.setup_api_key()
        self.initialize_chat()
        
    def setup_window(self):
        """設置主視窗"""
        self.window = ctk.CTk()
        self.window.title("AI 英語教練")
        self.window.geometry("800x600")
        
        # 設置網格權重
        self.window.grid_rowconfigure(1, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
        
        # API 金鑰輸入框
        self.api_frame = ctk.CTkFrame(self.window)
        self.api_frame.grid(row=0, column=0, padx=10, pady=5, sticky="ew")
        
        self.api_label = ctk.CTkLabel(self.api_frame, text="Google API 金鑰:")
        self.api_label.pack(side="left", padx=5)
        
        self.api_entry = ctk.CTkEntry(self.api_frame, width=300, show="*")
        self.api_entry.pack(side="left", padx=5)
        
        self.save_api_btn = ctk.CTkButton(self.api_frame, text="儲存金鑰", command=self.save_api_key)
        self.save_api_btn.pack(side="left", padx=5)
        
        # 聊天區域
        self.chat_frame = ctk.CTkFrame(self.window)
        self.chat_frame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        
        self.chat_text = ctk.CTkTextbox(self.chat_frame)
        self.chat_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # 輸入區域
        self.input_frame = ctk.CTkFrame(self.window)
        self.input_frame.grid(row=2, column=0, padx=10, pady=5, sticky="ew")
        
        self.input_entry = ctk.CTkEntry(self.input_frame, placeholder_text="輸入訊息...", width=600)
        self.input_entry.pack(side="left", padx=5, fill="x", expand=True)
        
        self.send_btn = ctk.CTkButton(self.input_frame, text="發送", command=self.send_message)
        self.send_btn.pack(side="left", padx=5)
        
        # 功能按鈕區
        self.button_frame = ctk.CTkFrame(self.window)
        self.button_frame.grid(row=3, column=0, padx=10, pady=5, sticky="ew")
        
        self.view_history_btn = ctk.CTkButton(
            self.button_frame, 
            text="查看歷史記錄", 
            command=self.view_history
        )
        self.view_history_btn.pack(side="left", padx=5)
        
        self.clear_btn = ctk.CTkButton(
            self.button_frame, 
            text="清除對話", 
            command=self.clear_chat
        )
        self.clear_btn.pack(side="left", padx=5)
        
        # 綁定Enter鍵
        self.input_entry.bind("<Return>", lambda event: self.send_message())
        
    def setup_api_key(self):
        """設置 API 金鑰"""
        load_dotenv()
        api_key = os.getenv('GOOGLE_API_KEY')
        if api_key and api_key.strip():
            self.api_entry.delete(0, "end")
            self.api_entry.insert(0, api_key)
            self.save_api_key()
    
    def save_api_key(self):
        """儲存 API 金鑰"""
        api_key = self.api_entry.get().strip()
        if not api_key:
            self.show_message("請輸入有效的 API 金鑰")
            return
        
        os.environ['GOOGLE_API_KEY'] = api_key
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(f'GOOGLE_API_KEY="{api_key}"')
        
        try:
            genai.configure(api_key=api_key)
            self.initialize_chat()
            self.show_message("API 金鑰設置成功！")
        except Exception as e:
            self.show_message(f"API 金鑰設置失敗：{str(e)}")
    
    def initialize_chat(self):
        """初始化聊天功能"""
        try:
            api_key = os.getenv('GOOGLE_API_KEY')
            if not api_key:
                self.show_message("請先設定 API 金鑰")
                return
                
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            self.message_history = []
            self.load_history()
            self.show_message("聊天功能初始化成功！")
        except Exception as e:
            self.show_message(f"初始化失敗：{str(e)}")
    
    def load_history(self):
        """載入歷史對話記錄"""
        try:
            if os.path.exists('chat_history.json'):
                with open('chat_history.json', 'r', encoding='utf-8') as f:
                    history = json.load(f)
                    for msg in history:
                        self.message_history.append(msg)
                        self.append_message(msg['type'], msg['content'])
        except Exception as e:
            self.show_message(f"載入歷史記錄失敗：{str(e)}")
    
    def save_history(self):
        """儲存對話歷史"""
        try:
            history = []
            for msg in self.message_history:
                msg_dict = {
                    'type': 'human' if msg.get('role') == 'user' else 'ai',
                    'content': msg.get('content'),
                    'timestamp': datetime.now().isoformat()
                }
                history.append(msg_dict)
            
            with open('chat_history.json', 'w', encoding='utf-8') as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.show_message(f"儲存歷史記錄失敗：{str(e)}")
    
    def format_prompt(self, user_input: str) -> str:
        """格式化提示詞"""
        coach_prompt = """As a professional English language coach, I will:
1. Help improve your English skills
2. Provide detailed feedback on grammar, vocabulary, and pronunciation
3. Always be encouraging and supportive
4. When correcting mistakes, first acknowledge what was done well
5. Explain the rules behind corrections
6. End with a practice suggestion
7. Remove markdown syntax, such as "**", just simple text

Student's input: """
        return coach_prompt + user_input
    
    def send_message(self):
        """發送訊息"""
        user_input = self.input_entry.get().strip()
        if not user_input:
            return
        
        self.input_entry.delete(0, "end")
        self.append_message('human', user_input)
        
        # 在新執行緒中處理 AI 回應
        threading.Thread(target=self.process_ai_response, args=(user_input,)).start()
    
    def process_ai_response(self, user_input):
        """處理 AI 回應"""
        try:
            if not hasattr(self, 'model'):
                self.show_message("請先設定有效的 API 金鑰")
                return
                
            formatted_input = self.format_prompt(user_input)
            self.message_history.append({"role": "user", "content": user_input})
            
            response = self.model.generate_content(formatted_input)
            
            if response.text:
                self.message_history.append({"role": "assistant", "content": response.text})
                self.window.after(0, self.append_message, 'ai', response.text)
                self.save_history()
            else:
                self.show_message("AI 未能生成有效回應")
            
        except Exception as e:
            error_msg = str(e)
            if "API key not available" in error_msg:
                self.show_message("錯誤：API 金鑰無效或未正確設定")
            elif "model not found" in error_msg:
                self.show_message("錯誤：無法存取 Gemini 模型，請確認您的 API 金鑰權限")
            else:
                self.show_message(f"發生錯誤：{error_msg}")
    
    def append_message(self, msg_type, content):
        """添加訊息到聊天視窗"""
        self.chat_text.configure(state="normal")
        if msg_type == 'human':
            self.chat_text.insert("end", "我: ", "bold")
        else:
            self.chat_text.insert("end", "AI 教練: ", "bold")
        self.chat_text.insert("end", f"{content}\n\n")
        self.chat_text.configure(state="disabled")
        self.chat_text.see("end")
    
    def show_message(self, message):
        """顯示系統訊息"""
        self.chat_text.configure(state="normal")
        self.chat_text.insert("end", f"系統: {message}\n\n", "system")
        self.chat_text.configure(state="disabled")
        self.chat_text.see("end")
    
    def clear_chat(self):
        """清除聊天內容"""
        self.chat_text.configure(state="normal")
        self.chat_text.delete(1.0, "end")
        self.chat_text.configure(state="disabled")
        self.message_history = []
        self.save_history()
    
    def view_history(self):
        """查看歷史記錄"""
        # 啟動本地伺服器
        import http.server
        import socketserver
        import threading
        
        def run_server():
            PORT = 8000
            Handler = http.server.SimpleHTTPRequestHandler
            try:
                with socketserver.TCPServer(("", PORT), Handler) as httpd:
                    self.show_message(f"伺服器已啟動於 http://localhost:{PORT}")
                    webbrowser.open(f'http://localhost:{PORT}/view_history.html')
                    httpd.serve_forever()
            except Exception as e:
                self.show_message(f"啟動伺服器失敗：{str(e)}")
        
        threading.Thread(target=run_server, daemon=True).start()
    
    def run(self):
        """運行應用程式"""
        self.window.mainloop()

def main():
    app = EnglishCoachGUI()
    app.run()

if __name__ == "__main__":
    main() 