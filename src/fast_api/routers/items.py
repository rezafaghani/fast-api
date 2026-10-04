import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_api.database import get_db
from fast_api.models import Item
from fast_api.schemas import ItemCreate, ItemRead, ItemUpdate

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/items", tags=["items"])
SessionDependency = Annotated[Session, Depends(get_db)]


def find_item(db: Session, item_id: int) -> Item:
    item = db.get(Item, item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


@router.post("/", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
def create_item(payload: ItemCreate, db: SessionDependency) -> Item:
    item = Item(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    logger.info("Created item %s", item.id)
    return item


@router.get("/", response_model=list[ItemRead])
def list_items(
    db: SessionDependency,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
) -> list[Item]:
    return list(db.scalars(select(Item).offset(offset).limit(limit)))


@router.get("/{item_id}", response_model=ItemRead)
def read_item(item_id: int, db: SessionDependency) -> Item:
    return find_item(db, item_id)


@router.patch("/{item_id}", response_model=ItemRead)
def update_item(item_id: int, payload: ItemUpdate, db: SessionDependency) -> Item:
    item = find_item(db, item_id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(item, field, value)
    db.commit()
    db.refresh(item)
    logger.info("Updated item %s", item.id)
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, db: SessionDependency) -> Response:
    item = find_item(db, item_id)
    db.delete(item)
    db.commit()
    logger.info("Deleted item %s", item.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
