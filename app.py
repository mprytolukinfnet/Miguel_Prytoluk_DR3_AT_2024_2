import streamlit as st
from data.loader import carregar_competicao_temporada_partida

state = st.session_state

# Configurações iniciais
st.set_page_config(page_title="Assistente Interativo de Futebol ⚽", layout="wide")

st.title("Assistente Interativo de Futebol ⚽")
st.markdown(
    """
    Explore eventos específicos das partidas, compare jogadores e descubra insights únicos sobre jogos de futebol.
    """
)

# Seleção de Competição
st.sidebar.header("Configurações")
state.selected_match, state.partida_id, state.match_events, state.lineups, state.descricao_partida = carregar_competicao_temporada_partida()

pages = [
    st.Page("st_pages/partida.py", title="Dados da Partida"),
    st.Page("st_pages/chat_assistente.py", title="Chat com Assistente"),
    st.Page("st_pages/jogadores.py", title="Estatísticas Jogadores"),
]
pg = st.navigation(pages)
pg.run()
