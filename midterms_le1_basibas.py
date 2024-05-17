# Dictionary to store game library with their quantities and rental costs
game_library = {
    "Donkey Kong": {"quantity": 3, "cost": 2},
    "Super Mario Bros": {"quantity": 5, "cost": 3},
    "Tetris": {"quantity": 2, "cost": 1},
    # Add more games as needed
}

# Dictionary to store user accounts with their balances and points
user_accounts = {}

# Admin account details
admin_username = "admin"
admin_password = "adminpass"

# Function to display available games with their quantities and rental costs
def display_available_games():
    print("=" * 10, "AVAILABLE GAMES", "=" * 10)
    for i, (game, details) in enumerate(game_library.items(), 1):
        print(f"{i}. {game}:\n\tQuantity: {details['quantity']} \n\tCost: ${details['cost']}\n")
    print("=" * 37)
    input("Press Enter to continue...")

# Function to register a new user
def register_user():
    print("=" * 12, "REGISTER", "=" * 13)
    user_name = input("Username: ")
    user_pass = input("Password: ")
    print("=" * 37)
    
    user_accounts[user_name] = {
        'password': user_pass,
        'balance': 0.0,
        'points': 0,
        'inventory': []
    }
    print("REGISTERED SUCCESSFULLY\n")

# Function to check user credentials
def check_credentials(username, password):
    if username == admin_username and password == admin_password:
        return 'admin'
    elif username in user_accounts and user_accounts[username]['password'] == password:
        return 'regular'
    else:
        return None

# Function to handle user login
def log_in():
    print("\n" + "=" * 14 + " LOGIN " + "=" * 14)
    user_name = input("Username: ")
    user_pass = input("Password: ")
    print("=" * 37)

    user_type = check_credentials(user_name, user_pass)
    if user_type == 'regular':
        print("Login successful!\n")
        logged_in_menu(user_name)
    else:
        print("Incorrect username or password. Please try again.\n")

# Function to handle admin login
def admin_login():
    print("\n" + "=" * 14 + " ADMIN LOGIN " + "=" * 14)
    admin_user = input("Admin Username: ")
    admin_pass = input("Admin Password: ")
    print("=" * 37)

    user_type = check_credentials(admin_user, admin_pass)
    if user_type == 'admin':
        print("Admin login successful!")
        admin_menu()
    else:
        print("Invalid admin credentials.")
        input("Press Enter to continue...\n")

# Function to rent a game
def rent_game(username):
    try:
        print("=" * 37)
        display_game_inventory()
        game_name = input("Enter the game you want to rent(NAME): ").title()
        if game_name in game_library:
            game_cost = game_library[game_name]['cost']
            if user_accounts[username]['balance'] >= game_cost:
                if game_library[game_name]['quantity'] > 0:
                    game_library[game_name]['quantity'] -= 1
                    user_accounts[username]['balance'] -= game_cost
                    user_accounts[username]['inventory'].append(game_name)
                    user_accounts[username]['points'] += game_cost // 2
                    print(f"Game '{game_name}' rented successfully by {username}!")
                    print(f"Points earned: {game_cost // 2}. Total points: {user_accounts[username]['points']}")
                else:
                    print(f"Sorry, '{game_name}' is out of stock.")
            else:
                print(f"Sorry, {username} does not have enough balance to rent '{game_name}'.")
        else:
            print(f"Sorry, '{game_name}' is not available in the game library.")
    except KeyError:
        print("An error occurred while processing your request.")
    input("Press Enter to continue...\n")

# Function to return a game
def return_game(username):
    try:
        display_inventory(username)
        print("=" * 37)
        inventory = user_accounts[username]['inventory']
        for item in inventory:
            print(item)
            game_to_return = input("Enter the name of the game you want to return: ")
            if game_to_return in inventory:
                inventory.remove(game_to_return)
                if game_to_return in game_library:
                    game_library[game_to_return]['quantity'] += 1
                else:
                    game_library[game_to_return] = {"quantity": 1, "cost": 0}
                print(f"Game '{game_to_return}' returned successfully by {username}!")
            else:
                print(f"You don't have '{game_to_return}' in your inventory.")
    except KeyError:
        print("An error occurred while processing your request.")
    input("Press Enter to continue...\n")

# Function to top-up user account
def top_up_account(username):
    try:
        print("=" * 37)
        amount = float(input("Enter Amount: "))
        user_accounts[username]['balance'] += amount
        print(f"Top-up successful! New balance for {username}: {user_accounts[username]['balance']}")
    except ValueError:
        print("Invalid input. Please enter a valid amount.")
    except KeyError:
        print("An error occurred...")
    input("Press Enter to continue...\n")

# Function to display user's inventory
def display_inventory(username):
    print("=" * 37)
    inventory = user_accounts[username]['inventory']
    if inventory:
        print(f"Inventory of {username}:")
        for item in inventory:
            print(item)
    else:
        print(f"{username}'s inventory is empty.")
    input("Press Enter to continue...\n")

# Function for admin to update game details
def admin_update_game():
    print("=" * 37)
    game_name = input("Enter the name of the game you want to update: ")
    if game_name in game_library:
        new_quantity = int(input("Enter the new quantity: "))
        new_cost = float(input("Enter the new cost: "))
        game_library[game_name]['quantity'] = new_quantity
        game_library[game_name]['cost'] = new_cost
        print(f"Game details updated successfully for '{game_name}'.")
    else:
        print(f"Game '{game_name}' not found in the library.")
    input("Press Enter to continue...\n")

# Admin menu
def admin_menu():
    while True:
        print("\n" + "=" * 12 + " ADMIN MENU " + "=" * 12)
        print("1. Update game details\n2. Logout")
        print("=" * 37)
        choice = input("Enter your choice: ")
        
        match choice:
            case '1':
                admin_update_game()
            case '2':
                print("Logged out.")
                break
            case _:
                print("Invalid choice.")
                input("Press Enter to continue...\n")

# Function for users to redeem points for a free game rental
def redeem_free_rental(username):
    try:
        print("=" * 37)
        points = user_accounts[username]['points']
        if points >= 3:  # Check if the user has enough points to redeem a free rental
            free_rentals = points // 3
            print(f"You have enough points to redeem {free_rentals} free game rental(s).")
            confirm = input("Do you want to redeem a free game rental? (yes/no): ").lower()
            if confirm == 'yes':
                # Ask the user to choose a game from the available games
                print("Choose a game to rent for free:")
                display_available_games()
                game_choice = input("Enter the name of the game: ").title()
                if game_choice in game_library and game_library[game_choice]['quantity'] > 0: 
                    game_library[game_choice]['quantity'] -= 1 # Rent the game for free
                    user_accounts[username]['points'] -= 3  # Minus points 
                    user_accounts[username]['inventory'].append(game_choice)
                    print(f"Game '{game_choice}' rented successfully for free by {username}!")
                else:
                    print(f"Sorry, '{game_choice}' is not available for rental.")
            else:
                print("Redemption cancelled.")
        else:
            print("You do not have enough points to redeem a free game rental.")
    except KeyError:
        print("An error occurred while processing your request.")
    input("Press Enter to continue...\n")


# Function to display game inventory
def display_game_inventory():
    print("=" * 37) 
    print("Game Inventory")
    i = 1
    for game, details in game_library.items():
        print(f"{i}: {game}\n\tQuantity: {details['quantity']}\n\tCost: ${details['cost']}\n")
        i += 1
    input("Press Enter to continue...\n")

# Function to handle user's logged-in menu
def logged_in_menu(username):
    while True:
        print("\n" + "=" * 13 + " LOGGED IN MENU " + "=" * 13)
        print("1. User Inventory\n2. Game Inventory\n3. Top Up\n4. Rent Game\n5. Return Game\n6. Redeem Free Rental\n7. Log Out")
        print("=" * 37)
        user_input = input("Enter your choice: ")

        match user_input:
            case '1':
                display_inventory(username)
            case '2':
                display_game_inventory()
            case '3':
                top_up_account(username)
            case '4':
                rent_game(username)
            case '5':
                return_game(username)
            case '6':
                redeem_free_rental(username)
            case '7':
                print("Logged out.")
                break
            case _:
                print("Invalid choice. Please try again.")
                input("Press Enter to continue...\n")

# Main function to run the program
def main():
    try:
        while True:
            print("=" * 6 + " VIDEO GAME RENTAL SYSTEM " + "=" * 5)
            print("1. Available Games\n2. Login\n3. Register\n4. Admin Login\n5. Exit")
            print("=" * 37)
            user_input = input("Enter your choice: ")

            match user_input:
                case '1':
                    display_available_games()
                case '2':
                    log_in()
                case '3':
                    register_user()
                case '4':
                    admin_login()
                case '5':
                    print("SYSTEM CLOSED")
                    break
                case _:
                    print("Invalid choice.")
                    input("Press Enter to continue...\n")
    except Exception as e:
        print("An error occurred:", e)
        
if __name__ == "__main__":
    main()
