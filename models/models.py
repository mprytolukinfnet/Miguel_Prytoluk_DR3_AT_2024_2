from pydantic import BaseModel, Field
from typing import Literal

class MatchSummaryRequest(BaseModel):
    match_id: int = Field(...,
                          description="ID único da partida a ser sumarizada.")
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "match_id": 3895302
                }
            ]
        }
    }


class MatchSummaryResponse(BaseModel):
    match_id: int
    summary: str
    model_config = {
        "json_schema_extra": {
            "examples": [
                {'match_id': 3895302,
                 'summary': 'O Bayer Leverkusen venceu o Werder Bremen por 5 a 0. Os destaques foram os gols de Victor Okoh Boniface aos 24 minutos (pênalti), e quatro gols de Florian Wirtz aos 59, 67, 82 e 89 minutos, sendo que o primeiro contou com uma assistência de Victor Okoh Boniface, o segundo teve assistência de Robert Andrich, o terceiro foi assistido por Exequiel Alejandro Palacios, e o último por Alejandro Grimaldo García. \n\nAlém dos gols, Leonardo Bittencourt (Werder Bremen) e Piero Martín Hincapié Reyna (Bayer Leverkusen) receberam cartões amarelos aos 46 minutos. No total, o Bayer Leverkusen fez cinco substituições, enquanto o Werder Bremen fez três ao longo da partida.'}
            ]
        }
    }


class PlayerProfileRequest(BaseModel):
    match_id: int = Field(..., description="ID único da partida.")
    player_id: int = Field(..., description="ID único do jogador.")
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "match_id": 3895302,
                    "player_id": 40724
                }
            ]
        }
    }


class PlayerProfileResponse(BaseModel):
    match_id: int
    player_id: int
    player_name: str
    profile: dict
    model_config = {
        "json_schema_extra": {
            "examples": [
                {'match_id': 3895302,
                 'player_id': 40724,
                 'player_name': 'Florian Wirtz',
                 'profile': {'Gols': 3,
                             'Assistências': 0,
                             'Chutes': 5,
                             'Finalizações-Gol (%)': 60.0,
                             'Passes': 27,
                             'Passes-Sucesso (%)': 92.6,
                             'Dribles': 3,
                             'Dribles-Sucesso (%)': 33.3,
                             'Recepções': 37,
                             'Recepções-Sucesso (%)': 86.5,
                             'Interceptações': 2,
                             'Interceptações-Sucesso (%)': 0.0}}
            ]
        }
    }


class MatchNarrativeRequest(BaseModel):
    match_id: int = Field(..., description="ID único da partida.")
    style: Literal["formal", "humoristico",
                   "tecnico"] = Field(..., description="Estilo da narrativa.")
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "match_id": 3895302,
                    "style": 'humoristico'
                }
            ]
        }
    }


class MatchNarrativeResponse(BaseModel):
    match_id: int
    style: str
    narrative: str
    model_config = {
        "json_schema_extra": {
            "examples": [
                {'match_id': 3895302,
                 'style': 'humoristico',
                 'narrative': 'Em uma tarde ensolarada na Alemanha, o Bayer Leverkusen recebeu o Werder Bremen em um duelo que mais parecia uma aula de futebol sobre como não se deve defender. O jogo começou com o Werder Bremen prometendo que ia dar trabalho, mas o único trabalho que eles realmente deram foi para o goleiro do Leverkusen, que teve mais tempo livre do que um funcionário público em dia de feriado.\n\nLogo aos 21 minutos, o Werder Bremen conseguiu a proeza de ganhar um pênalti! O defensor Julián Malatini fez uma falta que parecia mais uma tentativa de dança do que uma jogada de futebol. Victor Okoh Boniface, com a calma de um cirurgião, foi lá e converteu a penalidade aos 24 minutos, colocando o Leverkusen em vantagem. E a partir daí, a festa só começou!\n\nO Leverkusen resolveu que marcar só um gol não era suficiente e, no segundo tempo, decidiu fazer uma verdadeira "festa do gol". Granit Xhaka, com um chute digno de um filme de ação, colocou o segundo aos 59 minutos. O que veio a seguir foi um show de Florian Wirtz, que fez um hat-trick em menos de meia hora, como se estivesse competindo por um prêmio de "Melhor Atacante do Mês". Ele marcou aos 67, 82 e 89 minutos, fazendo os defensores do Werder parecerem mais estátuas do que jogadores de futebol.\n\nEnquanto isso, o Werder Bremen tentava se reforçar com substituições, mas parecia que estavam mais preocupados em não serem o próximo alvo de uma piada do que em realmente voltar para o jogo. E, para completar a comédia, Leonardo Bittencourt e Piero Hincapié Reyna decidiram receber cartões amarelos aos 46 minutos, como se estivessem competindo para ver quem conseguia mais cartões na temporada.\n\nNo final do dia, o Bayer Leverkusen saiu vitorioso por 5 a 0, deixando o Werder Bremen pensando que talvez uma partida de xadrez fosse uma escolha mais sábia para a próxima vez. Afinal, pelo menos lá eles podem pensar um pouco antes de fazer movimentos!'}
            ]
        }
    }
