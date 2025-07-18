import streamlit as st
from datetime import datetime
import pandas as pd
import pytz
import os

# Nome do arquivo CSV
CSV_PATH = "chegadas_atletas.csv"

# Timezone de São Paulo
tz = pytz.timezone("America/Sao_Paulo")

# Dicionário de número para nome
numero_para_nome = {
    101: "Antônio Leite",
    102: "Celdinei Ornelas",
    103: "Claudio Henrique",
    104: "Darlan Nonato",
    105: "Dowglas Ferreira",
    106: "Filipe Madeira",
    107: "Gerjane Oliveira",
    108: "Guilherme Silva",
    109: "Hebert Bruno",
    110: "Hebert Hoene",
    111: "Hellen Cristine",
    112: "Joaquim Bemfeito",
    113: "Jonathan Oliveira",
    114: "Katia Perdigão",
    115: "Leonardo Costa",
    116: "Lorena Teixeira",
    117: "Mauro Ribeiro",
    118: "Miriam Cristina",
    119: "Nathalia Perdigão",
    120: "Rafael Augusto",
    121: "Ramon Viterbo",
    122: "Raphael Vertello",
    123: "Rilk Brando",
    124: "Rodrigo Pereira",
    125: "Rogério Alves",
    126: "Samuel Costa",
    127: "Saulo Braga",
    128: "Silvania Maria",
    129: "Silvia Brangioni",
    130: "Wesley Souza"
}

# Inicializa CSV se não existir
if not os.path.exists(CSV_PATH):
    pd.DataFrame(columns=["Atleta", "Nome", "Horário de Chegada", "Tempo desde início"]).to_csv(CSV_PATH, index=False)

# Inicializa variáveis na sessão
if 'start_time' not in st.session_state:
    st.session_state.start_time = None

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
        try:
            numero = int(atleta)
            nome = numero_para_nome.get(numero, "Desconhecido")
        except ValueError:
            st.error("Número inválido")
            nome = "Desconhecido"
            numero = atleta  # salva o que foi digitado

        chegada = datetime.now(tz)
        tempo = chegada - st.session_state.start_time
        novo_registro = pd.DataFrame(
            [[numero, nome, chegada.strftime('%H:%M:%S'), str(tempo).split('.')[0]]],
            columns=["Atleta", "Nome", "Horário de Chegada", "Tempo desde início"]
        )

        # Adiciona no CSV
        novo_registro.to_csv(CSV_PATH, mode='a', header=False, index=False)
        st.success(f"Atleta {numero} ({nome}) registrado!")

# Lê os dados do CSV e mostra
try:
    dados_csv = pd.read_csv(CSV_PATH)
    dados_csv = dados_csv.drop_duplicates(subset=["Atleta"], keep="first")
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

# Botão para resetar CSV
if st.button("🗑️ Resetar Entrada dos Atletas"):
    os.remove(CSV_PATH)
    st.success("Arquivo resetado com sucesso!")
