import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Load data
df_ind = pd.read_csv('Eurostat_econ_indicators_V2.csv',index_col=0)


# --- Streamlit App ---
# st.set_page_config(page_title="Industrial Indicators", layout="centered")
# st.title("📈 Industrial Indicators")

st.markdown("""
This interactive chart displays quarterly labour market and industrial production indicators.
Select your country-sector combination on the left side of the screen. Only the indicators with available data will be plotted.
""")

# Define the country label you want first
preferred_country = "European Union"
# Get all countries
all_countries = df_ind['geo'].unique().tolist()
country_list = [preferred_country] + sorted(all_countries)

# Sidebar selectors
st.sidebar.title("Filter Options")
sector = st.sidebar.selectbox("Select sector", sorted(df_ind['nace_r2'].unique()))
country = st.sidebar.selectbox("Select country", country_list)

# Filter and reshape data # Transpose for plotting: years as index, fuels as columns
selected = df_ind[(df_ind['nace_r2']==sector)&(df_ind['geo']==country)]
selected = selected.drop(columns=['nace_r2', 'geo'])
selected.set_index('indic_bt', inplace=True)
df_selected = selected.T
df_selected.index.name = 'Quarter'

# Early exit if no data
if df_selected.empty:
    st.warning("No data available for this combination of country and sector.")
    st.stop()

# Create the figure
fig = go.Figure()

# Add traces for each indicator, only if the column exists
if 'Industrial production' in df_selected.columns:
    fig.add_trace(go.Scatter(
        x=df_selected.index,
        y=df_selected['Industrial production'],
        mode='lines',
        line=dict(color='blue'),
        name='Industrial production'
    ))

if 'Persons employed' in df_selected.columns:
    fig.add_trace(go.Scatter(
        x=df_selected.index,
        y=df_selected['Persons employed'],
        mode='lines',
        line=dict(color='light green', width=2, dash='dash'),
        name='Persons employed',
        opacity=0.3 
    ))

if 'Hours worked' in df_selected.columns:
    fig.add_trace(go.Scatter(
        x=df_selected.index,
        y=df_selected['Hours worked'],
        mode='lines',
        line=dict(color='green', width=2, dash='dot'),
        name='Hours worked',
        opacity=0.3 
    ))

if 'Turnover (revenues)' in df_selected.columns:
    fig.add_trace(go.Scatter(
        x=df_selected.index,
        y=df_selected['Turnover (revenues)'],
        mode='lines',
        line=dict(color='purple', width=2),
        name='Turnover (revenues)',
        opacity=0.3 
    ))

# Customize layout
fig.update_layout(
    title=f"{sector} short-term indicators in {country}",
    xaxis_title="Quarter",
    yaxis_title="Index (2021=100)",
    legend_title="De-select indicators here",
    hovermode="x unified",
    template="plotly_white",
    showlegend=True
)

# Show plot
st.plotly_chart(fig, use_container_width=True)


# Optional: show data
with st.expander("Show raw data"):
    st.dataframe(df_selected)


