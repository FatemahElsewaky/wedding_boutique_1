# function to help user sign up and manipulate database
def signup():
    pass
# function to search for user in database
def search_user():
    pass

# function to login in and manipulate only that user's data
def login():
    pass

# function to ensure
def options(input_d):
    if input_d in ["S", "L"]:
        return input_d
    print("Invalid input, please try again")
    return None


def main_entry():
    """Welcome page and get the user into the system through login or signup"""
    print("Welcome to H.E.M. Bridal Shop! Would you like to sign up or log in?")

    decision_in = input("Enter S to sign up or L to log in: ").strip().upper()
    decision = options(decision_in)
    while decision is None:     # Validate user input
        decision_in = input("Enter S to sign up or L to log in: ").strip().upper()
        decision = options(decision_in)
    return decision
def main_helper():
    decision = main_entry() # track the decision made by user

    username = None     # initializing username
    if decision == "S":
        username = signup()
    elif decision == "L":
        search_user()       # function to search for user in database
        username = login()



def main():
    """Main function that controls the flow of the program"""
    main_helper()