from fastapi import APIRouter
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
router = APIRouter(prefix="/items", tags=["items"])


@router.get("/{item_id}", response_model=dict[str, int | str | None])
def read_item(item_id: int, q: str | None = None) -> dict[str, int | str | None]:
    logger.info("Reading item %s with query %s", item_id, q)
    return {"item_id": item_id, "q": q}