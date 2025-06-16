import random
import pandas as pd
import os
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px

if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False

st.set_page_config(page_title='База пигментов', layout="wide")

# Функция пересчета длины волны в энергию
def wavelength_to_eV(wavelength_nm):
    return 1239.84193 / wavelength_nm

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
    st.title("Upload CSV file")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file is not None:
        df_band_gap = pd.read_csv(uploaded_file)
        st.write(df_band_gap)
        df_band_gap = df_band_gap.iloc[:, :-1]
        df_cleaned = df_band_gap.iloc[1:].reset_index(drop=True)

        columns_renamed = {
            col: f'Wavelength_{col}' if 'Unnamed' not in col else f'%R_{df_cleaned.columns[i-1]}'
            for i, col in enumerate(df_cleaned.columns)
        }

        df_cleaned = df_cleaned.rename(columns=columns_renamed)
        # Преобразование всех значений в числовой формат
        for col in df_cleaned.columns:
            df_cleaned[col] = pd.to_numeric(df_cleaned[col], errors='coerce')

        # Извлечение имен красителей
        dye_names = [col.replace('%R_', '') for col in df_cleaned.columns if col.startswith('%R_')]
        df_long = pd.DataFrame()

        for dye in dye_names:
            R_d = df_cleaned[f"%R_{dye}"] / 100
            F_R_d = ((1 - R_d) ** 2) / (2 * R_d)
            Energy = wavelength_to_eV(df_cleaned[f"Wavelength_{dye}"])
            temp = pd.DataFrame({
                "Energy": Energy,
                "F(R)": F_R_d,
                "Dye": dye
            })
            df_long = pd.concat([df_long, temp], ignore_index=True)

        # Построение графика
        fig = px.line(
            df_long,
            x="Energy",
            y="F(R)",
            color="Dye",
            title="Kubelka-Munk F(R) vs Energy (Plotly Express)"
        )
        fig.update_layout(xaxis=dict(range=[0, 3]))

        st.plotly_chart(fig)
