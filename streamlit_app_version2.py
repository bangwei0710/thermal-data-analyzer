import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Thermal Log 分析工具", layout="wide")

st.title("📊 Thermal Log 分析工具（進階版）")

uploaded_file = st.file_uploader("請上傳 thermal log 的 CSV 檔", type="csv")

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file, encoding='cp950', engine='python', skipfooter=2)
        df = df.iloc[5:].reset_index(drop=True)

        st.success("✅ 檔案讀取成功！")
        all_columns = df.columns.tolist()

        st.subheader("🧭 X 軸欄位設定")
        x_column = st.selectbox("請選擇作為 X 軸的欄位", all_columns, index=0)

        st.subheader("📋 選擇要分析的欄位（最多兩個）")
        selected_cols = st.multiselect("選擇 1~2 個欄位進行比較", all_columns, max_selections=2)

        st.subheader("🪜 選擇分析資料範圍")
        max_rows = len(df)
        row_limit = st.number_input("只取最後 N 筆資料（預設為全部）", min_value=1, max_value=max_rows, value=max_rows, step=100)

        st.subheader("🖋️ 圖表標題設定")
        chart_title = st.text_input("請輸入圖表標題（可選）", value="")

        if selected_cols:
            df_subset = df.tail(row_limit)
            for col in selected_cols + [x_column]:
                df_subset[col] = pd.to_numeric(df_subset[col], errors='coerce')

            st.subheader("📈 曲線圖")
            fig, ax1 = plt.subplots(figsize=(12, 5))

            ax1.plot(df_subset[x_column], df_subset[selected_cols[0]], color='blue', label=selected_cols[0])
            ax1.set_ylabel(selected_cols[0], color='blue')
            ax1.tick_params(axis='y', labelcolor='blue')

            if len(selected_cols) == 2:
                ax2 = ax1.twinx()
                ax2.plot(df_subset[x_column], df_subset[selected_cols[1]], color='green', label=selected_cols[1])
                ax2.set_ylabel(selected_cols[1], color='green')
                ax2.tick_params(axis='y', labelcolor='green')

            ax1.set_xlabel(x_column)
            ax1.set_title(chart_title if chart_title else "欄位趨勢比較")
            ax1.grid(True)
            st.pyplot(fig)

            st.subheader("📊 統計資訊")
            for col in selected_cols:
                st.write(f"🔹 **{col}**")
                st.write(f"- 最大值：{df_subset[col].max():.2f}")
                st.write(f"- 最小值：{df_subset[col].min():.2f}")
                st.write(f"- 平均值：{df_subset[col].mean():.2f}")
    except Exception as e:
        st.error(f"❌ 錯誤：{e}")
else:
    st.info("請先上傳 CSV 檔案以進行分析。")
