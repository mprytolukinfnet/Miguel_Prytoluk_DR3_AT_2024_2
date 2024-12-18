from langchain.agents import Tool
from langchain_core.tools import tool
import numpy as np

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
        def calcular_percentual(eventos, tipo, coluna_resultado, valor_sucesso):
            """Calcula o percentual de sucesso para um tipo específico de evento."""
            eventos_tipo = eventos[eventos['type'] == tipo]
            contagem_resultados = eventos_tipo[coluna_resultado].value_counts(dropna=False)
            if len(contagem_resultados) > 0:
                return round(contagem_resultados.get(valor_sucesso, 0) / contagem_resultados.sum() * 100, 1)
            return 0.0
        
        # Filtra os eventos do jogador
        dados_jogador = eventos[eventos['player'] == jogador]
        
        return {
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

    return resumo_jogador
