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
                # 使用 Meta 最新的開源大模型 Llama 3 (8B)
                client = InferenceClient(
                    model="meta-llama/Meta-Llama-3-8B-Instruct",
                    token=hf_token
                )
                
                # 設定 Prompt 引導 AI 進行翻譯
                prompt = f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n你是一位精通文言文與現代漢語轉換的文學專家。請將使用者輸入的文言文，翻譯成流暢、通順且精確的現代白話文。請直接輸出翻譯結果，不需要任何額外的解釋或問候語。<|eot_id|><|start_header_id|>user<|end_header_id|>\n{user_input}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n"
                
                response = client.text_generation(
                    prompt,
                    max_new_tokens=512,
                    temperature=0.3
                )
                
                # 顯示翻譯結果
                st.success("🎉 翻譯完成！")
                st.subheader("📝 現代白話文翻譯：")
                st.info(response.strip())
                
            except Exception as e:
                st.error(f"💥 翻譯發生錯誤：{e}\n請檢查您的 Token 是否正確，或稍後再試。")
