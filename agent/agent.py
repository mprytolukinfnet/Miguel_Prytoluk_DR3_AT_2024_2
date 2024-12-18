from tools.soccer import create_consultar_eventos, create_resumo_jogador, create_principais_eventos_partidas
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
load_dotenv()


class Agent():
    # Configura o agente
    def __init__(self, events, lineups, descricao_partida) -> None:
        self.llm = ChatOpenAI(model="gpt-4o-mini")
        self.tools = [
            create_consultar_eventos(events),
            create_resumo_jogador(events),
            create_principais_eventos_partidas(events),
        ]

        for team in lineups.keys():
            t = lineups[team]
            t['player_full'] = t.player_name + '(' + t.position + ')'
            lineups[team] = t['player_full'].to_list()

        self.system_prompt = f"""Você é um especialista em futebol capaz interagir com os dados de uma partida de futebol.
A partida que você vai analisar é : {descricao_partida}
Você é capaz de:
- Consultar eventos específicos da partida.
- Geração de comparações entre jogadores.
- Consultar os principais eventos da partida.
- Gerar uma sumarização dos principais eventos da partida.
- Criar narrativas baseadas nos eventos da partida.
Você é capaz de responde perguntas como:
"Quem deu mais passes na partida?"
"Qual jogador teve mais finalizações no primeiro tempo?
A lista de jogadores da partida no formato "{{'Time1': ['Jogador1(Posição)','Jogador2(Posição)'], 'Time2': (...)}} é: {lineups}. Faça a consulta baseada na lista de jogadores existentes.
Corrija caso o usuário forneça um nome de jogador ligeiramente incorreto, mas se negue caso o jogador não esteja na lista.
Se for solicitado um resumo/sumarização da partida, consulte os principais eventos e forneça no formato: "O time A venceu o time B por 3 a 1. Os destaques foram os gols de João aos X minutos, e Lucas aos X minutos, além de uma assistência de Ana aos X minutos. Os jogadores X e Y receberam cartões amarelos. Fulano Entrou para substituir Cicrano."
Se for solicitado que crie narrativas baseadas nos eventos da partida, você pode criar em diferentes estilos, como Formal (técnico e objetivo), Humorístico (descontraído e criativo) ou Técnico (análise detalhada dos eventos).
"""

    # Cria o agente
    def create_agent(self):
        return create_react_agent(
            self.llm, tools=self.tools, state_modifier=self.system_prompt, checkpointer=MemorySaver())
