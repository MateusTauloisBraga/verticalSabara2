import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import pytz
import time

# Timezone de São Paulo
tz = pytz.timezone("America/Sao_Paulo")

st.set_page_config(page_title="Cronometragem Vertical", layout="centered")
st.title("⏱️ Cronometragem Vertical")

# Inicializa variáveis na sessão
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'dados' not in st.session_state:
    st.session_state.dados = pd.DataFrame(columns=["Atleta", "Horário de Chegada", "Tempo desde início"])

# Botão para iniciar a prova
if st.button("▶️ Iniciar Prova"):
    st.session_state.start_time = datetime.now(tz)
    st.success(f"Prova iniciada em: {st.session_state.start_time.strftime('%H:%M:%S')}")

# Cronômetro visível
if st.session_state.start_time:
    tempo_atual = datetime.now(tz)
    tempo_decorrido = tempo_atual - st.session_state.start_time
    tempo_str = str(tempo_decorrido).split(".")[0]
    st.markdown(f"🕒 Tempo decorrido: **{tempo_str}**")

    # Campo para digitar o número do atleta
    atleta = st.text_input("Número do Atleta", placeholder="Digite o número e pressione Enter")

    if atleta:
        chegada = datetime.now(tz)
        tempo = chegada - st.session_state.start_time
        novo_registro = pd.DataFrame([[atleta, chegada.strftime('%H:%M:%S'), str(tempo).split('.')[0]]],
                                     columns=["Atleta", "Horário de Chegada", "Tempo desde início"])
        st.session_state.dados = pd.concat([st.session_state.dados, novo_registro], ignore_index=True)
        st.markdown("### 📋 Chegadas Registradas (parciais)")
        st.dataframe(st.session_state.dados, use_container_width=True)

# Mostra os dados
if not st.session_state.dados.empty:
    st.markdown("### 📋 Chegadas Registradas")
    st.dataframe(st.session_state.dados, use_container_width=True)

    # Exportar CSV
    csv = st.session_state.dados.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Baixar CSV",
        data=csv,
        file_name='chegadas_atletas.csv',
        mime='text/csv'
    )
