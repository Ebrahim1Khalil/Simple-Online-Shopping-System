import json
import os
import tkinter as tk
from tkinter import messagebox, ttk, simpledialog

class handle_files():
    if not os.path.exists("cart.json"):
        with open("cart.json", "w") as cart_file:
            json.dump({}, cart_file)

    with open("cart.json", "r") as cart_file1:
        cart = json.load(cart_file1)

    if not os.path.exists("users.json"):
        with open("users.json", "w") as users_file:
            json.dump({}, users_file)

    with open("users.json", "r") as users_file0:
        users = json.load(users_file0)

    # Define the path to your JSON file
    file_path = 'Categories.json'
    # Check if the file exists
    if not os.path.isfile(file_path):
        # Create the file with a default structure
        with open(file_path, 'w') as file:
            _structure = {
                "home appliances": {},
                "electronics": {},
                "fashion": {},
                "books": {},
                "sports": {}
            }
            json.dump(_structure, file)

    with open('Categories.json', "r") as catg_file:
        Categories = json.load(catg_file)


class Sign:
    def __init__(self, sign_pg):
        self.sign_pg = sign_pg
        self.sign_pg.title("User Registration & Login")
        self.sign_pg.geometry("400x400")

        # Global variables to store the entry widgets
        self.name_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.id_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.gender_var = tk.StringVar()
        self.age_var = tk.StringVar()
        self.gov_var = tk.StringVar()


        # Main Menu buttons
        tk.Button(self.sign_pg, text="Login", command=self.show_login_form).pack(pady=20)
        tk.Button(self.sign_pg, text="Register", command=self.show_registration_form).pack(pady=20)

    # Register user method
    def register_user(self):
        name = self.name_var.get()
        password = self.password_var.get()
        phone_number = self.phone_var.get()
        national_id = self.id_var.get()
        email = self.email_var.get()
        gender = self.gender_var.get()
        age = self.age_var.get()
        governorate = self.gov_var.get()

        # Validations for input fields
        if name.isalpha() and len(name) > 1 and \
                len(password) >= 4 and \
                phone_number.isdigit() and len(phone_number) == 11 and \
                national_id.isdigit() and len(national_id) == 14 and \
                "@" in email and "." in email and \
                gender in ('M', 'F', 'm', 'f') and age.isdigit() and 1 < int(age) <= 120 and \
                governorate.isalpha() and len(governorate) > 1:

            new_user = {
                "name": name,
                "password": password,
                "phone": phone_number,
                "national id": national_id,
                "mail": email,
                "gender": "Male" if gender == 'M' else "Female",
                "age": int(age),
                "governorate": governorate,
            }
            handle_files.users[email] = new_user

            with open("users.json", "w") as users_file_register:
                json.dump(handle_files.users, users_file_register, indent=4)
            messagebox.showinfo("Success", "Registration successful!")
        else:
            messagebox.showerror("Error", "Invalid input data! Please try again.")
            sign_pg.mainloop()

        self.sign_pg.destroy()
        App.email = email
        App.call_App()

    # Login user method
    def login_user(self):
        email = self.email_var.get()
        password = self.password_var.get()

        if email in handle_files.users:
            if handle_files.users[email]["password"] == password:
                messagebox.showinfo("Login", f"Welcome back {handle_files.users[email]["name"]}!")
                self.sign_pg.destroy()
                App.email = email
                App.call_App()

        elif email == "admin@gmail.com" and password == "admin123":
            self.sign_pg.destroy()
            Admin.admin_pg_call()

        else:
            response = messagebox.askyesno("Error", "Invalid email or password! Would you like to register?")
            if response:
                self.show_registration_form()

    # Registration form layout
    def create_registration_form(self):
        self.clear_form()
        tk.Label(self.sign_pg, text="Name").pack()
        tk.Entry(self.sign_pg, textvariable=self.name_var).pack()

        tk.Label(self.sign_pg, text="Password").pack()
        tk.Entry(self.sign_pg, textvariable=self.password_var, show="*").pack()

        tk.Label(self.sign_pg, text="Phone").pack()
        tk.Entry(self.sign_pg, textvariable=self.phone_var).pack()

        tk.Label(self.sign_pg, text="National ID").pack()
        tk.Entry(self.sign_pg, textvariable=self.id_var).pack()

        tk.Label(self.sign_pg, text="Email").pack()
        tk.Entry(self.sign_pg, textvariable=self.email_var).pack()

        tk.Label(self.sign_pg, text="Gender (M/F)").pack()
        tk.Entry(self.sign_pg, textvariable=self.gender_var).pack()

        tk.Label(self.sign_pg, text="Age").pack()
        tk.Entry(self.sign_pg, textvariable=self.age_var).pack()

        tk.Label(self.sign_pg, text="Governorate").pack()
        tk.Entry(self.sign_pg, textvariable=self.gov_var).pack()

        tk.Button(self.sign_pg, text="Register", command=self.register_user).pack()

    # Login form layout
    def create_login_form(self):
        self.clear_form()
        tk.Label(self.sign_pg, text="Email").pack()
        tk.Entry(self.sign_pg, textvariable=self.email_var).pack()

        tk.Label(self.sign_pg, text="Password").pack()
        tk.Entry(self.sign_pg, textvariable=self.password_var, show="*").pack()

        tk.Button(self.sign_pg, text="Login", command=self.login_user).pack()

    # Switch between forms
    def show_registration_form(self):
        self.create_registration_form()

    def show_login_form(self):
        self.create_login_form()

    # Clear form when switching between login and register forms
    def clear_form(self):
        for widget in self.sign_pg.winfo_children():
            widget.destroy()


class Admin:
    def __init__(self, admin_pg):
        self.admin_pg = admin_pg
        self.admin_pg.title("Edit Items")
        self.admin_pg.geometry("750x650")

        self.root_categories()

    def save_data(self):
        """Save the Categories data to the JSON file."""
        with open("Categories.json", "w") as catg_file:
            json.dump(handle_files.Categories, catg_file, indent=2)

    def root_categories(self):
        def selected_catg(_):
            selected = cmb_bx.get()
            self.edit_products_windows(selected)

        slc_catg = tk.Label(self.admin_pg, text="Select a Category")
        slc_catg.pack()

        cmb_bx = ttk.Combobox(self.admin_pg, values=["home appliances", "electronics", "fashion", "books", "sports"])
        cmb_bx.pack()
        cmb_bx.bind("<<ComboboxSelected>>", selected_catg)

    def edit_products_windows(self, selected_catg):
        # Frame for header
        hd_fr = tk.Frame(self.admin_pg, bg="lightgray", height=50)
        hd_fr.pack()
        tl = tk.Label(hd_fr, text="Edit Products", font=("Arial", 20, "bold"), bg="lightgray")
        tl.pack()

        def prod_selected_op(_):
            selected = cmb_bx.get()

            if selected == "Add Product":
                self.add_product(selected_catg)
            elif selected == "remove product":
                self.remove_product(selected_catg)
            elif selected == "update product":
                self.update_product(selected_catg)

        slc_op = tk.Label(self.admin_pg, text="Select an Operation")
        slc_op.pack()

        cmb_bx = ttk.Combobox(self.admin_pg, values=["Add Product", "remove product", "update product"])
        cmb_bx.pack()
        cmb_bx.bind("<<ComboboxSelected>>", prod_selected_op)

    def show_category_products_admin(self, category):
        show_w = tk.Tk()

        def create_text_with_scrollbars(new_text1):
            frame = tk.Frame(show_w)
            frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

            text_widget = tk.Text(frame, wrap=tk.NONE, height=10, width=50)
            text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            v_scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=text_widget.yview)
            v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            text_widget.config(yscrollcommand=v_scrollbar.set)

            h_scrollbar = tk.Scrollbar(frame, orient=tk.HORIZONTAL, command=text_widget.xview)
            h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
            text_widget.config(xscrollcommand=h_scrollbar.set)

            text_widget.insert(tk.END, new_text1)

        new_text = ""
        for product in handle_files.Categories[category]:
            this_product = handle_files.Categories[category][str(product)]

            new_text += (f"\nName: {this_product['name']} \nOriginal Price: {this_product['original price']}\n"
                         f"Discount: {this_product['discount']} \nDiscounted Price: {this_product['discounted price']}\n"
                         f"Brand: {this_product['brand']} \nModel Year: {this_product['model_year']}\nID: {product}\n{'--' * 20}\n")

        create_text_with_scrollbars(new_text)

        def show_refresh():
            show_w.destroy()
            self.show_category_products_admin(category)

        show_refresh_btn = tk.Button(show_w, text="Refresh", command=lambda: show_refresh())
        show_refresh_btn.pack(pady=15)

    def select_another_category(self):
        def go_select_another_category():
            self.admin_pg.destroy()
            Admin.admin_pg_call()

        select_another_category_btn = tk.Button(self.admin_pg, text="select another category",
                                                command=go_select_another_category)
        select_another_category_btn.pack(pady=10)

    def add_product(self, category):
        prod_n_l = tk.Label(self.admin_pg, text="Product Name")
        prod_n_l.pack()
        prod_n = tk.Entry(self.admin_pg)
        prod_n.pack()

        br_l = tk.Label(self.admin_pg, text="Brand")
        br_l.pack()
        br = tk.Entry(self.admin_pg)
        br.pack()

        md_y_l = tk.Label(self.admin_pg, text="Model Year")
        md_y_l.pack()
        md_y = tk.Entry(self.admin_pg)
        md_y.pack()

        org_pr_l = tk.Label(self.admin_pg, text="Original Price")
        org_pr_l.pack()
        org_pr = tk.Entry(self.admin_pg)
        org_pr.pack()

        pr_ds_l = tk.Label(self.admin_pg, text="Discount (in % form)")
        pr_ds_l.pack()
        pr_ds = tk.Entry(self.admin_pg)
        pr_ds.pack()

        def save_new_product():
            original_price = 0
            product_discount = 0

            try:
                original_price_txt = org_pr.get()
                original_price = float(original_price_txt)

                product_discount_txt = pr_ds.get()
                product_discount = int(product_discount_txt)
                if handle_files.Categories[category]:
                    last_id = list(handle_files.Categories[category].keys())[-1]
                    n_prod_id = int(last_id) + 50
                else:
                    n_prod_id = 0

                handle_files.Categories[category][str(n_prod_id)] = {
                    "name": prod_n.get(),
                    "original price": original_price,
                    "discount": product_discount,
                    "discounted price": original_price - (original_price * (product_discount / 100)),
                    "brand": br.get(),
                    "model_year": md_y.get()
                }

                self.save_data()

                tk.Label(self.admin_pg, text=f"Product {prod_n.get()} added successfully, id: {n_prod_id}.").pack(
                    pady=10)

            except ValueError:
                tk.Label(self.admin_pg, text="Price or Discount Invalid. Try again.").pack(pady=10)
                save_new_product()

        add_prod_btn = tk.Button(self.admin_pg, text="Add product", command=save_new_product)
        add_prod_btn.pack(pady=10)

        self.select_another_category()

    def remove_product(self, category):
        self.show_category_products_admin(category)

        del_prod_l = tk.Label(self.admin_pg, text="Enter product ID")
        del_prod_l.pack(pady=10)

        del_prod_ent = tk.Entry(self.admin_pg)
        del_prod_ent.pack(pady=10)

        def go_remove():
            _id = str(del_prod_ent.get())
            catg = handle_files.Categories[category]

            if _id in catg:
                # Save product name before deletion
                product_name = catg[_id]["name"]
                # Remove the product
                del catg[_id]
                # Inform the user
                confirmation_label = tk.Label(self.admin_pg, text=f"Product {product_name} removed successfully.")
                confirmation_label.pack(pady=10)
            else:
                # Inform the user that the product ID was not found
                rem_id_not_found_l = tk.Label(self.admin_pg, text="Enter Valid Product ID")
                rem_id_not_found_l.pack(pady=10)

            # Save the updated data after deletion
            self.save_data()

        del_prod_btn = tk.Button(self.admin_pg, text="Remove product", command=go_remove)
        del_prod_btn.pack(pady=10)

        def remove_another_prod():
            self.admin_pg.destroy()
            self.remove_product(category)

        self.select_another_category()

    def update_product(self, category):

        self.show_category_products_admin(category)

        upd_prod_l = tk.Label(self.admin_pg, text="Enter product ID")
        upd_prod_l.pack(pady=10)

        upd_prod_ent = tk.Entry(self.admin_pg)
        upd_prod_ent.pack(pady=10)

        def go_update_prod(prod_to_upd, _id):
            # Create UI elements for updating the product
            prod_upd_l = tk.Label(self.admin_pg, text="Product Name")
            prod_upd_l.pack()
            prod_upd_n = tk.Entry(self.admin_pg)
            prod_upd_n.pack()
            prod_upd_n.insert(0, prod_to_upd["name"])

            br_up_l = tk.Label(self.admin_pg, text="Brand")
            br_up_l.pack()
            br_up = tk.Entry(self.admin_pg)
            br_up.pack()
            br_up.insert(0, prod_to_upd["brand"])

            md_y_upd_l = tk.Label(self.admin_pg, text="Model Year")
            md_y_upd_l.pack()
            md_y_upd = tk.Entry(self.admin_pg)
            md_y_upd.pack()
            md_y_upd.insert(0, prod_to_upd["model_year"])

            org_pr_upd_l = tk.Label(self.admin_pg, text="Original Price")
            org_pr_upd_l.pack()
            org_pr_upd = tk.Entry(self.admin_pg)
            org_pr_upd.pack()
            org_pr_upd.insert(0, str(prod_to_upd["original price"]))

            pr_ds_upd_l = tk.Label(self.admin_pg, text="Discount (in % form)")
            pr_ds_upd_l.pack()
            pr_ds_upd = tk.Entry(self.admin_pg)
            pr_ds_upd.pack()
            pr_ds_upd.insert(0, str(prod_to_upd["discount"]))

            # Function to save updated product details
            def save_updated_product():
                try:
                    original_price = float(org_pr_upd.get())
                    product_discount = int(pr_ds_upd.get())

                    handle_files.Categories[category][upd_prod_ent.get()] = {
                        "name": prod_upd_n.get(),
                        "original price": original_price,
                        "discount": product_discount,
                        "discounted price": original_price - (original_price * (product_discount / 100)),
                        "brand": br_up.get(),
                        "model_year": md_y_upd.get()
                    }

                    self.save_data()

                    tk.Label(self.admin_pg, text=f"Product {prod_upd_n.get()} updated successfully, id: {_id}.").pack(
                        pady=10)

                except ValueError:
                    tk.Label(self.admin_pg, text="Invalid input. Price or Discount must be numeric. Try again.").pack(
                        pady=10)

            # Button to save the updated product
            upd_prod_btn = tk.Button(self.admin_pg, text="Update product", command=save_updated_product)
            upd_prod_btn.pack(pady=10)

            # Optional: Provide a button to select another category
            self.select_another_category()

        def id_validation(_id):
            if _id in handle_files.Categories[category]:
                # Retrieve the product to be updated
                prod_to_upd = handle_files.Categories[category][_id]
                go_update_prod(prod_to_upd, _id)
            else:
                error_l = tk.Label(self.admin_pg, text="Invalid Product ID. Try again")
                error_l.pack(pady=10)
                self.update_product(category)

        try_id_btn = tk.Button(self.admin_pg, text="Let's update it", command=lambda: id_validation(upd_prod_ent.get()))
        try_id_btn.pack(pady=10)

    @staticmethod
    def admin_pg_call():
        Admin.admin_pg = tk.Tk()
        admin_app = Admin(Admin.admin_pg)
        Admin.admin_pg.mainloop()


#########################################################################################################################################


# Data Classes
class Item:
    def __init__(self, name, price, brand, model_year, item_id, color):
        self.name = name
        self.price = price
        self.brand = brand
        self.model_year = model_year
        self.id = item_id
        self.color = color

    def __repr__(self):
        return f"ID: {self.id}, Name: {self.name}, Price: {self.price}, Brand: {self.brand}, Model Year: {self.model_year}, Color: {self.color}"


class Category:
    def __init__(self, name):
        self.name = name

    @staticmethod
    def binary_search(target_name, items_names):
        left, right = 0, len(items_names) - 1
        while left <= right:
            mid = (left + right) // 2
            mid_item = items_names[mid]
            if mid_item == target_name:
                return mid_item
            elif mid_item < target_name:
                left = mid + 1
            else:
                right = mid - 1
        return None

    @staticmethod
    def sort_by_price(items, trg):
        if len(items) <= 1:
            return items
        mid = len(items) // 2
        left_half = Category.sort_by_price(items[:mid], trg)
        right_half = Category.sort_by_price(items[mid:], trg)
        return Category.merge(left_half, right_half, trg)

    @staticmethod
    def merge(left, right, trg):
        sorted_list = []
        while left and right:
            if trg == "l":
                if left[0][1]["original price"] <= right[0][1]["original price"]:
                    sorted_list.append(left.pop(0))
                else:
                    sorted_list.append(right.pop(0))
            else:
                if left[0][1]["original price"] >= right[0][1]["original price"]:
                    sorted_list.append(left.pop(0))
                else:
                    sorted_list.append(right.pop(0))

        sorted_list.extend(left or right)
        return sorted_list


class Cart(handle_files):
    def __init__(self):
        handle_files.cart = {
            App.email: {
                "total after": 0,
                "products": []
            }
        }

    @staticmethod
    def save_data():
        with open("cart.json", "w") as cart_file_c:
            json.dump(handle_files.cart, cart_file_c)

    @staticmethod
    def add_item(item_id, category_name):
        if App.email not in handle_files.cart:
            handle_files.cart = {
                App.email: {
                    "total after": Cart.calculate_total(category_name),
                    "products": [item_id]
                }
            }
        else:
            handle_files.cart[App.email]["products"].append(item_id)
        Cart.save_data()

    @staticmethod
    def calculate_total(category_name):
        """Calculate total cost for a given user."""
        _sum = 0

        governorate = simpledialog.askstring("Input", "Enter governorate:")

        for product_id in handle_files.cart[App.email]["products"]:
            # Loop through categories to find the product by its ID
            for category_name, products in handle_files.Categories.items():
                if product_id in products:
                    _sum += products[product_id]["original price"]

        if governorate.lower() not in ['cairo', 'giza']:
            delivery_fee = Cart.calculate_delivery_fee(governorate)
            App.combined_total = _sum + delivery_fee
            messagebox.showinfo("Total + Delivery Fee", f"Combined total cost: {App.combined_total:.2f}")
        else:
            App.combined_total = _sum
            messagebox.showinfo("Total + Delivery Fee", f"Combined total cost: {App.combined_total:.2f}")

        Cart.save_data()
        return App.combined_total

    @staticmethod
    def delete_from_cart(index):
        """Delete an item from the cart."""
        if App.email in handle_files.cart and 0 <= index < len(handle_files.cart[App.email]["products"]):
            handle_files.cart[App.email]["products"].pop(index)
            Cart.save_data()

    @staticmethod
    def calculate_delivery_fee(governorate):
        """Calculate delivery fee based on the governorate."""
        if governorate.lower() not in ['cairo', 'giza']:
            return 50
        return 0


# Tkinter Application
class App:
    email = ""
    combined_total = 0

    def __init__(self, root):
        self.root = root
        self.root.title("Store")
        self.items_per_page = 5
        self.current_page = 0
        self.create_widgets()

    def create_widgets(self):
        self.tab_control = ttk.Notebook(self.root)

        self.tab_cart = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_cart, text='Cart')

        categories = ['home appliances', 'electronics', 'fashion', 'books', 'sports']

        # Create a tab for each category
        self.category_tabs = {}
        for category_name in categories:
            tab = ttk.Frame(self.tab_control)
            self.tab_control.add(tab, text=category_name)
            self.category_tabs[category_name] = tab
            self.create_category_tab_widgets(tab, category_name)

        self.tab_control.pack(expand=1, fill='both')

        # Cart Tab
        self.cart_frame = ttk.Frame(self.tab_cart)
        self.cart_frame.pack(pady=10)

        self.view_cart_button = ttk.Button(self.tab_cart, text="View Cart",
                                           command=lambda: self.view_cart(category_name))
        self.view_cart_button.pack(pady=10)

        self.calculate_total_button = ttk.Button(self.tab_cart, text="Calculate Total Cost",
                                                 command=lambda: self.calculate_cart_total(category_name))
        self.calculate_total_button.pack(pady=10)

        self.calculate_delivery_fee_button = ttk.Button(self.tab_cart, text="Calculate Delivery Fee",
                                                        command=self.calculate_delivery_fee)
        self.calculate_delivery_fee_button.pack(pady=10)

        self.delete_item_button = ttk.Button(self.tab_cart, text="Delete Selected Item from Cart",
                                             command=lambda: self.delete_selected_item_from_cart(category_name))
        self.delete_item_button.pack(pady=10)

        self.cart_listbox = tk.Listbox(self.tab_cart, height=10, width=50)
        self.cart_listbox.pack(side=tk.LEFT, padx=10)

        self.cart_scrollbar = tk.Scrollbar(self.tab_cart, orient=tk.VERTICAL, command=self.cart_listbox.yview)
        self.cart_scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        self.cart_listbox.config(yscrollcommand=self.cart_scrollbar.set)

    def create_category_tab_widgets(self, tab, category_name):
        category_listbox = tk.Listbox(tab, height=10, width=50)  # Use unique variable name
        category_listbox.pack(side=tk.LEFT, padx=10)

        category_scrollbar = tk.Scrollbar(tab, orient=tk.VERTICAL,
                                          command=category_listbox.yview)  # Use unique variable name
        category_scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        category_listbox.config(yscrollcommand=category_scrollbar.set)

        view_items_button = ttk.Button(tab, text="View Items in Category",
                                       command=lambda: self.view_items_in_category(category_name))
        view_items_button.pack(pady=10)

        search_item_button = ttk.Button(tab, text="Search Item",
                                        command=lambda: self.search_item_in_category(category_name))
        search_item_button.pack(pady=10)

        add_to_cart_button = ttk.Button(tab, text="Add Selected Item to Cart",
                                        command=lambda: self.add_selected_item_to_cart(category_name))
        add_to_cart_button.pack(pady=10)

        prev_page_button = ttk.Button(tab, text="Previous Page", command=lambda: self.previous_page(category_name))
        prev_page_button.pack(side=tk.LEFT, padx=5, pady=10)

        next_page_button = ttk.Button(tab, text="Next Page", command=lambda: self.next_page(category_name))
        next_page_button.pack(side=tk.LEFT, padx=5, pady=10)

        # Initialize buttons for pagination
        self.update_category_listbox(category_name)

        #sort by price botton
        self.sort_price_button = ttk.Button(tab, text="Sort by Price(low to high)",command=lambda: self.sort_items_by_price(category_name, "l"))
        self.sort_price_button.pack(pady=10)

        self.sort_price_button = ttk.Button(tab, text="Sort by Price(high to low)",command=lambda: self.sort_items_by_price(category_name, "h"))
        self.sort_price_button.pack(pady=10)

    def sort_items_by_price(self, category_name, trg):
        category = handle_files.Categories[category_name]
        items = list(category.items())
        sorted_items = Category.sort_by_price(items, trg)
        self.update_category_listbox_with_sorted_items(category_name, sorted_items)

    def update_category_listbox_with_sorted_items(self, category_name, sorted_items):
        tab = self.category_tabs[category_name]
        listbox = tab.winfo_children()[0]  # Assuming Listbox is the first child
        listbox.delete(0, tk.END)  # Clear current items in the Listbox

        # Insert sorted items into the Listbox
        for i, item in enumerate(sorted_items):
            listbox.insert(tk.END, f"Name: {item[1]['name']}        \nID: {item[0]}      \nbrand: {item[1]['brand']}\n\
             model year: {item[1]['model_year']}         \nprice: {item[1]['original price']}")

    def update_category_listbox(self, category_name):
        tab = self.category_tabs[category_name]
        listbox = tab.winfo_children()[0]  # Assuming listbox is the first child
        listbox.delete(0, tk.END)

        category = handle_files.Categories[category_name]

        items = list(category.values())  # Convert dictionary values to a list
        items_id = list(category.keys())
        start_index = self.current_page * self.items_per_page
        end_index = min(start_index + self.items_per_page, len(items))

        for i in range(start_index, end_index):
            item = items[i]
            item_id = items_id[i]
            listbox.insert(tk.END, f"{item["name"]} (ID: {item_id})")

        self.update_page(category_name)

    def update_page(self, category_name):
        tab = self.category_tabs[category_name]
        items = list(handle_files.Categories[category_name].keys())

        total_items = len(items)

        # Ensure buttons exist
        buttons = tab.winfo_children()
        if len(buttons) < 8:
            return

        prev_button = buttons[6]  # Assuming prev_button is the 7th child
        next_button = buttons[7]  # Assuming next_button is the 8th child

        prev_button.config(state=tk.NORMAL if self.current_page > 0 else tk.DISABLED)
        next_button.config(
            state=tk.NORMAL if (self.current_page + 1) * self.items_per_page < total_items else tk.DISABLED)

    def view_items_in_category(self, category_name):
        items = handle_files.Categories[category_name]
        if not items:
            messagebox.showinfo("No Items", "No items in this category.")
            return  # Exit early if no items are present

        # Initialize an empty string to accumulate item details
        item_details = ""

        for item_id, item_info in items.items():
            item_details += f"Name: {item_info['name']}        \nID: {item_id}      \nbrand: {item_info['brand']}\n"
            item_details += f"model year: {item_info['model_year']}         \nprice: {item_info['original price']}\n\n"

        # Display all item details in a single messagebox
        messagebox.showinfo("Items in Category", item_details)

    def search_item_in_category(self, category_name):
        item_name = simpledialog.askstring("Input", "Enter item name to search:")
        if not item_name:
            return

        category = handle_files.Categories[category_name]

        items = list(category.values())
        items_names = [item["name"] for item in items]
        item = Category.binary_search(item_name, items_names)

        prod = {}
        for i in items:
            if item == i["name"]:
                prod = i

        if item:
            messagebox.showinfo("Item Found", f"Item found: {item}      \nPrice: {prod["original price"]}\
        \nBrand: {prod["brand"]}        \nModel Year: {prod["model_year"]}")
        else:
            messagebox.showinfo("Item Not Found", "Item not found in this category.")

    def previous_page(self, category_name):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_category_listbox(category_name)

    def next_page(self, category_name):
        category = handle_files.Categories[category_name]
        if (self.current_page + 1) * self.items_per_page < len(list(category.values())):
            self.current_page += 1
            self.update_category_listbox(category_name)

    def add_selected_item_to_cart(self, category_name):
        listbox = self.category_tabs[category_name].winfo_children()[0]  # Assuming listbox is the first child
        selected_indices = listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Selection Error", "Please select an item.")
            return

        selected_index = selected_indices[0]
        items = list(handle_files.Categories[category_name].keys())
        if selected_index < 0 or selected_index >= len(items):
            messagebox.showwarning("Selection Error", "Invalid item selected.")
            return

        item = items[selected_index]
        Cart.add_item(item, category_name)
        messagebox.showinfo("Success", f"Item '{handle_files.Categories[category_name][item]["name"]}' added to cart.")
        self.update_cart_listbox(category_name)

    def delete_selected_item_from_cart(self, category_name):
        selected_indices = self.cart_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Selection Error", "Please select an item.")
            return

        selected_index = selected_indices[0]
        Cart.delete_from_cart(selected_index)  # Assuming cart.delete_from_cart works with indices
        messagebox.showinfo("Success", "Selected item removed from cart.")
        self.update_cart_listbox(category_name)

    def view_cart(self, category_name):
        self.update_cart_listbox(category_name)

    def update_cart_listbox(self, category_name):
        self.cart_listbox.delete(0, tk.END)

        for product_id in handle_files.cart[App.email]["products"]:
            for category_name, products in handle_files.Categories.items():
                if product_id in products:
                    this_prod = handle_files.Categories[category_name][product_id]
                    self.cart_listbox.insert(tk.END,
                                             f"Name: {this_prod["name"]}        \nID: {product_id}      \nbrand: {this_prod["brand"]}\
        \nmodel year: {this_prod["model_year"]}         \nprice: {this_prod["original price"]}")
                    break

    def calculate_cart_total(self, category_name):
        total = Cart.calculate_total(category_name)
        messagebox.showinfo("Total Cost", f"Total cart cost: {total:.2f}")

    def calculate_delivery_fee(self):
        governorate = simpledialog.askstring("Input", "Enter governorate:")
        if not governorate:
            return

        fee = Cart.calculate_delivery_fee(governorate)
        messagebox.showinfo("Delivery Fee", f"Delivery fee: {fee:.2f}")

        fee = Cart.calculate_delivery_fee(governorate)
        messagebox.showinfo("Delivery Fee", f"Delivery fee: {fee:.2f}")

    @staticmethod
    def call_App():

        if App.email not in handle_files.cart:
            handle_files.cart = {
                App.email: {
                    "total after": 0,
                    "products": []
                }
            }

        Cart.save_data()
        root = tk.Tk()
        app0 = App(root)
        root.geometry('800x600')
        root.mainloop()


# Create the main window and start the application
if __name__ == "__main__":
    sign_pg = tk.Tk()
    app = Sign(sign_pg)
    sign_pg.mainloop()
