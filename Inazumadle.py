#########
# SETUP #
#########

import random
import time
from characters import Characters, CharacterRef
import streamlit as st

character = random.choice(Characters)
if "character" not in st.session_state:
    st.session_state["character"] = character

Correct = False
key = 1

#############
# FUNCTIONS #
#############

def CheckValues():
  N = 1
  for key in st.session_state["character"]:
    time.sleep(0.2)
    variable_name = "col" + str(N)
    with globals()[variable_name]:
      if Characters[g_index][key] == st.session_state["character"][key]:
        st.write(":green-background[" + (Characters[g_index][key]) + "]")
      else:
        st.write(":red-background[" + (Characters[g_index][key]) + "]")
    N += 1

for T in range(5, -1, -1):
  guess = st.selectbox("Personajes", CharacterRef, index=None, placeholder="¡Adivina un personaje!", key=key, label_visibility="collapsed")
  col1, col2, col3, col4, col5, col6 = st.columns(6, gap="medium")
  g_index = CharacterRef.index(guess)
  if guess == st.session_state["character"]["Nombre"]:
    CheckValues()
    Correct = True
    st.write("")
    break
  else:
    st.write(":red[INCORRECTO]. Intentos restantes:", T)
    CheckValues()
  st.write("")
  key += 1

if Correct:
  st.subheader(":green[¡Correcto!] "+"El personaje era " + str(st.session_state["character"]["Nombre"]))
else:
  st.subheader("Te has quedado sin intentos... "+"El personaje era " + str(st.session_state["character"]["Nombre"]))
st.write("¡Recarga la página para volver a jugar!")