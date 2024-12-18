import streamlit as st
import plotly.express as px

# Função para selecionar a cor da métrica da partida de acordo com parâmetros
def select_color(n, min_n, max_n):
    # n == métrica
    # min_n == valor mínimo esperado
    # max_n == valor máximo esperado
    colors = px.colors.sequential.Oranges
    color_position = max(min(int(8 * (n - min_n) / (max_n - min_n)), 8), 0)
    return colors[color_position]

@st.cache_data
def metricas_eventos_partida(partida_selecionada, dados_partida, lineups):
    # Exibir informações básicas
    home_team, away_team = partida_selecionada.home_team, partida_selecionada.away_team
    st.subheader(
        f"{home_team} ({partida_selecionada.home_score}) x {away_team} ({partida_selecionada.away_score})"
    )
    match_col1, match_col2, match_col3 = st.columns(3)
    with match_col1:
        st.write(f"**Competição:** {st.session_state['competicao_nome']}")
    with match_col2:
        st.write(f"**Temporada:** {st.session_state['temporada_ano']}")
    with match_col3:
        st.write(f"**Data:** {partida_selecionada.match_date}")
    num_gols_partida = partida_selecionada.home_score + partida_selecionada.away_score
    num_chutes_partida = len(dados_partida[dados_partida.type == "Shot"])
    num_passes_partida = len(dados_partida[dados_partida.type == "Pass"])

    # Aplicar cores às métricas de acordo com o valor
    cores_metricas = f"""
    <style>
    .eiemyj2:nth-of-type(1) > div > div > div > div > div > div > div {{
    color: {select_color(num_gols_partida, 0, 10)};
    }}

    .eiemyj2:nth-of-type(2) > div > div > div > div > div > div > div {{
    color: {select_color(num_chutes_partida, 10, 50)};
    }}

    .eiemyj2:nth-of-type(3) > div > div > div > div > div > div > div {{
    color: {select_color(num_passes_partida, 1000, 1500)};
    }}

    </style>
    """
    st.markdown(cores_metricas, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("**Gols**", num_gols_partida)
    with col2:
        st.metric("**Chutes:**", num_chutes_partida)
    with col3:
        st.metric("**Passes:**", num_passes_partida)

    st.subheader("Lista de jogadores:")
    escalacao_cols = st.columns(2)
    for team_idx, team in enumerate((home_team, away_team)):
        with escalacao_cols[team_idx]:
            st.markdown(f"**{team}**")
            lineup = lineups[team]
            for idx, col in lineup.iterrows():
                st.write(f'{col.jersey_number}: {col.player_name} - {col.position}')

def mostrar_eventos(evento_selecionado, eventos):
    match evento_selecionado:
        case 'Substituições':
            eventos_filtrados = eventos[eventos.type == 'Substitution'][['minute', 'period', 'player', 'substitution_replacement', 'team']]
        case 'Pênaltis':
            eventos_filtrados = eventos[eventos['foul_committed_penalty'] == True] if 'foul_committed_penalty' in eventos else []
        case 'Assistências':
            eventos_filtrados = eventos[eventos['pass_goal_assist'] == True].dropna(axis=1) if 'pass_goal_assist' in eventos else []
        case 'Gols':
            eventos_filtrados = eventos[eventos['shot_outcome'] == 'Goal'].dropna(axis=1)
        case 'Cartões':
            eventos_filtrados = eventos[~eventos.bad_behaviour_card.isna()].dropna(axis=1) if 'bad_behaviour_card' in eventos else []
        case "Chutes":
            eventos_filtrados = eventos[eventos['type'] == "Shot"].dropna(axis=1)
        case "Passes":
            eventos_filtrados = eventos[eventos['type'] == "Pass"].dropna(axis=1)
        case "Dribles":
            eventos_filtrados = eventos[eventos['type'] == "Dribble"].dropna(axis=1)
        case "Recepções":
            eventos_filtrados = eventos[eventos['type'] == "Ball Receipt*"].dropna(axis=1)
        case "Interceptações":
            eventos_filtrados = eventos[eventos['type'] == "Interception"].dropna(axis=1)
    
    st.subheader(f"Visualização de {evento_selecionado}:")
    st.dataframe(eventos_filtrados)

state = st.session_state

event_options = ["Gols", "Assistências","Substituições", "Cartões", "Pênaltis", "Chutes", "Passes", "Dribles", "Recepções", "Interceptações"]
if 'evento_selecionado' not in state and 'evento_selecionado_persist' in state:
    state.evento_selecionado = state.evento_selecionado_persist
st.sidebar.selectbox(f'Selecione o  evento a ser visualizado', options = event_options, key='evento_selecionado')
state.evento_selecionado_persist = state.evento_selecionado

if state.selected_match is not None:
    metricas_eventos_partida(state.selected_match, state.match_events, state.lineups)
    mostrar_eventos(state.evento_selecionado, state.match_events)
