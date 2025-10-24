import tkinter as tk
from tkinter import messagebox, simpledialog

# Coffee data
MENU = {
    "Espresso": {"ingredients": {"water": 50, "coffee": 18}, "cost": 1.5},
    "Latte": {"ingredients": {"water": 200, "milk": 150, "coffee": 24}, "cost": 2.5},
    "Cappuccino": {"ingredients": {"water": 250, "milk": 100, "coffee": 24}, "cost": 3.0},
}

resources = {"water": 300, "milk": 200, "coffee": 100}
profit = 0


# ----- FUNCTIONS -----
def update_status():
    """Refresh the status label with current resources and profit."""
    status_text = (
        f"Water: {resources['water']}ml | Milk: {resources['milk']}ml | "
        f"Coffee: {resources['coffee']}g | Profit: ${profit:.2f}"
    )
    status_label.config(text=status_text)


def is_resource_sufficient(ingredients):
    """Check if enough resources are available."""
    for item, amount in ingredients.items():
        if resources.get(item, 0) < amount:
            messagebox.showerror("Not Enough Resources", f"Sorry, not enough {item}.")
            return False
    return True


def process_coins(drink):
    """Ask user for coins using dialogs and return total inserted."""
    total = 0
    try:
        quarters = simpledialog.askinteger("Coins", "How many quarters ($0.25)?", minvalue=0)
        dimes = simpledialog.askinteger("Coins", "How many dimes ($0.10)?", minvalue=0)
        nickels = simpledialog.askinteger("Coins", "How many nickels ($0.05)?", minvalue=0)
        pennies = simpledialog.askinteger("Coins", "How many pennies ($0.01)?", minvalue=0)
        total = (quarters * 0.25) + (dimes * 0.10) + (nickels * 0.05) + (pennies * 0.01)
    except TypeError:
        messagebox.showinfo("Cancelled", "Transaction cancelled.")
        return None
    return total


def make_coffee(drink_name, ingredients):
    """Deduct ingredients and serve coffee."""
    for item in ingredients:
        resources[item] -= ingredients[item]
    messagebox.showinfo("Enjoy!", f"☕ Your {drink_name} is ready!")
    update_status()


def order_coffee(drink_name):
    """Handle full coffee purchase flow."""
    global profit
    drink = MENU[drink_name]

    if not is_resource_sufficient(drink["ingredients"]):
        return

    cost = drink["cost"]
    messagebox.showinfo("Order", f"{drink_name} costs ${cost:.2f}")

    payment = process_coins(drink_name)
    if payment is None:
        return

    if payment >= cost:
        change = round(payment - cost, 2)
        if change > 0:
            messagebox.showinfo("Change", f"Here is ${change:.2f} in change.")
        profit += cost
        make_coffee(drink_name, drink["ingredients"])
    else:
        messagebox.showwarning("Insufficient Funds", "Sorry, not enough money. Money refunded.")


def restock():
    """Refill all resources."""
    resources["water"] = 300
    resources["milk"] = 200
    resources["coffee"] = 100
    messagebox.showinfo("Restocked", "Machine refilled successfully!")
    update_status()


def turn_off():
    """Close the machine."""
    window.destroy()


# ----- GUI SETUP -----
window = tk.Tk()
window.title("☕ Coffee Vending Machine")
window.geometry("400x350")
window.config(bg="#f5e6ca")

# Title
title_label = tk.Label(window, text="Coffee Vending Machine", font=("Arial", 18, "bold"), bg="#f5e6ca")
title_label.pack(pady=10)

# Coffee buttons
button_frame = tk.Frame(window, bg="#f5e6ca")
button_frame.pack(pady=10)

for drink in MENU:
    btn = tk.Button(
        button_frame,
        text=f"{drink} (${MENU[drink]['cost']})",
        font=("Arial", 12),
        width=15,
        bg="#d6a77a",
        command=lambda d=drink: order_coffee(d),
    )
    btn.pack(pady=5)

# Control buttons
control_frame = tk.Frame(window, bg="#f5e6ca")
control_frame.pack(pady=10)

tk.Button(control_frame, text="🔄 Restock", command=restock, bg="#b0e0a8", width=10).grid(row=0, column=0, padx=5)
tk.Button(control_frame, text="❌ Turn Off", command=turn_off, bg="#e08c8c", width=10).grid(row=0, column=1, padx=5)

# Status label
status_label = tk.Label(window, text="", font=("Arial", 10, "italic"), bg="#f5e6ca")
status_label.pack(pady=10)
update_status()

window.mainloop()
