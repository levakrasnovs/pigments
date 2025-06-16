import random
import pandas as pd
import os
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False

st.set_page_config(page_title='База пигментов', layout="wide")

df = pd.read_csv('pigments.csv')
compound_names = df['Name'].unique().tolist()

st.markdown(f"""
# База пигментов
""")

tabs = st.tabs(["Explore", "Band Gap"])

with tabs[0]:

    selected = st.selectbox(label='Выберите пигмент', options=compound_names, index=None, placeholder='STUDIO bordeaux')

    if selected:

        search_df = df[(df['Name'] == selected)]
        search_df.reset_index(drop=True, inplace=True)
        class_ = search_df['Класс соединения'].iloc[0]
        csd = search_df['CSD ID'].iloc[0]
        kremer = search_df['Кремер ID'].iloc[0]
        color = search_df['Код цвета'].iloc[0]
        color_compound = search_df['Красящее вещество'].iloc[0]
        admixture = search_df['Добавки/примеси'].iloc[0]

        if ';' not in color:
            fig, ax = plt.subplots(figsize=(1, 1), dpi=300)
            ax.set_facecolor(color)
            ax.set_xticks([])
            ax.set_yticks([])
            st.pyplot(fig, use_container_width=False)

        col1result, col2result = st.columns([1, 1])
        col1result.markdown(f'**Код цвета:** {color}')
        if not pd.isna(csd):
            csd = str(int(csd))
            col1result.markdown(f'CSD link: https://www.ccdc.cam.ac.uk/structures/Search?Ccdcid={csd}&DatabaseToSearch=CSD')
        if kremer is not None:
            col2result.markdown(f'**Кремер ID:** {kremer}')
        col2result.markdown(f'**Класс соединения:** {class_}')
        col1result.markdown(f'**Красящее вещество:** {color_compound}')
        if admixture is not None:
            col2result.markdown(f'**Добавки/примеси:** {admixture}')

        if f'{selected}.png' in os.listdir('РФА/'):
            col1result.markdown(f'### РФА')
            col1result.image(f'РФА/{selected}.png')
        if f'{selected}.png' in os.listdir('ИК/'):
            col2result.markdown(f'### ИК')
            col2result.image(f'ИК/{selected}.png')
        if f'{selected}.jpg' in os.listdir('Раман/'):
            col1result.markdown(f'### Раман')
            col1result.image(f'Раман/{selected}.jpg')
        if f'{selected}.jpg' in os.listdir('РЭМ/'):
            col2result.markdown(f'### РЭМ')
            col2result.image(f'РЭМ/{selected}.jpg')

            # col2result.markdown(f'CAS link: **https://commonchemistry.cas.org/detail?cas_rn={cas}**')
with tabs[1]:
    st.title("Upload CSV-файл")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file is not None:
        df_band_gap = pd.read_csv(uploaded_file)
        st.write(df_band_gap)