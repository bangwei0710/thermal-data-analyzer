import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Thermal Log 分析工具", layout="wide")

st.title("📊 Thermal Log 分析工具（Version 7：多檔同欄位疊圖）")

uploaded_files = st.file_uploader("請上傳 thermal log 的 CSV 檔（可多選）", type="csv", accept_multiple_files=True)

all_dataframes = {}
all_columns_sets = []

if uploaded_files:
    for uploaded_file in uploaded_files:
        try:
            filename = uploaded_file.name.lower()
            if "gpu" in filename:
                df = pd.read_csv(uploaded_file, encoding='cp950', engine='python', skiprows=35, skipfooter=2)
            else:
                df = pd.read_csv(uploaded_file, encoding='cp950', engine='python', skipfooter=2)

            df = df.reset_index(drop=True).iloc[5:]
            all_dataframes[uploaded_file.name] = df
            all_columns_sets.append(set(df.columns.tolist()))

            st.markdown(f"---\n### 📁 檔案：`{uploaded_file.name}`")
            st.info(f"📈 資料總筆數：{len(df)}")

            selected_cols = st.multiselect(f"選擇要分析的欄位（{uploaded_file.name}）", df.columns.tolist(), key=uploaded_file.name)

            total_rows = len(df)
            start_index = st.number_input(f"從第 N 筆開始（{uploaded_file.name}）", min_value=0, max_value=total_rows - 1, value=0, key='start_' + uploaded_file.name)
            end_index = st.number_input(f"到第 M 筆結束（{uploaded_file.name}）", min_value=start_index + 1, max_value=total_rows, value=total_rows, key='end_' + uploaded_file.name)

            chart_title = st.text_input(f"圖表標題（{uploaded_file.name}）", value="", key='title_' + uploaded_file.name)

            if selected_cols:
                df_subset = df.iloc[start_index:end_index]
                df_subset = df_subset[selected_cols].dropna()

                if df_subset.shape[0] < 2:
                    st.warning("❗ 資料筆數過少，無法繪圖。")
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

    # === 新增：同欄位疊圖比較 ===
    st.markdown("---")
    st.subheader("📌 同欄位跨檔案疊圖比較")

    # 找出交集欄位
    common_columns = set.intersection(*all_columns_sets) if all_columns_sets else []
    compare_column = st.selectbox("選擇要比較的欄位（所有檔案都必須包含）", sorted(common_columns))

    if compare_column:
        fig, ax = plt.subplots(figsize=(12, 5))
        for filename, df in all_dataframes.items():
            if compare_column in df.columns:
                y = pd.to_numeric(df[compare_column], errors='coerce').dropna()
                ax.plot(y.reset_index(drop=True), label=filename)
        ax.set_title(f"{compare_column} - 多檔案疊圖")
        ax.set_xlabel("Index")
        ax.set_ylabel(compare_column)
        ax.grid(True)
        ax.legend()
        st.pyplot(fig)
else:
    st.info("請上傳至少一個 CSV 檔案以開始分析。")
