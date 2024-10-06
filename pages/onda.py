mport streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.animation as animation
import io

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

    # Guardar la animación como un gif en memoria
    buf = io.BytesIO()
    anim.save(buf, writer='pillow', fps=30)
    buf.seek(0)
    
    return buf

# Aplicación Streamlit

st.title("Simulación de Onda de Voz")
st.write("Presiona el botón para activar la animación de la onda de voz.")

# Crear un botón
if st.button('Activar Animación'):
    # Crear y mostrar la animación
    animation_buf = create_voice_wave_animation()
    st.image(animation_buf, use_column_width=True)
else:
    st.write("La animación se mostrará aquí cuando actives el botón.")
