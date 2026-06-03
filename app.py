import streamlit as st
from huggingface_hub import InferenceClient

# 1. 網頁標題與外觀設定
st.set_page_config(page_title="唐詩與古文全方位賞析系統", page_icon="📜", layout="centered")
st.title("📜 唐詩與古文全方位精修系統")
st.write("輸入任何唐詩或文言文，AI 將依序為您進行作者介紹、繁體中文翻譯與深度賞析。")

# 2. 側邊欄：讓使用者輸入 Hugging Face Token
st.sidebar.header("🔑 系統設定")
hf_token = st.sidebar.text_input("請輸入您的 Hugging Face Token", type="password")
st.sidebar.markdown("[如何取得 Token？](https://huggingface.co/settings/tokens)")

# 3. 主畫面：輸入框與分析按鈕
user_input = st.text_area("請輸入唐詩（如靜夜思、琵琶行等）或文言文：", height=150, placeholder="例如：床前明月光，疑是地上霜。")
analyze_button = st.button("全方位解析 ✨", type="primary")

# 4. 解析邏輯處理
if analyze_button:
    if not hf_token:
        st.error("❌ 請先在左側邊欄輸入您的 Hugging Face Token (hf_...)！")
    elif not user_input.strip():
        st.warning("⚠️ 請輸入需要解析的詩詞或古文。")
    else:
        with st.spinner("⏳ AI 正在查閱詩集、推敲文意中..."):
            try:
                # 初始化客戶端
                client = InferenceClient(token=hf_token)
                
                # 在 Prompt 中嚴格規定輸出的順序：作者 -> 翻譯 -> 賞析
                system_prompt = """你是一位精通中國古典文學、唐詩三百首與歷史背景的權威教授。
請針對使用者輸入的詩詞或文言文，進行全方位的解析。

【核心強制規範】
- 你只能、也必須完全使用「繁體中文（台灣白話文）」進行回答！
- 絕對禁止使用英文回答任何一個字！
- 內文請直接輸出以下三個標題與內容，不需要任何額外的開場白或問候語。

回覆結構規範（請嚴格遵循以下順序輸出標題）：
### 👤 作者背景介紹
[請先用繁體中文介紹這位詩人或作者，包含其生平地位、作詩風格與對後世的影響。若無明確作者則介紹作品出處與編纂背景]

### 📝 現代白話翻譯
[接著，將輸入的詩句或文言文，逐字逐句翻譯成流暢、通順且優美的台灣現代白話文]

### 🔍 深度文學賞析
[最後，用繁體中文分析這首詩或文章的核心意境、文學技巧、寫作背景，以及作者想傳達的深層情感]"""

                response = client.chat_completion(
                    model="meta-llama/Meta-Llama-3-8B-Instruct",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"請完全使用繁體中文，依序進行作者介紹、翻譯與賞析：\n{user_input}"}
                    ],
                    max_tokens=1200,
                    temperature=0.1 # 保持最低隨機性，讓它乖乖聽從順序與語言限制
                )
                
                # 擷取回覆
                result = response.choices[0].message.content
                
                # 顯示結果
                st.success("🎉 解析完成！")
                st.markdown(result.strip())
                
            except Exception as e:
                st.error(f"💥 解析發生錯誤：{e}\n請檢查您的 Token 是否正確，或稍後再試。")
