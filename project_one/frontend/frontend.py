from urllib.request import urlopen
import json
import streamlit as st
import requests
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


API_URL = "http://127.0.0.1:5000/schools"

response = requests.get(API_URL)
details = response.json()
school_df = pd.DataFrame(details)
school_df['borough'] = school_df['borough'].replace('NEW YORK',value='MANHATTAN')

top_5 = st.beta_container()

st.title('SCHOOLSY')
    
with top_5:
    st.write(" Number of High Schools by Borough ")
    fig = go.Figure()
    fig.add_trace(go.Histogram(histfunc="count",  x=school_df['borough']))
    st.plotly_chart(fig)