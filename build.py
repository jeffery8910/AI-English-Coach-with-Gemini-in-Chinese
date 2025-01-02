import PyInstaller.__main__
import os
import sys
import shutil
import time
import site
import customtkinter

def get_customtkinter_path():
    """獲取 customtkinter 套件路徑"""
    return os.path.dirname(customtkinter.__file__)

def clean_dist():
    """清理 dist 目錄"""
    dist_dir = os.path.join(current_dir, 'dist')
    if os.path.exists(dist_dir):
        try:
            shutil.rmtree(dist_dir)
            time.sleep(1)  # 等待系統完全釋放資源
        except Exception as e:
            print(f"清理 dist 目錄時發生錯誤: {e}")
            print("請手動關閉所有相關程式後再試")
            sys.exit(1)

# 獲取當前目錄
current_dir = os.path.dirname(os.path.abspath(__file__))

# 清理舊的建置檔案
clean_dist()

# 獲取 customtkinter 路徑
ctk_path = get_customtkinter_path()

# 準備 PyInstaller 參數
params = [
    'english_coach_gui.py',  # 主程式檔案
    '--name=AI英語教練',  # 輸出的程式名稱
    '--onefile',  # 打包成單一檔案
    '--windowed',  # 使用 GUI 模式
    '--icon=icon.ico',  # 如果有圖示檔案的話
    '--add-data=view_history.html;.',  # 添加額外檔案
    f'--add-data={ctk_path};customtkinter/',  # 添加 customtkinter 資源
    '--noconfirm',  # 覆蓋現有檔案
    '--clean',  # 清理暫存檔案
    
    # 安全性標記
    '--disable-windowed-traceback',  # 禁用視窗追蹤
    '--runtime-tmpdir=.',  # 使用當前目錄作為臨時目錄
    
    # 版本資訊
    '--version-file=version.txt',
    
    # 修正模組導入
    '--hidden-import=pydantic.v1',
    '--hidden-import=pydantic.v2',
    '--hidden-import=pydantic.v1.decorator',
    '--hidden-import=pydantic.v1.utils',
    '--hidden-import=pydantic.v1.validators',
    '--hidden-import=pydantic_core',
    '--hidden-import=pydantic_core._pydantic_core',
    '--hidden-import=langchain',
    '--hidden-import=langchain.chat_models',
    '--hidden-import=langchain.schema',
    '--hidden-import=langchain_core',
    '--hidden-import=langchain_community',
    '--hidden-import=google.generativeai',
    '--hidden-import=customtkinter',
    '--hidden-import=customtkinter.windows.widgets',
    '--hidden-import=customtkinter.windows.widgets.core_widget_classes',
    '--hidden-import=customtkinter.windows.widgets.utility',
    
    # 收集所有相關套件
    '--collect-submodules=langchain',
    '--collect-submodules=langchain_core',
    '--collect-submodules=langchain_community',
    '--collect-submodules=google.generativeai',
    '--collect-submodules=customtkinter',
    
    # 收集數據文件
    '--collect-data=langchain',
    '--collect-data=langchain_core',
    '--collect-data=langchain_community',
    '--collect-data=google.generativeai',
    '--collect-data=customtkinter',
]

# 創建版本信息檔案
version_info = '''VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo([
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'AI English Coach'),
         StringStruct(u'FileDescription', u'AI English Learning Assistant - Educational Software'),
         StringStruct(u'FileVersion', u'1.0.0'),
         StringStruct(u'InternalName', u'AI_English_Coach'),
         StringStruct(u'LegalCopyright', u'Copyright (c) 2024'),
         StringStruct(u'OriginalFilename', u'AI英語教練.exe'),
         StringStruct(u'ProductName', u'AI English Coach'),
         StringStruct(u'ProductVersion', u'1.0.0'),
         StringStruct(u'Comments', u'Educational AI Assistant for English Learning'),
         StringStruct(u'LegalTrademarks', u'AI English Coach is a trademark of its respective owner')])
    ]),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)'''

print("開始打包程序...")
print("1. 清理舊檔案")
clean_dist()

print("2. 寫入版本信息")
with open('version.txt', 'w', encoding='utf-8') as f:
    f.write(version_info)

try:
    print("3. 執行打包")
    print(f"CustomTkinter 路徑: {ctk_path}")
    PyInstaller.__main__.run(params)
    print("\n打包完成！檔案位於 dist 目錄中")
    
    print("4. 清理臨時檔案")
    if os.path.exists('version.txt'):
        os.remove('version.txt')
        
except Exception as e:
    print(f"\n打包過程中發生錯誤: {e}")
    print("請確保：")
    print("1. 已關閉所有相關程式")
    print("2. 有足夠的磁碟空間")
    print("3. 具有寫入權限")
    print("4. 所有必要的套件都已正確安裝") 