import streamlit as st
import numpy as np
import plotly.graph_objs as go
import time

# Configuración de la página
st.set_page_config(
    page_title="Animación de Onda Vibrante",
    layout="wide",
)

# Generar datos de la onda
def generar_onda(frecuencia, amplitud, tiempo, muestreo):
    t = np.linspace(0, tiempo, int(tiempo * muestreo), endpoint=False)
    onda = amplitud * np.sin(2 * np.pi * frecuencia * t)
    return t, onda

# Configuración inicial
frecuencia = 2  # Frecuencia en Hz
amplitud = 1  # Amplitud de la onda
tiempo = 5  # Duración en segundos
muestreo = 500  # Frecuencia de muestreo en Hz

# Crear la animación de la onda
st.title("Animación de Onda Vibrante")
placeholder = st.empty()

t, onda = generar_onda(frecuencia, amplitud, tiempo, muestreo)
fig = go.Figure()
fig.add_trace(go.Scatter(x=t, y=onda, mode="lines"))

# Configurar la gráfica
fig.update_layout(
    xaxis_title="Tiempo (s)",
    yaxis_title="Amplitud",
    title="Sistema de Voz en Reproducción",
    yaxis=dict(range=[-1.5, 1.5]),
    xaxis=dict(range=[0, tiempo]),
)

# Mostrar la animación en Streamlit
for i in range(1, len(t)):
    fig.update_traces(go.Scatter(x=t[:i], y=onda[:i], mode="lines"))
    placeholder.write(fig.to_html(), unsafe_allow_html=True)
    time.sleep(0.01)
