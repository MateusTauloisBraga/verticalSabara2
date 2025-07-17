import streamlit as st
from datetime import datetime
import pandas as pd
import pytz
import os

# Nome do arquivo CSV
CSV_PATH = "chegadas_atletas.csv"

# Timezone de São Paulo
tz = pytz.timezone("America/Sao_Paulo")

st.set_page_config(page_title="Cronometragem Vertical", layout="centered")
st.title("⏱️ Cronometragem Vertical")

# Inicializa CSV se não existir
if not os.path.exists(CSV_PATH):
    pd.DataFrame(columns=["Atleta", "Horário de Chegada", "Tempo desde início"]).to_csv(CSV_PATH, index=False)

# Inicializa variáveis na sessão
if 'start_time' not in st.session_state:
    st.session_state.start_time = None

# Botão para iniciar a prova
if st.button("▶️ Iniciar Prova"):
    st.session_state.start_time = datetime.now(tz)
    st.success(f"Prova iniciada em: {st.session_state.start_time.strftime('%H:%M:%S')}")

# Botão para limpar o CSV com confirmação

    

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

        # Adiciona no CSV
        novo_registro.to_csv(CSV_PATH, mode='a', header=False, index=False)
        st.success(f"Atleta {atleta} registrado!")

# Lê os dados do CSV e mostra
try:
    dados_csv = pd.read_csv(CSV_PATH)
    if not dados_csv.empty:
        st.markdown("### 📋 Chegadas Registradas")
        st.dataframe(dados_csv, use_container_width=True)

        # Exportar CSV
        csv = dados_csv.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Baixar CSV",
            data=csv,
            file_name='chegadas_atletas.csv',
            mime='text/csv'
        )

except Exception as e:
    st.error(f"Erro ao ler CSV: {e}")

if st.button("🗑️ Resetar Entrada dos Atletas"):
    import os

    file_to_delete = CSV_PATH
    os.remove(file_to_delete)
    print(f"File '{file_to_delete}' deleted successfully.")
