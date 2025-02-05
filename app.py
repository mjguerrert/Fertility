import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuración de la página
st.set_page_config(layout="wide", page_title="Evolución TEF en Colombia")

# Cargar datos
tef_data = pd.read_excel("TEF_grupo_de_edad_nacional_Completo.xlsx", sheet_name="Sheet1")
timeline_data = pd.read_excel("Timeline_Normativas_Anticoncepcion_Colombia.xlsx", sheet_name="Hoja1")

# ---------------------------
# 1️⃣ Gráfica de TEF
# ---------------------------
st.title("Evolución de la Tasa Efectiva de Fecundidad (TEF) en Colombia")
fig_tef = px.line(
    tef_data,
    x="AÑO",
    y="TEF_10_49",
    title="Tasa Efectiva de Fecundidad (TEF) en Colombia",
    labels={"AÑO": "Año", "TEF_10_49": "TEF (10-49 años)"},
    markers=True,
)
st.plotly_chart(fig_tef, use_container_width=True)

# ---------------------------
# 2️⃣ Línea de tiempo interactiva
# ---------------------------
st.subheader("Línea de Tiempo de Políticas y Normativas")
selected_year = st.slider(
    "Selecciona un año en la línea de tiempo:",
    min_value=int(timeline_data["Año"].min()),
    max_value=int(timeline_data["Año"].max()),
    step=1,
)

# Crear gráfica de línea de tiempo
fig_timeline = go.Figure()

# Agregar eventos como banderitas
for _, row in timeline_data.iterrows():
    fig_timeline.add_trace(go.Scatter(
        x=[row["Año"]],
        y=[1],
        mode="markers+text",
        marker=dict(size=12, symbol="triangle-up", color="blue"),
        text=row["Normativa"],
        textposition="top center"
    ))

fig_timeline.update_layout(
    title="Eventos Clave en la Línea de Tiempo",
    xaxis=dict(title="Año", tickmode="linear"),
    yaxis=dict(visible=False),
    showlegend=False
)

st.plotly_chart(fig_timeline, use_container_width=True)

# ---------------------------
# 3️⃣ Bloque de explicación dinámica
# ---------------------------
st.subheader("Detalles del Evento Seleccionado")
event_details = timeline_data[timeline_data["Año"] == selected_year]

if not event_details.empty:
    normativa = event_details.iloc[0]["Normativa"]
    descripcion = event_details.iloc[0]["Descripción"]
    st.markdown(f"### **{normativa}**")
    st.write(descripcion)
else:
    st.write("No hay información para este año.")

# ---------------------------
# Instrucciones finales
# ---------------------------
st.info("Usa la gráfica, línea de tiempo y slider para explorar la evolución histórica de la TEF y las normativas.")
