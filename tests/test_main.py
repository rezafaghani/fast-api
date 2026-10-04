from unittest import TestCase

from fast_api.routers.health import health
from fast_api.routers.items import read_item


class ApiTests(TestCase):
    def test_health(self) -> None:
        self.assertEqual(health(), {"status": "ok"})

    def test_read_item(self) -> None:
        self.assertEqual(read_item(42, "example"), {"item_id": 42, "q": "example"})
