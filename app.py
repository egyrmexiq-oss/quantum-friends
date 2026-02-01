import streamlit as st
from openai import OpenAI

# ===============================
# CONFIGURACIÓN GENERAL
# ===============================
#
st.set_page_config(page_title="Quantum University", page_icon="🧑‍🎓", layout="wide")

st.set_page_config(
    page_title="Quantum-Friends",
    layout="centered"
)

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

MODEL_NAME = "gpt-4.1-mini"
MAX_TOKENS = 300
TEMPERATURE = 0.7


# ===============================
# PROMPT BASE (IDENTIDAD)
# ===============================

SYSTEM_PROMPT = """
Eres Quantum-Friends.

Hablas como un amigo cercano, coloquial, empático y optimista.
NO eres terapeuta, NO diagnosticas, NO das órdenes.

Siempre inicias con frases de cercanía como:
"Oye", "Uhh, entiendo", "Caray", "No me digas", "En serio…?"

Haces preguntas suaves para entender el estado emocional.
Nunca te presentas como el único apoyo ni sustituyes relaciones humanas.
Si algo parece requerir ayuda profesional, lo sugieres con respeto y ligereza.
"""


# ===============================
# DETECCIÓN DE FLAGS (HEURÍSTICA INICIAL)
# ===============================

def detect_flag(text: str) -> str:
    text = text.lower()

    red_keywords = [
        "no quiero vivir", "quiero desaparecer", "ya no puedo",
        "me quiero morir", "todo es inútil"
    ]

    yellow_keywords = [
        "triste", "apagado", "cansado", "sin ganas",
        "solo", "desmotivado", "estresado"
    ]

    high_energy_keywords = [
        "logré", "éxito", "feliz", "emocionado", "orgulloso"
    ]

    for k in red_keywords:
        if k in text:
            return "ROJA"

    for k in yellow_keywords:
        if k in text:
            return "AMARILLA"

    for k in high_energy_keywords:
        return "VERDE"

    return "VERDE"


# ===============================
# REFUERZOS POR FLAG
# ===============================

def flag_reinforcement(flag: str) -> str:
    if flag == "AMARILLA":
        return (
            "Oye, y dime… ¿esto es algo reciente o ya lleva varios días así?\n"
            "A veces entender el ritmo ayuda a ver opciones."
        )

    if flag == "S":
        return (
            "Recuerda que, entre amigos, a veces solo ponerlo en palabras ya cambia algo.\n"
            "Aquí podemos ir viendo opciones con calma."
        )

    if flag == "ROJA":
        return (
            "Caray… esto sí suena pesado.\n"
            "Si en algún momento sientes que rebasa lo que podemos charlar aquí, "
            "buscar apoyo profesional puede ser una buena idea. No es obligación, "
            "solo una opción más."
        )

    return ""


# ===============================
# LLAMADA AL MODELO
# ===============================

def generate_response(messages):
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE
    )
    return response.choices[0].message.content


# ===============================
# UI
# ===============================

st.title("🤝 Quantum-Friends")
st.write("Oye… ¿qué tal va tu día hoy?")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

user_input = st.text_input("Tú:")

if user_input:
    flag = detect_flag(user_input)

    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    assistant_reply = generate_response(st.session_state.messages)
    reinforcement = flag_reinforcement(flag)

    full_reply = assistant_reply
    if reinforcement:
        full_reply += "\n\n" + reinforcement

    st.session_state.messages.append(
        {"role": "assistant", "content": full_reply}
    )

# Mostrar conversación
for msg in st.session_state.messages[1:]:
    if msg["role"] == "user":
        st.markdown(f"**Tú:** {msg['content']}")
    else:
        st.markdown(f"**Quantum-Friends:** {msg['content']}")

