<!-- @format -->

Food Delivery System

A command-line-based food delivery system that allows users to order food, admins to manage restaurants and drivers, and drivers to deliver orders. Built using Python.
Features

    User Roles:

        Users: Register, log in, place orders, and view order history.

        Admins: Add/remove restaurants, update menus, manage drivers, and assign orders.

        Drivers: Accept and complete orders.

    Restaurant Management:

        Add, update, or remove restaurants.

        Manage menus (add/remove items, update prices).

    Order Management:

        Users can place orders from available restaurants.

        Admins can assign orders to drivers.

        Drivers can mark orders as delivered.

    Data Persistence:

        Data is saved to JSON files (users.json, restaurants.json, orders.json, drivers.json).

Prerequisites

    Python 3.x

    Basic knowledge of command-line interfaces.

Installation

    Clone the repository:
    bash
    Copy

    git clone https://github.com/Falasefemi2/fm-places
    cd fm-places

    Run the program:
    bash
    Copy

    python main.py

Usage

1. Main Menu

When you run the program, you'll see the following menu:
Copy

Menu:

1.  Register User
2.  User Login
3.  List All Users (Admin Only)
4.  Add Restaurant (Admin Only)
5.  List Restaurants
6.  Place Order
7.  Assign Order to Driver (Admin Only)
8.  Complete Order (Driver Only)
9.  Add Driver (Admin Only)
10. List Drivers (Admin Only)
11. Save Data
12. Exit

13. User Registration

    Select option 1 to register a new user.

    Provide your name, email, and password.

14. User Login

    Select option 2 to log in as a user.

    After logging in, you can:

        Place orders.

        View your order history.

15. Admin Functions

    Add Restaurant: Select option 4 to add a new restaurant.

    List Restaurants: Select option 5 to view all restaurants.

    Add Driver: Select option 9 to add a new driver.

    List Drivers: Select option 10 to view all drivers.

    Assign Order to Driver: Select option 7 to assign a pending order to an available driver.

16. Driver Functions

    Complete Order: Select option 8 to mark an order as delivered.

17. Save Data

    Select option 11 to save all data to JSON files.

18. Exit

    Select option 12 to exit the program.

File Structure
Copy

food-delivery-system/
├── main.py # Main program file
├── users.json # Stores user data
├── restaurants.json # Stores restaurant data
├── orders.json # Stores order data
├── drivers.json # Stores driver data
├── README.md # Project documentation

Example Workflow

    Register a User:
    Copy

    Select an option (1-12): 1
    Enter your name: John Doe
    Enter your email: john@example.com
    Enter your password: password123
    User 'John Doe' registered successfully!

    Log in as a User:
    Copy

    Select an option (1-12): 2
    Enter your email: john@example.com
    Enter your password: password123
    Welcome back, John Doe!

    Place an Order:
    Copy

    Select an option (1-3): 1
    Enter restaurant name: Pizza Palace
    Enter items as JSON (e.g., {"item": quantity}): {"Pepperoni Pizza": 2, "Coke": 1}
    Order placed successfully! Total: $25.00

    Admin Assigns Order to Driver:
    Copy

    Select an option (1-12): 7
    Order for 'Pizza Palace' assigned to driver 'Jane Doe'.

    Driver Completes Order:
    Copy

    Select an option (1-12): 8
    Enter your email: jane@example.com
    Order for 'Pizza Palace' completed by driver 'Jane Doe'.

Future Enhancements

    Database Integration: Replace JSON files with a database (e.g., SQLite, PostgreSQL).

    Authentication: Add password hashing for secure user authentication.

    User Interface: Build a web or GUI-based interface for better usability.

    Real-Time Tracking: Add real-time order tracking for users and drivers.

    Notifications: Send email or SMS notifications for order updates.

Contributing

Contributions are welcome! If you'd like to contribute, please follow these steps:

    Fork the repository.

    Create a new branch for your feature or bug fix.

    Commit your changes.

    Submit a pull request.

License

This project is licensed under the MIT License. See the LICENSE file for details.
Contact

For questions or feedback, please contact:

    Your Name

    Email: femifalase228@gmail.com

Enjoy using the Food Delivery System! 🍕🚚
