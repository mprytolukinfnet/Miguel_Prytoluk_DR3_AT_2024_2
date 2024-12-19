from agent.agent import Agent
from data.loader import get_matches_dict, load_match_events, get_lineups, get_descricao_partida, get_partida_selecionada, get_resumo_jogador

# Inicialização dos dados de competição e temporada por partida
matches_dict = get_matches_dict()

def prompt_agent(match_id, prompt):
    """
    Função auxiliar para interagir com o agente de chat.
    """
    partida_selecionada = get_partida_selecionada(match_id, matches_dict)
    agent = Agent(load_match_events(match_id), get_lineups(
        match_id), get_descricao_partida(partida_selecionada)).create_agent()
    input = {"messages": [("user", prompt)]}
    config = {"configurable": {"thread_id": "thread-1"}}
    response = agent.invoke(input, config)['messages']
    # Você pode fazer o Debug da resposta do agente aqui:
    # print(response, "\n\n")
    response = response[-1].content
    return response


def get_match_summary(match_id: int) -> str:
    """
    Retorna uma sumarização da partida.
    """
    prompt = "Gere um resumo da partida."
    response = prompt_agent(match_id, prompt)
    return response


def get_player_profile(match_id: int, player_id: int) -> dict:
    """
    Retorna um perfil do jogador.
    """
    eventos = load_match_events(match_id)
    dados_jogador = eventos[eventos['player_id'] == player_id]
    nome_jogador = dados_jogador.head(1).player.iloc[0]
    profile = get_resumo_jogador(dados_jogador)
    return nome_jogador, profile


def get_match_narrative(match_id: int, style: str) -> str:
    """
    Retorna uma narrativa da partida com base no estilo selecionado.
    """
    match style:
        case "formal" | "humoristico" | "tecnico":
            prompt = f"Crie uma narrativa da partida em estilo {style}."
            response = prompt_agent(match_id, prompt)
            return response
        case _:
            raise ValueError("Estilo de narrativa inválido.")
