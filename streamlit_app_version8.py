import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Thermal Log 分析工具", layout="wide")
st.title("📊 Thermal Log 分析工具（Version 8：跨檔不同欄位同圖比較）")

uploaded_files = st.file_uploader("請上傳 thermal log 的 CSV 檔（可多選）", type="csv", accept_multiple_files=True)

all_dataframes = {}
file_column_selection = {}

if uploaded_files:
    st.info("📌 每個檔案可選擇不同欄位進行比較，最終畫在同一張圖上。")

    for uploaded_file in uploaded_files:
        try:
            filename = uploaded_file.name
            shortname = filename.split('/')[-1]

            if "gpu" in filename.lower():
                df = pd.read_csv(uploaded_file, encoding='cp950', engine='python', skiprows=35, skipfooter=2)
            else:
                df = pd.read_csv(uploaded_file, encoding='cp950', engine='python', skipfooter=2)

            df = df.reset_index(drop=True).iloc[5:]
            all_dataframes[shortname] = df

            st.markdown(f"---\n### 📁 檔案：`{shortname}`")
            selected_col = st.selectbox(f"請選擇此檔要繪圖的欄位", df.columns.tolist(), key=shortname)
            file_column_selection[shortname] = selected_col
        except Exception as e:
            st.error(f"❌ 檔案 {uploaded_file.name} 發生錯誤：{e}")

    # 圖表標題設定
    chart_title = st.text_input("🖋️ 圖表標題", value="跨檔案比較圖")

    st.subheader("📈 同圖比較曲線圖")
    fig, ax = plt.subplots(figsize=(12, 5))

    for shortname, df in all_dataframes.items():
        col = file_column_selection[shortname]
        if col in df.columns:
            series = pd.to_numeric(df[col], errors='coerce').dropna()
            ax.plot(series.reset_index(drop=True), label=f"{shortname} - {col}")

    ax.set_title(chart_title)
    ax.set_xlabel("Index")
    ax.set_ylabel("Value")
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)
else:
    st.info("請上傳至少一個檔案以開始。")
