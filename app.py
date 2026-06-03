import streamlit as st
from huggingface_hub import InferenceClient

# 1. 網頁標題與外觀設定
st.set_page_config(page_title="唐詩與古文全方位賞析系統", page_icon="📜", layout="centered")
st.title("📜 唐詩與古文全方位精修系統")
st.write("輸入任何唐詩或文言文，AI 將依序為您進行精確的作者介紹、繁體中文翻譯與深度賞析。")

# 2. 側邊欄：讓使用者輸入 Hugging Face Token
st.sidebar.header("🔑 系統設定")
hf_token = st.sidebar.text_input("請輸入您的 Hugging Face Token", type="password")
st.sidebar.markdown("[如何取得 Token？](https://huggingface.co/settings/tokens)")

# 3. 主畫面：輸入框與分析按鈕
user_input = st.text_area("請輸入唐詩（如問劉十九、送友人）或文言文：", height=150, placeholder="例如：綠蟻新醅酒，紅泥小火爐。")
analyze_button = st.button("全方位解析 ✨", type="primary")

# 4. 解析邏輯處理
if analyze_button:
    if not hf_token:
        st.error("❌ 請先在左側邊欄輸入您的 Hugging Face Token (hf_...)！")
    elif not user_input.strip():
        st.warning("⚠️ 請輸入需要解析的詩詞或古文。")
    else:
        with st.spinner("⏳ 新大腦正在精密考證古籍中..."):
            try:
                # 初始化客戶端
                client = InferenceClient(token=hf_token)
                
                # 重新打造 Prompt，特別強調不要把白居易認成辛棄疾
                system_prompt = """你是一位精通中國古典文學、唐詩三百首與宋詞考證的泰斗級教授。
請針對使用者輸入的詩詞或文言文，進行絕對精確、毫無破綻的全方位解析。

【核心歷史考證規範】
1. 必須嚴格核對作者身份，絕對不能張冠李戴！例如：「綠蟻新醅酒，紅泥小火爐。晚來天欲雪，能飲一杯無？」的作者是唐代大詩人【白居易】，絕對不是辛棄疾！請拿出你最高的文學專業，嚴禁瞎編！
2. 你只能、也必須完全使用「繁體中文（台灣白話文）」進行回答！絕對禁止使用英文或簡體字。
3. 內文請直接輸出以下三個標題與內容，不需要任何額外的開場白或問候語。

回覆結構規範（請嚴格遵循以下順序輸出標題）：
### 👤 作者背景介紹
[請精確指出這首詩或文章的正確作者與篇名，並用繁體中文介紹這位作者，包含其生平地位、作詩風格與對後世的影響。]

### 📝 現代白話翻譯
[將輸入的詩句或文言文，逐字逐句翻譯成流暢、通順且優美的台灣現代白話文。]

### 🔍 深度文學賞析
[用繁體中文分析這首詩或文章的核心意境、文學技巧、寫作背景，以及作者想傳達的深層情感。]"""

                # 關鍵改動：將模型換成對亞洲詩詞更敏感的 mistralai/Mistral-Nemo-Instruct-2407
                response = client.chat_completion(
                    model="mistralai/Mistral-Nemo-Instruct-2407",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"請嚴謹考證並完全使用繁體中文，依序進行作者介紹、翻譯與賞析：\n{user_input}"}
                    ],
                    max_tokens=1200,
                    temperature=0.01
                )
                
                # 擷取回覆
                result = response.choices[0].message.content
                
                # 顯示結果
                st.success("🎉 全新大腦解析完成！")
                st.markdown(result.strip())
                
            except Exception as e:
                st.error(f"💥 解析發生錯誤：{e}\n請檢查您的 Token 是否正確，或稍後再試。")
