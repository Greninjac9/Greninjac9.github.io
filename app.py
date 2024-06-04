import random
import time
import streamlit as st
from characters import Characters, CharacterRef
import os
import base64

# Define el directorio de las imágenes
IMAGE_DIR = "assets/images"  # Ajusta el directorio según tu estructura

# Escoger un personaje aleatorio al inicio de la sesión
if "character" not in st.session_state:
    st.session_state["character"] = random.choice(Characters)

character = st.session_state["character"]
Correct = False
key = 1

# Función para verificar los valores y mostrar el resultado
def CheckValues():
    N = 1
    for key in character:
        color = "red"
        size = "100%"
        time.sleep(0.2)
        variable_name = "col" + str(N)
        with globals()[variable_name]:
            if Characters[g_index][key] == character[key]:
                color = "green"
            if key in ["Elemento", "Género"]:
                size = "50%"
            image_path = os.path.join(IMAGE_DIR, f"{Characters[g_index][key]}.png")
            if os.path.exists(image_path):
                with open(image_path, 'rb') as image_file:
                    image_data = base64.b64encode(image_file.read()).decode()
                st.markdown(f"""
                <div style='background-color:{color}; padding: 10px; border-radius: 10px;'>
                    <img src="data:image/png;base64,{image_data}" style="width: {size};" />
                </div>
                """, unsafe_allow_html=True)
        N += 1

# CSS para mejorar la apariencia con fondo oscuro
st.markdown("""
    <style>
        body {
            background-color: #1e1e1e;
            color: #f5f5f5;
        }
        .main {
            background-color: #333;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.5);
        }
        .title {
            font-size: 24px;
            margin-bottom: 20px;
            color: #f5f5f5;
        }
        .result {
            margin-top: 20px;
            font-size: 18px;
        }
        .correct {
            color: #4caf50;
        }
        .incorrect {
            color: #f44336;
        }
        .remaining {
            margin-top: 10px;
            color: #9e9e9e;
        }
    </style>
""", unsafe_allow_html=True)

# Título de la aplicación
st.markdown("<div class='main'><div class='title'>¡Adivina un personaje!</div>", unsafe_allow_html=True)

for T in range(5, -1, -1):
    guess = st.selectbox("Personajes", CharacterRef, index=None, placeholder="¡Adivina un personaje!", key=key, label_visibility="collapsed")
    col1, col2, col3, col4, col5, col6 = st.columns(6, gap="medium")
    g_index = CharacterRef.index(guess)
    if guess == character["Nombre"]:
        CheckValues()
        Correct = True
        st.markdown("<div class='result correct'>¡Correcto! El personaje era " + character["Nombre"] + "</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        break
    else:
        st.markdown("<div class='result incorrect'>INCORRECTO. Intentos restantes: " + str(T) + "</div>", unsafe_allow_html=True)
        CheckValues()
    key += 1

if not Correct:
    st.markdown("<div class='result incorrect'>Te has quedado sin intentos... El personaje era " + character["Nombre"] + "</div>", unsafe_allow_html=True)
st.markdown("<div class='remaining'>¡Recarga la página para volver a jugar!</div></div>", unsafe_allow_html=True)