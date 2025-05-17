from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from betai.models import calc_edge
from betai.allocator import allocate_bank

app = FastAPI(
    title="BetAI API",
    description="API для расчета преимущества (edge) и распределения банка для ставок",
    version="0.1.0",
)

class BetInput(BaseModel):
    fixture_id: int = Field(..., description="ID матча")
    team_id: int = Field(..., description="ID команды")
    market: str = Field(..., description="Тип рынка (например, 'Match Winner')")
    k_dec: float = Field(..., description="Десятичный коэффициент букмекера")
    p_model: float = Field(..., ge=0, le=1, description="Вероятность исхода по модели (от 0 до 1)")
    description: Optional[str] = Field(None, description="Описание ставки")

class EdgeResponse(BaseModel):
    fixture_id: int
    team_id: int
    market: str
    k_dec: float
    p_model: float
    edge: float
    description: Optional[str] = None

class AllocateInput(BaseModel):
    bets: List[Dict[str, Any]] = Field(..., description="Список ставок с рассчитанным edge")
    bank: float = Field(..., gt=0, description="Размер банка")
    fraction_multiplier: float = Field(0.5, gt=0, le=1, description="Множитель доли Келли")
    max_total_risk: float = Field(0.1, gt=0, le=1, description="Максимальный общий риск")

@app.post("/edges", response_model=List[EdgeResponse])
async def calculate_edges(bets: List[BetInput]):
    """
    Рассчитывает edge (преимущество) для списка ставок
    """
    results = []
    for bet in bets:
        edge = calc_edge(bet.k_dec, bet.p_model)
        results.append(
            EdgeResponse(
                fixture_id=bet.fixture_id,
                team_id=bet.team_id,
                market=bet.market,
                k_dec=bet.k_dec,
                p_model=bet.p_model,
                edge=edge,
                description=bet.description
            )
        )
    return results

@app.post("/allocate")
async def allocate_bets(input_data: AllocateInput):
    """
    Распределяет банк между ставками, используя модифицированный критерий Келли
    с ограничением общего риска
    """
    try:
        result = allocate_bank(
            input_data.bets,
            input_data.bank,
            input_data.fraction_multiplier,
            input_data.max_total_risk
        )
        return {"bets": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
