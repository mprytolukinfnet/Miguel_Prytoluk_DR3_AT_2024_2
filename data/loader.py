import streamlit as st
from statsbombpy import sb
import pandas as pd
import numpy as np

state = st.session_state

def clear_data():
    for prop in ['agent', 'messages', 'jogador_0_persist', 'jogador_1_persist']:
        if prop in state:
            del state[prop]

def get_position(positions, prop):
    extracted = [item[prop] for item in positions]
    return np.nan if len(extracted) == 0 else extracted[0]

def get_lineup(lineup):
    lineup['position'] = lineup.positions.apply(lambda x: get_position(x, 'position'))
    lineup['position_id'] = lineup.positions.apply(lambda x: get_position(x, 'position_id'))
    lineup = lineup[['player_name', 'position', 'position_id', 'jersey_number']].dropna().sort_values('position_id').drop('position_id', axis=1)
    return lineup

@st.cache_data
def load_competitions():
    """Carrega todas as competições disponíveis."""
    return sb.competitions()

@st.cache_data
def load_matches(competicao_id, season_id):
    """Carrega as partidas da competição selecionada"""
    return sb.matches(competition_id=competicao_id, season_id = season_id)

@st.cache_data
def load_match_events(match_id):
    match_events = sb.events(match_id=match_id)
    match_events['timestamp'] = pd.to_datetime(match_events['timestamp'], format='%H:%M:%S.%f').dt.time 
    return match_events

def carregar_competicao_temporada_partida():
    '''
    Seleciona a Competição, a Temporada e a Partida com base na opção do usuário.
    Retorna:
        (partida_selecionada, dados_partida, temporada_ano)
    '''
    progresso = st.progress(0)
    with st.spinner('Carregando dados...'):
        # Seletor de competição
        competicoes = load_competitions()
        competicoes_df = pd.DataFrame(competicoes)
        state['competicao_nome'] = st.sidebar.selectbox(
            'Selecione uma competição', competicoes_df['competition_name'].unique(), on_change=clear_data
        )
        competicao = competicoes_df[competicoes_df['competition_name'] == state['competicao_nome']].iloc[0]

        progresso.progress(33)

        # Seletor de temporada
        temporadas = competicoes_df[competicoes_df['competition_id'] == competicao['competition_id']]
        state['temporada_ano'] = st.sidebar.selectbox(
            'Selecione uma temporada', temporadas['season_name'].unique(), on_change=clear_data
        )
        temporada = temporadas[temporadas['season_name'] == state['temporada_ano']].iloc[0]

        progresso.progress(66)

        # Seletor de partida
        partidas = load_matches(competicao['competition_id'], temporada['season_id'])
        partidas_df = pd.DataFrame(partidas).sort_values(['home_team', 'away_team', 'match_date'])

        def get_match_title(match_id):
            p = partidas_df[partidas_df.match_id == match_id].iloc[0]
            return f"{p['home_team']} x {p['away_team']} ({p['match_date']})"

        partida_id = st.sidebar.selectbox(
            'Selecione uma partida', partidas_df['match_id'].unique(), format_func=get_match_title, on_change=clear_data
        )
        partida_selecionada = partidas_df[partidas_df.match_id == partida_id].iloc[0]

        # Carregar os dados da partida selecionada
        dados_partida = load_match_events(partida_id)

        lineups = sb.lineups(partida_id)
        home_team, away_team = partida_selecionada.home_team, partida_selecionada.away_team
        lineups[home_team] = get_lineup(lineups[home_team])
        lineups[away_team] = get_lineup(lineups[away_team])

        descricao_partida = f"{home_team} ({partida_selecionada.home_score}) x {away_team} ({partida_selecionada.away_score})\n"+\
        f"**Competição:** {state['competicao_nome']}\n"+\
        f"**Temporada:** {state['temporada_ano']}\n"+\
        f"**Data:** {partida_selecionada.match_date}\n"

        progresso.progress(100)

    progresso.empty()

    return partida_selecionada, partida_id, dados_partida, lineups, descricao_partida
