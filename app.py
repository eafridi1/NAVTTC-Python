# Coffee Vending Machine Simulation

MENU = {
    "espresso": {
        "ingredients": {"water": 50, "coffee": 18},
        "cost": 1.5,
    },
    "latte": {
        "ingredients": {"water": 200, "milk": 150, "coffee": 24},
        "cost": 2.5,
    },
    "cappuccino": {
        "ingredients": {"water": 250, "milk": 100, "coffee": 24},
        "cost": 3.0,
    }
}

resources = {
    "water": 300,
    "milk": 200,
    "coffee": 100,
}

profit = 0

def is_resource_sufficient(order_ingredients):
    """Returns True when order can be made, False if ingredients are insufficient."""
    for item in order_ingredients:
        if order_ingredients[item] > resources.get(item, 0):
            print(f"❌ Sorry, not enough {item}.")
            return False
    return True

def process_coins():
    """Returns the total calculated from coins inserted."""
    print("🪙 Please insert coins.")
    total = int(input("How many quarters? ")) * 0.25
    total += int(input("How many dimes? ")) * 0.10
    total += int(input("How many nickels? ")) * 0.05
    total += int(input("How many pennies? ")) * 0.01
    return total

def transaction_successful(money_received, drink_cost):
    """Return True when payment is accepted, False if not enough money."""
    global profit
    if money_received >= drink_cost:
        change = round(money_received - drink_cost, 2)
        print(f"💰 Here is ${change} in change.")
        profit += drink_cost
        return True
    else:
        print("❌ Sorry, that's not enough money. Money refunded.")
        return False

def make_coffee(drink_name, order_ingredients):
    """Deduct the required ingredients from resources."""
    for item in order_ingredients:
        resources[item] -= order_ingredients[item]
    print(f"☕ Here is your {drink_name}. Enjoy!\n")

def report():
    """Prints a report of current resources and profit."""
    print("\n📋 Machine Report:")
    for item, amount in resources.items():
        unit = "ml" if item != "coffee" else "g"
        print(f"{item.capitalize()}: {amount}{unit}")
    print(f"Profit: ${profit}\n")

def coffee_machine():
    is_on = True
    while is_on:
        choice = input("What would you like? (espresso/latte/cappuccino): ").lower()
        if choice == "off":
            print("👋 Shutting down. Goodbye!")
            is_on = False
        elif choice == "report":
            report()
        elif choice in MENU:
            drink = MENU[choice]
            if is_resource_sufficient(drink["ingredients"]):
                payment = process_coins()
                if transaction_successful(payment, drink["cost"]):
                    make_coffee(choice, drink["ingredients"])
        else:
            print("❌ Invalid selection. Please try again.")

# Run the coffee machine
if __name__ == "__main__":
    coffee_machine()
