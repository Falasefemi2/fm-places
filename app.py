import json
import bcrypt
from typing import Optional, List, Dict
from datetime import datetime


class User:
    """User Registration and Authentication"""
    def __init__(self, name: str, email: str, password: str, hashed: bool = False) -> None:
        self.name = name
        self.email = email
        if not hashed:
            self.password = self.hash_password(password)
        else:
            self.password = password
        self.created_at = datetime.now()


    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using bcrypt"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode(), salt).decode()

    def check_password(self, password: str) -> bool:
        """Verify password"""
        return bcrypt.checkpw(password.encode(), self.password.encode())

    def to_dict(self) -> Dict:
        """Convert user to dictionary for JSON serialization"""
        return {
            "name": self.name,
            "email": self.email,
            "password": self.password,  # This is the hashed password
            "created_at": self.created_at.isoformat()
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'User':
        """Create user from dictionary without re-hashing the already hashed password"""
        # We pass hashed=True so the _init_ knows the password is already hashed
        user = cls(data['name'], data['email'], data['password'], hashed=True)
        user.created_at = datetime.fromisoformat(data['created_at'])
        return user

    @staticmethod
    def login(email: str, password: str, users: List['User']) -> Optional['User']:
        """Authenticate user login"""
        if not users:
            raise ValueError("No users available")
        if not email or not password:
            raise ValueError('Email and password are required')

        for user in users:
            if user.email == email and user.check_password(password):
                return user
        return None


    @staticmethod
    def save_users(users: List['User'], filename: str = 'users.json') -> None:
        """Save users to JSON file"""
        with open(filename, 'w', encoding="utf-8") as f:
            json.dump([user.to_dict() for user in users], f, indent=4)

    @staticmethod
    def load_users(filename: str = 'users.json') -> List['User']:
        """Load users from JSON file"""
        try:
            with open(filename, 'r', encoding="utf-8") as f:
                user_data = json.load(f)
                return [User.from_dict(data) for data in user_data]
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            print("Error: Corrupted users.json file")
            return []


class Restaurant:
    """Registration for restaurants"""

    def __init__(self, name: str, menus: Dict[str, Dict[str, float]], availability: bool = True) -> None:
        self.name = name
        self.menus = menus  # e.g., {"breakfast": {"Pancakes": 5.99, "Coffee": 2.99}, ...}
        self.availability = availability

    def to_dict(self) -> Dict:
        """Convert restaurant to dictionary for JSON serialization"""
        return {
            "name": self.name,
            "menus": self.menus,
            "availability": self.availability
        }


    @classmethod
    def from_dict(cls, data: Dict) -> 'Restaurant':
        """Create Restaurant instance from dictionary"""
        menus = data.get('menus', {})
        # Using .get for availability in case it is missing in JSON (default True)
        return cls(data['name'], menus, data.get('availability', True))

    @staticmethod
    def save_restaurants(restaurants: List['Restaurant'], file_name: str = 'restaurants.json') -> None:
        """Save restaurants to a JSON file"""
        try:
            with open(file_name, "w", encoding="utf-8") as file:
                json.dump([restaurant.to_dict() for restaurant in restaurants], file, indent=4)
        except Exception as e:
            print(f"Error saving data: {e}")

    @staticmethod
    def load_restaurants(file_name: str = 'restaurants.json') -> List['Restaurant']:
        """Load restaurants from a JSON file"""
        try:
            with open(file_name, "r", encoding="utf-8") as file:
                restaurant_data = json.load(file)
                return [Restaurant.from_dict(data) for data in restaurant_data]
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            print("Error: Corrupted JSON file.")
            return []

    def update_menu(self, menu_type: str, new_menu: Dict[str, float]) -> str:
        """Update or add a specific menu type"""
        self.menus[menu_type] = new_menu
        return f"Menu '{menu_type}' updated for '{self.name}'."

    def remove_menu(self, menu_type: str) -> str:
        """Remove a specific menu type"""
        if menu_type in self.menus:
            del self.menus[menu_type]
            return f"Menu '{menu_type}' removed from '{self.name}'."
        return f"Menu '{menu_type}' not found in '{self.name}'."

    def display_info(self) -> None:
        """Display restaurant information"""
        print("=" * 40)
        print(f"🍽 Restaurant: {self.name}")
        print(f"📌 Status: {'🟢 Open' if self.availability else '🔴 Closed'}")
        print("-" * 40)
        print("📜 Menus:")
        # Loop through each menu type and its items
        for menu_type, items in self.menus.items():
            print(f"  🍱 {menu_type.capitalize()}:")
            if isinstance(items, dict):
                for item, price in items.items():
                    print(f"    - {item}: ${price:.2f}")
            else:
                print(f"    - Invalid menu format for {menu_type}")
        print("=" * 40)


class Order:
    """Take customer order"""

    def __init__(self, user_email: str, restaurant_name: str, items: Dict[str, int], 
                 status: str = 'pending', driver_email: Optional[str] = None) -> None:
        self.user_email = user_email
        self.restaurant_name = restaurant_name
        self.items = items  # items is a dictionary like {"Pancakes": 3}
        self.status = status
        self.driver_email = driver_email
        self.orderAt = datetime.now()


    def to_dict(self) -> Dict:
        """Convert order to dictionary for JSON serialization"""
        return {
            "user_email": self.user_email,
            "restaurant_name": self.restaurant_name,
            "items": self.items,
            "status": self.status,
            "driver_email": self.driver_email,
            "orderAt": self.orderAt.isoformat()
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Order':
        """Load order from dictionary"""
        order = cls(
            data['user_email'],
            data['restaurant_name'],
            data['items'],
            data.get('status', 'pending'),
            data.get('driver_email')
        )
        order.orderAt = datetime.fromisoformat(data['orderAt'])
        return order

    @staticmethod
    def save_order(orders: List['Order'], file_name: str = 'orders.json') -> None:
        """Save orders to a JSON file"""
        try:
            with open(file_name, "w", encoding="utf-8") as file:
                json.dump([order.to_dict() for order in orders], file, indent=4)
        except Exception as e:
            print(f"Error saving orders: {e}")

    @staticmethod
    def load_order(file_name: str = 'orders.json') -> List['Order']:
        """Load orders from a JSON file"""
        try:
            with open(file_name, "r", encoding="utf-8") as file:
                order_data = json.load(file)
                return [Order.from_dict(data) for data in order_data]
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            print("Error: Corrupted JSON file.")
            return []

    def update_status(self, status: str) -> str:
        """Update order status"""
        self.status = status
        return f"Order status updated to: {self.status}"

    def display_receipt(self, user: User, restaurant: Restaurant) -> None:
        """Display order receipt"""
        print("\n--- RECEIPT ---")
        print(f"👤 Customer: {user.name}")
        print(f"🏪 Restaurant: {restaurant.name}")
        print("🍽 Ordered Items:")

        total_price = 0
        for item, quantity in self.items.items():
            item_price = None
            # Search through each menu in the restaurant for the item
            for menu in restaurant.menus.values():
                if item in menu:
                    item_price = menu[item]
                    break

            if item_price is not None:
                price = item_price * quantity
                total_price += price
                print(f"  - {item}: {quantity} x ${item_price:.2f} = ${price:.2f}")
            else:
                print(f"  - {item}: Not found in {restaurant.name}")

        print(f"💰 Total: ${total_price:.2f}")
        print(f"📌 Status: {self.status.capitalize()}")
        print(f"📅 Ordered at: {self.orderAt.strftime('%Y-%m-%d %H:%M:%S')}")
        print("----------------\n")


class Driver:
    """Class for drivers"""

    def __init__(self, name: str, email: str) -> None:
        self.name = name
        self.email = email
        self.orders: List[Order] = []  # This will hold the orders assigned to the driver
        self.available = True          # Indicates if the driver is available for a new order


    def to_dict(self) -> Dict:
        """Convert driver to dictionary for JSON serialization"""
        return {
            "name": self.name,
            "email": self.email,
            "orders": [order.to_dict() for order in self.orders],
            "available": self.available
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Driver':
        """Load driver from dictionary"""
        driver = cls(data['name'], data['email'])
        driver.orders = [Order.from_dict(order_data) for order_data in data.get('orders', [])]
        driver.available = data.get('available', True)
        return driver

    @staticmethod
    def save_driver(drivers: List['Driver'], file_name: str = 'drivers.json') -> None:
        """Save driver list to a JSON file"""
        try:
            with open(file_name, "w", encoding="utf-8") as file:
                json.dump([driver.to_dict() for driver in drivers], file, indent=4)
        except Exception as e:
            print(f"Error saving drivers: {e}")

    @staticmethod
    def load_driver(file_name: str = 'drivers.json') -> List['Driver']:
        """Load drivers from a JSON file"""
        try:
            with open(file_name, "r", encoding="utf-8") as file:
                driver_data = json.load(file)
                return [Driver.from_dict(data) for data in driver_data]
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            print("Error: Corrupted JSON file.")
            return []

    def assign_order(self, order: Order) -> None:
        """Assign an order to the driver"""
        if not self.available:
            print(f"🚫 Driver {self.name} is not available to take new orders.")
            return

        self.available = False
        self.orders.append(order)
        order.status = "assigned"
        order.driver_email = self.email
        print(f"✅ Order for {order.restaurant_name} assigned to driver {self.name}.")

    def complete_order(self) -> None:
        """Complete the last assigned order"""
        if not self.orders:
            print(f"🚫 Driver {self.name} has no active orders to complete.")
            return

        order = self.orders.pop()
        order.status = "delivered"
        self.available = True
        print(f"✅ Order from '{order.restaurant_name}' delivered by driver '{self.name}'.")


class Admin:
    """Admin panel for managing users, restaurants, orders, and drivers"""
    def __init__(self) -> None:
        self.restaurants: List[Restaurant] = []
        self.users: List[User] = []
        self.orders: List[Order] = []
        self.drivers: List[Driver] = []

    def save_data(
        self, 
        user_file: str = 'users.json', 
        restaurant_file: str = 'restaurants.json', 
        order_file: str = 'orders.json', 
        driver_file: str = 'drivers.json'
    ):
        """Save all data to JSON files"""
        User.save_users(self.users, user_file)
        Restaurant.save_restaurants(self.restaurants, restaurant_file)
        Order.save_order(self.orders, order_file)
        Driver.save_driver(self.drivers, driver_file)
        print("✅ Data saved successfully!")

    def load_data(
        self, 
        user_file: str = 'users.json', 
        restaurant_file: str = 'restaurants.json', 
        order_file: str = 'orders.json', 
        driver_file: str = 'drivers.json'
    ):
        """Load all data from JSON files"""
        self.users = User.load_users(user_file)
        self.restaurants = Restaurant.load_restaurants(restaurant_file)
        self.orders = Order.load_order(order_file)
        self.drivers = Driver.load_driver(driver_file)
        print("✅ Data loaded successfully!")

    def add_user(self, name: str, email: str, password: str) -> None:
        """Add a new user"""
        if any(user.email == email for user in self.users):
            print(f"🚫 User with email {email} already exists.")
            return
        new_user = User(name, email, password)
        self.users.append(new_user)
        print(f"✅ User '{name}' added successfully!")

    def add_restaurant(self, name: str, menus: Dict[str, Dict[str, float]], availability: bool = True):
        """Add a new restaurant"""
        if any(r.name == name for r in self.restaurants):
            print(f"🚫 Restaurant '{name}' already exists.")
            return
        new_restaurant = Restaurant(name, menus, availability)
        self.restaurants.append(new_restaurant)
        print(f"✅ Restaurant '{name}' added successfully!")

    def add_driver(self, name: str, email: str):
        """Add a new driver"""
        if any(d.email == email for d in self.drivers):
            print(f"🚫 Driver with email {email} already exists.")
            return
        new_driver = Driver(name, email)
        self.drivers.append(new_driver)
        print(f"✅ Driver '{name}' added successfully!")

    def update_restaurant_menu(self, restaurant_name: str, menu_type: str, new_menu: Dict[str, float]) -> None:
        """
        Update a specific menu type for a restaurant.
        This method now requires the menu type (like 'breakfast') as well.
        """
        restaurant = next((r for r in self.restaurants if r.name == restaurant_name), None)
        if not restaurant:
            print(f"🚫 Restaurant '{restaurant_name}' not found!")
            return
        result = restaurant.update_menu(menu_type, new_menu)
        print(f"✅ {result}")

    def remove_restaurant(self, restaurant_name: str) -> None:
        """Remove a restaurant"""
        self.restaurants = [r for r in self.restaurants if r.name != restaurant_name]
        print(f"✅ Restaurant '{restaurant_name}' removed.")

    def update_availability(self, restaurant_name: str, availability: bool) -> None:
        """Update restaurant availability"""
        restaurant = next((r for r in self.restaurants if r.name == restaurant_name), None)
        if not restaurant:
            print(f"🚫 Restaurant '{restaurant_name}' not found!")
            return
        restaurant.availability = availability
        print(f"✅ Availability updated for '{restaurant_name}'.")

    def list_users(self) -> None:
        """List all users"""
        if not self.users:
            print("🚫 No users available!")
            return
        for user in self.users:
            print(f"👤 User: {user.name}, Email: {user.email}")

    def list_restaurants(self) -> None:
        """List all restaurants"""
        if not self.restaurants:
            print("🚫 No restaurants available!")
            return
        for restaurant in self.restaurants:
            restaurant.display_info()

    def list_drivers(self) -> None:
        """List all drivers"""
        if not self.drivers:
            print("🚫 No drivers available!")
            return
        for driver in self.drivers:
            status = "Available" if driver.available else "Delivering"
            print(f"👤 Driver: {driver.name}, Email: {driver.email}, Status: {status}")

    def place_order(self, user_email: str, restaurant_name: str, items: Dict[str, int]) -> None:
        """Place an order with item validation"""
        restaurant = next((r for r in self.restaurants if r.name == restaurant_name and r.availability), None)
        if not restaurant:
            print(f"🚫 Restaurant '{restaurant_name}' is not available!")
            return

        total_price = 0
        valid_items = {}
        for item, quantity in items.items():
            item_price = None
            for menu in restaurant.menus.values():
                if item in menu:
                    item_price = menu[item]
                    break
            if item_price is None:
                print(f"🚫 Item '{item}' not found in {restaurant.name}'s menu")
                continue
            valid_items[item] = quantity
            total_price += item_price * quantity

        if not valid_items:
            print("🚫 No valid items in order!")
            return

        order = Order(user_email, restaurant_name, valid_items)
        self.orders.append(order)
        print(f"✅ Order placed successfully! Total: ${total_price:.2f}")

    def assign_order_to_driver(self) -> None:
        """Assign pending orders to available drivers"""
        pending_orders = [order for order in self.orders if order.status == "pending"]
        available_drivers = [driver for driver in self.drivers if driver.available]

        if not pending_orders:
            print("🚫 No pending orders!")
            return

        if not available_drivers:
            print("🚫 No available drivers!")
            return

        for i, order in enumerate(pending_orders):
            driver = available_drivers[i % len(available_drivers)]
            driver.assign_order(order)
            print(f"✅ Order from '{order.restaurant_name}' assigned to driver '{driver.name}'.")

    def complete_order(self, driver_email: str) -> None:
        """Complete the last order assigned to a driver"""
        driver = next((d for d in self.drivers if d.email == driver_email), None)
        if not driver:
            print(f"🚫 Driver with email {driver_email} not found!")
            return

        if not driver.orders:
            print(f"🚫 Driver '{driver.name}' has no active orders!")
            return

        driver.complete_order()
        print(f"✅ Order completed by driver '{driver.name}'.")


def main():
    """_main system_
    """
    admin = Admin()

    # Load data from files at the beginning.
    # Note: We now use "drivers.json" (plural) for consistency.
    admin.load_data(user_file='users.json', 
                    restaurant_file='restaurants.json', 
                    order_file='orders.json', 
                    driver_file='drivers.json')

    while True:
        print("\nMenu:")
        print("1. Register User")
        print("2. User Login")
        print("3. List All Users (Admin Only)")
        print("4. Add Restaurant (Admin Only)")
        print("5. List Restaurants")
        print("6. Place Order")
        print("7. Assign Order to Driver (Admin Only)")
        print("8. Complete Order (Driver Only)")
        print("9. Add Driver (Admin Only)")
        print("10. List Drivers (Admin Only)")
        print("11. Save Data")
        print("12. Exit")

        choice = input("Select an option (1-12): ")

        # User Registration
        if choice == "1":
            name = input("Enter your name: ")
            email = input("Enter email: ")
            password = input("Enter password: ")
            admin.add_user(name, email, password)

        # User Login
        elif choice == "2":
            email = input("Enter email: ")
            password = input("Enter password: ")
            logged_in_user = User.login(email, password, admin.users)
            if logged_in_user:
                print(f"Welcome back, {logged_in_user.name}")

                while True:
                    print("\nUser menu:")
                    print("1. Place order")
                    print("2. View orders")
                    print("3. Logout")

                    user_choice = input("Select an option (1-3): ")

                    if user_choice == "1":
                        restaurant_name = input("Enter restaurant name: ")
                        items_input = input("Enter items as JSON (e.g: {\"item\": quantity}): ")
                        try:
                            items = json.loads(items_input)
                            admin.place_order(logged_in_user.email, restaurant_name, items)
                        except json.JSONDecodeError:
                            print("Invalid JSON format. Please try again.")

                    elif user_choice == "2":
                        # List orders that belong to the logged-in user.
                        user_orders = [order for order in admin.orders if order.user_email == logged_in_user.email]
                        if not user_orders:
                            print("No orders found")
                        else:
                            for order in user_orders:
                                restaurant = next((r for r in admin.restaurants if r.name == order.restaurant_name), None)
                                if restaurant:
                                    # Pass the whole user object instead of the email.
                                    order.display_receipt(logged_in_user, restaurant)
                                else:
                                    print(f"Restaurant '{order.restaurant_name}' not found for the order.")
                    elif user_choice == "3":
                        print("Logging out...")
                        break
                    else:
                        print("Invalid option. Try again later.")

        # Admin Actions
        elif choice == "3":
            print("Listing all users:")
            admin.list_users()

        elif choice == "4":
            name = input("Enter restaurant name: ")
            menus_input = input("Enter menus as JSON (e.g: {\"breakfast\": {\"Pancakes\": 5.99, \"Coffee\": 2.99}}): ")
            try:
                menus = json.loads(menus_input)
                admin.add_restaurant(name, menus)
            except json.JSONDecodeError:
                print("Invalid menu format. Please try again.")

        elif choice == "5":
            admin.list_restaurants()

        elif choice == "7":
            admin.assign_order_to_driver()

        elif choice == "9":
            name = input("Enter driver name: ")
            email = input("Enter driver email: ")
            admin.add_driver(name, email)

        elif choice == "10":
            admin.list_drivers()

        # Driver-only Actions
        elif choice == "8":
            driver_email = input("Enter driver email: ")
            admin.complete_order(driver_email)

        # Save Data
        elif choice == "11":
            admin.save_data()

        # Exit Program
        elif choice == "12":
            print("Exiting the system...")
            break

        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()