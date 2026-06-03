import streamlit as st
from openai import OpenAI

# 1. 網頁標題與外觀設定
st.set_page_config(page_title="古文翻譯系統", page_icon="📜", layout="centered")
st.title("📜 智能古文翻譯系統")
st.write("在下方輸入文言文，AI 將自動為您翻譯成現代白話文。")

# 2. 側邊欄：讓使用者輸入 API Key
st.sidebar.header("🔑 設定")
api_key = st.sidebar.text_input("請輸入您的 OpenAI API Key", type="password")
st.sidebar.markdown("[如何取得 API Key？](https://platform.openai.com/api-keys)")

# 3. 主畫面：輸入框與翻譯按鈕
user_input = st.text_area("請輸入文言文：", height=150, placeholder="例如：學而時習之，不亦說乎？")
translate_button = st.button("開始翻譯 ✨", type="primary")

# 4. 翻譯邏輯處理
if translate_button:
    if not api_key:
        st.error("❌ 請先在左側邊欄輸入您的 OpenAI API Key！")
    elif not user_input.strip():
        st.warning("⚠️ 請輸入需要翻譯的古文。")
    else:
        with st.spinner("⏳ AI 正在挑燈夜讀、推敲字句中..."):
            try:
                # 呼叫 OpenAI API
                client = OpenAI(api_key=api_key)
                response = client.chat.completions.create(
                    model="gpt-4o-mini", # 速度快且便宜的模型
                    messages=[
                        {
                            "role": "system", 
                            "content": "你是一位精通文言文與現代漢語轉換的文學專家。請將使用者輸入的文言文，翻譯成流暢、通順且精確的現代白話文。請直接輸出翻譯結果，不需要任何額外的解釋或問候語。"
                        },
                        {"role": "user", "content": user_input}
                    ]
                )
                
                # 顯示翻譯結果
                result = response.choices[0].message.content
                st.success("🎉 翻譯完成！")
                st.subheader("📝 現代白話文翻譯：")
                st.info(result)
                
            except Exception as e:
                st.error(f"💥 翻譯發生錯誤：{e}\n請檢查您的 API Key 是否正確或是否有餘額。")
