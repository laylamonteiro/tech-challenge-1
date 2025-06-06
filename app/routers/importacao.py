from typing import List, Type

from sqlmodel import SQLModel
from fastapi import APIRouter, Depends

from app.auth import get_current_user
from app.db import get_session
from app.model.tables import Importa
from app.routers.base_routers import BaseRouters


router = APIRouter(
    prefix="/importacao",
    tags=["importacao"],
    dependencies=[Depends(get_current_user)],
    responses={404: {"description": "Not found"}},
)

@router.post("/criar/")
def create_importa(importa: Importa, session=Depends(get_session)) -> dict:
    return BaseRouters.create(importa, Importa, session)

@router.patch("/atualizar/")
def update_importa(importa: Importa, session=Depends(get_session)) -> Importa:
    return BaseRouters.update(importa, Importa, session)

@router.get("/obter/")
def get_importa(item_id: int, session=Depends(get_session)) -> Importa:
    return BaseRouters.get(item_id, Importa, session)

@router.delete("/excluir/")
def delete_importa(item_id: int, session=Depends(get_session)) -> dict:
    return BaseRouters.delete(item_id, Importa, session)

@router.get("/importacao_por_ano")
def get_importa_por_ano(ano: str, session=Depends(get_session)) -> List[Importa]:
    return BaseRouters.get_by_field(ano, Importa.ano, Importa, session)

@router.get("/importacao_por_tipo")
def get_importa_por_tipo(tipo: str, session=Depends(get_session)) -> List[Importa]:
    return BaseRouters.get_by_field(tipo, Importa.tipo, Importa, session)
