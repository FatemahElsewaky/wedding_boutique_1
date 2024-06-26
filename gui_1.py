import tkinter as tk
from tkinter import *
from tkinter import filedialog

class ProfilePage:
    def __init__(self, master):
        self.master = master
        self.master.title("User Profile")
        self.master.geometry("1280x800")  # Adjusted height for better visibility

        # Placeholder data for the user
        self.user_data = {
            "Username": "johndoe",
            "First Name": "John",
            "Last Name": "Doe",
            "Address": "1234 Bridal St",
            "Payment Info": "Visa **** 4242",
            "Email": "johndoe@example.com",
            "Phone Number": "1234567890"
        }

        # Display name and last name in a bigger font at the top center
        name_label = tk.Label(master, text=f"{self.user_data['First Name']} {self.user_data['Last Name']}", font=("Helvetica", 48, "bold"))
        name_label.pack(pady=20)

        # Adding a line for separation before username
        separator_before_username = tk.Frame(master, height=2, bd=1, relief="groove")
        separator_before_username.pack(fill="x", padx=20, pady=10)

        # Display username in a better position
        username_label = tk.Label(master, text=f"Username: {self.user_data['Username']}", font=("Helvetica", 12, "bold"))
        username_label.pack(pady=10)

        # Adding a line for separation after username
        separator_after_username = tk.Frame(master, height=2, bd=1, relief="groove")
        separator_after_username.pack(fill="x", padx=20, pady=10)

        # Initial row index for other information entries
        row = 2
        # Display the rest of the information starting below the username section
        self.entry_fields = {}
        self.labels = {}
        for key, value in self.user_data.items():
            if key not in ["First Name", "Last Name", "Username"]:
                label = tk.Label(master, text=f"{key}: ", font=("Helvetica", 12, "bold"))
                label.place(x=master.winfo_screenwidth() // 2 - 150, y=250 + row * 30, anchor="e")

                entry = tk.Entry(master, font=("Helvetica", 12))
                entry.insert(0, value)
                entry.place(x=master.winfo_screenwidth() // 2 - 100, y=250 + row * 30, anchor="w")
                entry.config(state="disabled")
                self.entry_fields[key] = entry

                edit_button = tk.Button(master, text="Edit", command=lambda k=key, e=entry: self.toggle_edit_field(k, e))
                edit_button.place(x=master.winfo_screenwidth() // 2 + 100, y=250 + row * 30, anchor="w")

                row += 1

    def toggle_edit_field(self, field, entry):
        if entry["state"] == "disabled":
            entry.config(state="normal")
            entry.focus_set()
        else:
            entry.config(state="disabled")


class MainPage:
    def __init__(self, master):
        self.master = master
        self.master.title("Main Page")
        self.master.geometry("1280x1920")

        self.label = tk.Label(master, text="H.E.M.", font=("Helvetica", 48))
        self.label.pack(pady=20)

        # Set background color for the menu bar
        menu_bg_color = self.master.cget("bg")

        # Create a frame to hold the menu bar
        menu_frame = tk.Frame(master, bg=menu_bg_color)  # Add border and relief
        menu_frame.pack(side=tk.TOP, pady=10)

        # Create a dropdown button for the account
        self.account_menu = tk.Menubutton(menu_frame, text="Account", compound=tk.LEFT, bg=menu_bg_color,
                                          font=("Helvetica", 18))
        self.account_menu.menu = tk.Menu(self.account_menu, tearoff=0)
        self.account_menu["menu"] = self.account_menu.menu

        # Add options to the account menu
        self.account_menu.menu.add_command(label="Profile", command=self.show_profile)
        self.account_menu.menu.add_command(label="Logout", command=self.logout)

        self.account_menu.pack(side=tk.RIGHT, padx=10)

        # Configure button style to remove button shape
        button_style = {"border": 0, "bg": menu_bg_color, "width": 13, "height": 2}

        # Create menu buttons
        button_wedding = tk.Button(menu_frame, text="Wedding Dresses", font=("Helvetica", 28),
                                   command=self.show_wedding_dresses, **button_style)
        button_wedding.pack(side=tk.LEFT, padx=10)

        button_collections = tk.Button(menu_frame, text="Collections", font=("Helvetica", 28),
                                       command=self.show_collections, **button_style)
        button_collections.pack(side=tk.LEFT, padx=10)

        button_styles = tk.Button(menu_frame, text="Styles", font=("Helvetica", 28),
                                  command=self.show_styles, **button_style)
        button_styles.pack(side=tk.LEFT, padx=10)

        button_brands = tk.Button(menu_frame, text="Brands", font=("Helvetica", 28),
                                  command=self.show_brands, **button_style)
        button_brands.pack(side=tk.LEFT, padx=10)

        # Center the menu bar horizontally
        menu_frame.place(relx=.5, rely=.15, anchor=tk.CENTER)

    def show_wedding_dresses(self):
        # Placeholder method to display wedding dresses
        print("Displaying Wedding Dresses")

    def show_collections(self):
        # Placeholder method to display bridesmaid dresses
        print("Displaying Bridesmaid Dresses")

    def show_styles(self):
        # Placeholder method to display evening gowns
        print("Displaying Evening Gowns")

    def show_brands(self):
        # Placeholder method to display evening gowns
        print("Displaying Evening Gowns")

    def show_profile(self):
        # Placeholder method to show account profile page
        print("Showing Profile Page")
        root = tk.Tk()
        app = ProfilePage(root)
        root.mainloop()


    def logout(self):
        print("You logged out successfully.")
        self.master.destroy()
        root = tk.Tk()
        app = HomePage(root)
        root.mainloop()

class LoginPage:
    def __init__(self, master, homepage):
        self.master = master
        self.master.title("Login / Sign Up")
        self.master.geometry("1280x1920")
        self.homepage = homepage

        self.label_login = tk.Label(master, text="Login", font=("Helvetica", 12, "bold"))
        self.label_login.pack(pady=10)

        self.label_username = tk.Label(master, text="Username:")
        self.label_username.pack()

        self.entry_username = tk.Entry(master)
        self.entry_username.pack()

        self.label_password = tk.Label(master, text="Password:")
        self.label_password.pack()

        self.entry_password = tk.Entry(master, show="*")
        self.entry_password.pack()

        self.login_button = tk.Button(master, text="Login", command=self.login)
        self.login_button.pack(pady=10)

        self.label_signup = tk.Label(master, text="Sign Up", font=("Helvetica", 12, "bold"))
        self.label_signup.pack(pady=10)

        self.label_new_username = tk.Label(master, text="New Username:")
        self.label_new_username.pack()

        self.entry_new_username = tk.Entry(master)
        self.entry_new_username.pack()

        self.label_new_password = tk.Label(master, text="New Password:")
        self.label_new_password.pack()

        self.entry_new_password = tk.Entry(master, show="*")
        self.entry_new_password.pack()

        self.signup_button = tk.Button(master, text="Sign Up", command=self.signup)
        self.signup_button.pack(pady=10)

        self.message = tk.Label(master, text="", fg="red")
        self.message.pack()

        self.message = tk.Label(master, text="", fg="red")
        self.message.pack()

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        # Placeholder authentication logic
        # Replace this with your actual authentication logic
        if username == "admin" and password == "admin":
            self.master.destroy()  # Close the login window
            root = tk.Tk()  # Create a new Tkinter root window for the main page
            app = MainPage(root)  # Open the main page
            root.mainloop()  # Show the homepage
        else:
            self.message.config(text="Invalid username or password")

    def signup(self):
        new_username = self.entry_new_username.get()
        new_password = self.entry_new_password.get()

        # Placeholder sign up logic
        # Replace this with your actual sign up logic
        if new_username and new_password:
            self.message.config(text="Sign up successful!")
            self.master.destroy()  # Close the login window
            root = tk.Tk()  # Create a new Tkinter root window for the main page
            app = MainPage(root)  # Open the main page
            root.mainloop()
        else:
            self.message.config(text="Please enter both username and password")



class HomePage:
    def __init__(self, master):
        self.master = master
        self.master.title("Bridal Website")

        # Set window size to 800x600 pixels
        self.master.geometry("1280x1920")

        self.label = tk.Label(master, text="H.E.M.", font=("Helvetica", 48))
        self.label.pack(pady=20)

        self.label_2 = tk.Label(master, text="Welcome to our Bridal Website!", font=("Helvetica", 48))
        self.label_2.pack(pady=20)

        self.login_button = tk.Button(master, text="Login", command=self.open_login, width=20, height=4,
                                      bg="blue", fg="white", font=("Helvetica", 36))
        self.login_button.pack(pady=10)

        self.exit_button = tk.Button(master, text="Exit", command=master.quit)
        self.exit_button.pack(pady=10)

    def open_login(self):
        # Add code to open the login window
        self.master.iconify()  # Minimize the homepage window
        login_window = tk.Toplevel(self.master)
        LoginPage(login_window, self)
        pass



def main():
    root = tk.Tk()
    app = HomePage(root)
    root.mainloop()


if __name__ == "__main__":
    main()
