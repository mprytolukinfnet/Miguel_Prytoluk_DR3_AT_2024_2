from langchain_core.tools import tool
import numpy as np
from data.loader import get_resumo_jogador

def create_consultar_eventos(eventos):
    @tool
    def consultar_eventos(tipo_eventos: str):
        """
        Consulta eventos específicos da partida. Escolha um tipo de eventos como "passes", "chutes" ou "faltas".
        """
        # Filtragem baseada no tipo de eventos solicitados na partida
        filtro_eventos = tipo_eventos.lower()
        if "pass" in filtro_eventos:
            filtrados = eventos[eventos['type'] == "Pass"]
        elif "chute" in filtro_eventos or "shot" in filtro_eventos or "finaliza" in filtro_eventos:
            filtrados = eventos[eventos['type'] == "Shot"]
        elif "falta" in filtro_eventos:
            filtrados = eventos[eventos['type'] == 'Foul Committed']
        else:
            return "Tipo de evento não identificado. Tente 'passes' ou 'chutes'."
        
        # Resumindo os dados para exibição
        resumo = filtrados[['minute', 'period', 'player', 'team']]
        return resumo.to_string(index=False)
    return consultar_eventos

def create_principais_eventos_partidas(eventos):
    @tool
    def principais_eventos_partida():
        """
        Retorna os principais eventos da partida: Substituições, Pênaltis, Assistências, Gols e Cartões.
        """
        substituicoes = eventos[eventos.type == 'Substitution'][['minute', 'period', 'player', 'substitution_replacement', 'team']]
        penaltis = eventos[eventos['foul_committed_penalty'] == True][['minute', 'period', 'player', 'team']] if 'foul_committed_penalty' in eventos else []
        assistencias = eventos[eventos['pass_goal_assist'] == True][['minute', 'period', 'player', 'team']] if 'pass_goal_assist' in eventos else []
        gols = eventos[eventos['shot_outcome'] == 'Goal'][['minute', 'period', 'player', 'team', 'shot_body_part', 'shot_type']]
        cartoes = eventos[~eventos.bad_behaviour_card.isna()][["bad_behaviour_card", "minute", "period", "player", "team"]] if 'bad_behaviour_card' in eventos else []
        
        return {
            "Substituições": substituicoes,
            "Cartões": cartoes,
            "Pênaltis": penaltis,
            "Gols": gols,
            "Assistências": assistencias,
        }

    return principais_eventos_partida

def create_resumo_jogador(eventos):
    @tool
    def resumo_jogador(jogador: str):
        """
        Retorna estatísticas detalhadas de um jogador da partida.
        Passe o nome do jogadores para ter suas estatísticas retornadas.
        """
        # Filtra os eventos do jogador
        dados_jogador = eventos[eventos['player'] == jogador]
        return get_resumo_jogador(dados_jogador)

    return resumo_jogador
