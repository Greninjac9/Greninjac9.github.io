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
if "selected_characters" not in st.session_state:
    st.session_state["selected_characters"] = []

character = st.session_state["character"]
Correct = False

# Función para verificar los valores y mostrar el resultado
def CheckValues():
    current_row = []
    for N, key in enumerate(character.keys(), start=1):
        color = "red"
        size = "100%"
        time.sleep(0.1)
        if Characters[g_index][key] == character[key]:
            color = "green"
        if key in ["Elemento", "Género", "Invocador"]:
            size = "65%"
        image_path = os.path.join(IMAGE_DIR, f"{Characters[g_index][key]}.png")
        if os.path.exists(image_path):
            with open(image_path, 'rb') as image_file:
                image_data = base64.b64encode(image_file.read()).decode()
            current_row.append(f"""
            <div style='background-color:{color}; padding: 10px; margin-bottom: 10px; border-radius: 10px;'>
                <img src="data:image/png;base64,{image_data}" style="width: {size};" />
            </div>""")
    
    st.session_state["rows"].append(current_row)

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
guess = st.selectbox("Personajes", [ch for ch in CharacterRef if ch not in st.session_state["selected_characters"]], index=None, placeholder="¡Adivina un personaje!", key=st.session_state["key"], label_visibility="collapsed")

for row in st.session_state["rows"]:
    cols = st.columns(len(row))
    for idx, img in enumerate(row):
        with cols[idx]:
            st.markdown(img, unsafe_allow_html=True)
    st.divider()

if guess:
    st.session_state["selected_characters"].append(guess)
    g_index = CharacterRef.index(guess)
    CheckValues()
    if guess == character["Nombre"]:
        Correct = True
        st.markdown("<div class='result correct'>¡Correcto! El personaje era " + character["Nombre"] + "</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<div class='remaining'>¡Recarga la página para volver a jugar!</div></div>", unsafe_allow_html=True)
    else:
        st.session_state["Tries"] -= 1
        st.markdown("<div class='result incorrect'>Intentos restantes: " + str(st.session_state["Tries"]) + "</div>", unsafe_allow_html=True)
        st.session_state["key"] += 1

    # Eliminar el personaje seleccionado de las listas
    Characters.pop(g_index)
    CharacterRef.pop(g_index)

if st.session_state["Tries"] == 0 and not Correct:
    st.markdown("<div class='result incorrect'>Te has quedado sin intentos... El personaje era " + character["Nombre"] + "</div>", unsafe_allow_html=True)
    st.markdown("<div class='remaining'>¡Recarga la página para volver a jugar!</div></div>", unsafe_allow_html=True)
