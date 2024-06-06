import random
import time
import streamlit as st
from characters import Characters, CharacterRef
import os
import base64

st.set_page_config(
    page_title="Inazumadle",
    page_icon="⚡",
    layout="centered"
)

# Define el directorio de las imágenes
IMAGE_DIR = "assets/images"  # Ajusta el directorio según tu estructura

# Escoger un personaje aleatorio al inicio de la sesión
if "character" not in st.session_state:
    st.session_state["character"] = random.choice(Characters)

character = st.session_state["character"]
Correct = False
key = 1

# Cargar y codificar la imagen de fondo
background_image_path = "/mnt/data/image.png"
if os.path.exists(background_image_path):
    with open(background_image_path, 'rb') as image_file:
        background_image_data = base64.b64encode(image_file.read()).decode()
else:
    st.error("La imagen de fondo no se encontró.")

# Función para verificar los valores y mostrar el resultado
def CheckValues():
    N = 1
    for key in character:
        color = "red"
        size = "100%"
        time.sleep(0.1)
        variable_name = "col" + str(N)
        with globals()[variable_name]:
            if Characters[g_index][key] == character[key]:
                color = "green"
            if key in ["Elemento", "Género","Invocador"]:
                size = "65%"
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
    st.divider()

# CSS para mejorar la apariencia con fondo oscuro y una imagen de fondo difuminada
st.markdown(f"""
    <style>
        body {{
            color: #f5f5f5;
        }}
        [data-testid="stAppViewContainer"] {{
            background: url('data:image/png;base64,{background_image_data}') no-repeat center center fixed;
            background-size: cover;
        }}
        [data-testid="stAppViewContainer"] > .main {{
            background: rgba(51, 51, 51, 0.8);
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(10px); /* Aplica el efecto de difuminado */
        }}
        .title {{
            font-size: 24px;
            margin-bottom: 20px;
            color: #f5f5f5;
        }}
        .result {{
            margin-top: 20px;
            font-size: 18px;
        }}
        .correct {{
            color: #4caf50;
        }}
        .incorrect {{
            color: #f44336;
        }}
        .remaining {{
            margin-top: 10px;
            color: #9e9e9e;
        }}
    </style>
""", unsafe_allow_html=True)

st.image("assets/Inazumadle.png", caption=None, width=None, use_column_width="always", clamp=False, channels="RGB", output_format="PNG")

for T in range(5, -1, -1):
    guess = st.selectbox("Personajes", CharacterRef, index=None, placeholder="¡Adivina un personaje!", key=f"selectbox_{key}", label_visibility="collapsed")
    while guess == None:
        guess = st.selectbox("Personajes", CharacterRef, index=None, placeholder="¡Adivina un personaje!", key=f"selectbox_{key}", label_visibility="collapsed")
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7, gap="medium")
    g_index = CharacterRef.index(guess)
    if guess == character["Nombre"]:
        CheckValues()
        Correct = True
        st.markdown("<div class='result correct'>¡Correcto! El personaje era " + character["Nombre"] + "</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        break
    else:
        st.markdown("<div class='result incorrect'>Intentos restantes: " + str(T) + "</div>", unsafe_allow_html=True)
        CheckValues()
    key += 1

if not Correct:
    st.markdown("<div class='result incorrect'>Te has quedado sin intentos... El personaje era " + character["Nombre"] + "</div>", unsafe_allow_html=True)
st.markdown("<div class='remaining'>¡Recarga la página para volver a jugar!</div></div>", unsafe_allow_html=True)
