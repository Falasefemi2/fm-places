import json
from typing import Optional, List, Dict
from datetime import datetime

class User:
    """Registration of users"""
    def __init__(self, name: str, email: str, password: str) -> None:
        self.name = name
        self.email = email
        self.password = password
        self.created_at = datetime.now()
    
    def to_dict(self) -> Dict:
        """Convert user to dictionary for JSON serialization"""
        return {
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "created_at": self.created_at.isoformat()
        }
        
    @staticmethod
    def login(email: str, password: str, users: List['User']) -> Optional['User']:
        """Login user"""
        if not users:
            raise ValueError("No users available")
        if not email or not password:
            raise ValueError('Email and password are required')
        for user in users:
            if user.email == email and user.password == password:
                return user
        return None
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'User':
        """Create user from dictionary"""
        user = cls(data['name'], data['email'], data['password'])
        user.created_at = datetime.fromisoformat(data['created_at'])
        return user
    
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

class Restaurant:
    """Restaurant with multiple menus"""
    def __init__(self, name: str, menus: Dict[str, Dict[str, float]], availability: bool = True) -> None:
        self.name = name
        self.menus = menus  # Nested dictionary: {menu_type: {item: price}}
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
        """Create restaurant from dictionary, handle missing menus key."""
        menus = data.get('menus', {})  # Default to an empty dictionary if 'menus' key is missing
        return cls(data['name'], menus, data['availability'])

    def update_menu(self, menu_type: str, new_menu: Dict[str, float]) -> None:
        """Update or add a specific menu type"""
        self.menus[menu_type] = new_menu
        print(f"Menu '{menu_type}' updated for '{self.name}'.")

    def remove_menu(self, menu_type: str) -> None:
        """Remove a specific menu type"""
        if menu_type in self.menus:
            del self.menus[menu_type]
            print(f"Menu '{menu_type}' removed from '{self.name}'.")
        else:
            print(f"Menu '{menu_type}' not found in '{self.name}'.")

    def display_info(self) -> None:
        """Display restaurant information"""
        print(f"Restaurant: {self.name}")
        print(f"Availability: {'Open' if self.availability else 'Closed'}")
        print("Menus:")
        for menu_type, items in self.menus.items():
            print(f" {menu_type.capitalize()}:")
            for item, price in items.items():
                print(f"  - {item}: ${price:.2f}")

class Order:
    def __init__(self, user_email: str, restaurant_name: str, items: Dict[str, int], status: str = "Pending", driver_email: Optional[str] = None):
        self.user_email = user_email
        self.restaurant_name = restaurant_name
        self.items = items
        self.status = status
        self.driver_email = driver_email
        self.created_at = datetime.now()

    def to_dict(self):
        return {
            "user_email": self.user_email,
            "restaurant_name": self.restaurant_name,
            "items": self.items,
            "status": self.status,
            "driver_email": self.driver_email,
            "created_at": self.created_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data):
        order = cls(data["user_email"], data["restaurant_name"], data["items"], data["status"], data.get("driver_email"))
        order.created_at = datetime.fromisoformat(data["created_at"])
        return order

    def update_status(self, status: str) -> None:
        """Update the status of the order."""
        self.status = status

    def display_receipt(self, user: User, restaurant: Restaurant) -> None:
        """Display the receipt for the order."""
        print("\n--- Receipt ---")
        print(f"Customer: {user.name}")
        print(f"Restaurant: {restaurant.name}")
        print("Items:")
        total_price = 0
        for item, quantity in self.items.items():
            price = restaurant.menus.get(item, {}).get('price', 0) * quantity
            total_price += price
            print(f"  - {item}: {quantity} x ${restaurant.menus.get(item, {}).get('price', 0):.2f} = ${price:.2f}")
        print(f"Total: ${total_price:.2f}")
        print(f"Status: {self.status}")
        print(f"Ordered at: {self.created_at}")
        print("---------------\n")

class Driver:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email
        self.orders = []  # List of order IDs
        self.available = True

    def to_dict(self):
        return {
            "name": self.name,
            "email": self.email,
            "orders": self.orders,
            "available": self.available,
        }

    @classmethod
    def from_dict(cls, data):
        driver = cls(data["name"], data["email"])
        driver.orders = data["orders"]
        driver.available = data["available"]
        return driver

    def assign_order(self, order: Order) -> None:
        """Assign an order to the driver."""
        self.available = False
        self.orders.append(order)
        order.update_status("Assigned")
        print(f"Order for '{order.restaurant_name}' assigned to driver '{self.name}'.")

    def complete_order(self) -> None:
        """Complete the current order."""
        self.available = True
        if self.orders:
            order = self.orders.pop(0)
            order.update_status("Delivered")
            print(f"Order for '{order.restaurant_name}' completed by driver '{self.name}'.")

class Admin:
    """Admin class"""
    def __init__(self) -> None:
        self.restaurants: List[Restaurant] = []
        self.users: List[User] = []
        self.orders: List[Order] = []  # List to manage orders
        self.drivers: List[Driver] = []  # List to manage drivers

    def save_data(self, restaurants_file: str = 'restaurants.json', 
                  users_file: str = 'users.json', orders_file: str = 'orders.json', 
                  drivers_file: str = 'drivers.json') -> None:
        """Save restaurants, users, orders, and drivers to JSON files"""
        with open(restaurants_file, 'w', encoding="utf-8") as f:
            json.dump([restaurant.to_dict() for restaurant in self.restaurants], f, indent=4)
        
        User.save_users(self.users, users_file)

        with open(orders_file, 'w', encoding="utf-8") as f:
            json.dump([order.to_dict() for order in self.orders], f, indent=4)

        with open(drivers_file, 'w', encoding="utf-8") as f:
            json.dump([driver.to_dict() for driver in self.drivers], f, indent=4)

        print("Data saved successfully.")

    def load_data(self, restaurants_file: str = 'restaurants.json', 
                  users_file: str = 'users.json', orders_file: str = 'orders.json', 
                  drivers_file: str = 'drivers.json') -> None:
        """Load restaurants, users, orders, and drivers from JSON files"""
        try:
            with open(restaurants_file, 'r', encoding="utf-8") as f:
                restaurant_data = json.load(f)
                self.restaurants = [Restaurant.from_dict(data) for data in restaurant_data]
            print(f"Loaded {len(self.restaurants)} restaurants.")
        except FileNotFoundError:
            print("No saved restaurants found.")

        try:
            self.users = User.load_users(users_file)
            print(f"Loaded {len(self.users)} users.")
        except FileNotFoundError:
            print("No saved users found.")

        try:
            with open(orders_file, 'r', encoding="utf-8") as f:
                order_data = json.load(f)
                self.orders = [Order.from_dict(data) for data in order_data]
            print(f"Loaded {len(self.orders)} orders.")
        except FileNotFoundError:
            print("No saved orders found.")

        try:
            with open(drivers_file, 'r', encoding="utf-8") as f:
                driver_data = json.load(f)
                self.drivers = [Driver.from_dict(data) for data in driver_data]
            print(f"Loaded {len(self.drivers)} drivers.")
        except FileNotFoundError:
            print("No saved drivers found.")

    def add_user(self, name: str, email: str, password: str) -> None:
        """Add a user"""
        new_user = User(name, email, password)
        self.users.append(new_user)
        print(f"User '{name}' registered successfully!")

    def add_restaurant(self, name: str, menu: Dict[str, float], 
                       availability: bool = True) -> None:
        """Add restaurant"""
        new_restaurant = Restaurant(name, menu, availability)
        self.restaurants.append(new_restaurant)
        print(f"Restaurant '{name}' added successfully!!")
        
    def update_restaurant_menu(self, restaurant_name: str, 
                                new_menu: Dict[str, float]) -> None:
        """Update restaurant menu"""
        for restaurant in self.restaurants:
            if restaurant.name == restaurant_name:
                restaurant.update_menu(new_menu)
                print(f"Menu updated for '{restaurant.name}'.")
                return
        print(f"Restaurant '{restaurant_name}' not found")
    
    def update_availability(self, restaurant_name: str, availability: bool) -> None:
        """Update restaurant availability"""
        for restaurant in self.restaurants:
            if restaurant.name == restaurant_name:
                restaurant.availability = availability
                print(f"Availability updated for '{restaurant_name}'.")
                return
        print(f"Restaurant '{restaurant_name}' not found")
        
    def remove_restaurant(self, restaurant_name: str) -> None:
        """Remove restaurant"""
        for restaurant in self.restaurants:
            if restaurant.name == restaurant_name:
                self.restaurants.remove(restaurant)
                print(f"Restaurant '{restaurant_name}' removed successfully.")
                return
        print(f"Restaurant '{restaurant_name}' not found")
    
    def list_restaurants(self):
        """List all restaurants"""
        if not self.restaurants:
            print("No available restaurants")
        else:
            for restaurant in self.restaurants:
                restaurant.display_info()

    def add_driver(self, name: str, email: str) -> None:
        """Add a delivery driver."""
        driver = Driver(name, email)
        self.drivers.append(driver)
        print(f"Driver '{name}' added successfully!")

    def list_drivers(self) -> None:
        """List all drivers."""
        for driver in self.drivers:
            status = "Available" if driver.available else "Delivering"
            print(f"Driver: {driver.name}, Email: {driver.email}, Status: {status}")

    def place_order(self, user_email: str, restaurant_name: str, items: Dict[str, int]) -> None:
        """Place a new order."""
        # Find the restaurant
        restaurant = next((r for r in self.restaurants if r.name == restaurant_name), None)
        if not restaurant or not restaurant.availability:
            print(f"Restaurant '{restaurant_name}' is not available.")
            return

        # Calculate total price
        total_price = sum(restaurant.menus.get(item, {}).get('price', 0) * quantity for item, quantity in items.items())

        # Create and save the order
        order = Order(user_email, restaurant_name, items)
        self.orders.append(order)
        print(f"Order placed successfully! Total: ${total_price:.2f}")

    def assign_order_to_driver(self) -> None:
        """Assign pending orders to available drivers."""
        # Find a pending order and an available driver
        pending_orders = [order for order in self.orders if order.status == "Pending"]
        available_drivers = [driver for driver in self.drivers if driver.available]

        if not pending_orders:
            print("No pending orders.")
            return
        if not available_drivers:
            print("No available drivers.")
            return

        # Assign the first pending order to the first available driver
        order = pending_orders[0]
        driver = available_drivers[0]
        driver.assign_order(order)
        print(f"Order for '{order.restaurant_name}' assigned to driver '{driver.name}'.")

    def complete_order(self, driver_email: str) -> None:
        """Mark an order as completed."""
        driver = next((d for d in self.drivers if d.email == driver_email), None)
        if not driver or not driver.orders:
            print("Driver or current order not found.")
            return

        # Complete the order
        driver.complete_order()

def main():
    """Main system"""
    admin = Admin()
    admin.load_data(users_file='users.json', restaurants_file='restaurants.json', 
                    orders_file='orders.json', drivers_file='drivers.json')  # Load all data

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

        if choice == '1':  # Register User
            name = input("Enter your name: ")
            email = input("Enter your email: ")
            password = input("Enter your password: ")
            admin.add_user(name, email, password)

        elif choice == '2':  # User Login
            email = input("Enter your email: ")
            password = input("Enter your password: ")
            logged_in_user = User.login(email, password, admin.users)
            if logged_in_user:
                print(f"Welcome back, {logged_in_user.name}!")
                while True:
                    print("\nUser Menu:")
                    print("1. Place Order")
                    print("2. View Orders")
                    print("3. Logout")
                    user_choice = input("Select an option (1-3): ")

                    if user_choice == '1':  # Place Order
                        restaurant_name = input("Enter restaurant name: ")
                        items_input = input("Enter items as JSON (e.g., {\"item\": quantity}): ")
                        items = json.loads(items_input)
                        admin.place_order(logged_in_user.email, restaurant_name, items)

                    elif user_choice == '2':  # View Orders
                        user_orders = [order for order in admin.orders if order.user_email == logged_in_user.email]
                        if not user_orders:
                            print("No orders found.")
                        else:
                            for order in user_orders:
                                restaurant = next((r for r in admin.restaurants if r.name == order.restaurant_name), None)
                                if restaurant:
                                    order.display_receipt(logged_in_user, restaurant)

                    elif user_choice == '3':  # Logout
                        print("Logging out...")
                        break

                    else:
                        print("Invalid option. Please try again.")

            else:
                print("Invalid email or password. Please try again.")

        elif choice == '3':  # List All Users (Admin Only)
            print("\nRegistered Users:")
            if not admin.users:
                print("No users registered.")
            else:
                for user in admin.users:
                    print(f"Name: {user.name}, Email: {user.email}, Registered At: {user.created_at}")

        elif choice == '4':  # Add Restaurant (Admin Only)
            name = input("Enter restaurant name: ")
            menu_input = input("Enter restaurant menu as JSON (e.g., {\"item\": price}): ")
            menu = json.loads(menu_input)
            admin.add_restaurant(name, menu)

        elif choice == '5':  # List Restaurants
            admin.list_restaurants()

        elif choice == '6':  # Place Order
            email = input("Enter your email: ")
            password = input("Enter your password: ")
            logged_in_user = User.login(email, password, admin.users)
            if logged_in_user:
                restaurant_name = input("Enter restaurant name: ")
                items_input = input("Enter items as JSON (e.g., {\"item\": quantity}): ")
                items = json.loads(items_input)
                admin.place_order(logged_in_user.email, restaurant_name, items)
            else:
                print("Invalid email or password. Please try again.")

        elif choice == '7':  # Assign Order to Driver (Admin Only)
            admin.assign_order_to_driver()

        elif choice == '8':  # Complete Order (Driver Only)
            driver_email = input("Enter your email: ")
            admin.complete_order(driver_email)

        elif choice == '9':  # Add Driver (Admin Only)
            name = input("Enter driver's name: ")
            email = input("Enter driver's email: ")
            admin.add_driver(name, email)

        elif choice == '10':  # List Drivers (Admin Only)
            admin.list_drivers()

        elif choice == '11':  # Save Data
            admin.save_data(users_file='users.json', restaurants_file='restaurants.json', 
                            orders_file='orders.json', drivers_file='drivers.json')

        elif choice == '12':  # Exit
            print("Exiting...")
            break

        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()