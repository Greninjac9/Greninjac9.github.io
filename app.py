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
if "images" not in st.session_state:
    st.session_state["images"] = []
if "Tries" not in st.session_state:
    st.session_state["Tries"] = 6
if "key" not in st.session_state:
    st.session_state["key"] = 1
if "checked" not in st.session_state:
    st.session_state["checked"] = []

character = st.session_state["character"]
Correct = False

# Función para verificar los valores y mostrar el resultado
def CheckValues():
    for N, key in enumerate(character.keys(), start=1):
        if Characters[g_index][key] == character[key]:
            color = "green"
        else:
            color = "red"
        size = "100%" if key not in ["Elemento", "Género", "Invocador"] else "65%"
        image_path = os.path.join(IMAGE_DIR, f"{Characters[g_index][key]}.png")
        if os.path.exists(image_path):
            with open(image_path, 'rb') as image_file:
                image_data = base64.b64encode(image_file.read()).decode()
            image_html = f"""
            <div style='background-color:{color}; padding: 10px; border-radius: 10px;'>
                <img src="data:image/png;base64,{image_data}" style="width: {size};" />
            </div>"""
            st.session_state["checked"].append((image_html, key))
    
    # Mostrar las imágenes de forma persistente
    unique_keys = list(set([key for _, key in st.session_state["checked"]]))
    for unique_key in unique_keys:
        filtered_images = [img for img, key in st.session_state["checked"] if key == unique_key]
        if filtered_images:
            num_cols = 7
            rows = [st.columns(num_cols, gap="medium") for _ in range((len(filtered_images) + num_cols - 1) // num_cols)]
            for idx, img in enumerate(filtered_images):
                row = rows[idx // num_cols]
                with row[idx % num_cols]:
                    st.markdown(img, unsafe_allow_html=True)
            st.divider()

# CSS para mejorar la apariencia con fondo oscuro y una imagen de fondo difuminada
st.markdown(f"""
    <style>
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
guess = st.selectbox("Personajes", CharacterRef, index=None, placeholder="¡Adivina un personaje!", key=st.session_state["key"], label_visibility="collapsed")

g_index = CharacterRef.index(guess)
if guess == character["Nombre"]:
    CheckValues()
    Correct = True
    st.markdown("<div class='result correct'>¡Correcto! El personaje era " + character["Nombre"] + "</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<div class='remaining'>¡Recarga la página para volver a jugar!</div></div>", unsafe_allow_html=True)
else:
    st.session_state["Tries"] -= 1
    st.markdown("<div class='result incorrect'>Intentos restantes: " + str(st.session_state["Tries"]) + "</div>", unsafe_allow_html=True)
    CheckValues()
    st.session_state["key"] += 1

if st.session_state["Tries"] == 0 and not Correct:
    st.markdown("<div class='result incorrect'>Te has quedado sin intentos... El personaje era " + character["Nombre"] + "</div>", unsafe_allow_html=True)
    st.markdown("<div class='remaining'>¡Recarga la página para volver a jugar!</div></div>", unsafe_allow_html=True)
