
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 欄位名稱標準化函式
def normalize(col):
    return col.strip().lower().replace(" ", "").replace(":", "").replace("（", "(").replace("）", ")")

st.set_page_config(page_title="Thermal Log 分析工具", layout="wide")
st.title("📊 Thermal Log 分析工具（Version 30：常用參數整合區塊）")

uploaded_files = st.file_uploader("請上傳 thermal log 的 CSV 檔（可多選）", type="csv", accept_multiple_files=True)

all_dataframes = {}
file_column_selection = {}
file_range_selection = {}
valid_dataframes = []
common_params = ['Total System Power [W]', 'CPU Package Power [W]', ' 1:TGP (W)', 'Charge Rate [W]', 'IA Cores Power [W]', 'GT Cores Power [W]', ' 1:NVVDD Power (W)', ' 1:FBVDD Power (W)', 'CPU Package [蚓]', ' 1:Temperature GPU (C)', ' 1:Temperature Memory (C)', 'Temp0 [蚓]', 'SEN1-temp(Degree C)', 'SEN2-temp(Degree C)', 'SEN3-temp(Degree C)', 'SEN4-temp(Degree C)', 'SEN5-temp(Degree C)', 'SEN6-temp(Degree C)', 'SEN7-temp(Degree C)', 'SEN8-temp(Degree C)', 'SEN9-temp(Degree C)']

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
            valid_dataframes.append((shortname, df))

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

    # 整合所有檔案在同一個區塊顯示常用參數平均值
    st.markdown("---")
    
    # 整合所有檔案在同一個區塊顯示常用參數平均值
    st.markdown("---")
    st.subheader("📌 常用參數快速分析（直式顯示）")

    results = []

    for shortname, df in valid_dataframes:
        df_tail = df.tail(600)
        row = {"檔名": shortname}
        for col in common_params:
            match = [c for c in df_tail.columns if normalize(c) == normalize(col)]
            if match:
                values = pd.to_numeric(df_tail[match[0]], errors='coerce').dropna()
                row[col] = f"{values.mean():.2f}" if not values.empty else "-"
            else:
                row[col] = "-"
        results.append(row)

    summary_df = pd.DataFrame(results)
    summary_df = summary_df[["檔名"] + common_params]

    for idx, row in summary_df.iterrows():
        st.markdown(f"**📁 檔案：{row['檔名']}**")
        transposed_df = pd.DataFrame({
            "參數名稱": common_params,
            "數值": [row[col] for col in common_params]
        })
        st.dataframe(transposed_df, use_container_width=True)


    results = []

    for shortname, df in valid_dataframes:
        df_tail = df.tail(600)
        row = {"檔名": shortname}
        for col in common_params:
            match = [c for c in df_tail.columns if normalize(c) == normalize(col)]
            if match:
                values = pd.to_numeric(df_tail[match[0]], errors='coerce').dropna()
                row[col] = f"{values.mean():.2f}" if not values.empty else "-"
            else:
                row[col] = "-"
        results.append(row)

    
summary_df = pd.DataFrame(results)
summary_df = summary_df[["檔名"] + common_params]

st.markdown("### 📌 常用參數快速分析（直式顯示）")

for idx, row in summary_df.iterrows():
    st.markdown(f"**📁 檔案：{row['檔名']}**")
    transposed_df = pd.DataFrame({
        "參數名稱": common_params,
        "數值": [row[col] for col in common_params]
    })
    st.dataframe(transposed_df, use_container_width=True)


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
