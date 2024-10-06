import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.animation as animation
from io import BytesIO

def create_voice_wave_animation():
    # Configuración de la figura
    fig, ax = plt.subplots(figsize=(10, 3))
    ax.set_xlim(0, 2*np.pi)
    ax.set_ylim(-1, 1)
    ax.axis('off')

    # Crear la línea inicial
    line, = ax.plot([], [], lw=3)

    # Función de inicialización
    def init():
        line.set_data([], [])
        return line,

    # Función de animación
    def animate(i):
        x = np.linspace(0, 2*np.pi, 1000)
        y = np.sin(5*x + i/10) * np.exp(-0.1 * ((x - np.pi) ** 2))
        line.set_data(x, y)
        return line,

    # Crear la animación
    anim = FuncAnimation(fig, animate, init_func=init, frames=200, interval=30, blit=True)

    # Guardar la animación como HTML
    html_io = BytesIO()
    anim.save(html_io, writer='html', fps=30)
    html = html_io.getvalue().decode()

    plt.close(fig)  # Cerrar la figura para liberar memoria

    return html

# Aplicación Streamlit

st.title("Simulación de Onda de Voz")
st.write("Presiona el botón para activar la animación de la onda de voz.")

# Crear un botón
if st.button('Activar Animación'):
    # Crear y mostrar la animación
    animation_html = create_voice_wave_animation()
    st.components.v1.html(animation_html, height=300)
else:
    st.write("La animación se mostrará aquí cuando actives el botón.")



