import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Thermal Log 分析工具", layout="wide")

st.title("📊 Thermal Log 分析工具（X 軸固定為 Time）")

uploaded_file = st.file_uploader("請上傳 thermal log 的 CSV 檔", type="csv")

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file, encoding='cp950', engine='python', skipfooter=2)
        df = df.iloc[5:].reset_index(drop=True)

        st.success("✅ 檔案讀取成功！")
        all_columns = df.columns.tolist()

        st.info(f"📈 資料總筆數：{len(df)}")

        # 選擇 Y 軸欄位（不設數量限制）
        selected_cols = st.multiselect("📋 選擇要分析的欄位（1 個以上）", all_columns)

        # 自訂範圍選取
        st.subheader("📊 選擇分析資料的範圍")
        total_rows = len(df)
        start_index = st.number_input("從第 N 筆開始", min_value=0, max_value=total_rows - 1, value=0)
        end_index = st.number_input("到第 M 筆結束", min_value=start_index + 1, max_value=total_rows, value=total_rows)

        # 自訂圖表標題
        st.subheader("🖋️ 圖表標題設定")
        chart_title = st.text_input("請輸入圖表標題（可選）", value="")

        if selected_cols:
            df_subset = df.iloc[start_index:end_index]
            df_subset = df_subset[selected_cols].dropna()

            if df_subset.shape[0] < 2:
                st.warning("❗ 資料筆數過少，無法繪圖，請調整範圍或確認欄位內容。")
            else:
                for col in selected_cols:
                    df_subset[col] = pd.to_numeric(df_subset[col], errors='coerce')

                st.subheader("📈 曲線圖")
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
