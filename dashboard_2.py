# Kita akan mulai dengan mengimpor beberapa library penting yang akan kita gunakan
from turtle import width
import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt


# Membangun aplikasi dashboard
st.title("Covid-19 Dashboard For Indonesia")
st.write("It shows ***Coronavirus Cases*** in Indonesia")
image = Image.open("Corona.jpeg")
st.image(image, width=500)
st.markdown("The dashboard will visualize the Covid-19 Situation in Indonesia")
st.markdown("Coronavirus disease (COVID-19) is an infectious disease caused by a newly discovered coronavirus. Most people infected with the COVID-19 virus will experience mild to moderate respiratory illness and recover without requiring special treatment.")
st.markdown('<style>body{background-color: lightblue}</style>', unsafe_allow_html=True)

# Import Dataset
@st.cache
def load_data():
    df = pd.read_csv("state_wise.csv")
    return df

df = load_data()

visualization = st.sidebar.selectbox('Select a Chart type',('Bar Chart', 'Pie Chart', 'Line Chart'))
state_select = st.sidebar.selectbox('Select a state', df['Location'].unique())
selected_state = df[df['Location'] == state_select]
st.title('Location level analysis')

def get_total_dataframe(df):
    total_dataframe = pd.DataFrame({
        'Status':['Total Cases', 'Total Recovered', 'Total Deaths', 'Total Active Cases'],
        'Number of cases': (df.iloc[0]['Total Cases'],
                            df.iloc[0]['Total Recovered'],
                            df.iloc[0]['Total Deaths'],
                            df.iloc[0]['Total Active Cases'])
    })
    return total_dataframe

state_total = get_total_dataframe(selected_state)
if visualization == 'Bar Chart':
    state_total_graph = px.bar(state_total, x='Status', y='Number of cases',
                               labels={'Number of cases': 'Number of cases in %s' % (state_select)}, color='Status')
    st.plotly_chart(state_total_graph)
elif visualization == 'Pie Chart':
    status_select = st.sidebar.radio('Covid-19 patient status', ('Total Cases', 'Total Recovered', 'Total Deaths', 'Total Active Cases'))
    if status_select == 'Total Cases':
        st.markdown('## **Total Cases**')
        fig = px.pie(df, values=df['Total Cases'][:5], names=df['Location'][:5])
        st.plotly_chart(fig)
    elif status_select == 'Total Active Cases':
        st.markdown('## **Total Activ Cases**')
        fig = px.pie(df, values=df['Total Active Cases'][:5], names=df['Location'][:5])
        st.plotly_chart(fig)
    elif status_select == 'Total Deaths':
        st.markdown('## **Total Death Cases**')
        fig = px.pie(df, values=df['Total Deaths'][:5], names=df['Location'][:5])
        st.plotly_chart(fig)
    else:
        st.markdown('## **Total Recovered Cases**')
        fig = px.pie(df, values=df['Total Recovered'][:5], names=df['Location'][:5])
        st.plotly_chart(fig)
elif visualization == 'Line Chart':
    status_select = st.sidebar.radio('Covid-19 patient status', ('Total Cases', 'Total Recovered', 'Total Deaths', 'Total Active Cases'))
    if status_select == 'Total Cases':
        st.markdown('## **Total Confirmed Cases**')
        fig = px.line(df, x=df['Total Cases'], y=df['Location'])
        st.plotly_chart(fig)
    elif status_select == 'Total Active Cases':
        st.markdown('## **Total Activ Cases**')
        fig = px.line(df, x=df['Total Active Cases'], y=df['Location'])
        st.plotly_chart(fig)
    elif status_select == 'Total Deaths':
        st.markdown('## **Total Death Cases**')
        fig = px.line(df, x=df['Total Deaths'], y=df['Location'])
        st.plotly_chart(fig)
    else:
        st.markdown('## **Total Recovered Cases**')
        fig = px.line(df, x=df['Total Recovered'], y=df['Location'])
        st.plotly_chart(fig)

def get_table():
    datatable = df[['Location', 'Total Cases', 'Total Recovered', 'Total Deaths', 'Total Active Cases']].sort_values(by=['Total Cases'],
                ascending=False)
    return datatable

datatable = get_table()
st.dataframe(datatable)