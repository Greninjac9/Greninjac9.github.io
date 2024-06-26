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

IMAGE_DIR = "assets/images" 

# Escoger un personaje aleatorio al inicio de la sesión
if "character" not in st.session_state:
    st.session_state["character"] = random.choice(Characters)

character = st.session_state["character"]
Correct = False
key = 1

# Función para verificar los valores y mostrar el resultado
def CheckValues(g_index):
    N = 1
    for key in character:
        color = "red"
        size = "100%"
        time.sleep(0.1)
        variable_name = "col" + str(N)
        if N == 1 or N == 7 or N == 4 or N == 6:
            Split_Key = Characters[g_index][key].split()
            Split_char = character[key].split()
            if N == 1 and Split_Key[:2] == Split_char[:2]:
                color = "#FFBF00"
            elif N == 4 or N == 6:
                Pos = ["DF", "LB", "EG_Y", "EG_ARM"]
                if Characters[g_index][key] in Pos and character[key] in Pos:
                    color = "#FFBF00"
            elif N == 7:
                Equipos_Coincidentes = ["RAIMON", "ALPINO", "ACADEMIA ALIUS", "PROTOCOLO OMEGA", "INAZUMA JAPON", "ZEUS"]
                if ((" ".join(Split_Key[:1])) in Equipos_Coincidentes  and (" ".join(Split_char[:1])) in Equipos_Coincidentes
                    and Equipos_Coincidentes.index((" ".join(Split_Key[:1]))) == Equipos_Coincidentes.index((" ".join(Split_char[:1])))):
                    color = "#FFBF00"
                elif ((" ".join(Split_Key[:2])) in Equipos_Coincidentes  and (" ".join(Split_char[:2])) in Equipos_Coincidentes
                    and Equipos_Coincidentes.index((" ".join(Split_Key[:2]))) == Equipos_Coincidentes.index((" ".join(Split_char[:2])))):
                    color = "#FFBF00"
        if Characters[g_index][key] == character[key]:
            color = "green"
        if key in ["Elemento", "Género", "Invocador"]:
            size = "65%"
        with globals()[variable_name]:
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

st.image("assets/Inazumadle.png", caption=None, width=None, use_column_width="always", clamp=False, channels="RGB", output_format="PNG")
for T in range(5, -1, -1):
    guess = st.selectbox("Personajes", CharacterRef, index=None, placeholder="¡Adivina un personaje!", key=key, label_visibility="collapsed")
    while guess == None:
        guess = st.selectbox("Personajes", CharacterRef, index=None, placeholder="¡Adivina un personaje!", key=key, label_visibility="collapsed")
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7, gap="medium")
    g_index = CharacterRef.index(guess)
    if Characters[g_index]["Nombre"] == character["Nombre"]:
        CheckValues(g_index)
        Correct = True
        st.markdown("<div class='result correct'>¡Correcto! El personaje era " + character["Nombre"] + "</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        break
    else:
        st.markdown("<div class='result incorrect'>Intentos restantes: " + str(T) + "</div>", unsafe_allow_html=True)
        CheckValues(g_index)
    key += 1

if not Correct:
    st.markdown("<div class='result incorrect'>Te has quedado sin intentos... El personaje era " + character["Nombre"] + "</div>", unsafe_allow_html=True)
st.markdown("<div class='remaining'>¡Recarga la página para volver a jugar!</div></div>", unsafe_allow_html=True)
