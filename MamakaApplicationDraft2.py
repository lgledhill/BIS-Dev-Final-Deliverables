"""
Application: Mamaka Bowls Ordering System
Developer: Code Runners
Date: 4/14/2025
Purpose: A system that allows users to order food items from Mamaka Bowls and calculates the total cost.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import random
import re

TAX_RATE = 0.0825

class MamakaApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mamaka Bowls Online Ordering")
        self.geometry("800x600")
        self.configure(bg="#FAF3E0")
        self.cart = []
        self.customer_info = {}
        self.payment_info = {}
        self.frames = {}
        self.switch_frame(HomePage)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if hasattr(self, 'current_frame'):
            self.current_frame.destroy()
        self.current_frame = new_frame
        self.current_frame.pack(fill="both", expand=True)

class HomePage(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#FAF3E0")
        tk.Label(self, text="Welcome to Mamaka Bowls!", font=("Helvetica", 24, "bold"), bg="#FAF3E0").pack(pady=10)
        tk.Label(self, text="Choose a category:", font=("Helvetica", 16), bg="#FAF3E0").pack(pady=5)

        for category in ["Bowls", "Smoothies", "Coffee", "Food"]:
            tk.Button(self, text=category, font=("Helvetica", 14), width=20,
                      command=lambda c=category: master.switch_frame(lambda m=master: MenuPage(m, c))).pack(pady=5)

        tk.Button(self, text="Checkout", font=("Helvetica", 14), bg="#8DB596",
                  command=lambda: master.switch_frame(CustomerInfoPage)).pack(pady=20)

class MenuPage(tk.Frame):
    def __init__(self, master, category):
        super().__init__(master, bg="#FAF3E0")
        self.master = master
        self.category = category

        tk.Label(self, text=f"{category} Menu", font=("Helvetica", 20, "bold"), bg="#FAF3E0").pack(pady=10)

        items = {
            "Bowls": [("Mamaka", 9.50), ("The Larry", 11.00)],
            "Smoothies": [("The Bean Bowl", 8.50), ("The Bro", 10.00)],
            "Coffee": [("Cold Brew", 4.00), ("Latte", 5.00)],
            "Food": [("Avocado Toast", 7.50), ("Banana Bread", 3.00)]
        }

        for name, price in items.get(category, []):
            frame = tk.Frame(self, bg="#FFFFFF", pady=10, padx=10, relief="raised", bd=2)
            info = tk.Frame(frame, bg="#FFFFFF")
            tk.Label(info, text=f"{name}\n${price:.2f}", font=("Helvetica", 12), bg="#FFFFFF").pack(anchor="w")
            tk.Button(info, text="Customize",
                      command=lambda n=name, p=price: master.switch_frame(lambda m=master: CustomizationPage(m, n, p))).pack(anchor="w")
            info.pack(side="left", padx=10)
            frame.pack(pady=5, padx=20, fill="x")

        tk.Button(self, text="Back to Home", command=lambda: master.switch_frame(HomePage)).pack(pady=20)

class CustomizationPage(tk.Frame):
    def __init__(self, master, item_name, base_price):
        super().__init__(master, bg="#FAF3E0")
        self.master = master
        self.item_name = item_name
        self.base_price = base_price

        tk.Label(self, text=f"Customize: {item_name}", font=("Helvetica", 20, "bold"), bg="#FAF3E0").pack(pady=10)

        self.var_size = tk.StringVar()
        ttk.Label(self, text="Select Size:").pack()
        self.size_combo = ttk.Combobox(self, textvariable=self.var_size, values=["Small", "Regular"])
        self.size_combo.pack()

        self.var_quantity = tk.IntVar(value=1)
        ttk.Label(self, text="Quantity:").pack()
        ttk.Combobox(self, textvariable=self.var_quantity, values=list(range(1, 10))).pack()

        self.special_request = tk.Entry(self, width=40)
        ttk.Label(self, text="Special Requests:").pack()
        self.special_request.pack()

        self.check_vars = []
        ttk.Label(self, text="Add-ons ($0.50 each):").pack(pady=5)
        for topping in ["Strawberry", "Banana", "Almond Butter", "Coconut"]:
            var = tk.IntVar()
            self.check_vars.append((topping, var))
            ttk.Checkbutton(self, text=topping, variable=var).pack(anchor='w', padx=40)

        ttk.Button(self, text="Add to Cart", command=self.add_to_cart).pack(pady=20)
        ttk.Button(self, text="Back", command=lambda: master.switch_frame(HomePage)).pack()

    def add_to_cart(self):
        if not self.var_size.get():
            messagebox.showerror("Size Required", "Please select a size before adding to cart.")
            return
        selected_addons = [t for t, var in self.check_vars if var.get() == 1]
        total_price = self.base_price + len(selected_addons) * 0.50
        item = {
            "name": self.item_name,
            "size": self.var_size.get(),
            "quantity": self.var_quantity.get(),
            "addons": selected_addons,
            "special": self.special_request.get(),
            "price": total_price
        }
        self.master.cart.append(item)
        messagebox.showinfo("Added", f"{self.item_name} added to cart.")
        self.master.switch_frame(HomePage)

class CustomerInfoPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#FAF3E0")
        self.master = master
        self.entries = {}

        tk.Label(self, text="Customer Information", font=("Helvetica", 20, "bold"), bg="#FAF3E0").pack(pady=10)
        for label in ["First Name", "Last Name", "Phone", "Email"]:
            tk.Label(self, text=label, bg="#FAF3E0").pack()
            entry = tk.Entry(self)
            entry.pack()
            self.entries[label] = entry

        tk.Button(self, text="Next: Payment Info", bg="#8DB596", command=self.save_info).pack(pady=20)

    def save_info(self):
        for key, entry in self.entries.items():
            if not entry.get():
                messagebox.showerror("Missing Information", f"Please enter your {key}.")
                return
        self.master.customer_info = {key: entry.get() for key, entry in self.entries.items()}
        self.master.switch_frame(PaymentInfoPage)

class PaymentInfoPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#FAF3E0")
        self.master = master
        self.entries = {}

        vcmd = (self.register(self.validate_numeric), '%P')

        tk.Label(self, text="Payment Information", font=("Helvetica", 20, "bold"), bg="#FAF3E0").pack(pady=10)
        fields = [
            ("Card Holder Name", None),
            ("Card Number", vcmd),
            ("CVV", vcmd),
            ("Expiration Date (MMYY)", vcmd)
        ]
        for label, validate in fields:
            tk.Label(self, text=label, bg="#FAF3E0").pack()
            entry = tk.Entry(self, validate='key', validatecommand=validate) if validate else tk.Entry(self)
            entry.pack()
            self.entries[label] = entry

        tk.Button(self, text="Next: Checkout", bg="#8DB596", command=self.save_info).pack(pady=20)

    def validate_numeric(self, value):
        return re.fullmatch(r"\d*", value) is not None

    def save_info(self):
        for key, entry in self.entries.items():
            if not entry.get():
                messagebox.showerror("Missing Information", f"Please enter {key}.")
                return
        self.master.payment_info = {key: entry.get() for key, entry in self.entries.items()}
        self.master.switch_frame(CheckoutPage)

class CheckoutPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#FAF3E0")
        tk.Label(self, text="Review Your Order", font=("Helvetica", 20, "bold"), bg="#FAF3E0").pack(pady=10)

        subtotal = sum(item['price'] * item['quantity'] for item in master.cart)
        tax = subtotal * TAX_RATE
        total = subtotal + tax

        for item in master.cart:
            item_text = f"{item['quantity']}x {item['name']} ({item['size']}) - ${item['price']:.2f}"
            if item['addons']:
                item_text += f" | Add-ons: {', '.join(item['addons'])}"
            if item['special']:
                item_text += f" | Note: {item['special']}"
            tk.Label(self, text=item_text, bg="#FAF3E0").pack(anchor='w', padx=20)

        tk.Label(self, text=f"Subtotal: ${subtotal:.2f}\nTax: ${tax:.2f}\nTotal: ${total:.2f}", font=("Helvetica", 14), bg="#FAF3E0").pack(pady=10)
        tk.Button(self, text="Place Order", bg="#8DB596", command=lambda: master.switch_frame(ConfirmationPage)).pack()

class ConfirmationPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#FAF3E0")
        order_id = random.randint(1000, 9999)
        pickup_time = (datetime.datetime.now() + datetime.timedelta(minutes=15)).strftime("%I:%M %p")

        tk.Label(self, text="Order Confirmed!", font=("Helvetica", 20, "bold"), bg="#FAF3E0").pack(pady=10)
        tk.Label(self, text=f"Order ID: {order_id}", bg="#FAF3E0").pack()
        tk.Label(self, text=f"Pickup Time: {pickup_time}", bg="#FAF3E0").pack()
        tk.Label(self, text="A receipt will be sent to your phone.", bg="#FAF3E0").pack(pady=10)
        tk.Button(self, text="Back to Home", command=lambda: master.switch_frame(HomePage)).pack(pady=20)

if __name__ == "__main__":
    app = MamakaApp()
    app.mainloop()
