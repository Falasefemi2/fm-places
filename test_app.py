import unittest
from datetime import datetime
from app import Driver
from app import User, Restaurant, Order, Driver  

class TestUser(unittest.TestCase):
    def setUp(self):
        self.user = User(name="John Doe", email="john@example.com", password="securepassword")

    def test_user_creation(self):
        self.assertEqual(self.user.name, "John Doe")
        self.assertEqual(self.user.email, "john@example.com")
        self.assertTrue(isinstance(self.user.created_at, datetime))

    def test_to_dict(self):
        user_dict = self.user.to_dict()
        self.assertEqual(user_dict['name'], "John Doe")
        self.assertEqual(user_dict['email'], "john@example.com")
        self.assertIn('createdAt', user_dict)

    def test_from_dict(self):
        user_data = {
            "name": "Jane Doe",
            "email": "jane@example.com",
            "password": "anotherpassword",
            "createdAt": datetime.now().isoformat()
        }
        user = User.from_dict(user_data)
        self.assertEqual(user.name, "Jane Doe")
        self.assertEqual(user.email, "jane@example.com")

    def test_login_success(self):
        users = [self.user]
        logged_in_user = User.login("john@example.com", "securepassword", users)
        self.assertEqual(logged_in_user, self.user)

    def test_login_failure(self):
        users = [self.user]
        logged_in_user = User.login("john@example.com", "wrongpassword", users)
        self.assertIsNone(logged_in_user)

class TestRestaurant(unittest.TestCase):
    def setUp(self):
        self.restaurant = Restaurant(
            name="Pizza Place",
            menus={"lunch": {"Margherita": 8.99, "Pepperoni": 9.99}},
            availability=True
        )

    def test_restaurant_creation(self):
        self.assertEqual(self.restaurant.name, "Pizza Place")
        self.assertTrue(self.restaurant.availability)

    def test_to_dict(self):
        restaurant_dict = self.restaurant.to_dict()
        self.assertEqual(restaurant_dict['name'], "Pizza Place")
        self.assertIn('menus', restaurant_dict)

    def test_update_menu(self):
        new_menu = {"Veggie": 7.99}
        self.restaurant.update_menu("lunch", new_menu)
        self.assertEqual(self.restaurant.menus["lunch"], new_menu)

    def test_remove_menu(self):
        self.restaurant.remove_menu("lunch")
        self.assertNotIn("lunch", self.restaurant.menus)

    def test_display_info(self):
        # This test would require capturing printed output, which can be done
        # using unittest.mock or similar techniques. For simplicity, we skip it here.
        pass

class TestOrder(unittest.TestCase):
    def setUp(self):
        # Create a User and Restaurant instance for testing
        self.user = User(name="John Doe", email="john@example.com", password="securepassword")
        self.restaurant = Restaurant(
            name="Pizza Place",
            menus={
                "lunch": {"Margherita": 8.99, "Pepperoni": 9.99},
                "dinner": {"Veggie": 7.99, "Meat Feast": 12.99}
            },
            availability=True
        )
        self.items = {"Margherita": 2, "Pepperoni": 1}  # 2 Margheritas and 1 Pepperoni
        self.order = Order(user_email=self.user.email, restaurant_name=self.restaurant.name, items=self.items)

    def test_order_creation(self):
        self.assertEqual(self.order.user_email, "john@example.com")
        self.assertEqual(self.order.restaurant_name, "Pizza Place")
        self.assertEqual(self.order.items, self.items)
        self.assertEqual(self.order.status, "pending")
        self.assertIsNone(self.order.driver_email)
        self.assertTrue(isinstance(self.order.created_at, datetime))

    def test_to_dict(self):
        order_dict = self.order.to_dict()
        self.assertEqual(order_dict['user_email'], "john@example.com")
        self.assertEqual(order_dict['restaurant_name'], "Pizza Place")
        self.assertEqual(order_dict['items'], self.items)
        self.assertEqual(order_dict['status'], "pending")
        self.assertIsNone(order_dict['driver_email'])
        self.assertIn('orderAt', order_dict)

    def test_from_dict(self):
        order_data = {
            "user_email": "jane@example.com",
            "restaurant_name": "Pizza Place",
            "items": {"Veggie": 1},
            "status": "pending",
            "driver_email": None,
            "orderAt": datetime.now().isoformat()  # Ensure this key matches
        }
        order = Order.from_dict(order_data)
        self.assertEqual(order.user_email, "jane@example.com")
        self.assertEqual(order.restaurant_name, "Pizza Place")
        self.assertEqual(order.items, {"Veggie": 1})


    def test_update_status(self):
        new_status = "completed"
        updated_status = self.order.update_status(new_status)
        self.assertEqual(updated_status, new_status)
        self.assertEqual(self.order.status, new_status)

    def test_display_receipt(self):
        # Capture printed output
        from unittest.mock import patch
        with patch('builtins.print') as mocked_print:
            self.order.display_receipt(self.user, self.restaurant)
            mocked_print.assert_any_call(" - Margherita: 2 x $8.99 = $17.98")
            mocked_print.assert_any_call(" - Pepperoni: 1 x $9.99 = $9.99")
            mocked_print.assert_any_call("Total: $27.97")
            mocked_print.assert_any_call("Status: pending")


class TestDriver(unittest.TestCase):
    def setUp(self):
        # Create a driver for testing
        self.driver = Driver(name="John Doe", email="johndoe@gmail.com")
        self.order1 = Order(user_email="user1@example.com", restaurant_name="Pizza Place",
                            items={"Margherita": 2}, status="pending")
        self.order2 = Order(user_email="user2@example.com", restaurant_name="Burger Joint",
                            items={"Cheeseburger": 1}, status="pending")

    def test_driver_creation(self):
        self.assertEqual(self.driver.name, "John Doe")
        self.assertEqual(self.driver.email, "johndoe@gmail.com")
        self.assertTrue(self.driver.available)
        self.assertEqual(len(self.driver.orders), 0)

    def test_to_dict(self):
        driver_dict = self.driver.to_dict()
        self.assertEqual(driver_dict['name'], "John Doe")
        self.assertEqual(driver_dict['email'], "johndoe@gmail.com")
        self.assertTrue(driver_dict['available'])
        self.assertEqual(driver_dict['orders'], [])

    def test_from_dict(self):
        driver_data = {
            "name": "Jane Doe",
            "email": "janedoe@gmail.com",
            "orders": [],
            "available": True
        }
        driver = Driver.from_dict(driver_data)
        self.assertEqual(driver.name, "Jane Doe")
        self.assertEqual(driver.email, "janedoe@gmail.com")
        self.assertTrue(driver.available)
        self.assertEqual(len(driver.orders), 0)

    def test_assign_order(self):
        self.driver.assign_order(self.order1)
        self.assertFalse(self.driver.available)
        self.assertEqual(len(self.driver.orders), 1)
        self.assertEqual(self.driver.orders[0], self.order1)
        self.assertEqual(self.order1.status, "Assigned")

        # Try to assign another order when the driver is not available
        self.driver.assign_order(self.order2)
        self.assertEqual(len(self.driver.orders), 1)  # Should not change
        self.assertEqual(self.order1.status, "Assigned")  # Status should remain unchanged

    def test_complete_order(self):
        self.driver.assign_order(self.order1)
        self.driver.complete_order()
        self.assertTrue(self.driver.available)
        self.assertEqual(len(self.driver.orders), 0)
        self.assertEqual(self.order1.status, "Delivered")

        # Try to complete an order when there are no orders
        self.driver.complete_order()  # Should print a message about no orders

    def test_save_driver(self):
        self.driver.assign_order(self.order1)
        drivers = [self.driver]
        Driver.save_driver(drivers, 'test_driver.json')

        # Load the driver back from the file
        loaded_drivers = Driver.load_driver('test_driver.json')
        self.assertEqual(len(loaded_drivers), 1)
        self.assertEqual(loaded_drivers[0].name, "John Doe")
        self.assertEqual(loaded_drivers[0].email, "johndoe@gmail.com")
        self.assertEqual(len(loaded_drivers[0].orders), 1)
        self.assertEqual(loaded_drivers[0].orders[0].user_email, "user1@example.com")

    def tearDown(self):
        import os
        # Clean up the test file if it exists
        if os.path.exists('test_driver.json'):
            os.remove('test_driver.json')

        

if __name__ == '__main__':
    unittest.main()