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

def get_lineups(partida_id):
    lineups = sb.lineups(partida_id)
    for team in lineups.keys():
        lineups[team] = get_lineup(lineups[team])
    return lineups

def get_descricao_partida(partida_selecionada):
    descricao = f"{partida_selecionada.home_team} ({partida_selecionada.home_score}) x {partida_selecionada.away_team} ({partida_selecionada.away_score})\n"+\
    f"**Competição:** {partida_selecionada.competition}\n"+\
    f"**Temporada:** {partida_selecionada.season}\n"+\
    f"**Data:** {partida_selecionada.match_date}\n"
    return descricao

def get_matches_dict():
    competitions = sb.competitions()[['competition_id', 'season_id']]
    # for each competion/season_id in competition, get its matches and store it to a dict in the format match_id: {competition_id, season_id}:
    matches_dict = {}
    for i, comp_row in competitions.iterrows():
        competition_id = int(comp_row['competition_id'])
        season_id = int(comp_row['season_id'])
        matches = sb.matches(competition_id, season_id)
        for j, match_row in matches.iterrows():
            matches_dict[match_row['match_id']] = {'competition_id': competition_id, 'season_id': season_id}
    return matches_dict

def get_partida_selecionada(partida_id, matches_dict):
    match_data = matches_dict[partida_id]
    partidas_df = pd.DataFrame(sb.matches(match_data['competition_id'], match_data['season_id']))
    partida_selecionada = partidas_df[partidas_df.match_id == partida_id].iloc[0]
    return partida_selecionada

def get_resumo_jogador(dados_jogador: pd.DataFrame):
    """
    Retorna estatísticas detalhadas de um jogador da partida.
    Passe um DataFrame com os eventos do jogador para ter suas estatísticas retornadas.
    """
    def calcular_percentual(eventos, tipo, coluna_resultado, valor_sucesso):
        """Calcula o percentual de sucesso para um tipo específico de evento."""
        eventos_tipo = eventos[eventos['type'] == tipo]
        contagem_resultados = eventos_tipo[coluna_resultado].value_counts(dropna=False)
        if len(contagem_resultados) > 0:
            return round(contagem_resultados.get(valor_sucesso, 0) / contagem_resultados.sum() * 100, 1)
        return 0.0
    
    return {
        "Gols": len(dados_jogador[dados_jogador['shot_outcome'] == "Goal"]),
        "Assistências": len(dados_jogador[dados_jogador['pass_goal_assist'] == True]),
        "Chutes": len(dados_jogador[dados_jogador['type'] == "Shot"]),
        "Finalizações-Gol (%)": calcular_percentual(
            dados_jogador, "Shot", "shot_outcome", "Goal"
        ),
        "Passes": len(dados_jogador[dados_jogador['type'] == "Pass"]),
        "Passes-Sucesso (%)": calcular_percentual(
            dados_jogador, "Pass", "pass_outcome", np.nan
        ),
        "Dribles": len(dados_jogador[dados_jogador['type'] == "Dribble"]),
        "Dribles-Sucesso (%)": calcular_percentual(
            dados_jogador, "Dribble", "dribble_outcome", "Complete"
        ),
        "Recepções": len(dados_jogador[dados_jogador['type'] == "Ball Receipt*"]),
        "Recepções-Sucesso (%)": calcular_percentual(
            dados_jogador, "Ball Receipt*", "ball_receipt_outcome", np.nan
        ),
        "Interceptações": len(dados_jogador[dados_jogador['type'] == "Interception"]),
        "Interceptações-Sucesso (%)": calcular_percentual(
            dados_jogador, "Interception", "interception_outcome", "Won"
        ),
    }

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

        lineups = get_lineups(partida_id)


        descricao_partida = get_descricao_partida(partida_selecionada)

        progresso.progress(100)

    progresso.empty()

    return partida_selecionada, partida_id, dados_partida, lineups, descricao_partida
