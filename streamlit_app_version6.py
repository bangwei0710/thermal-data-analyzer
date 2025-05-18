import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Thermal Log 分析工具", layout="wide")

st.title("📊 Thermal Log 分析工具（Version 6：支援多檔分析）")

uploaded_files = st.file_uploader("請上傳 thermal log 的 CSV 檔（可多選）", type="csv", accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        try:
            filename = uploaded_file.name.lower()

            # 自動判斷 GPUmon 檔案
            if "gpu" in filename:
                df = pd.read_csv(uploaded_file, encoding='cp950', engine='python', skiprows=35, skipfooter=2)
            else:
                df = pd.read_csv(uploaded_file, encoding='cp950', engine='python', skipfooter=2)

            df = df.reset_index(drop=True).iloc[5:]  # 移除前 5 筆異常值
            all_columns = df.columns.tolist()

            st.markdown(f"---\n### 📁 檔案：`{uploaded_file.name}`")
            st.info(f"📈 資料總筆數：{len(df)}")

            # 欄位選擇
            selected_cols = st.multiselect(f"選擇要分析的欄位（{uploaded_file.name}）", all_columns, key=uploaded_file.name)

            # 資料範圍選擇
            total_rows = len(df)
            start_index = st.number_input(f"從第 N 筆開始（{uploaded_file.name}）", min_value=0, max_value=total_rows - 1, value=0, key='start_' + uploaded_file.name)
            end_index = st.number_input(f"到第 M 筆結束（{uploaded_file.name}）", min_value=start_index + 1, max_value=total_rows, value=total_rows, key='end_' + uploaded_file.name)

            # 圖表標題設定
            chart_title = st.text_input(f"圖表標題（{uploaded_file.name}）", value="", key='title_' + uploaded_file.name)

            if selected_cols:
                df_subset = df.iloc[start_index:end_index]
                df_subset = df_subset[selected_cols].dropna()

                if df_subset.shape[0] < 2:
                    st.warning("❗ 資料筆數過少，無法繪圖，請調整範圍或確認欄位內容。")
                else:
                    for col in selected_cols:
                        df_subset[col] = pd.to_numeric(df_subset[col], errors='coerce')

                    st.subheader(f"📈 曲線圖：{uploaded_file.name}")
                    fig, ax1 = plt.subplots(figsize=(12, 5))
                    ax1.plot(df_subset.index, df_subset[selected_cols[0]], color='blue', label=selected_cols[0])
                    ax1.set_ylabel(selected_cols[0], color='blue')
                    ax1.tick_params(axis='y', labelcolor='blue')

                    if len(selected_cols) >= 2:
                        ax2 = ax1.twinx()
                        ax2.plot(df_subset.index, df_subset[selected_cols[1]], color='green', label=selected_cols[1])
                        ax2.set_ylabel(selected_cols[1], color='green')
                        ax2.tick_params(axis='y', labelcolor='green')

                    ax1.set_xlabel("Time")
                    ax1.set_title(chart_title if chart_title else f"{uploaded_file.name} 趨勢比較")
                    ax1.grid(True)
                    st.pyplot(fig)

                    st.subheader(f"📊 統計資訊：{uploaded_file.name}")
                    for col in selected_cols:
                        st.write(f"🔹 **{col}**")
                        st.write(f"- 最大值：{df_subset[col].max():.2f}")
                        st.write(f"- 最小值：{df_subset[col].min():.2f}")
                        st.write(f"- 平均值：{df_subset[col].mean():.2f}")
        except Exception as e:
            st.error(f"❌ 檔案 {uploaded_file.name} 發生錯誤：{e}")
else:
    st.info("請上傳至少一個 CSV 檔案以開始分析。")
