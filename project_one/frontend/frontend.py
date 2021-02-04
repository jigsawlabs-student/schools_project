from urllib.request import urlopen
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

API_URL = "http://127.0.0.1:5000/schools"

response = requests.get(API_URL)
details = response.json()
original_df = pd.DataFrame(details)

def clean(df):
    df = df.swapaxes("index", "columns").dropna(0)
    df['borough'] = df['borough'].replace('NEW YORK',value='MANHATTAN')
    return df

df = clean(original_df)

top_bot_5 = st.beta_container()
borough_stats = st.beta_container()



with borough_stats:
    st.title('Top Five')
    st.write(" Number of High Schools ")
    fig = go.Figure()
    fig.add_trace(go.Histogram(histfunc="count", x=df['borough'],marker_color=['#6600FF','#FF0033','#CCFF00']))
    st.plotly_chart(fig)

    st.write('Average Sat Score')
    fig_2 = go.Figure()
    fig_2.add_trace(go.Histogram(histfunc="avg",  x=df['borough'],y=df['tot_sat_score'],marker_color = ['#6600FF','#FF0033','#CCFF00']))
    st.plotly_chart(fig_2)

    st.write('Average Graduation Rate')
    fig_3 = go.Figure()
    fig_3.add_trace(go.Histogram(histfunc="avg", x=df['borough'],y=df['graduation_rate'],marker_color= ['#6600FF','#FF0033','#CCFF00']))
    st.plotly_chart(fig_3)


# with top_bot_5:
#     st.title('Top Five')
#         # st.write("Sat Scores")
#         # fig = go.Figure()
#         # fig.add_trace(go.Histogram(histfunc="count", x=df['borough'],marker_color=['#6600FF','#FF0033','#CCFF00']))
#         # st.plotly_chart(fig)

#         # st.write('Graduation Rate')
#         # fig_2 = go.Figure()
#         # fig_2.add_trace(go.Histogram(histfunc="avg",  x=df['borough'],y=df['tot_sat_score'],marker_color = ['#6600FF','#FF0033','#CCFF00']))
#         # st.plotly_chart(fig_2)

#         # st.write('Average Graduation Rate by Borough')
#         # fig_3 = go.Figure()
#         # fig_3.add_trace(go.Histogram(histfunc="avg", x=df['borough'],y=df['graduation_rate'],marker_color= ['#6600FF','#FF0033','#CCFF00']))
#         # st.plotly_chart(fig_3)
#     st.title('Bottom Five')

