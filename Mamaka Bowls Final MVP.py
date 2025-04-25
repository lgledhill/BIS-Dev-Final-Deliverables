"""
Application:    Mamaka Bowls Ordering System
Developer:      Code Runners
Date:           4/22/2025
Purpose:        A system that allows users to order food items from Mamaka Bowls and calculates the total cost.
"""
#Importing libraries
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk #importing image manager
import os, random, re #importing os for file handling, random for the order id, and re for input validation

#This class will be used to hold the images load them when they are called
class ImageManager: 
    def __init__(self, image_folder='images', size=(80, 80)):
        self.image_folder = image_folder
        self.default_size = size
        self.images = {}
        self.load_images()

    #loading images from the given folder
    def load_images(self): 
        for filename in os.listdir(self.image_folder):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                name = os.path.splitext(filename)[0].lower()
                path = os.path.join(self.image_folder, filename)
                try:
                    image = Image.open(path)
                    image.thumbnail(self.default_size)
                    self.images[name] = ImageTk.PhotoImage(image)
                except Exception as e:
                    print(f'Failed to load {filename}: {e}')

    #Retrieve and resizing images
    def get_image(self, key, size=None): 
        image = self.images.get(key.lower())
        if image and size:
            try:
                original_image = Image.open(os.path.join(self.image_folder, f"{key.lower()}.png"))
                resized_image = original_image.resize(size, Image.LANCZOS)
                return ImageTk.PhotoImage(resized_image)
            except Exception as e:
                print(f"Error resizing image {key}: {e}")
                return image
        return image

#Main application class
class MamakaBowlsApp(tk.Tk): 
    def __init__(self):
        super().__init__() 
        self.title("Mamaka Bowls Online Ordering System")
        self.geometry("500x750") 
        self.configure(bg="lightblue") 

        self.custom_font = ("Segoe UI", 11)
        self.style = ttk.Style(self)
        self.style.theme_use("default")
        self.style.configure("TLabel", font=self.custom_font, background="lightblue")
        self.style.configure("TButton", font=self.custom_font, padding=6, background="lightblue")
        self.style.configure("TFrame", background="lightblue") 
        #Defining the fonts and theme styles

        self.image_manager = ImageManager()

        #Assigning item names to image filenames
        self.image_aliases = { 
            'larry bowl': 'larry',
            'bean bowl': 'bean',
            'bro bowl': 'bro',
            'mamaka bowl': 'mamaka',
            'mamaka': 'mamakasmo',
            'larry': 'larrysmo',
            'bean': 'beansmo',
            'bro': 'brosmo',
            'matcha': 'matcha',
            'latte': 'coffee',
            'cappuccino': 'coffee',
            'americano': 'coffee',
            'breakfast tacos': 'taco'
        } 

        self.menu_items = { #Defining the different menu items to their categories
            "Bowls": ["Mamaka Bowl", "Larry Bowl", "Bean Bowl", "Bro Bowl"],
            "Smoothies": ["Mamaka", "Larry", "Bean", "Bro"],
            "Coffee": ["Latte", "Cappuccino", "Americano", "Matcha"],
            "Tacos": ["Breakfast Tacos"]
        }

        self.add_ons = ["Strawberry", "Peanut Butter", "Agave", "Coconut Flakes", "Chia Seeds", "Bananas"] #List for the add-ons

        self.bowl_prices = { #Dictionary to assign prices to the sizes of the bowls
            "Small": 9.50,
            "Regular": 11.00
        }

        self.prices = { #Assigning prices to the different menu items
            "Mamaka": 6.50,
            "Larry": 6.50,
            "Bean": 6.50,
            "Bro": 6.50,
            "Latte": 4.75,
            "Cappuccino": 4.50,
            "Americano": 3.50,
            "Matcha": 5.00,
            "Breakfast Tacos": 3.25,
            "Strawberry": 0.50,
            "Peanut Butter": 0.50,
            "Agave": 0.50,
            "Coconut Flakes": 0.50,
            "Chia Seeds": 0.50,
            "Bananas": 0.50
        }

        #Cart and order data holders
        self.cart = {}
        self.customer_info = {}
        self.payment_info = {}
        self.order_id = None
        self.current_category = None
        self.selected_addons = []
        self.selected_bowl_size = tk.StringVar(value="Regular") 
        #Loading the main home page
        self.create_home_page()

    #Function to clear all widgets from the window
    def clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()

    #displaying the logo on the given frame
    def display_logo(self, parent):
        logo = self.image_manager.get_image("logo", size=(120, 120))
        if logo:
            logo_label = tk.Label(parent, image=logo, bg="lightblue")
            logo_label.image = logo
            logo_label.pack(pady=(0, 10))

    #Creating the footer with the navigation buttons
    def create_footer(self, parent):
        footer = ttk.Frame(parent, style="TFrame")
        footer.pack(side="bottom", fill="x", pady=10)
        ttk.Button(footer, text="🏠 Home", command=self.create_home_page).pack(side="left", padx=10)
        ttk.Button(footer, text="🛒 View Cart", command=self.view_cart_page).pack(side="right", padx=10)
        ttk.Button(footer, text="❓ FAQ", command=self.show_faq_page).pack(side="right", padx=10)

    #Displaying the home screen with the category buttons
    def create_home_page(self):
        self.clear_frame()
        frame = ttk.Frame(self, padding=20, style="TFrame")
        frame.pack(fill="both", expand=True)

        self.display_logo(frame)
        ttk.Label(frame, text="Welcome to Mamaka Bowls!", font=("Segoe UI", 16, "bold"), style="TLabel").pack(pady=20)

        #icons for the buttons
        emoji_icons = {
            "Bowls": "🥣",
            "Smoothies": "🥤",
            "Coffee": "☕",
            "Tacos": "🌮"
        }

        for category in self.menu_items:
            icon = emoji_icons.get(category, "")
            display_text = f"{icon} {category}"
            ttk.Button(frame, text=display_text, command=lambda c=category: self.show_menu_page(c)).pack(pady=8, ipadx=10)

        self.create_footer(frame)

    def show_menu_page(self, category):
        self.clear_frame()
        self.current_category = category
        frame = ttk.Frame(self, padding=20, style="TFrame")
        frame.pack(fill="both", expand=True)

        self.display_logo(frame)
        ttk.Label(frame, text=f"{category} Menu", font=("Segoe UI", 16, "bold"), style="TLabel").pack(pady=10)

        if category == "Bowls":
            # Show pricing information in red under the header
            ttk.Label(frame, text="Small: $9.50   Regular: $11.00", foreground="red", font=("Segoe UI", 11, "bold"), style="TLabel").pack(pady=(0, 10))

        for name in self.menu_items[category]:
            card = ttk.Frame(frame, relief="ridge", borderwidth=2, padding=8, style="TFrame")
            card.pack(fill="x", pady=5)

            alias = self.image_aliases.get(name.lower(), name.lower().replace(" ", ""))
            image = self.image_manager.get_image(alias)
            if image:
                img_label = tk.Label(card, image=image, bg="lightblue")
                img_label.image = image
                img_label.pack(side="left")

            info_frame = ttk.Frame(card, style="TFrame")
            info_frame.pack(side="left", padx=10, fill="x", expand=True)

            ttk.Label(info_frame, text=f"{name}", style="TLabel").pack(anchor="w")

            if category == "Bowls":
                ttk.Label(info_frame, text="Select Size:", style="TLabel").pack(anchor="w")
                size_menu = ttk.OptionMenu(info_frame, self.selected_bowl_size, "Regular", *self.bowl_prices.keys())
                size_menu.pack(anchor="w")
            else:
                price = self.prices[name]
                ttk.Label(info_frame, text=f"Price: ${price:.2f}", style="TLabel").pack(anchor="w")

            # Move Add to Cart button to right side (its own vertical column)
            button_frame = ttk.Frame(card, style="TFrame")
            button_frame.pack(side="right", padx=5)
            ttk.Button(button_frame, text="➕ Add to Cart", command=lambda n=name: self.show_add_ons(n) if category in ["Bowls", "Smoothies"] else self.quick_add_to_cart(n)).pack(ipadx=4, ipady=3)

        self.create_footer(frame)

    #Function to hold the add-ons 
    def show_add_ons(self, item_name):
        self.clear_frame()
        self.selected_item = item_name
        self.selected_addons = []
        frame = ttk.Frame(self, padding=20, style="TFrame")
        frame.pack(fill="both", expand=True)

        self.display_logo(frame)
        ttk.Label(frame, text="Select Add-ons", font=("Segoe UI", 16, "bold"), style="TLabel").pack(pady=10)

        self.addon_vars = {}
        for addon in self.add_ons:
            var = tk.BooleanVar()
            chk = tk.Checkbutton(frame, text=f"{addon} (+${self.prices[addon]:.2f})", variable=var, bg="lightblue")
            chk.pack(anchor="w")
            self.addon_vars[addon] = var

        ttk.Button(frame, text="Add to Cart", command=self.add_item_to_cart).pack(pady=10)
        self.create_footer(frame)

    #Adding items to cart with add-ons and their prices
    def add_item_to_cart(self):
        item = self.selected_item
        size = self.selected_bowl_size.get() if self.current_category == "Bowls" else "Regular"
        addons = [a for a, v in self.addon_vars.items() if v.get()]
        key = f"{item} ({size}) ({', '.join(addons)})" if addons else f"{item} ({size})"
        price = self.bowl_prices[size] if self.current_category == "Bowls" else self.prices[item]
        total_price = price + sum(self.prices[a] for a in addons)

        if key in self.cart:
            self.cart[key]['quantity'] += 1
        else:
            self.cart[key] = {"price": total_price, "quantity": 1}

        add_on_msg = f" with selected add-ons ({', '.join(addons)})" if addons else " with no add-ons"
        messagebox.showinfo("Cart Updated", f"{item} ({size}){add_on_msg} has been added to your cart.")
        self.create_home_page()

    #Function to add non-customizable items like coffee or tacos to cart
    def quick_add_to_cart(self, item_name):
        size = "Regular"
        key = f"{item_name} ({size})"
        price = self.prices[item_name]

        #add or update items in the cart
        if key in self.cart:
            self.cart[key]['quantity'] += 1
        else:
            self.cart[key] = {"price": price, "quantity": 1}

        messagebox.showinfo("Cart Updated", f"{item_name} ({size}) has been added to your cart.")
        self.create_home_page()

    #Display the cart contents and allow updates
    def view_cart_page(self):
        self.clear_frame()
        frame = ttk.Frame(self, padding=20, style="TFrame")
        frame.pack(fill="both", expand=True)
        self.display_logo(frame)
        ttk.Label(frame, text="🛒 Your Cart", font=("Segoe UI", 16, "bold")).pack(pady=10)
        if not self.cart:
            ttk.Label(frame, text="Your cart is empty.").pack()
        else:
            total = 0
            for item, details in self.cart.items():
                item_frame = ttk.Frame(frame)
                item_frame.pack(fill="x", pady=5)
                #Display item and quantity controls
                ttk.Label(item_frame, text=item, style="TLabel", wraplength=250, justify="left").pack(side="left", padx=(0, 10))
                ttk.Button(item_frame, text="-", width=2, command=lambda i=item: self.update_quantity(i, -1)).pack(side="left", padx=2)
                ttk.Label(item_frame, text=str(details['quantity'])).pack(side="left")
                ttk.Button(item_frame, text="+", width =2, command=lambda i=item: self.update_quantity(i, 1)).pack(side="left", padx=2)
                item_total = details['price'] * details['quantity']
                total += item_total
                ttk.Label(item_frame, text=f"${item_total:.2f}", width=10, anchor="e").pack(side="right")
            #Displaying total and special request box
            ttk.Label(frame, text=f"Total: ${total:.2f}", font=self.custom_font).pack(pady=10)
            self.special_request = tk.Text(frame, height=3, width=50, wrap="word")
            ttk.Label(frame, text="Special Requests:", style="TLabel").pack(anchor="w", pady=(10, 0))
            self.special_request.pack(pady=(0, 10))
            ttk.Button(frame, text="Proceed to Checkout", command=self.go_to_customer_info).pack(pady=10)
        self.create_footer(frame)

    #Function to adjust quantity of an item in cart
    def update_quantity(self, item, change):
        if item in self.cart:
            self.cart[item]['quantity'] += change
            if self.cart[item]['quantity'] <= 0:
                del self.cart[item]
        self.view_cart_page()

    #Form to collect the customers information
    def go_to_customer_info(self):
        self.clear_frame()
        frame = ttk.Frame(self, padding=20, style="TFrame")
        frame.pack(fill="both", expand=True)
        self.display_logo(frame)
        ttk.Label(frame, text="Customer Info", font=("Segoe UI", 16, "bold"), style="TLabel").pack(pady=10)

        ttk.Label(frame, text="First Name:", style="TLabel").pack(anchor="w")
        self.first_name_entry = ttk.Entry(frame)
        self.first_name_entry.pack(fill="x")
        ttk.Label(frame, text="Last Name:", style="TLabel").pack(anchor="w")
        self.last_name_entry = ttk.Entry(frame)
        self.last_name_entry.pack(fill="x")
        ttk.Label(frame, text="Phone Number:", style="TLabel").pack(anchor="w")
        self.phone_entry = ttk.Entry(frame)
        self.phone_entry.pack(fill="x")
        ttk.Label(frame, text="Email:", style="TLabel").pack(anchor="w")
        self.email_entry = ttk.Entry(frame)
        self.email_entry.pack(fill="x")

        ttk.Button(frame, text="Continue to Payment", command=self.validate_customer_info).pack(pady=10)
        self.create_footer(frame)

    #Validating function for the user input
    def validate_customer_info(self):
        first = self.first_name_entry.get().strip()
        last = self.last_name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()

        if not (first and last and phone and email):
            messagebox.showerror("Input Error", "Please fill out all customer information fields.")
            return
        if not re.fullmatch(r"\d{10}", phone):
            messagebox.showerror("Input Error", "Phone number must be exactly 10 digits.")
            return
        if "@" not in email or not email.endswith(".com"):
            messagebox.showerror("Input Error", "Please enter a valid email address.")
            return

        self.customer_info = {
            "first_name": first, "last_name": last,
            "phone": phone, "email": email
        }
        self.go_to_payment_info()

    #Payment info screen after the customer info screen
    def go_to_payment_info(self):
        self.clear_frame()
        frame = ttk.Frame(self, padding=20, style="TFrame")
        frame.pack(fill="both", expand=True)
        self.display_logo(frame)
        #Creating the input fields for payment info
        ttk.Label(frame, text="Payment Info", font=("Segoe UI", 16, "bold"), style="TLabel").pack(pady=10)
        ttk.Label(frame, text="Full Name on Card:", style="TLabel").pack(anchor="w")
        self.card_name = ttk.Entry(frame)
        self.card_name.pack(fill="x")
        ttk.Label(frame, text="Card Number:", style="TLabel").pack(anchor="w")
        self.card_number = ttk.Entry(frame)
        self.card_number.pack(fill="x")
        ttk.Label(frame, text="CVV:", style="TLabel").pack(anchor="w")
        self.card_cvv = ttk.Entry(frame)
        self.card_cvv.pack(fill="x")
        ttk.Label(frame, text="Expiration Date (MM/YYYY):", style="TLabel").pack(anchor="w")
        self.card_exp = ttk.Entry(frame)
        self.card_exp.pack(fill="x")

        ttk.Button(frame, text="Place Order", command=self.validate_payment_info).pack(pady=10)
        self.create_footer(frame)

    #Validation function for the payment info inputs
    def validate_payment_info(self):
        import datetime

        name = self.card_name.get().strip()
        number = self.card_number.get().strip()
        cvv = self.card_cvv.get().strip()
        exp = self.card_exp.get().strip()

        #Ensuring all fields are filled 
        if not (name and number and cvv and exp):
            messagebox.showerror("Input Error", "Please fill out all payment information fields.")
            return
        if not re.fullmatch(r"\d{16}", number):
            messagebox.showerror("Input Error", "Card number must be 16 digits.")
            return
        if not re.fullmatch(r"\d{3}", cvv):
            messagebox.showerror("Input Error", "CVV must be 3 digits.")
            return
        if not re.fullmatch(r"(0[1-9]|1[0-2])/\d{4}", exp):
            messagebox.showerror("Input Error", "Expiration must be in MM/YYYY format.")
            return

        #Verifying that exp date is in the future
        month, year = map(int, exp.split("/"))
        today = datetime.date.today()
        if year < today.year or (year == today.year and month < today.month):
            messagebox.showerror("Input Error", "Card expiration date must be in the future.")
            return

        #Matching provided info 
        self.payment_info = {
            "card_name": name,
            "card_number": number,
            "cvv": cvv,
            "exp": exp
        }
        self.show_checkout()

    #Showing final order summary
    def show_checkout(self):
        self.payment_info = {
            "card_name": self.card_name.get(),
            "card_number": self.card_number.get(),
            "cvv": self.card_cvv.get(),
            "exp": self.card_exp.get()
        }
        self.clear_frame()
        frame = ttk.Frame(self, padding=20)
        frame.pack(fill="both", expand=True)
        self.display_logo(frame)
        ttk.Label(frame, text="Checkout", font=("Segoe UI", 16, "bold")).pack(pady=10)
        total = 0
        #Show order summary and calculating totals
        for item, details in self.cart.items():
            item_total = details['price'] * details['quantity']
            total += item_total
            ttk.Label(frame, text=f"{item} x{details['quantity']} - ${item_total:.2f}", style="TLabel", wraplength=400, justify="left").pack(anchor="w")
        tax = total * 0.0825
        grand_total = total + tax
        ttk.Label(frame, text=f"Tax (8.25%): ${tax:.2f}").pack(anchor="w", pady=5)
        ttk.Label(frame, text=f"Total: ${grand_total:.2f}", font=("Segoe UI", 12, "bold"), foreground="red").pack(anchor="w", pady=5)
        self.order_id = random.randint(100000, 999999)
        ttk.Button(frame, text="Confirm Order", command=self.place_order).pack(pady=10)
        self.create_footer(frame)

    # In place_order(), update the confirmation screen to show receipt and wait time
    def place_order(self):
        self.clear_frame()
        frame = ttk.Frame(self, padding=20, style="TFrame")
        frame.pack(fill="both", expand=True)
        self.display_logo(frame)

        ttk.Label(frame, text="Order Confirmed!", font=("Segoe UI", 16, "bold"), foreground="red", style="TLabel").pack(pady=10)
        ttk.Label(frame, text=f"Order ID: {self.order_id}", style="TLabel").pack(pady=5)
        ttk.Label(frame, text="Thank you for ordering from Mamaka Bowls!", style="TLabel").pack(pady=5)

        # Add two extra lines for confirmation page
        customer_phone = self.customer_info.get("phone", "[number not provided]")
        ttk.Label(frame, text=f"Your order receipt has been sent to {customer_phone}", style="TLabel").pack(pady=5)
        ttk.Label(frame, text="Estimated wait time is: 15 Minutes", style="TLabel").pack(pady=5)

        ttk.Button(frame, text="🏠 Back to Home", command=self.create_home_page).pack(pady=10)
        #Reset application state for a new order
        self.cart.clear()
        self.customer_info.clear()
        self.payment_info.clear()
        self.order_id = None
    
    #FAQ page
    def show_faq_page(self):
        self.clear_frame()
        frame = ttk.Frame(self, padding=20, style="TFrame")
        frame.pack(fill="both", expand=True)

        self.display_logo(frame)
        ttk.Label(frame, text="Frequently Asked Questions", font=("Segoe UI", 16, "bold"), style="TLabel").pack(pady=10)

        #List of questions for FAQ and the following answers
        faqs = [
            ("What are your hours?", "Mamaka Bowls is open from 8 AM to 8 PM, Monday through Saturday. We are closed on Sundays."),
            ("Can I customize my bowl?", "Yes! You can select from a variety of sizes and add-ons when ordering your bowl or smoothie."),
            ("Do you offer delivery?", "We offer delivery through third-party apps like Uber Eats and DoorDash."),
            ("Can I pay with a credit card?", "Yes! We accept all major credit and debit cards.")
        ]

        for question, answer in faqs:
            ttk.Label(frame, text=f"Q: {question}", font=("Segoe UI", 11, "bold"), style="TLabel", wraplength=450, justify="left").pack(anchor="w", pady=(10, 0))
            ttk.Label(frame, text=f"A: {answer}", style="TLabel", wraplength=450, justify="left").pack(anchor="w")

        ttk.Button(frame, text="⬅ Back to Home", command=self.create_home_page).pack(pady=20)
        self.create_footer(frame)

#Start of the application 
if __name__ == '__main__':
    app = MamakaBowlsApp()
    app.mainloop()
