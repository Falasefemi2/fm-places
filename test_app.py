import unittest
from datetime import datetime
from app import Order

class TestOrder(unittest.TestCase):
    def setUp(self):
        self.order_data = {
            "user_email": "test@example.com",
            "restaurant_name": "Test Restaurant",
            "items": {"burger": 2, "fries": 1},
            "status": "Pending",
            "driver_email": "driver@example.com",
            "created_at": datetime.now().isoformat(),
        }
        self.order = Order(
            user_email=self.order_data["user_email"],
            restaurant_name=self.order_data["restaurant_name"],
            items=self.order_data["items"],
            status=self.order_data["status"],
            driver_email=self.order_data["driver_email"]
        )

    def test_order_initialization(self):
        self.assertEqual(self.order.user_email, self.order_data["user_email"])
        self.assertEqual(self.order.restaurant_name, self.order_data["restaurant_name"])
        self.assertEqual(self.order.items, self.order_data["items"])
        self.assertEqual(self.order.status, self.order_data["status"])
        self.assertEqual(self.order.driver_email, self.order_data["driver_email"])
        self.assertIsInstance(self.order.created_at, datetime)

    def test_order_to_dict(self):
        order_dict = self.order.to_dict()
        self.assertEqual(order_dict["user_email"], self.order_data["user_email"])
        self.assertEqual(order_dict["restaurant_name"], self.order_data["restaurant_name"])
        self.assertEqual(order_dict["items"], self.order_data["items"])
        self.assertEqual(order_dict["status"], self.order_data["status"])
        self.assertEqual(order_dict["driver_email"], self.order_data["driver_email"])
        self.assertEqual(order_dict["created_at"], self.order_data["created_at"])

    def test_order_from_dict(self):
        order_from_dict = Order.from_dict(self.order_data)
        self.assertEqual(order_from_dict.user_email, self.order_data["user_email"])
        self.assertEqual(order_from_dict.restaurant_name, self.order_data["restaurant_name"])
        self.assertEqual(order_from_dict.items, self.order_data["items"])
        self.assertEqual(order_from_dict.status, self.order_data["status"])
        self.assertEqual(order_from_dict.driver_email, self.order_data["driver_email"])
        self.assertIsInstance(order_from_dict.created_at, datetime)

if __name__ == "__main__":
    unittest.main()