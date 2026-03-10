import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ===============================
# CONFIG PAGE
# ===============================
st.set_page_config(page_title="Dashboard Soil Moisture", layout="wide")

st.title("📊 DASHBOARD SOIL MOISTURE")

# ===============================
# LOAD DATA
# ===============================
df = pd.read_csv("data_soil_moisture_clean.csv")

# ===============================
# HITUNG RATA-RATA
# ===============================
avg_moisture = df[['moisture0','moisture1','moisture2','moisture3','moisture4']].mean().mean()

# ===============================
# LINE CHART (TREND SENSOR)
# ===============================
st.subheader("Tren Kelembapan Multi Sensor")

fig_line = px.line(
    df,
    x="day",
    y=['moisture0','moisture1','moisture2','moisture3','moisture4'],
    title="Trend Soil Moisture"
)

st.plotly_chart(fig_line, use_container_width=True)

# ===============================
# DISTRIBUSI KONDISI TANAH
# ===============================

st.subheader("Distribusi Kondisi Tanah")

df["status"] = df["moisture0"].apply(
    lambda x: "Lembap" if x > 0.5 else "Kering"
)

status_count = df["status"].value_counts()

fig_pie = px.pie(
    values=status_count.values,
    names=status_count.index,
    hole=0.5
)

st.plotly_chart(fig_pie)

# ===============================
# GAUGE RATA RATA
# ===============================

st.subheader("Rata Rata Kelembapan Tanah")

fig_gauge = go.Figure(go.Indicator(
    mode="gauge+number",
    value=avg_moisture,
    title={'text': "Moisture"},
    gauge={
        'axis': {'range': [0,1]},
        'bar': {'color': "lightblue"}
    }
))

st.plotly_chart(fig_gauge)

# ===============================
# TABEL POLA WAKTU
# ===============================

st.subheader("Pola Kelembapan Berdasarkan Waktu")

st.dataframe(df)

# ===============================
# INSIGHT
# ===============================

st.subheader("Insight")

st.markdown(f"""
• Rata rata kelembapan tanah **{avg_moisture:.2f}**  

• Kondisi tanah relatif **stabil**  

• Distribusi air cukup **merata pada seluruh sensor**  

• Tidak terdapat indikasi **tanah terlalu kering atau terlalu basah**
""")