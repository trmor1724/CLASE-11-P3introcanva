import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import tempfile
import base64
import os

def create_voice_wave_animation():
    # Configuración de la figura
    fig, ax = plt.subplots(figsize=(10, 3))
    ax.set_xlim(0, 2*np.pi)
    ax.set_ylim(-1.5, 1.5)
    ax.axis('off')

    # Crear la línea inicial
    line, = ax.plot([], [], lw=2)

    # Función de inicialización
    def init():
        line.set_data([], [])
        return line,

    # Función de animación con variaciones aleatorias
    def animate(i):
        x = np.linspace(0, 2*np.pi, 1000)
        random_amp = np.random.uniform(0.5, 1.5)
        random_freq = np.random.uniform(4, 6)
        noise = np.random.normal(0, 0.1, 1000)
        y = random_amp * np.sin(random_freq*x + i/10) * np.exp(-0.1 * ((x - np.pi) ** 2)) + noise
        line.set_data(x, y)
        return line,

    # Crear la animación
    anim = FuncAnimation(fig, animate, init_func=init, frames=200, interval=50, blit=True)

    # Crear un archivo temporal
    with tempfile.NamedTemporaryFile(suffix='.gif', delete=False) as temp_file:
        # Guardar la animación como gif en el archivo temporal
        anim.save(temp_file.name, writer='pillow', fps=25)
        plt.close(fig)

        # Leer el archivo y codificarlo en base64
        with open(temp_file.name, 'rb') as f:
            gif_data = f.read()
            b64 = base64.b64encode(gif_data).decode('utf-8')

    # Eliminar el archivo temporal
    os.unlink(temp_file.name)

    return b64

def create_static_wave():
    fig, ax = plt.subplots(figsize=(10, 3))
    ax.set_xlim(0, 2*np.pi)
    ax.set_ylim(-1.5, 1.5)
    ax.axis('off')

    x = np.linspace(0, 2*np.pi, 1000)
    #y = np.sin(5*x) * np.exp(-0.1 * ((x - np.pi) ** 2))
    y = np.zeros_like(x)
    ax.plot(x, y, lw=2)

    # Guardar la imagen estática
    buf = tempfile.NamedTemporaryFile(suffix='.png')
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode()
    buf.close()

    return img_str

# Aplicación Streamlit

st.title("Simulación de Onda de Voz con Controles")
st.write("Usa los botones para controlar la animación de la onda de voz.")

# Inicializar variables de estado
if 'animation_running' not in st.session_state:
    st.session_state.animation_running = False
if 'gif_base64' not in st.session_state:
    st.session_state.gif_base64 = None
if 'static_img' not in st.session_state:
    st.session_state.static_img = create_static_wave()

# Botones de control
col1, col2 = st.columns(2)
with col1:
    if st.button('Iniciar Animación'):
        st.session_state.animation_running = True
        st.session_state.gif_base64 = create_voice_wave_animation()
with col2:
    if st.button('Detener Animación'):
        st.session_state.animation_running = False

# Mostrar animación o imagen estática
if st.session_state.animation_running and st.session_state.gif_base64:
    st.markdown(f'<img src="data:image/gif;base64,{st.session_state.gif_base64}" alt="voice wave animation">', unsafe_allow_html=True)
else:
    st.markdown(f'<img src="data:image/png;base64,{st.session_state.static_img}" alt="static voice wave">', unsafe_allow_html=True)

