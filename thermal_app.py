import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Thermal Log 分析工具", layout="wide")

st.title("📊 Thermal Log 分析工具")
st.markdown("""
這是一個線上工具，可上傳熱測試記錄檔（CSV），並快速查看各參數的最大/最小/平均值與趨勢圖。
""")

uploaded_file = st.file_uploader("請上傳 thermal log 的 CSV 檔", type="csv")

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file, encoding='cp950', engine='python', skipfooter=2)
        df = df.iloc[5:].reset_index(drop=True)

        st.success("✅ 檔案讀取成功！")
        st.subheader("📋 可選欄位")
        columns = df.columns.tolist()
        selected_cols = st.multiselect("請選擇要分析的欄位", columns)

        if selected_cols:
            st.subheader("📈 曲線圖")
            fig, ax = plt.subplots(figsize=(12, 5))
            for col in selected_cols:
                df[col] = pd.to_numeric(df[col], errors='coerce')
                ax.plot(df[col].values, label=col)
            ax.set_title("欄位曲線比較")
            ax.set_xlabel("Index")
            ax.set_ylabel("數值")
            ax.grid(True)
            ax.legend()
            st.pyplot(fig)

            st.subheader("📊 統計資訊")
            for col in selected_cols:
                st.write(f"🔹 **{col}**")
                st.write(f"- 最大值：{df[col].max():.2f}")
                st.write(f"- 最小值：{df[col].min():.2f}")
                st.write(f"- 平均值：{df[col].mean():.2f}")
    except Exception as e:
        st.error(f"❌ 錯誤：{e}")
else:
    st.info("請先上傳 CSV 檔案以進行分析。")
