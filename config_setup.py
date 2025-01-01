import os

def 設定API金鑰():
    print("\n=== Google API 金鑰設定精靈 ===")
    print("請將您的 Google API 金鑰貼在下方")
    print("（如果您還沒有 API 金鑰，請訪問 https://makersuite.google.com/app/apikey 申請）")
    
    api_金鑰 = input("\n請輸入您的 API 金鑰: ").strip()
    
    # 檢查是否為空
    if not api_金鑰:
        print("錯誤：API 金鑰不能為空！")
        return False
    
    try:
        # 建立或更新 .env 檔案
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(f'GOOGLE_API_KEY={api_金鑰}')
        print("\n✓ API 金鑰已成功儲存！")
        print("現在您可以執行 english_coach.py 來開始使用英語教練了！")
        return True
    except Exception as e:
        print(f"\n錯誤：無法儲存 API 金鑰！\n錯誤訊息：{str(e)}")
        return False

def 檢查API金鑰():
    """檢查是否已經設定 API 金鑰"""
    if os.path.exists('.env'):
        with open('.env', 'r', encoding='utf-8') as f:
            content = f.read()
            if 'GOOGLE_API_KEY' in content:
                return True
    return False

if __name__ == "__main__":
    if 檢查API金鑰():
        print("\n您已經設定過 API 金鑰！")
        重新設定 = input("是否要重新設定？(y/n): ").lower()
        if 重新設定 == 'y':
            設定API金鑰()
    else:
        設定API金鑰() 