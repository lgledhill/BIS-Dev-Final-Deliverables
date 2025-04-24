"""
Application: Mamaka Bowls Ordering System
Developer: Code Runners
Date: 4/18/2025
Purpose: A system that allows users to order food items from Mamaka Bowls and calculates the total cost.
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import os  # Import the os module
import random
import re  # For phone number validation

class ImageManager:
    def __init__(self, image_folder='images', size=(80, 80)):
        self.image_folder = image_folder
        self.default_size = size  # Store the default size
        self.images = {}
        self.load_images()

    def load_images(self):
        for filename in os.listdir(self.image_folder):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                name = os.path.splitext(filename)[0].lower()
                path = os.path.join(self.image_folder, filename)
                try:
                    image = Image.open(path)
                    image.thumbnail(self.default_size)  # Use the default size
                    self.images[name] = ImageTk.PhotoImage(image)
                except Exception as e:
                    print(f'Failed to load {filename}: {e}')

    def get_image(self, key, size=None):
        """
        Gets an image by key. Allows specifying a different size.

        Args:
            key (str): The key of the image.
            size (tuple, optional): The size to resize the image to. Defaults to None.
        """
        image = self.images.get(key.lower())
        if image and size:
            try:
                original_image = Image.open(os.path.join(self.image_folder, f"{key.lower()}.png")) # added .png
                resized_image = original_image.resize(size, Image.LANCZOS)
                return ImageTk.PhotoImage(resized_image)
            except Exception as e:
                print(f"Error resizing image {key}: {e}")
                return image  # Return the original image if resizing fails
        return image
    
class MamakaBowlsApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mamaka Bowls Online Ordering System")
        self.geometry("500x700")
        self.configure(bg="#e0f7fa")

        self.style = ttk.Style(self)
        self.style.theme_use("default")

        self.style.configure("TLabel", foreground="black", background="#e0f7fa", font=('Helvetica', 10, 'bold'))
        self.style.configure("TButton", foreground="black", background="#b0e0e6", font=('Helvetica', 10, 'bold'))
        self.style.configure("TEntry", foreground="black", background="white")
        self.style.configure("Lightblue.TFrame", background="#e0f7fa")

        self.image_manager = ImageManager()
        self.image_aliases = {
            'larry bowl': 'larry',
            'bean bowl': 'bean',
            'bro bowl': 'bro',
            'mamaka bowl': 'mamaka',
            'mamaka': 'mamakasmo',
            'larry': 'larrysmo',
            'bean': 'beansmo',
            'bro': 'brosmo',
        }
        self.menu_items = {
            "Bowls": [
                {"name": "Mamaka Bowl", "sizes": {"Small": 9.50, "Regular": 11.00}},
                {"name": "Larry Bowl", "sizes": {"Small": 9.50, "Regular": 11.00}},
                {"name": "Bean Bowl", "sizes": {"Small": 9.50, "Regular": 11.00}},
                {"name": "Bro Bowl", "sizes": {"Small": 9.50, "Regular": 11.00}},
            ],
            "Smoothies": [
                {"name": "Mamaka", "price": 6.50},
                {"name": "Larry", "price": 6.50},
                {"name": "Bean", "price": 6.50},
                {"name": "Bro", "price": 6.50},  # Flat rate for smoothies
            ],
            "Coffee": [
                {"name": "Latte", "price": 4.75},
                {"name": "Cappuccino", "price": 4.50},
                {"name": "Americano", "price": 3.50},
                {"name": "Matcha", "price": 5.00},
            ],
            "Tacos": [
                {"name": "Breakfast Tacos", "price": 3.25}, # Only option for tacos
            ],
            "Add-ons": [
                {"name": "Strawberry", "price": 0.50},
                {"name": "Peanut Butter", "price": 0.50},
                {"name": "Agave", "price": 0.50},
                {"name": "Coconut Flakes", "price": 0.50},
                {"name": "Chia Seeds", "price": 0.50},
                {"name": "Bananas", "price": 0.50},
            ]
        }

        self.cart = []
        self.customer_info = {}
        self.payment_info = {}
        self.order_id = None

        self.create_home_page()

    def clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()
    
    def display_logo(self, parent):
        logo = self.image_manager.get_image('logo', size=(150, 150))  # Increased size for logo
        if logo:
            logo_label = tk.Label(parent, image=logo, bg='#e0f7fa')
            logo_label.image = logo
            logo_label.pack(pady=(10, 0))

    # ---------------------- Home Page ----------------------
    def create_home_page(self):
        """
        Displays the home page with category selection and checkout options.
        """
        self.clear_frame()
        home_frame = ttk.Frame(self, padding="20", style="Lightblue.TFrame")
        home_frame.pack(fill="both", expand=True)

        self.display_logo(home_frame)

        title_label = ttk.Label(home_frame, text="Welcome to Mamaka Bowls!", font=("Helvetica", 16, "bold"), style="TLabel")
        title_label.pack(pady="20")

        category_label = ttk.Label(home_frame, text="Select a category:", style="TLabel")
        category_label.pack(pady="10")

        categories_frame = ttk.Frame(home_frame, style="Lightblue.TFrame")
        categories_frame.pack()

        #  Add buttons for each category
        for category in ["Bowls", "Smoothies", "Coffee", "Tacos"]: # Removed Add-ons
            category_button = ttk.Button(categories_frame, text=category, command=lambda c=category: self.show_menu(c), style="TButton")
            category_button.pack(side="left", padx="10")

        footer_frame = ttk.Frame(home_frame, style="Lightblue.TFrame")
        footer_frame.pack(side="bottom", fill="x")

        back_button = ttk.Button(footer_frame, text="Home", command=self.create_home_page, style="TButton")
        back_button.pack(side="left", padx=(0, 10), pady=10)
        checkout_button = ttk.Button(footer_frame, text="Checkout", command=self.go_to_customer_info, style="TButton")
        checkout_button.pack(side="right", padx=(10, 0), pady=10)

    # ---------------------- Menu Page ----------------------
    def show_menu(self, category):
        self.clear_frame()
        menu_frame = ttk.Frame(self, padding="20", style="Lightblue.TFrame")
        menu_frame.pack(fill="both", expand=True)

        self.display_logo(menu_frame)

        title_label = ttk.Label(menu_frame, text=f"{category} Menu", font=("Helvetica", 16, "bold"), style="TLabel")
        title_label.pack(pady="20")

        back_button = ttk.Button(menu_frame, text="Home", command=self.create_home_page, style="TButton")
        back_button.pack(anchor="nw")

        if category == "Bowls":
            prices_label = ttk.Label(menu_frame, text="Small: $9.50, Regular: $11.00", foreground="red", anchor="center", style="TLabel")
            prices_label.pack(pady="10")

        # Display menu items based on the category
        for item in self.menu_items[category]:
            item_frame = ttk.Frame(menu_frame, style="Lightblue.TFrame")
            item_frame.pack(pady="10", fill="x")

            item_key = item["name"].lower().strip()
            item_key = self.image_aliases.get(item_key, item_key.replace(" ", ""))

            if category == "Coffee" and item["name"].lower() == "matcha":
                image = self.image_manager.get_image("matcha")
            elif category == "Coffee":
                image = self.image_manager.get_image("coffee")
            elif category == "Tacos":
                image = self.image_manager.get_image("taco")
            else:
                image = self.image_manager.get_image(item_key)

            if image:
                img_label = tk.Label(item_frame, image=image, bg="#e0f7fa")
                img_label.image = image
                img_label.pack(side="left")


            name_label = ttk.Label(item_frame, text=item["name"], width=20, anchor="w", style="TLabel")
            name_label.pack(side="left", padx='5')
            # Display price, handling cases where price is directly available or within 'sizes'
            if "sizes" in item:
                size_options = list(item["sizes"].keys())  # Get the size names
                size_var = tk.StringVar()
                size_var.set(size_options[0])  # Default size
                size_dropdown = ttk.OptionMenu(item_frame, size_var, size_options[0], *size_options)
                size_dropdown.pack(side="right", padx="10")

                add_to_cart_button = ttk.Button(item_frame, text="Add to Cart",
                                                 command=lambda selected_item=item, size_var=size_var, category=category: self.handle_add_to_cart(selected_item, category, size_var.get()),
                                                 style="TButton")
                add_to_cart_button.pack(side="right", padx="10")
            else:
                price_label = ttk.Label(item_frame, text=f"${item['price']:.2f}", width=10, anchor="e", style="TLabel")
                price_label.pack(side="right")
                add_to_cart_button = ttk.Button(item_frame, text="Add to Cart",
                                                 command=lambda selected_item=item, category=category: self.handle_add_to_cart(selected_item, category),
                                                 style="TButton")
                add_to_cart_button.pack(side="right", padx="10")

        footer_frame = ttk.Frame(menu_frame, style="Lightblue.TFrame")
        footer_frame.pack(side="bottom", fill="x")
        back_button = ttk.Button(footer_frame, text="Home", command=self.create_home_page, style="TButton")
        back_button.pack(side="left", padx=(0, 10), pady=10)
        checkout_button = ttk.Button(footer_frame, text="Checkout", command=self.go_to_customer_info, style="TButton")
        checkout_button.pack(side="right", padx=(10, 0), pady=10)

    # ---------------------- Add-ons Page ----------------------
    def show_add_ons(self, selected_item, size="Regular"):
        """
        Displays the add-ons selection page for a selected item.

        Args:
        selected_item (dict): The item to add add-ons to.
        size (str): Size of the item to use for correct pricing.
        """
        self.clear_frame()
        add_ons_frame = ttk.Frame(self, padding="20", style="Lightblue.TFrame")
        add_ons_frame.pack(fill="both", expand=True)

        title_label = ttk.Label(add_ons_frame, text="Select Add-ons", font=("Helvetica", 16, "bold"), style="TLabel")
        title_label.pack(pady="20")

        back_button = ttk.Button(add_ons_frame, text="Back to Menu",
                                 command=lambda: self.show_menu("Bowls"),
                                 style="TButton")
        back_button.pack(anchor="nw")

        self.selected_addons = []
        for addon in self.menu_items["Add-ons"]:
            addon_frame = ttk.Frame(add_ons_frame, style="Lightblue.TFrame")
            addon_frame.pack(pady="5", fill="x")
            checkbox_var = tk.BooleanVar()
            checkbox = tk.Checkbutton(addon_frame, text=addon["name"], variable=checkbox_var, bg="#e0f7fa", fg="black")
            checkbox.pack(side="left")
            price_label = ttk.Label(addon_frame, text=f"${addon['price']:.2f}", width=10, anchor="e", style="TLabel")
            price_label.pack(side="right")
            addon["checkbox_var"] = checkbox_var

        add_to_cart_button = ttk.Button(add_ons_frame, text="Add to Cart",
                                     command=lambda: self.add_to_cart(selected_item, size=size),
                                     style="TButton")
        add_to_cart_button.pack(pady="20")

        footer_frame = ttk.Frame(add_ons_frame, style="Lightblue.TFrame")
        footer_frame.pack(side="bottom", fill="x")
        back_button = ttk.Button(footer_frame, text="Home", command=self.create_home_page, style="TButton")
        back_button.pack(side="left", padx=(0, 10), pady=10)
        checkout_button = ttk.Button(footer_frame, text="Checkout", command=self.go_to_customer_info, style="TButton")
        checkout_button.pack(side="right", padx=(10, 0), pady=10)


    # ---------------------- Add to Cart Function ----------------------
    def handle_add_to_cart(self, selected_item, category, size="Regular", coffee_option=None):
        """
        Handles the add-to-cart process, showing add-ons if applicable, or directly adding to cart.

        Args:
        selected_item (dict): The item to add to the cart.
        category (str): The category of the item.
        size (str, optional): The size of the item (for bowls). Defaults to "Regular".
        coffee_option (str, optional): The selected coffee option. Defaults to None.
        """
        if category in ["Bowls", "Smoothies"]:
            self.show_add_ons(selected_item, size=size)  # Pass selected size
        elif category == "Coffee":
            self.add_to_cart(selected_item, size=coffee_option)
        else:
            self.add_to_cart(selected_item, size)


    def add_to_cart(self, selected_item, size="Regular"):
        """
        Adds the selected item and add-ons to the shopping cart.

        Args:
            selected_item (dict): The item to add to the cart.
            size (str): The size of the item (e.g., "Small", "Regular", "Latte").
        """
        selected_addons = []
        for addon in self.menu_items["Add-ons"]:
            if "checkbox_var" in addon and addon["checkbox_var"].get():
                selected_addons.append(addon["name"])

        #  Use size pricing if available, otherwise fall back to fixed item price
        if "sizes" in selected_item:
            price = selected_item["sizes"].get(size, selected_item["sizes"]["Regular"])
        else:
            price = selected_item["price"]

        total_price = price + len(selected_addons) * 0.50

        self.cart.append({
            "name": selected_item["name"],
            "size": size,
            "price": total_price,
            "addons": selected_addons,
            "quantity": 1
        })
        messagebox.showinfo("Added to Cart", f"{selected_item['name']} ({size}) with selected add-ons has been added to your cart.")
        self.create_home_page()

    # ---------------------- Customer Info Page ----------------------
    def go_to_customer_info(self):
        """
        Displays the customer information entry form.
        """
        if not self.cart:  # Check if the cart is empty
            messagebox.showerror("Error", "Please add items to your cart before proceeding to checkout.")
            return  # Stop the checkout process
        
        self.clear_frame()
        customer_info_frame = ttk.Frame(self, padding="20", style="Lightblue.TFrame")
        customer_info_frame.pack(fill="both", expand=True)

        title_label = ttk.Label(customer_info_frame, text="Customer Information", font=("Helvetica", 16, "bold"), style="TLabel")
        title_label.pack(pady="20")

        first_name_label = ttk.Label(customer_info_frame, text="First Name:", style="TLabel")
        first_name_label.pack(anchor="w")
        self.first_name_entry = ttk.Entry(customer_info_frame)
        self.first_name_entry.pack(fill="x")

        last_name_label = ttk.Label(customer_info_frame, text="Last Name:", style="TLabel")
        last_name_label.pack(anchor="w")
        self.last_name_entry = ttk.Entry(customer_info_frame)
        self.last_name_entry.pack(fill="x")

        phone_label = ttk.Label(customer_info_frame, text="Phone Number (10-digit format):", style="TLabel")
        phone_label.pack(anchor="w")
        self.phone_entry = ttk.Entry(customer_info_frame)
        self.phone_entry.pack(fill="x")

        email_label = ttk.Label(customer_info_frame, text="Email:", style="TLabel")
        email_label.pack(anchor="w")
        self.email_entry = ttk.Entry(customer_info_frame)
        self.email_entry.pack(fill="x")

        next_button = ttk.Button(customer_info_frame, text="Next", command=self.validate_customer_info, style="TButton")
        next_button.pack(pady="20")

        footer_frame = ttk.Frame(customer_info_frame, style="Lightblue.TFrame")
        footer_frame.pack(side="bottom", fill="x")
        back_button = ttk.Button(footer_frame, text="Home", command=self.create_home_page, style="TButton")
        back_button.pack(side="left", padx=(0, 10), pady=10)
        checkout_button = ttk.Button(footer_frame, text="Checkout", command=self.go_to_customer_info, style="TButton")
        checkout_button.pack(side="right", padx=(10, 0), pady=10)

    def validate_customer_info(self):
        """
        Validates the customer information entered by the user.
        Displays an error message if any field is invalid.
        """
        first_name = self.first_name_entry.get().strip()
        last_name = self.last_name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()

        if not first_name or not last_name or not phone or not email:
            messagebox.showerror("Error", "All fields are required.")
            return

        if not re.match(r"^\d{10}$", phone):
            messagebox.showerror("Error", "Invalid phone number format. Please use 10-digit format.")
            return

        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
            messagebox.showerror("Error", "Invalid email address.")
            return

        self.customer_info = {
            "first_name": first_name,
            "last_name": last_name,
            "phone": phone,
            "email": email
        }
        self.go_to_payment_info()

    # ---------------------- Payment Info Page ----------------------
    def go_to_payment_info(self):
        """
        Displays the payment information entry form.
        """
        self.clear_frame()
        payment_info_frame = ttk.Frame(self, padding="20", style="Lightblue.TFrame")
        payment_info_frame.pack(fill="both", expand=True)

        title_label = ttk.Label(payment_info_frame, text="Payment Information", font=("Helvetica", 16, "bold"), style="TLabel")
        title_label.pack(pady="20")

        full_name_label = ttk.Label(payment_info_frame, text="Full Name on Card:", style="TLabel")
        full_name_label.pack(anchor="w")
        self.full_name_entry = ttk.Entry(payment_info_frame)
        self.full_name_entry.pack(fill="x")

        card_number_label = ttk.Label(payment_info_frame, text="Card Number:", style="TLabel")
        card_number_label.pack(anchor="w")
        self.card_number_entry = ttk.Entry(payment_info_frame)
        self.card_number_entry.pack(fill="x")

        cvv_label = ttk.Label(payment_info_frame, text="CVV:", style="TLabel")
        cvv_label.pack(anchor="w")
        self.cvv_entry = ttk.Entry(payment_info_frame)
        self.cvv_entry.pack(fill="x")

        expiration_date_label = ttk.Label(payment_info_frame, text="Expiration Date (MM/YYYY):", style="TLabel")
        expiration_date_label.pack(anchor="w")
        self.expiration_date_entry = ttk.Entry(payment_info_frame)
        self.expiration_date_entry.pack(fill="x")

        next_button = ttk.Button(payment_info_frame, text="Next", command=self.validate_payment_info, style="TButton")
        next_button.pack(pady="20")

        footer_frame = ttk.Frame(payment_info_frame, style="Lightblue.TFrame")
        footer_frame.pack(side="bottom", fill="x")
        back_button = ttk.Button(footer_frame, text="Home", command=self.create_home_page, style="TButton")
        back_button.pack(side="left", padx=(0, 10), pady=10)
        checkout_button = ttk.Button(footer_frame, text="Checkout", command=self.go_to_customer_info, style="TButton")
        checkout_button.pack(side="right", padx=(10, 0), pady=10)

    def validate_payment_info(self):
        """
        Validates the payment information entered by the user.
        Displays an error message if any field is invalid.
        """
        full_name = self.full_name_entry.get().strip()
        card_number = self.card_number_entry.get().strip()
        cvv = self.cvv_entry.get().strip()
        expiration_date = self.expiration_date_entry.get().strip()

        if not full_name or not card_number or not cvv or not expiration_date:
            messagebox.showerror("Error", "All fields are required.")
            return

        if not re.match(r"^\d{16}$", card_number):
            messagebox.showerror("Error", "Invalid card number. Please use 16-digit format.")
            return

        if not re.match(r"^\d{3,4}$", cvv):
            messagebox.showerror("Error", "Invalid CVV. Please use 3 or 4 digits.")
            return

        if not re.match(r"^(0[1-9]|1[0-2])\/?(20)?\d{2}$", expiration_date):
            messagebox.showerror("Error", "Invalid expiration date. Please use MM/YYYY format.")
            return

        self.payment_info = {
            "full_name": full_name,
            "card_number": card_number,
            "cvv": cvv,
            "expiration_date": expiration_date
        }
        self.show_checkout()

    # ---------------------- Checkout Page ----------------------
    def show_checkout(self):
        """
        Displays the order summary and total, and allows the user to place the order.
        """
        self.clear_frame()
        checkout_frame = ttk.Frame(self, padding="20", style="Lightblue.TFrame")
        checkout_frame.pack(fill="both", expand=True)

        title_label = ttk.Label(checkout_frame, text="Checkout", font=("Helvetica", 16, "bold"), style="TLabel")
        title_label.pack(pady="20")

        order_summary_label = ttk.Label(checkout_frame, text="Order Summary:", font=("Helvetica", 12, "underline"), style="TLabel")
        order_summary_label.pack(anchor="w")

        total_price = 0
        for item in self.cart:
            item_frame = ttk.Frame(checkout_frame, style="Lightblue.TFrame")
            item_frame.pack(pady="5", fill="x")

            name_label = ttk.Label(item_frame, text=f"{item['name']} ({item['size']}) x {item['quantity']}", width=30, anchor="w", style="TLabel")
            name_label.pack(side="left")
            price_label = ttk.Label(item_frame, text=f"${item['price']:.2f}", width=10, anchor="e", style="TLabel")
            price_label.pack(side="right")
            if item['name'] in ["Mamaka Bowl", "Larry Bowl", "Bean Bowl", "Bro Bowl", "Mamaka", "Larry", "Bean", "Bro"]:
                addons_label = ttk.Label(item_frame, text=f"Add-ons: {', '.join(item['addons']) if item['addons'] else 'None'}",
                                             width=40, anchor="w", style="TLabel")
                addons_label.pack(side="left")
            total_price += item["price"]

        tax_rate = 0.0825
        tax_amount = total_price * tax_rate
        total_with_tax = total_price + tax_amount

        tax_label = ttk.Label(checkout_frame, text=f"Tax (8.25%): ${tax_amount:.2f}", style="TLabel")
        tax_label.pack(anchor="w")
        total_label = ttk.Label(checkout_frame, text=f"Total: ${total_with_tax:.2f}", font=("Helvetica", 12, "bold"), style="TLabel")
        total_label.pack(anchor="w")

        self.order_id = random.randint(100000, 999999)
        order_id_label = ttk.Label(checkout_frame, text=f"Order ID: {self.order_id}", font=("Helvetica", 12), style="TLabel")
        order_id_label.pack(anchor="w")

        place_order_button = ttk.Button(checkout_frame, text="Place Order", command=self.place_order, style="TButton")
        place_order_button.pack(pady="20")

        footer_frame = ttk.Frame(checkout_frame, style="Lightblue.TFrame")
        footer_frame.pack(side="bottom", fill="x")
        back_button = ttk.Button(footer_frame, text="Home", command=self.create_home_page, style="TButton")
        back_button.pack(side="left", padx=(0, 10), pady=10)
        checkout_button = ttk.Button(footer_frame, text="Checkout", command=self.go_to_customer_info, style="TButton")
        checkout_button.pack(side="right", padx=(10, 0), pady=10)

    # ---------------------- Place Order Function ----------------------
    def place_order(self):
        """
        Finalizes the order, displays a confirmation message, and clears the cart.
        """
        self.clear_frame()
        order_confirmation_frame = ttk.Frame(self, padding="20", style="Lightblue.TFrame")
        order_confirmation_frame.pack(fill="both", expand=True)

        self.display_logo(order_confirmation_frame)

        title_label = ttk.Label(order_confirmation_frame, text="Order Confirmed!", font=("Helvetica", 20, "bold"), foreground="red", style="TLabel")
        title_label.pack(pady="20")

        confirmation_label = ttk.Label(order_confirmation_frame, text=f"Your order has been placed successfully! Your Order ID is {self.order_id}.", style="TLabel")
        confirmation_label.pack(pady="10")

        number_label = ttk.Label(order_confirmation_frame, text=f"An order summary has been sent to {self.customer_info['phone']}.", style="TLabel")
        number_label.pack(pady="10")

        wait_time_label = ttk.Label(order_confirmation_frame, text="Estimated Wait Time: 15 Minutes", style="TLabel")
        wait_time_label.pack(pady="10")

        home_button = ttk.Button(order_confirmation_frame, text="Home", command=self.create_home_page, style="TButton")
        home_button.pack(pady="20")

        footer_frame = ttk.Frame(order_confirmation_frame, style="Lightblue.TFrame")
        footer_frame.pack(side="bottom", fill="x")
        back_button = ttk.Button(footer_frame, text="Home", command=self.create_home_page, style="TButton")
        back_button.pack(side="left", padx=(0, 10), pady=10)
        checkout_button = ttk.Button(footer_frame, text="Checkout", command=self.go_to_customer_info, style="TButton")
        checkout_button.pack(side="right", padx=(10, 0), pady=10)

    # Clear session state for new order
        self.cart = []
        self.customer_info = {}
        self.payment_info = {}
        self.order_id = None


    # ---------------------- Utility Function ----------------------
    def clear_frame(self):
        """
        Clears all widgets from the current frame.
        """
        for widget in self.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = MamakaBowlsApp()
    app.mainloop()

