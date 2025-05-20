
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 欄位名稱標準化函式（去除空格、冒號、小寫統一）
def normalize(col):
    return col.strip().lower().replace(" ", "").replace(":", "").replace("（", "(").replace("）", ")")

st.set_page_config(page_title="Thermal Log 分析工具", layout="wide")
st.title("📊 Thermal Log 分析工具（Version 29a：移除常用參數彙總區塊）")

uploaded_files = st.file_uploader("請上傳 thermal log 的 CSV 檔（可多選）", type="csv", accept_multiple_files=True)

all_dataframes = {}
file_column_selection = {}
file_range_selection = {}
valid_dataframes = []

if uploaded_files:
    st.info("📌 每個檔案可選擇多個欄位與資料範圍，圖表支援高解析度（DPI 200）")

    for uploaded_file in uploaded_files:
        try:
            filename = uploaded_file.name
            shortname = filename.split('/')[-1]

            if "gpu" in filename.lower():
                df = pd.read_csv(uploaded_file, encoding='cp950', engine='python', skiprows=35, skipfooter=2, on_bad_lines='skip')
            else:
                df = pd.read_csv(uploaded_file, encoding='cp950', engine='python', skipfooter=2, on_bad_lines='skip')

            df.columns = df.columns.str.strip()
            df = df.reset_index(drop=True).iloc[5:]
            all_dataframes[shortname] = df
            valid_dataframes.append(df)

            st.markdown(f"---\n### 📁 檔案：`{shortname}`")

            selected_cols = st.multiselect(f"選擇要分析的欄位（{shortname}）", df.columns.tolist(), key='col_' + shortname)
            file_column_selection[shortname] = selected_cols

            total_rows = len(df)
            start_index = st.number_input(f"從第 N 筆開始（{shortname}）", min_value=0, max_value=total_rows - 1, value=0, key='start_' + shortname)
            end_index = st.number_input(f"到第 M 筆結束（{shortname}）", min_value=start_index + 1, max_value=total_rows, value=total_rows, key='end_' + shortname)
            file_range_selection[shortname] = (start_index, end_index)

            if selected_cols:
                df_subset = df.iloc[start_index:end_index]
                st.write("📊 統計資訊：")
                for col in selected_cols:
                    series = pd.to_numeric(df_subset[col], errors='coerce').dropna()
                    st.write(f"🔹 **{col}**")
                    st.write(f"- 最大值：{series.max():.2f}")
                    st.write(f"- 最小值：{series.min():.2f}")
                    st.write(f"- 平均值：{series.mean():.2f}")

        except Exception as e:
            st.error(f"❌ 檔案 {filename} 發生錯誤：{e}")

    chart_title = st.text_input("🖋️ 圖表標題", value="跨檔案多欄位比較圖")

    st.subheader("📈 同圖比較曲線圖")
    fig, ax = plt.subplots(figsize=(12, 5), dpi=200)

    for shortname, df in all_dataframes.items():
        selected_cols = file_column_selection.get(shortname, [])
        start_index, end_index = file_range_selection.get(shortname, (0, len(df)))
        df_subset = df.iloc[start_index:end_index]

        for col in selected_cols:
            if col in df_subset.columns:
                series = pd.to_numeric(df_subset[col], errors='coerce').dropna()
                ax.plot(series.reset_index(drop=True), label=f"{shortname} - {col}")

    ax.set_title(chart_title)
    ax.set_xlabel("Index")
    ax.set_ylabel("Value")
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)
else:
    st.info("請上傳至少一個檔案以開始。")
