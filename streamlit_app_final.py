
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 欄位名稱標準化函式
def normalize(col):
    return col.strip().lower().replace(" ", "").replace(":", "").replace("（", "(").replace("）", ")")

st.set_page_config(page_title="Thermal Log 分析工具", layout="wide")
st.title("Thermal Log 分析工具")
 = st.file_uploader("請上傳 thermal log 的 CSV 檔（可多選）", type="csv", accept_multiple_files=True)

all_dataframes = {}
file_column_selection = {}
file_range_selection = {}
valid_dataframes = []
common_params = [
    'Total System Power [W]',
    'CPU Package Power [W]',
    ' 1:TGP (W)',
    'Charge Rate [W]',
    'IA Cores Power [W]',
    'GT Cores Power [W]',
    ' 1:NVVDD Power (W)',
    ' 1:FBVDD Power (W)',
    'CPU Package [蟒]',
    ' 1:Temperature GPU (C)',
    ' 1:Temperature Memory (C)',
    'SEN1-temp(Degree C)',
    'SEN2-temp(Degree C)',
    'SEN3-temp(Degree C)',
    'SEN4-temp(Degree C)',
    'SEN5-temp(Degree C)',
    'SEN6-temp(Degree C)',
    'SEN7-temp(Degree C)',
    'SEN8-temp(Degree C)',
    'SEN9-temp(Degree C)'
]

if 