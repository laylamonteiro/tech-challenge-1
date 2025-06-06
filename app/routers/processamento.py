from typing import List, Type

from sqlmodel import SQLModel
from fastapi import APIRouter, Depends

from app.auth import get_current_user
from app.db import get_session
from app.model.tables import Processamento
from app.routers.base_routers import BaseRouters


router = APIRouter(
    prefix="/processamento",
    tags=["processamento"],
    dependencies=[Depends(get_current_user)],
    responses={404: {"description": "Not found"}},
)

@router.post("/criar/")
def create_proc(proc: Processamento, session=Depends(get_session)) -> dict:
    return BaseRouters.create(proc, Processamento, session)

@router.patch("/atualizar/")
def update_proc(proc: Processamento, session=Depends(get_session)) -> Processamento:
    return BaseRouters.update(proc, Processamento, session)

@router.get("/obter/")
def get_proc(item_id: int, session=Depends(get_session)) -> Processamento:
    return BaseRouters.get(item_id, Processamento, session)

@router.delete("/excluir/")
def delete_proc(item_id: int, session=Depends(get_session)) -> dict:
    return BaseRouters.delete(item_id, Processamento, session)

@router.get("/processamento_por_ano/")
def get_proc_por_ano(ano: int, session=Depends(get_session)) -> List[Processamento]:
    return BaseRouters.get_by_field(ano, Processamento.ano, Processamento, session)

@router.get("/processamento_por_periodo/")
def get_proc_por_periodo(apos: int, ate: int, session=Depends(get_session)) -> List[Processamento]:
    return BaseRouters.filter_by_period(ate, apos, Processamento.ano, Processamento, session)

@router.get("/processamento_por_tipo/")
def get_proc_por_tipo(tipo: str, session=Depends(get_session)) -> List[Processamento]:
    return BaseRouters.get_by_field(tipo, Processamento.tipo, Processamento, session)
