import streamlit as st
from huggingface_hub import InferenceClient

# 1. 網頁標題與外觀設定
st.set_page_config(page_title="古文翻譯系統", page_icon="📜", layout="centered")
st.title("📜 免費版！智能古文翻譯系統")
st.write("在下方輸入文言文，AI 將自動為您翻譯成現代白話文（基於 Hugging Face 免費模型）。")

# 2. 側邊欄：讓使用者輸入 Hugging Face Token
st.sidebar.header("🔑 設定")
hf_token = st.sidebar.text_input("請輸入您的 Hugging Face Token", type="password")
st.sidebar.markdown("[如何取得 Token？](https://huggingface.co/settings/tokens)")

# 3. 主畫面：輸入框與翻譯按鈕
user_input = st.text_area("請輸入文言文：", height=150, placeholder="例如：學而時習之，不亦說乎？")
translate_button = st.button("開始翻譯 ✨", type="primary")

# 4. 翻譯邏輯處理
if translate_button:
    if not hf_token:
        st.error("❌ 請先在左側邊欄輸入您的 Hugging Face Token (hf_...)！")
    elif not user_input.strip():
        st.warning("⚠️ 請輸入需要翻譯的古文。")
    else:
        with st.spinner("⏳ AI 正在挑燈夜讀、推敲字句中..."):
            try:
                # 初始化客戶端
                client = InferenceClient(token=hf_token)
                
                # 在 system prompt 強烈要求必須使用台灣繁體中文
                response = client.chat_completion(
                    model="meta-llama/Meta-Llama-3-8B-Instruct",
                    messages=[
                        {
                            "role": "system", 
                            "content": "你是一位精通文言文與現代漢語轉換的文學專家。請將使用者輸入的文言文，翻譯成流暢、通順且精確的現代繁體中文（台灣白話文）。核心規範：請絕對必須完全使用繁體中文回答，禁止使用英文回覆！請直接輸出翻譯結果，不需要任何額外的解釋或問候語。"
                        },
                        {"role": "user", "content": f"請將這段古文翻譯成繁體中文：\n{user_input}"}
                    ],
                    max_tokens=512,
                    temperature=0.2 # 降低隨機性，讓它更聽話
                )
                
                # 擷取翻譯文本
                result = response.choices[0].message.content
                
                # 顯示翻譯結果
                st.success("🎉 翻譯完成！")
                st.subheader("📝 現代白話文翻譯：")
                st.info(result.strip())
                
            except Exception as e:
                st.error(f"💥 翻譯發生錯誤：{e}\n請檢查您的 Token 是否正確，或稍後再試。")
