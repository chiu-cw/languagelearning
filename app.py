import streamlit as st
from huggingface_hub import InferenceClient

# 1. 網頁標題與外觀設定
st.set_page_config(page_title="論語 AI 陪讀書院", page_icon="👨‍🏫", layout="centered")
st.title("👨‍🏫 論語 AI 智慧陪讀書院")
st.write("歡迎來到論語共學空間！無論是想翻譯章句、理解背後故事，還是探討現代生活應用，AI 導師都會為您解惑。")

# 2. 側邊欄：讓使用者輸入 Hugging Face Token
st.sidebar.header("🔑 系統設定")
hf_token = st.sidebar.text_input("請輸入您的 Hugging Face Token", type="password")
st.sidebar.markdown("[如何取得 Token？](https://huggingface.co/settings/tokens)")

# 3. 貼心的引導字句（讓使用者知道怎麼提問）
st.markdown("""
### 💡 您可以這樣詢問 AI 導師：
* *「我想了解『學而時習之』這整段是什麼意思？」*
* *「孔子說的『三十而立』，在我們現代三十歲時該怎麼實踐？」*
* *「子貢是一個怎麼樣的人？孔子為什麼常常跟他對話？」*
""")

# 4. 主畫面：輸入框與請教按鈕
user_input = st.text_area("請輸入您想請教的論語章句或問題：", height=120, placeholder="例如：吾日三省吾身是什麼意思？")
ask_button = st.button("向導師請教 🖋️", type="primary")

# 5. 導師回覆邏輯
if ask_button:
    if not hf_token:
        st.error("❌ 請先在左側邊欄輸入您的 Hugging Face Token (hf_...)！")
    elif not user_input.strip():
        st.warning("⚠️ 請輸入您想探討的內容。")
    else:
        with st.spinner("⏳ 導師正在撫鬚思索、準備教材中..."):
            try:
                # 初始化客戶端
                client = InferenceClient(token=hf_token)
                
                # 重新打造 Prompt：賦予 AI 儒學導師的靈魂與繁體中文規範
                system_prompt = """你是一位慈祥、博學多聞的儒學大師，專門帶領現代人學習《論語》。
你的任務是針對使用者提出的《論語》章句或相關問題，提供深入淺出、溫暖且富有智慧的解答。

回覆結構規範：
1. 【章句釋義】：用流暢優美的台灣繁體中文（白話文）解釋這句話的意思。
2. 【歷史背景或小故事】：（選填）如果該章句涉及特定弟子（如子路、顏回）或歷史背景，請簡述其故事，讓學習更有趣。
3. 【現代生活應用】：告訴使用者，這句兩千年前的智慧，可以如何應用在現代人的生活、工作或人際關係中。

核心要求：
- 請絕對必須完全使用台灣繁體中文回答，禁止使用英文回覆！
- 語氣要像一位良師益友，多用「我們」、「您」，避免死板的教科書語氣。"""

                response = client.chat_completion(
                    model="meta-llama/Meta-Llama-3-8B-Instruct",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_input}
                    ],
                    max_tokens=800, # 稍微拉長，讓老師可以解釋得更詳細
                    temperature=0.4
                )
                
                # 擷取導師回覆
                result = response.choices[0].message.content
                
                # 顯示結果
                st.success("🎉 導師開講：")
                st.markdown(result.strip())
                
            except Exception as e:
                st.error(f"💥 書院連線發生錯誤：{e}\n請檢查 Token 是否正確，或稍後再試。")
