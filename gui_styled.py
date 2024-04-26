import tkinter as tk
from database_code import *
import string

class ProfilePage:
    def __init__(self, master):
        self.master = master
        self.master.title("User Profile")
        self.master.geometry("1280x800")  # Adjusted height for better visibility
        self.master.configure(bg='#FFF8E7')  # Cream background

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
        name_label = tk.Label(master, text=f"{self.user_data['First Name']} {self.user_data['Last Name']}", 
                              font=("Lucida Calligraphy", 36), bg='#FFF8E7', fg='black')
        name_label.pack(pady=20)

        # Adding a line for separation
        separator1 = tk.Frame(master, height=2, bd=1, relief="groove", bg='black')
        separator1.pack(fill="x", padx=20, pady=10)

        # Display username in a better position
        username_label = tk.Label(master, text=f"Username: {self.user_data['Username']}", 
                                  font=("Brush Script MT", 20), bg='#FFF8E7', fg='black')
        username_label.pack(pady=10)

        # Adding more separation
        separator2 = tk.Frame(master, height=2, bd=1, relief="groove", bg='black')
        separator2.pack(fill="x", padx=20, pady=10)

        row = 2
        # Display the rest of the information in the middle of the page
        self.entry_fields = {}
        self.labels = {}
        for key, value in self.user_data.items():
            if key not in ["First Name", "Last Name", "Username"]:
                label = tk.Label(master, text=f"{key}: ", font=("Brush Script MT", 16), 
                                 bg='#FFF8E7', fg='black')
                label.place(x=640-150, y=150+row*30, anchor="e")
                self.labels[key] = label

                entry = tk.Entry(master, font=("Arial", 12), bg='white', fg='black')
                entry.insert(0, value)
                entry.place(x=640-100, y=150+row*30, anchor="w")
                entry.config(state="disabled")
                self.entry_fields[key] = entry
                
                edit_button = tk.Button(master, text="Edit", command=lambda k=key, e=entry: self.toggle_edit_field(k, e))
                
                edit_button.place(x=640+100, y=150+row*30, anchor="w")

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
        self.master.configure(bg='#FFF8E7')  # Cream background

        self.label = tk.Label(master, text="H.E.M.", font=("Lucida Calligraphy", 48), bg='#FFF8E7', fg='black')
        self.label.pack(pady=20)

        # Set background color for the menu bar
        menu_bg_color = self.master.cget("bg")

        # Create a frame to hold the menu bar
        menu_frame = tk.Frame(master, bg=menu_bg_color)  # Add border and relief
        menu_frame.pack(side=tk.TOP, pady=10)

        # Create a dropdown button for the account
        self.account_menu = tk.Menubutton(menu_frame, text="Account", compound=tk.LEFT, bg=menu_bg_color,
                                          font=("Brush Script MT", 18))
        self.account_menu.menu = tk.Menu(self.account_menu, tearoff=0)
        self.account_menu["menu"] = self.account_menu.menu

        # Add options to the account menu
        self.account_menu.menu.add_command(label="Profile", command=self.show_profile)
        self.account_menu.menu.add_command(label="Logout", command=self.logout)

        self.account_menu.pack(side=tk.RIGHT, padx=10)

        # Configure button style to remove button shape
        button_style = {"border": 0, "bg": menu_bg_color, "width": 13, "height": 2}

        buttons_data = [
            ("Wedding Dresses",
            self.show_wedding_dresses),
            ("Collections", self.show_collections),
            ("Styles", self.show_styles),
            ("Brands", self.show_brands)
        ]

        # Create menu buttons
        for text, command in buttons_data:
            button = tk.Button(menu_frame, text=text, font=("Brush Script MT", 24),
                                   command=command, **button_style)
            button.pack(side=tk.LEFT, padx=10)

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


def verify_password(password):
    # At least 8 characters
    if len(password) < 8:
        return False

    # At least one uppercase letter
    if not any(char.isupper() for char in password):
        return False

    # At least one special character
    if not any(char in string.punctuation for char in password):
        return False

    # At least one number
    if not any(char.isdigit() for char in password):
        return False

    return True

class CustomerLoginPage:
    def __init__(self, master):
        self.master = master
        self.master.title("Login / Sign Up")
        self.master.geometry("1280x1920")
        self.master.configure(bg='#FFF8E7')  # Cream background

        self.label_login = tk.Label(master, text="Login", font=("Lucida Calligraphy", 12, "bold"), bg='#FFF8E7',
                                    fg='black')
        self.label_login.pack(pady=10)

        self.label_username = tk.Label(master, text="Username:", font=("Lucida Calligraphy", 12), bg='#FFF8E7',
                                       fg='black')
        self.label_username.pack()

        self.entry_username = tk.Entry(master, bg='white', fg='black')
        self.entry_username.pack()

        self.label_password = tk.Label(master, text="Password:", font=("Lucida Calligraphy", 12), bg='#FFF8E7',
                                       fg='black')
        self.label_password.pack()

        self.entry_password = tk.Entry(master, show="*", bg='white', fg='black')
        self.entry_password.pack()

        self.login_button = tk.Button(master, text="Login", command=self.login, bg='white', fg='black')
        self.login_button.pack(pady=10)

        self.label_signup = tk.Label(master, text="Sign Up", font=("Lucida Calligraphy", 12, "bold"), bg='#FFF8E7',
                                     fg='black')
        self.label_signup.pack(pady=10)

        self.label_new_username = tk.Label(master, text="New Username:", font=("Lucida Calligraphy", 12), bg='#FFF8E7',
                                           fg='black')
        self.label_new_username.pack()

        self.entry_new_username = tk.Entry(master, bg='white', fg='black')
        self.entry_new_username.pack()

        self.label_new_password = tk.Label(master, text="New Password:", font=("Lucida Calligraphy", 12), bg='#FFF8E7',
                                           fg='black')
        self.label_new_password.pack()

        self.entry_new_password = tk.Entry(master, show="*", bg='white', fg='black')
        self.entry_new_password.pack()

        self.label_firstname = tk.Label(master, text="First Name:", font=("Lucida Calligraphy", 12), bg='#FFF8E7',
                                           fg='black')
        self.label_firstname.pack()

        self.entry_firstname = tk.Entry(master, bg='white', fg='black')
        self.entry_firstname.pack()

        self.label_lastname = tk.Label(master, text="Last Name:", font=("Lucida Calligraphy", 12), bg='#FFF8E7',
                                           fg='black')
        self.label_lastname.pack()

        self.entry_lastname = tk.Entry(master, bg='white', fg='black')
        self.entry_lastname.pack()

        self.signup_button = tk.Button(master, text="Sign Up", command=self.signup, bg='white', fg='black')
        self.signup_button.pack(pady=10)

        self.message = tk.Label(master, text="", fg="red", bg='#FFF8E7')
        self.message.pack()

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        # Placeholder authentication logic
        # Replace this with your actual authentication logic
        if u_check_login(username, password):
            self.master.destroy()  # Close the login window
            root = tk.Tk()  # Create a new Tkinter root window for the main page
            app = MainPage(root)  # Open the main page
            root.mainloop()  # Show the homepage
        else:
            self.message.config(text="Invalid username or password")

    def signup(self):
        # Reset the error message label
        self.message.config(text="")
        new_username = self.entry_new_username.get()
        new_password = self.entry_new_password.get()
        firstname = self.entry_firstname.get()
        lastname = self.entry_lastname.get()

        # Verify password
        if not verify_password(new_password):
            self.message.config(text="Password does not meet the requirements.")
        elif not new_username or not new_password:
            self.message.config(text="Please enter both username and password.")
        else:
            if create_user(new_username, new_password, firstname, lastname,  "", "", "", ""):
                self.message.config(text="Sign up successful!")
                self.master.destroy()  # Close the login window
                root = tk.Tk()  # Create a new Tkinter root window for the main page
                app = MainPage(root)  # Open the main page
                root.mainloop()
            else:
                self.message.config(text="Failed to sign up. Please try again.")



class EmployeeLoginPage:
    def __init__(self, master):
        self.master = master
        self.master.title("Login / Sign Up")
        self.master.geometry("1280x1920")
        self.master.configure(bg='#FFF8E7')  # Cream background

        self.label_login = tk.Label(master, text="Login", font=("Lucida Calligraphy", 12, "bold"), bg='#FFF8E7',
                                    fg='black')
        self.label_login.pack(pady=10)

        self.label_employee_id = tk.Label(master, text="Employee ID:", font=("Lucida Calligraphy", 12), bg='#FFF8E7',
                                       fg='black')
        self.label_employee_id.pack()

        self.entry_employee_id = tk.Entry(master, bg='white', fg='black')
        self.entry_employee_id.pack()

        self.label_username = tk.Label(master, text="Username:", font=("Lucida Calligraphy", 12), bg='#FFF8E7',
                                       fg='black')
        self.label_username.pack()

        self.entry_username = tk.Entry(master, bg='white', fg='black')
        self.entry_username.pack()

        self.label_password = tk.Label(master, text="Password:", font=("Lucida Calligraphy", 12), bg='#FFF8E7',
                                       fg='black')
        self.label_password.pack()

        self.entry_password = tk.Entry(master, show="*", bg='white', fg='black')
        self.entry_password.pack()

        self.login_button = tk.Button(master, text="Login", command=self.login, bg='white', fg='black')
        self.login_button.pack(pady=10)


    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        employee_id = self.entry_employee_id.get()

        # Placeholder authentication logic
        # Replace this with your actual authentication logic
        if e_check_login(employee_id, username, password):
            self.master.destroy()  # Close the login window
            root = tk.Tk()  # Create a new Tkinter root window for the main page
            app = MainPage(root)  # Open the choose to edit account or database
            root.mainloop()  # Show the homepage
        else:
            self.message.config(text="Invalid employee ID, username, or password")

class LoginDecide:
    def __init__(self, master, homepage):
        self.master = master
        self.master.title("Login Decision")
        self.master.geometry("1280x1920")
        self.homepage = homepage
        self.master.configure(bg='#FFF8E7')  # Cream background
        self.label = tk.Label(master, text="Customer or Employee", font=("Brush Script MT", 48), bg='#FFF8E7',
                              fg='black')
        self.label.pack(pady=20)

        login_frame = tk.Frame(master, pady=20)
        login_frame.pack()

        customer_login_button = tk.Button(login_frame, text="Login as Customer", command=self.login_customer, height=2,
                                          width=20)
        customer_login_button.pack(side=tk.LEFT, padx=10)

        employee_btn = tk.Button(login_frame, text="Login as Employee", command=self.login_employee, height=2, width=20)
        employee_btn.pack(side=tk.LEFT, padx=10)



    def login_customer(self):
        self.master.destroy()
        root = tk.Tk()  # Create a new Tkinter root window for the main page
        app = CustomerLoginPage(root)  # Open the main page
        root.mainloop()  # Show the homepage

    def login_employee(self):
        self.master.destroy()
        root = tk.Tk()  # Create a new Tkinter root window for the main page
        app = EmployeeLoginPage(root)  # Open the main page
        root.mainloop()  # Show the homepage

class HomePage:
    def __init__(self, master):
        self.master = master
        self.master.title("Bridal Website")
        self.master.geometry("1280x1920")
        self.master.configure(bg='#FFF8E7')  # Cream background

        self.label = tk.Label(master, text="H.E.M.", font=("Lucida Calligraphy", 48), bg='#FFF8E7', fg='black')
        self.label.pack(pady=20)

        self.label_2 = tk.Label(master, text="Welcome to our Bridal Website!", font=("Brush Script MT", 48), bg='#FFF8E7', fg='black')
        self.label_2.pack(pady=20)

        self.login_button = tk.Button(master, text="Login", command=self.open_login, width=20, height=4,
                                      bg ="black", fg="black", font=("Lucida Calligraphy", 36))
        self.login_button.pack(pady=10)

        self.exit_button = tk.Button(master, text="Exit", command=master.quit, bg="black", fg="black", font=("Lucida Calligraphy", 36))
        self.exit_button.pack(pady=10)

    def open_login(self):
        # Add code to open the login window
        self.master.iconify()  # Minimize the homepage window
        login_window = tk.Toplevel(self.master)
        LoginDecide(login_window, self)
        pass

def main():
    root = tk.Tk()
    app = HomePage(root)
    root.mainloop()

if __name__ == "__main__":
    main()
