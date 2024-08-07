# Name_Culling
## 檔名剔除器

![Name Culling cover](https://github.com/zz22558822/Name_Culling/blob/main/img/Name_Culling.png)

---

## 使用方法:
1. 使用 Name_Culling.exe
2. 輸入要檢查的資料夾目錄 (若 Name_Culling_Default.txt 存在且符合則會跳過)
3. 輸入是否限制副檔名 (預設y)
4. 決定是否處理所有子資料夾的檔案 (預設n)

## 檔案結構
File/  
├── Name_Culling.exe  
├── Name_Culling_Default.txt  
├── Name_Culling_Settings.txt  
└── Name_Culling_Whitelist.txt  


Name_Culling.exe → 主程序  
Name_Culling_Default.txt → 預設路徑(若想手動輸入請改名或刪除)  
Name_Culling_Settings.txt → 去除要包含的字串(每行一個)，建議字數多的優先在上方  
Name_Culling_Whitelist.txt → 限定處理副檔名的白名單  

---

## Releases 有打包完成的版本(建議使用)
