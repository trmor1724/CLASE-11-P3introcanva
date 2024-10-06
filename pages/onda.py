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
    ax.set_ylim(-1.5, 1.5)  # Aumentamos el rango del eje y para acomodar las variaciones
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
        # Generamos componentes aleatorios para la amplitud y la frecuencia
        random_amp = np.random.uniform(0.5, 1.5)
        random_freq = np.random.uniform(4, 6)
        # Añadimos un componente de ruido
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

# Aplicación Streamlit

st.title("Simulación de Onda de Voz")
st.write("Presiona el botón para activar la animación de la onda de voz.")

# Crear un botón
if st.button('Activar Animación'):
    # Crear y mostrar la animación
    gif_base64 = create_voice_wave_animation()
    html = f'<img src="data:image/gif;base64,{gif_base64}" alt="voice wave animation">'
    st.markdown(html, unsafe_allow_html=True)
else:
    st.write("La animación se mostrará aquí cuando actives el botón.")






