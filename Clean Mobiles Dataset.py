import re
import pandas as pd

# 讀取 CSV 檔案，指定編碼
file_path = 'C:/Users/chao/Desktop/Data Analysis/Datasets/Mobiles Dataset (2025).csv'
df = pd.read_csv(file_path, encoding="ISO-8859-1")

# 定義貨幣轉換匯率（最新匯率，請確認）
exchange_rates = {
    "India": 0.012,     # 1 INR = 0.012 USD
    "China": 0.14,      # 1 CNY = 0.14 USD
    "Pakistan": 0.0036, # 1 PKR = 0.0036 USD
    "Dubai": 0.27       # 1 AED = 0.27 USD
}

# 定義函式來清理價格並轉換為 USD
def clean_and_convert(price_str, country):
    if pd.isna(price_str) or price_str == "" or price_str == "-":
        return None  # 避免 NaN 或空值
    
    # 移除所有非數字字符（保留小數點）
    price_str = re.sub(r"[^\d.]", "", str(price_str))
    
    try:
        price = float(price_str)  # 轉換為數字
        return round(price * exchange_rates[country], 2)  # 轉換為 USD，保留兩位小數
    except ValueError:
        return None  # 如果轉換失敗，返回 None

# 應用函式到各國價格
df["Launched Price (India) (USD)"] = df["Launched Price (India)"].apply(lambda x: clean_and_convert(x, "India"))
df["Launched Price (China) (USD)"] = df["Launched Price (China)"].apply(lambda x: clean_and_convert(x, "China"))
df["Launched Price (Pakistan) (USD)"] = df["Launched Price (Pakistan)"].apply(lambda x: clean_and_convert(x, "Pakistan"))
df["Launched Price (Dubai) (USD)"] = df["Launched Price (Dubai)"].apply(lambda x: clean_and_convert(x, "Dubai"))

# 清理美金價格欄位（移除 "USD " 和逗號，並轉換為浮點數）
df["Launched Price (USA)"] = df["Launched Price (USA)"].str.replace("USD ", "").str.replace(",", "").astype(float)

# 轉換 Battery Capacity 為數字
df["Battery Capacity (mAh)"] = df["Battery Capacity"].str.replace("mAh", "").str.replace(",", "").astype(float)

# 定義函式來清理 Screen Size 並提取主要尺寸
def clean_screen_size(size_str):
    if pd.isna(size_str) or size_str == "" or size_str == "-":
        return None  # 避免 NaN 或空值
    
    # 提取第一個數字（主要尺寸）
    match = re.search(r"\d+\.\d+", str(size_str))
    if match:
        return float(match.group())  # 轉換為浮點數
    else:
        return None  # 如果沒有匹配到數字，返回 None

# 轉換 Screen Size 為數字
df["Screen Size (inches)"] = df["Screen Size"].apply(clean_screen_size)

# 轉換年份為數值
df["Launched Year"] = pd.to_numeric(df["Launched Year"], errors="coerce")

# 移除原始貨幣欄位 & 單位欄位
df.drop(columns=["Launched Price (India)", "Launched Price (China)", "Launched Price (Pakistan)", "Launched Price (Dubai)", "Battery Capacity", "Screen Size"], inplace=True)

# 儲存清理後的數據
cleaned_file_path = "C:/Users/chao/Desktop/Data Analysis/Datasets/Mobiles_Cleaned.csv"
df.to_csv(cleaned_file_path, index=False)

print(f"清理後的數據已儲存至: {cleaned_file_path}")