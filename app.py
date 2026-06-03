import streamlit as st
from huggingface_hub import InferenceClient

# 1. 網頁標題與外觀設定
st.set_page_config(page_title="文言文全方位賞析系統", page_icon="📜", layout="centered")
st.title("📜 文言文全方位精修與賞析系統")
st.write("輸入任何文言文章句，AI 將為您精確翻譯、深度賞析並介紹作者背景。")

# 2. 側邊欄：讓使用者輸入 Hugging Face Token
st.sidebar.header("🔑 系統設定")
hf_token = st.sidebar.text_input("請輸入您的 Hugging Face Token", type="password")
st.sidebar.markdown("[如何取得 Token？](https://huggingface.co/settings/tokens)")

# 3. 主畫面：輸入框與分析按鈕
user_input = st.text_area("請輸入文言文（如論語、古文觀止等章句）：", height=150, placeholder="例如：學而時習之，不亦說乎？")
analyze_button = st.button("全方位解析 ✨", type="primary")

# 4. 解析邏輯處理
if analyze_button:
    if not hf_token:
        st.error("❌ 請先在左側邊欄輸入您的 Hugging Face Token (hf_...)！")
    elif not user_input.strip():
        st.warning("⚠️ 請輸入需要解析的古文。")
    else:
        with st.spinner("⏳ AI 正在查閱典籍、推敲文意中..."):
            try:
                # 初始化客戶端
                client = InferenceClient(token=hf_token)
                
                # 重新打造 Prompt，嚴格規範輸出格式
                system_prompt = """你是一位精通中國古典文學與歷史背景的權威教授。
請針對使用者輸入的文言文，進行全方位的解析。

回覆結構規範（請嚴格遵循以下標題輸出）：
### 📝 現代白話翻譯
[請將輸入的文言文，翻譯成流暢、通順且精確的台灣現代白話文]

### 🔍 深度文學賞析
[請分析這段話的核心思想、文學技巧、寫作背景，以及它想傳達的哲理或深層涵義]

### 👤 作者背景介紹
[請介紹這段話的作者（若無明確作者則介紹作品出處，如《論語》則介紹孔子及編纂背景），包含其生平地位與對後世的影響]

核心要求：
1. 請絕對必須完全使用台灣繁體中文回答，禁止使用英文或簡體字回覆！
2. 內文請直接輸出上述三個標題與內容，不需要任何額外的開場白或問候語。"""

                response = client.chat_completion(
                    model="meta-llama/Meta-Llama-3-8B-Instruct",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"請解析以下這段古文：\n{user_input}"}
                    ],
                    max_tokens=1000,
                    temperature=0.3
                )
                
                # 擷取回覆
                result = response.choices[0].message.content
                
                # 顯示結果
                st.success("🎉 解析完成！")
                st.markdown(result.strip())
                
            except Exception as e:
                st.error(f"💥 解析發生錯誤：{e}\n請檢查您的 Token 是否正確，或稍後再試。")
