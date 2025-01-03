import os
import json
import threading
from datetime import datetime
import customtkinter as ctk
from dotenv import load_dotenv
import google.generativeai as genai

class EnglishCoachGUI:
    def __init__(self):
        """初始化 GUI"""
        self.window = ctk.CTk()
        self.window.title("AI 英語教練")
        self.window.geometry("800x600")
        
        # 創建標籤頁控制器
        self.tabview = ctk.CTkTabview(self.window)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=5)
        
        # 添加聊天和歷史標籤頁
        self.chat_tab = self.tabview.add("聊天")
        self.history_tab = self.tabview.add("歷史記錄")
        
        # 設置聊天標籤頁
        self.setup_chat_tab()
        
        # 設置歷史記錄標籤頁
        self.setup_history_tab()
        
        # 初始化消息歷史
        self.message_history = []
        
        # 設置 API 金鑰
        self.setup_api_key()
        
        self.window.mainloop()
    
    def setup_chat_tab(self):
        """設置聊天標籤頁"""
        # API 金鑰框架
        api_frame = ctk.CTkFrame(self.chat_tab)
        api_frame.pack(fill="x", padx=10, pady=5)
        
        api_label = ctk.CTkLabel(api_frame, text="API 金鑰:")
        api_label.pack(side="left", padx=5)
        
        self.api_entry = ctk.CTkEntry(api_frame, width=300, show="*")
        self.api_entry.pack(side="left", padx=5)
        
        api_button = ctk.CTkButton(api_frame, text="設定", command=self.save_api_key)
        api_button.pack(side="left", padx=5)
        
        # 聊天區域
        self.chat_text = ctk.CTkTextbox(self.chat_tab, wrap="word")
        self.chat_text.pack(fill="both", expand=True, padx=10, pady=5)
        
        # 輸入區域框架
        input_frame = ctk.CTkFrame(self.chat_tab)
        input_frame.pack(fill="x", padx=10, pady=5)
        
        self.input_entry = ctk.CTkEntry(input_frame, placeholder_text="輸入訊息...")
        self.input_entry.pack(side="left", fill="x", expand=True, padx=5)
        
        send_button = ctk.CTkButton(input_frame, text="發送", command=self.send_message)
        send_button.pack(side="left", padx=5)
        
        clear_button = ctk.CTkButton(input_frame, text="清除", command=self.clear_chat)
        clear_button.pack(side="left", padx=5)
        
        # 綁定回車鍵
        self.input_entry.bind("<Return>", lambda event: self.send_message())
    
    def setup_history_tab(self):
        """設置歷史記錄標籤頁"""
        # 搜尋框架
        search_frame = ctk.CTkFrame(self.history_tab)
        search_frame.pack(fill="x", padx=10, pady=5)
        
        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="搜尋歷史記錄...")
        self.search_entry.pack(side="left", fill="x", expand=True, padx=5)
        
        search_button = ctk.CTkButton(search_frame, text="搜尋", command=self.search_history)
        search_button.pack(side="left", padx=5)
        
        clear_search_button = ctk.CTkButton(search_frame, text="清除搜尋", command=self.clear_search)
        clear_search_button.pack(side="left", padx=5)
        
        # 歷史記錄顯示區域
        self.history_text = ctk.CTkTextbox(self.history_tab, wrap="word")
        self.history_text.pack(fill="both", expand=True, padx=10, pady=5)
    
    def search_history(self):
        """搜尋歷史記錄"""
        search_text = self.search_entry.get().strip().lower()
        if not search_text:
            self.display_all_history()
            return
            
        self.history_text.configure(state="normal")
        self.history_text.delete(1.0, "end")
        
        for msg in self.message_history:
            content = msg.get('content', '').lower()
            if search_text in content:
                msg_type = '我' if msg.get('role') == 'user' else 'AI 教練'
                self.history_text.insert("end", f"{msg_type}: {msg.get('content')}\n\n")
        
        self.history_text.configure(state="disabled")
    
    def clear_search(self):
        """清除搜尋"""
        self.search_entry.delete(0, "end")
        self.display_all_history()
    
    def display_all_history(self):
        """顯示所有歷史記錄"""
        self.history_text.configure(state="normal")
        self.history_text.delete(1.0, "end")
        
        for msg in self.message_history:
            msg_type = '我' if msg.get('role') == 'user' else 'AI 教練'
            self.history_text.insert("end", f"{msg_type}: {msg.get('content')}\n\n")
        
        self.history_text.configure(state="disabled")
    
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
                        self.message_history.append({
                            'role': 'user' if msg['type'] == 'human' else 'assistant',
                            'content': msg['content']
                        })
                    self.display_all_history()
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
            
            # 更新歷史記錄顯示
            self.display_all_history()
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

def main():
    """主程式"""
    app = EnglishCoachGUI()

if __name__ == "__main__":
    main() 