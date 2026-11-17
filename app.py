Python
import os
import streamlit as st
from groq import Groq

# Configurazione della pagina
st.set_page_config(page_title="Itiner AI v0.1", page_icon="🧭", layout="centered")
st.title("Itiner")
st.caption("Versione 0.1 — Il tuo compagno di viaggio nella conoscenza")

# Inizializza il client Groq con la chiave segreta
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Selettore dei moduli
modulo = st.sidebar.selectbox(
    "Scegli il modulo di Itiner:",
    [
        "📚 Itiner Studio (Scuola & Interrogazioni)",
        "🎧 Itiner Sound (Musica, Beat & Mix)",
        "🧠 Itiner Core (Assistente Generale)",
    ],
)

istruzioni_moduli = {
    "📚 Itiner Studio (Scuola & Interrogazioni)": (
        "Sei Itiner Studio, un tutor scolastico brillante. Non dare solo la risposta pronta: "
        "spiega i concetti in chiaro con esempi pratici e, alla fine, fai sempre "
        "una domanda di verifica allo studente per testare se ha capito."
    ),
    "🎧 Itiner Sound (Musica, Beat & Mix)": (
        "Sei Itiner Sound, un producer musicale e ingegnere del suono esperto. "
        "Aiuti cantanti e DJ a scrivere testi, strutturare beat, scegliere accordi e "
        "impostare EQ, compressori e mastering."
    ),
    "🧠 Itiner Core (Assistente Generale)": (
        "Sei Itiner, un'intelligenza artificiale progettata per guidare l'utente "
        "nella risoluzione di problemi complessi in modo chiaro, diretto e pratico."
    ),
}
# Memoria della chat
if "messaggi" not in st.session_state:
    st.session_state.messaggi = []

for msg in st.session_state.messaggi:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input dell'utente
if prompt := st.chat_input("Chiedi qualcosa a Itiner..."):
    st.session_state.messaggi.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Prepara la cronologia dei messaggi per Groq
        chat_history = [{"role": "system", "content": istruzioni_moduli[modulo]}]
        for m in st.session_state.messaggi:
            chat_history.append({"role": m["role"], "content": m["content"]})

        # Genera la risposta usando il modello Llama 3 di Groq
        risposta_stream = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=chat_history,
            stream=True,
        )

        # Mostra la risposta in streaming
        contenuto_risposta = st.write_stream(
            chunk.choices[0].delta.content
            for chunk in risposta_stream
            if chunk.choices[0].delta.content is not None
        )
        st.session_state.messaggi.append(
            {"role": "assistant", "content": contenuto_risposta}
        )
