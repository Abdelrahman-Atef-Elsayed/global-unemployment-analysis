import streamlit as st
import pandas as pd
import plotly.express as px

# إعداد العنوان
st.set_page_config(layout="wide")
st.title("🌍 Global Unemployment Dashboard")

# تحميل البيانات
@st.cache_data
def load_data():
    df = pd.read_csv("data/unemployment_rate_annual.csv")
    df = df.dropna(subset=['obs_value'])
    return df

df = load_data()

# تصفية البيانات: فقط للجنس Total
df = df[df['sex.label'] == 'Total']

# اختيار دولة
countries = sorted(df['ref_area.label'].unique())
selected_country = st.selectbox("اختر دولة", countries)

# عرض رسم خطي للدولة المختارة
df_country = df[df['ref_area.label'] == selected_country]
fig_line = px.line(df_country, x='time', y='obs_value',
                   title=f"Unemployment Trend in {selected_country}",
                   labels={'time': 'Year', 'obs_value': 'Unemployment Rate (%)'},
                   markers=True)
st.plotly_chart(fig_line, use_container_width=True)

# رسم الخريطة التفاعلية (لآخر سنة فقط)
latest_year = df['time'].max()
df_latest = df[df['time'] == latest_year]

fig_map = px.choropleth(
    df_latest,
    locations='ref_area.label',
    locationmode='country names',
    color='obs_value',
    color_continuous_scale='Reds',
    title=f"Unemployment Rates in {latest_year}",
    labels={'obs_value': 'Unemployment Rate (%)'}
)
fig_map.update_layout(geo=dict(showframe=False, showcoastlines=False))
st.plotly_chart(fig_map, use_container_width=True)
