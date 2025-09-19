import os
import sys
from alive_progress import alive_bar

Settings_path = 'Name_Culling_Settings.txt'  # 要剃除的字串
Whitelist_path = 'Name_Culling_Whitelist.txt'  # 只處理指定的副檔名白名單
default_path = 'Name_Culling_Default.txt'  # 預設檔案路徑，這樣就不用手動輸入


# 顯示版本資訊
def show_version_info():
    print("====================================================================================")
    print("=                                                                                  =")
    print("=                                Name_Culling v2.2.0                               =")
    print("=                                                                       By. Chek   =")
    print("====================================================================================")
    print()


# 檢查檔案是否存在，若不存在則建立
def check_and_create_file(filepath, default_content=""):
    try:
        if not os.path.exists(filepath):
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(default_content)
            print(f"已建立: {filepath}")
    except IOError as e:
        print(f"建立文件失敗: {filepath} - {e}")


# 檢查預設路徑是否存在
def check_default_path():
    try:
        if os.path.exists(default_path):
            with open(default_path, 'r', encoding='utf-8') as file:
                folder_path = file.readline().strip()
            return folder_path
    except IOError as e:
        print(f"讀取預設路徑失敗: {e}")
    return None


# 讀取白名單檔案，返回包含所有副檔名的列表
def read_whitelist(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            whitelist = [line.strip().lstrip('.') for line in file if line.strip()]
            print(f"副檔名白名單: {whitelist}")
            return whitelist
    except FileNotFoundError:
        print(f"檔案未找到: {filepath}")
        return []
    except IOError as e:
        print(f"讀取白名單失敗: {e}")
        return []


# 讀取去除字串設定檔案，返回包含所有需要去除字串的列表
def read_culling_settings(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            culling_settings = [line.strip() for line in file if line.strip()]
            print(f"要刪除的字串: {culling_settings}")
            print()
            return culling_settings
    except FileNotFoundError:
        print(f"檔案未找到: {filepath}")
        return []
    except IOError as e:
        print(f"讀取去除字串失敗: {e}")
        return []


# 判斷檔案是否應該處理
def should_process_file(filename, whitelist, restrict_extensions):
    if not restrict_extensions:
        return True
    file_extension = os.path.splitext(filename)[1][1:]  # 取得副檔名，不帶點
    return file_extension in whitelist


# 防止重新命名重複
def get_unique_name(directory, name):
    base, extension = os.path.splitext(name)
    counter = 1
    new_name = name

    # 確保名稱未更動
    while os.path.exists(os.path.join(directory, new_name)):
        new_name = f"{base}-{counter}{extension}"
        counter += 1

    return new_name


# 重新命名
def process_files(folder, restrict_extensions=True):
    # 根據是否限制副檔名來讀取白名單
    whitelist = read_whitelist(Whitelist_path) if restrict_extensions else []
    # 讀取去除字串設定檔案
    culling_settings = read_culling_settings(Settings_path)

    # 處理子資料夾選擇
    while True:
        All_Subfolders = input("▲ 是否處理所有子資料夾(預設n) (y/n): ").strip().lower()
        print()
        if All_Subfolders in ['y', 'n', '']:
            if All_Subfolders == 'y':
                # 遍歷資料夾中的所有檔案，根據白名單和副檔名限制過濾 (包含子資料夾)
                files_to_process = [
                    (root, filename)
                    for root, _, files in os.walk(folder)
                    for filename in files
                    if should_process_file(filename, whitelist, restrict_extensions)
                ]
            else:
                # 遍歷指定資料夾中的檔案 (不包含子資料夾)
                files_to_process = [
                    (folder, filename)
                    for filename in os.listdir(folder)
                    if os.path.isfile(os.path.join(folder, filename)) and
                    should_process_file(filename, whitelist, restrict_extensions)
                ]
            break
        else:
            print("輸入無效，請輸入 'y' 或 'n'。")
            print()

    # 儲存需要重新命名的檔案
    files_to_rename = []
    for root, filename in files_to_process:
        new_name = filename
        # 遍歷所有要去除的字串並從檔案名稱中去除
        for to_remove in culling_settings:
            new_name = new_name.replace(to_remove, "")

        # 移除檔名開頭和結尾的空白
        new_name = new_name.strip()

        # 檢查檔案名稱是否已經改變
        if filename != new_name:
            files_to_rename.append((root, filename, new_name))

    # 如果沒有需要重新命名的檔案，顯示提示訊息並結束
    if not files_to_rename:
        print('---------------------------------------------')
        print(' ※ 當前資料夾位置內沒有需要重新命名的檔案。')
        print('---------------------------------------------')
        return

    # 使用進度條來顯示重新命名進度
    with alive_bar(len(files_to_rename), title='處理中...') as bar:
        for root, filename, new_name in files_to_rename:
            # 確保檔案名稱唯一，避免衝突
            new_name = get_unique_name(root, new_name)
            old_path = os.path.join(root, filename)
            new_path = os.path.join(root, new_name)
            # 重新命名檔案
            if old_path != new_path:
                # print(f"重新命名: {old_path} -> {new_path}")
                os.rename(old_path, new_path)
            bar()

    print('---------------------------------------------')
    print(f' ※ 完成處理: {len(files_to_rename)} 個檔案。')
    print('---------------------------------------------')


# 主程序
def main():
    # 顯示檔案版本
    show_version_info()

    # 檢查所有必要的檔案是否存在
    if not os.path.exists(Settings_path):
        check_and_create_file(Settings_path)
    if not os.path.exists(Whitelist_path):
        check_and_create_file(Whitelist_path)
    if not os.path.exists(default_path):
        check_and_create_file(default_path)
        
    # 如果有建立檔案 提示用戶重新運行
    if not os.path.exists(Settings_path) or not os.path.exists(Whitelist_path) or not os.path.exists(default_path):
        print("請用戶填入資料後重新運行本程序。")
        print()
        os.system('pause')
        sys.exit()

    # 讓用戶輸入目錄位置
    folder_path = check_default_path()  # 調用預設路徑
    if not folder_path or not os.path.isdir(folder_path):  # 若預設路徑是錯誤的目錄
        while True:
            folder_path = input("▲ 請輸入目錄位置: ").strip()
            if os.path.isdir(folder_path):
                break
            else:
                print("輸入的目錄無效，請重新輸入。")
                print()

    # 限制副檔名的選擇
    while True:
        restrict_extensions = input("▲ 是否限制副檔名(預設y) (y/n): ").strip().lower()
        print()
        if restrict_extensions in ['y', 'n', '']:
            process_files(folder_path, restrict_extensions in ['y', ''])
            break
        else:
            print("輸入無效，請輸入 'y' 或 'n'。")
            print()


# 初始化
if __name__ == "__main__":
    main()  # 主程序
    print()
    os.system('pause')
    sys.exit()
