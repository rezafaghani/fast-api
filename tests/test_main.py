from decimal import Decimal
from unittest import TestCase

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from fast_api.database import Base
from fast_api.routers.health import health
from fast_api.routers.items import (
    create_item,
    delete_item,
    list_items,
    read_item,
    update_item,
)
from fast_api.schemas import ItemCreate, ItemUpdate


class ApiTests(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.engine = create_engine(
            "sqlite://",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        Base.metadata.create_all(cls.engine)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.engine.dispose()

    def setUp(self) -> None:
        self.db = Session(self.engine)

    def tearDown(self) -> None:
        self.db.rollback()
        for table in reversed(Base.metadata.sorted_tables):
            self.db.execute(table.delete())
        self.db.commit()
        self.db.close()

    def test_health(self) -> None:
        self.assertEqual(health(), {"status": "ok"})

    def test_item_crud(self) -> None:
        item = create_item(
            ItemCreate(name="Keyboard", description="Mechanical", price="99.90"),
            self.db,
        )

        self.assertEqual(read_item(item.id, self.db).name, "Keyboard")
        self.assertEqual(list_items(self.db, 0, 20), [item])

        updated = update_item(
            item.id,
            ItemUpdate(name="Quiet keyboard", price=Decimal("89.90")),
            self.db,
        )
        self.assertEqual(updated.name, "Quiet keyboard")
        self.assertEqual(updated.price, Decimal("89.90"))

        response = delete_item(item.id, self.db)
        self.assertEqual(response.status_code, 204)
        self.assertIsNone(self.db.get(type(item), item.id))
