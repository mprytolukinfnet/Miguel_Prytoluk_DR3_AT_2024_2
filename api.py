from fastapi import FastAPI, HTTPException
from models.models import MatchSummaryRequest, MatchSummaryResponse, PlayerProfileRequest, PlayerProfileResponse, MatchNarrativeRequest, MatchNarrativeResponse
from controllers.controllers import get_match_summary, get_player_profile, get_match_narrative

# Inicialização da API
app = FastAPI(title="Futebol Insights API",
              description="API para análise e narrativas de partidas de futebol.")

# Endpoints
@app.post("/match_summary", response_model=MatchSummaryResponse)
async def match_summary(request: MatchSummaryRequest):
    """
    Retorna uma sumarização de uma partida baseada no match_id.
    """
    match_id = request.match_id

    try:
        summary = get_match_summary(match_id)
        return {"match_id": match_id, "summary": summary}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao gerar sumarização: {str(e)}")


@app.post("/player_profile", response_model=PlayerProfileResponse)
async def player_profile(request: PlayerProfileRequest):
    """
    Retorna o perfil detalhado de um jogador com base no match_id e player_id.
    """
    match_id = request.match_id
    player_id = request.player_id

    try:
        nome_jogador, profile = get_player_profile(match_id, player_id)
        return {"match_id": match_id, "player_id": player_id, "player_name": nome_jogador, "profile": profile}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao obter perfil do jogador: {str(e)}")


@app.post("/match_narrative", response_model=MatchNarrativeResponse)
async def match_narrative(request: MatchNarrativeRequest):
    """
    Retorna uma narrativa personalizada com base nos eventos da partida e no estilo selecionado.
    Valores aceitos para estilo: "formal", "humoristico" e "tecnico".
    """
    match_id = request.match_id
    style = request.style

    try:
        narrative = get_match_narrative(match_id, style)
        return {"match_id": match_id, "style": style, "narrative": narrative}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao gerar narrativa: {str(e)}")
