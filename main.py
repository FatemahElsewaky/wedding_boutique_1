# Imports /////////////////////////////////////////////////////////////////
# importing Packages needed to run the program
import shutil
import string
import sys
import time

from database_helper import *

# Major Global Variables /////////////////////////////////////////////////////////////////

# this will make the login attempts be unlimited and make it easier for testing for unlimited attempts right now
LOGIN_NUM_LIMIT = 1000000000
# Number of users, or accounts, that can be made in this project
USER_NUM_LIMIT = 10

# Print Preset  /////////////////////////////////////////////////////////////////

# Python "Set" Data type for features: this is a quick variable to reference when you need to print out the main menu
FEATURES = {
    "a": "Search for a job",
    "b": "Find someone you know",
    "c": "Learn a new skill",
    "d": "Go to Navigation Links",
    "e": "Show My Network",
    "f": "Check Pending Friend Requests",
    "g": "Display Profiles",
    "h": "Messenger",
    "i": "Log Out",
}

# Python "Set" Data type for MESSENGER: this is a quick variable to reference when printing out the options for messenging people.
MESSENGER = {
    "a": "Inbox",
    "b": "Send Message",
    "c": "Go back",
}

# Python "Set" Data type for INBOX_OPTIONS: this is a quick variable to reference when printing out the inbox options
INBOX_OPTIONS = {
    "a": "Reply",
    "b": "Delete",
    "c": "Go Back",
}

# Python "Set" Data type for Job_Options: this is a quick variable to reference when printing out the job options
JOB_OPTIONS = {
    "a": "Post a job",
    "b": "Apply for a Job",
    "c": "View Jobs",
    "d": "Delete a job",
    "e": "Save/unsave a job for later",
    "f": "Go back",
}

# Python "Set" Data type for Job_LISTING: this is a quick variable to reference when printing out the ways to list job
JOB_LISTING = {
    "a": "List all jobs available",
    "b": "List only applied jobs",
    "c": "List only not applied jobs",
    "d": "List only saved jobs",
    "e": "List only unsaved jobs",
    "f": "Go back",
}

# Python "Set" Data type for Friend_Options: this is a quick variable to reference when printing out the friend search options
FRIEND_OPTIONS = {
    "a": "Find by last name",
    "b": "Find by university",
    "c": "Find by major",
    "d": "Go back",
}

# Python "Set" Data type for Friend Request: this is a quick variable to reference when printing out the friend request options
FRIEND_REQUEST = {
    "a": "Accept",
    "r": "Reject",
    "b": "Go Back",
}

# Python "Set" Data type for Friend Request: this is a quick variable to reference when printing out the friend request options
PROFILE_OPTIONS = {
    "a": "Create or Update Your Profile",
    "b": "Display Your Profile",
    "c": "Display Your Friend's Profile",
    "d": "Go Back",
}

# Python "Set" Data type for Navigation Link: this is a quick variable to reference when printing out the Navigation link options
NAVIGATION_LINKS_GROUP = {
    "a": "Useful Links",
    "b": "InCollege Important Links",
    "c": "Go back",
}

# Python "Set" Data type for Navigation Link: this is a quick variable to reference when printing out the Navigation link options
USEFUL_LINKS_GROUP = {
    "a": "General",
    "b": "Browse InCollege",
    "c": "Business Solutions",
    "d": "Directories",
    "e": "Go back",
}

# Python "Set" Data type for Important Links: this is a quick variable to reference when printing out the Important link options
INCOLLEGE_IMPORTANT_LINKS_GROUP = {
    "a": "A Copyright Notice",
    "b": "About",
    "c": "Accessibility",
    "d": "User Agreement",
    "e": "Privacy Policy",
    "f": "Cookie Policy",
    "g": "Copyright Policy",
    "h": "Brand Policy",
    "i": "Languages",
    "j": "Go back",
}
# Python "Set" Data type for General Link: this is a quick variable to reference when printing out the General link options
# This version is for when the user isn't signed in
NOT_SIGNED_IN_GENERAL_LINKS_GROUP = {
    "a": "Sign Up",
    "b": "Help Center",
    "c": "About",
    "d": "Press",
    "e": "Blog",
    "f": "Careers",
    "g": "Developers",
    "h": "Go back",
}

# Python "Set" Data type for Navigation Link: this is a quick variable to reference when printing out the General link options
# This version is for when the user is signed in
SIGNED_IN_GENERAL_LINKS_GROUP = {
    "a": "Help Center",
    "b": "About",
    "c": "Press",
    "d": "Blog",
    "e": "Careers",
    "f": "Developers",
    "g": "Go back",
}

# Python "Set" Data type for Guest Controls: this is a quick variable to reference when printing out Guest options
GUEST_CONTROLS = {"a": "Email", "b": "SMS", "c": "Target_Advertising"}

# Python "Set" Data type for turning off and on: this is a quick variable to reference when printing out turning off and on options
TURN_ON_OFF = {"a": "Turn On", "b": "Turn Off"}

# Python "list" Data type for skills: this is a quick variable to reference when printing out skills you can learn
SKILLS = ["Python", "Java", "C++", "JavaScript", "SQL"]

# Python "Set" Data type for Languages: this is a quick variable to reference when printing out language options
LANGUAGES = {"a": "English", "b": "Spanish"}

# Minor Global Variables /////////////////////////////////////////////////////////////////

# Login limit should start at false
limit_login = False
# Login attempts should start at zero
login_attempts = 0
# User should be signed out at start
signed_in = False
# Language should not be specified yet before settings
language = ""
# Email is shut off by default
email = 0
# SMS is shut off by default
SMS = 0
# Target Ads is shut off by default
target_ads = 0
# Number of days that a student hasn't applied for a job
# To simulate days passing, we count each login as a seperate day
num_days_since_applied = 0

# Functions ///////////////////////////////////////////////////////////////////////


# Function that prompts the user if they'd like to look for someone
# This is so people can find their friend before signing in
def prompt_person_search():
    """Ask user if they want to search for someone before logging in"""
    decision = (
        input("Before logging in, Do you want to look for someone (Y / N)? ")
        .strip()
        .upper()
    )

    # If yes, do name search function
    if decision == "Y":
        name_search()
    # If no, skip to log in
    elif decision == "N":
        return False
    else:
        # If no matching option, retry this function for an appropriate response
        print("Invalid input, please try again")
        prompt_person_search()


# Function that allow you to log in, or atleast attempt to
def login():
    """Get username and password from user and check if they match a user in the database"""
    draw_line(message="Login")
    username = input("Enter your username: ").strip()
    password = input("Enter your password: ").strip()

    # If you succeed in logging in, then you're signed in under that username
    if check_login(username, password):
        print("You have successfully logged in")
        global signed_in
        signed_in = True

        return username

    # If you fail, you can try to log in again
    # If you fail too many times, then you could be locked out (not implemented yet)
    else:
        print("Incorrect username / password, please try again")
        if try_again():
            return login()


# Function for signing up for a new account
def signup():
    """Signup a new user if the username is not already taken and password meets requirements"""
    db_num_users = get_num_of_users()

    # If user limit is reached, return a none type
    if reached_user_limit(db_num_users):
        return None

    # Sign in header is printed
    draw_line(message="Sign Up")

    # Prompt user for username
    username = input("Enter your username: ").strip()

    # If user already exist, then restart sign up to prompt different username
    if does_username_exist(username):
        print("Username already exists, please try again")
        return signup()

    print(
        """Password must be 8-12 characters long and contain at least \
          one uppercase letter, one digit, and one special character"""
    )

    # Prompt for password
    password_in = input("Enter your password: ").strip()

    # Test the password to see if it works properly
    password = validate_password(password_in)

    # If password returns none, then keep asking for a valid password
    # This will occur untils a valid password is entered
    while password is None:
        password_in = input("Enter your password: ").strip()
        password = validate_password(password_in)

    # Prompt user for first name, last name, university, and major
    firstname = input("Please insert your first name: ")
    lastname = input("Please insert your last name: ")
    university = input("Please insert the university you are attending: ")
    major = input("Please insert your major: ")

    # Ask the user if they wish to upgrade their into database
    print(
        "\nHere at Incollege, we offer the ability for accounts to be upgraded to plus tier. For $10 a month, you can message and contact all users on this site without them being on your friend's list.\n"
    )
    account_type = (
        input("Would you like to upgrade your account? (Y / N): ").strip().upper()
    )

    if account_type == "Y":
        print("\nYou have upgraded your account to plus tier. Thank you!\n")
    else:
        print("\nYou have chosen to stay as a standard user. Thank you!\n")

    tier = 1 if account_type == "Y" else 0

    # If you can create a user with no problems, then sign up is successful
    # Sign them in, set language to english by default, and set email, SMS, and Ads
    if create_user(username, password, firstname, lastname, university, major, tier, 0):
        print("Signup successful!")
        notify_new_user(username, firstname, lastname)
        global signed_in
        signed_in = True
        language = "English"
        email = 1
        SMS = 1
        target_ads = 1
        return username

    # Else, its likely a username error: so restart signup
    else:
        print("Username already exists, please try again")
        return signup()


# Function checks to see if job limit is exceeded.
def reached_job_limit(num_jobs):
    """Check if jobs are as many as users"""
    if num_jobs >= USER_NUM_LIMIT:
        print("All permitted jobs have been created, please come back later")
        return True
    return False


# Function checks to see if user limit is exceeded.
def reached_user_limit(num_users):
    """Check if users are as many as permitted"""
    if num_users == USER_NUM_LIMIT:
        print("All permitted accounts have been created, please come back later")
        return True
    return False


# Function checks to see if password meets requirements for sign up.


def validate_password(input_p):
    """Check if password meets requirements"""

    # Sends a none type if it fails the password check
    if not (
        8 <= len(input_p) <= 12
        and any(char.isupper() for char in input_p)
        and any(char.isdigit() for char in input_p)
        and any(char in string.punctuation for char in input_p)
    ):
        print("Password does not meet requirements, please try again")
        return None

    # Sends back input type if it succeeds the password check
    return input_p


## EPIC #8 Pt.1 Start ########################


# Function that are a series of notifications for the user upon login
def notifications_on_login(username):
    # prints a notification if more than 7 days has passed since they applied for a job
    days = get_days(username)

    print("\n")

    if days >= 7:
        print(
            "Remember - you're going to want to have a job when you graduate. Make sure that you start to apply for jobs today!"
        )

    print("\n")
    # prints a notification if the user hasn't created a profile
    if get_profile(username) is None:
        print("Don't forget to create a profile!")
        print("\n")
    # helper function to check user's inbox to print out a notification if needed
    new_message_check(username)
    print("\n")
    new_notification(username)
    print("\n")


def new_notification(username):
    """Check if user has new messages"""

    new_messages = get_notification(username)

    # If new messages are found for the user, then message user after log in
    # Delete them from the new message messages table
    if new_messages:
        for messages in new_messages:
            print(messages[0])
            print("\n")
            remove_notification(username, messages[1], messages[0])


## EPIC #8 Pt.1 End ########################


# Function that acts as the main menu.
def choose_features(username):
    """Display features and get user's choice"""
    draw_line(message="NOTIFICATIONS")
    # First, it outputs a series of notifications if specific conditions are met
    notifications_on_login(username)

    # Then, it displays a menu full of choices that the user can select
    draw_line(message="Features")
    print(f"Hi {username}! What would you like do?\n")

    # Prints out features of Incollege
    for key, value in FEATURES.items():
        print(f"{key}. {value}")

    # prompt user to select a feature
    feature_choice = input(f"Choose one of {list(FEATURES.keys())}: ").strip().lower()

    # If input matches feature, then go to proper feature
    if feature_choice in FEATURES:
        print(f"You selected {FEATURES[feature_choice]}")
        feature_direct(feature_choice, username)

    # else repeat this function again for a proper feature input
    else:
        print("Feature ID not identied. Please try again")
        return choose_features(username)


# Function designed to direct user to the proper feature
# Feature traveled to changes based on input
def feature_direct(feature_choice, username):
    """Direct user to the feature they chose"""
    if feature_choice == "a":
        job_search(username)
    elif feature_choice == "b":
        friend_search(username)
    elif feature_choice == "c":
        learn_skill(username)
    elif feature_choice == "d":
        choose_navigation_link()
    elif feature_choice == "e":
        show_network(username)
    elif feature_choice == "f":
        check_friend_request(username)
    elif feature_choice == "g":
        display_profile_navigation(username)
    elif feature_choice == "h":
        messenger(username)
    elif feature_choice == "i":
        logout(username)


#### EPIC 7 CHANGES START ###############################


# Checks if a new message is in the user's inbox
# Function is called from the choose_features function
def new_message_check(username):
    """Check if user has new messages"""
    new_messages = get_new_message(username)

    # If new messages are found for the user, then message user after log in
    # Delete them from the new message messages table
    if new_messages:
        print("You have messages waiting for you!\n")
        for messages in new_messages:
            remove_new_message(username, messages[1], messages[0])


# Function designed for messenging people and receiving messages
def messenger(username):
    """Function that allows user to send messages to friends"""
    draw_line(message="MESSENGER")
    print("What would you like do?\n")

    # Prints out features of the messenger
    for key, value in MESSENGER.items():
        print(f"{key}. {value}")

    # prompt user to select a feature
    messenger_choice = (
        input(f"\nChoose one of {list(MESSENGER.keys())}: ").strip().lower()
    )

    # If user enters a, then go to inbox.
    if messenger_choice == "a":
        inbox(username)

    # Else if the user enters b, then go to send message
    elif messenger_choice == "b":
        send_message(username)

    # Else if the user enters c, then prompt user to go back or quit
    elif messenger_choice == "c":
        if go_back():
            return choose_features(username)

    # Else prompt the user to go back or quit
    else:
        if go_back():
            return choose_features(username)


# Function designed to send messages for the standard user
def standard_messenger(username):
    """Function that allows user to send messages to friends"""

    # Ask if user would like to see friends they can message
    check_friends = (
        input(
            "\nWould you like to list your friends before choosing a recepient?(y/n): "
        )
        .strip()
        .lower()
    )

    # Check the friend list of the user
    friend_list = list_of_friends(username)

    # If the user wants to list their friends, then print out their friends
    if check_friends == "y":
        # Check the friend list of the user
        friend_list = list_of_friends(username)

        # If friend list is empty, inform user that they have no friends
        # Send user back to feature select
        if friend_list is False:
            print(
                "\nYou have no friends! Please be aware that you can't message anyone as a standard user if you have no friends.\n"
            )

        # Else print friend list
        else:
            print("\nHere's a list of your friends: \n")
            for i, name in enumerate(friend_list):
                print(f"{name[1]}")

    print("\n")

    # Prompt user for the user they want to send a message to
    receiver = input("Please enter the username of who you wish to send a message to: ")

    # Check if the receiver is an existing user
    # if so, proceed with message
    if get_user(receiver) is not None:
        # Ask user for message
        message = input("Enter your message: ")

        # Prompt user to confirm message
        confirm = (
            input(
                f"\nAre you sure you want to send this message to {receiver}? (y/n): "
            )
            .strip()
            .lower()
        )

        # If user selects yes, then search for the receiver in the friends table
        if confirm == "y":
            # If receiver is found, then add message to the message table
            # Inform user that message has been sent
            if is_friend(username, receiver):
                create_message(message, username, receiver)
                create_new_message(message, username, receiver)
                print("\nMessage sent!\n")
                choose_features(username)

            # If receiver is not found, inform user that they are not friends
            # Send user back to feature select
            else:
                print("\nI'm sorry, you are not friends with that person.\n")
                choose_features(username)

        # If you selects no, or other options, then prompt user to go back to feature select
        else:
            if go_back():
                choose_features(username)

    # If receiver is not found, inform user that the person doesn't exist
    # Send user back to feature select
    else:
        print("The user doesn't exist, please try again")
        choose_features(username)


# Function designed to send messages for the plus users
def plus_messenger(username):
    # Ask user if they want to see all the users they can message
    check_users = (
        input(
            "\nWould you like to list all users in the system before choosing a recepient?(y/n): "
        )
        .strip()
        .lower()
    )

    # If user wants to see all users, then print out all users
    if check_users == "y":
        # Print user list text
        draw_line(message="User List")
        # Check the friend list of the user
        user_list = list_of_users(username)

        # If friend list is empty, inform user that there are no users
        # Send user back to feature select
        if user_list is False:
            print(
                "There are no users in the system to message! Returning to main menu \n"
            )
            choose_features(username)

        # Else print user list
        else:
            print("\nHere's a list of every user in the system:\n")
            for i, name in enumerate(user_list):
                print(name[0])

    print("\n")
    # Prompt user for the user they want to send a message to
    receiver = input("Please enter the username of who you wish to send a message to: ")

    # Check if the receiver is an existing user
    # If so, proceed with message
    if get_user(receiver) is not None:
        # Ask user for message
        message = input("Enter your message: ")

        # Prompt user to confirm message
        confirm = (
            input(
                f"\nAre you sure you want to send this message to {receiver}? (y/n): "
            )
            .strip()
            .lower()
        )

        # If user selects yes, send message to user
        # Add message as new message to the message notification table
        if confirm == "y":
            create_message(message, username, receiver)
            create_new_message(message, username, receiver)
            print("\nMessage sent!\n")
            choose_features(username)

        # If you select no or other options, then prompt user to go back to feature select
        else:
            if go_back():
                choose_features(username)

    # If receiver is not found, inform user that the person doesn't exist
    else:
        print("The user doesn't exist, please try again")
        choose_features(username)


# Function designed to send messages by interpreting what user they are
def send_message(username):
    """Function that allows user to send messages to other users"""
    draw_line(message="SEND MESSAGE")

    # See which tier the user is in
    tier = is_plus_tier(username)

    # If user is in tier 1, call the plus messenger function
    if tier == 1:
        plus_messenger(username)

    # else call the standard messenger function
    else:
        standard_messenger(username)


# Function designed to allow user to view their inbox
def inbox(username):
    """Function that allows user to view inbox"""
    draw_line(message="INBOX")

    # Get inbox text
    inbox_collection = get_message(username)

    # If inbox is empty, print out a message
    if not inbox_collection:
        print("Your inbox is empty")
        choose_features(username)

    # If inbox is not empty, print out the messages
    else:
        print("You have messages: \n")
        for message in inbox_collection:
            print(f"From {message[1]}: {message[0]}\n")

        # Ask user what they would like to do with the messages
        print("\nWhat would you like to do with these messages?")
        for key, value in INBOX_OPTIONS.items():
            print(f"{key}. {value}")
        inbox_choice = (
            input(f"\nChoose one of {list(INBOX_OPTIONS.keys())}: ").strip().lower()
        )

        # If option a, reply to message
        if inbox_choice == "a":
            reply_message(username)

        # Else if option r, delete the message
        elif inbox_choice == "b":
            delete_message(username)

        # Else if option b, prompt return to the main menu or quit
        elif inbox_choice == "c":
            if go_back():
                choose_features(username)

        # Else go back to the main menu
        else:
            if go_back():
                choose_features(username)


# Function designed to allow user to reply to messages
def reply_message(username):
    """Function that allows user to reply to messages"""
    draw_line(message="REPLY MESSAGE")

    # prompt user for user they wish to address
    receiver = input("\nPlease enter the name of the user you wish to reply to: ")

    # Check if the receiver is an existing user and that they've messaged each other
    if get_transaction(username, receiver):
        # Prompt user for message
        reply = input("\nPlease enter your reply: ")

        # Prompt user to confirm message
        confirm = (
            input(
                f"\nAre you sure you want to send this message to {receiver}? (y/n): "
            )
            .strip()
            .lower()
        )

        # If user selects yes, then send relpy to the user
        # Add message as new message to the message notification table
        if confirm == "y":
            create_message(reply, username, receiver)
            create_new_message(reply, username, receiver)
            print("\nMessage sent!\n")
            choose_features(username)

        # If you select no or other options, then prompt user to go back to feature select
        else:
            print("\n")
            if go_back():
                choose_features(username)

    # If receiver is not found, inform user that the person doesn't exist
    else:
        print(
            "\nThe user doesn't exist, or hasn't sent a message for replying. Please try again."
        )
        choose_features(username)


# Function designed to allow user to delete messages
def delete_message(username):
    """Function that allows user to delete messages"""
    draw_line(message="DELETE MESSAGE")

    # Prompt user for user they wish to address
    receiver = input(
        "\nPlease enter the name of the user you wish to delete a message from: "
    )

    # Prompt user to enter the message they wish to delete
    message = input("\nPlease enter the message you wish to delete: ")

    # Confirm if user wishes to delete this message
    confirm = (
        input(
            f"\nAre you sure you want to delete this message from {receiver}? (y/n): "
        )
        .strip()
        .lower()
    )

    # If user selects yes, then delete the message after a check
    if confirm == "y":
        # If the message can be deleted, delete the message from the message notification table
        if remove_message(username, receiver, message):
            print("\nMessage deleted!\n")
            choose_features(username)

        # If the message can't be deleted, inform user that the message doesn't exist
        else:
            print("\nMessage not found. Please try again.\n")
            choose_features(username)

    # If you select no or other options, then prompt user to go back to feature select
    else:
        print("\n")
        if go_back():
            choose_features(username)

    #### EPIC 7 CHANGES END ###############################


## EPIC #8 Pt.2 Start ########################
def notify_applied_jobs(student_id):
    applied_jobs_count = applied_jobs_list(student_id)
    applied_jobs_count = len(applied_jobs_count)
    if applied_jobs_count:
        print(f"You have currently applied for {applied_jobs_count } job(s) total.")
    else:
        print("You have not applied for any jobs yet")


def notify_new_user(username, firstname, lastname):
    message = f"{firstname} {lastname} has joined InCollege"
    allusers = list_of_users(username)
    for i, name in enumerate(allusers):
        create_notification(message, "System", name[0])


def notify_new_job(username, new_job_title):
    """Notify userx that a new job has been posted"""

    message = f"A new job for {new_job_title} has been posted"
    allusers = list_of_users(username)
    for i, name in enumerate(allusers):
        create_notification(message, "System", name[0])


def notify_deleted_applied_job(username, deleted_job_title):
    """Notify user that a job they applied to was deleted"""

    message = f"A job you applied for, {deleted_job_title}, has been deleted"
    userlist = get_applicants_for_job(deleted_job_title)
    for i, name in enumerate(userlist):
        print(name)
        create_notification(message, "System", name)


## EPIC #8 Pt.2 END ########################


# Function designed to help user search for jobs
def job_search(username):
    """Job search page"""
    draw_line(message="JOB_OPTIONS")

    notify_applied_jobs(username)
    print("\n")

    # Prompt and list options for job search
    print("What would you like to do with jobs?")
    for key, value in JOB_OPTIONS.items():
        print(f"{key}. {value}")
    feature_choice = input(f"Choose one of {list(JOB_OPTIONS.keys())}:").strip().lower()

    # If feature a is chosen, then post job
    if feature_choice == "a":
        job_posting(username)

    # Else if feature b is chosen, then list all jobs by default
    elif feature_choice == "b":
        job_select(username)

    # Else if feature c is chosen, then go to special job listings for viewing
    elif feature_choice == "c":
        job_listing(username)

    # Else if feature d is chosen, then delete a job
    elif feature_choice == "d":
        job_delete(username)

    # Else if feature e is chosen, then save the job
    elif feature_choice == "e":
        save_job(username)

    # Else if feature e is chosen, then prompt to go back to feature select
    elif feature_choice == "f":
        if go_back():
            choose_features(username)
    else:
        print("Invalid input. Please try again.")
        choose_features(username)


# Function to post a job
def job_posting(username):
    """Post a job page"""
    db_num_jobs = get_num_of_jobs()

    # Return none if job limit has been reached
    if reached_job_limit(db_num_jobs):
        return None

    # Print job posting line
    draw_line(message="JOB_POSTING")

    # Prompt user for job's title, description, employer, location, and salary
    job_title = input("Please enter the job's title: ")
    job_description = input("Please enter the job's description: ")
    job_employer = input("Please enter the job's employer: ")
    job_location = input("Please enter the job's location: ")
    job_salary = input("Please enter the job's salary: ")

    # Use create job function to use input data for a job entry
    # *** This function is in the database_helper
    create_job(
        job_title,
        job_description,
        job_employer,
        job_location,
        job_salary,
        get_first_name(username),
        get_last_name(username),
    )

    # Inform user that the job has been created
    print(
        "\nJob created: Thank You for posting. We hope you'll find great employees!\n"
    )
    notify_new_job(username, job_title)
    # Go back to feature select by default
    choose_features(username)


# Function designed to delete a job
def job_delete(username):
    """Job delete page"""
    draw_line(message="JOB DELETE")
    print("Here are the jobs you posted that you can delete:\n")
    jobs = get_job_list_posted_by_user(
        get_first_name(username), get_last_name(username)
    )
    if jobs:
        for idx, job in enumerate(jobs):
            print(f"{idx + 1} - {job}")
    else:
        print("You have not posted any jobs yet. So you can't delete any jobs.")

    # Prompt user to select a job to delete
    if jobs:
        delete_job_confirmation = input("Would you like to delete a job? y/n: ").lower()
        if delete_job_confirmation == "y":
            delete_job_title = input("Please enter the job title you want to delete: ")
            if delete_job_title in jobs:
                delete_job(delete_job_title)
                clean_saved_jobs_when_job_deleted(delete_job_title)
                notify_deleted_applied_job(username, delete_job_title)
                print("Job deleted successfully!")
            else:
                print("You don't have a job with that title.")
        elif delete_job_confirmation == "n":
            print("You have chosen not to delete a job.")
        else:
            print("Invalid input. Please try again.")

    # Go back to feature select by default
    if go_back():
        choose_features(username)


def save_job(username):
    """Save/unsave a job page"""
    draw_line(message="SAVE/UNSAVE JOB FOR LATER")
    print("Here are the jobs you can save for later:\n")
    jobs = [
        unsaved_job
        for unsaved_job in all_jobs_list(username)
        if unsaved_job not in get_saved_jobs(username)
    ]
    if jobs:
        for idx, job in enumerate(jobs):
            print(f"{idx + 1} - {job}")
    else:
        print("There are no jobs you can save for later.")

    # Prompt user to select a job to save
    save_job_confirmation = input("Would you like to save a job? y/n: ").lower()
    if save_job_confirmation == "y":
        save_job_title = input("Please enter the job title you want to save: ")
        if save_job_title in jobs:
            save_job_for_user(username, save_job_title)
            print("Job saved successfully!")
        else:
            print("We don't have a job with that title.")
    elif save_job_confirmation == "n":
        print("You have chosen not to save a job.")
    else:
        print("Invalid input. Please try again.")

    unsave_job_confirmation = input("\nWould you like to unsave a job? y/n: ").lower()
    if unsave_job_confirmation == "y":
        saved_jobs = get_saved_jobs(username)
        if saved_jobs:
            print("Here are the jobs you can unsave:")
            for idx, job in enumerate(saved_jobs):
                print(f"{idx + 1} - {job}")
            print("\n")
            unsave_job_title = input("Please enter the job title you want to unsave: ")
            if unsave_job_title in get_saved_jobs(username):
                delete_saved_job(username, unsave_job_title)
                print("Job unsaved successfully!")
            else:
                print("We don't have a job with that title.")
        else:
            print("There are no jobs you can unsave.")
    elif unsave_job_confirmation == "n":
        print("You have chosen not to unsave a job.")
    else:
        print("Invalid input. Please try again.")

    # Go back to feature select by default
    if go_back():
        choose_features(username)


# Function designed to let user decide on how to view jobs
def job_listing(username):
    """Job list page"""
    draw_line(message="JOB_LISTING")

    # Prompt user to select the way they'd like to view the list of jobs
    print("How would you like to view the jobs listed?")
    for key, value in JOB_LISTING.items():
        print(f"{key}. {value}")
    feature_choice = input(f"Choose one of {list(JOB_LISTING.keys())}:").strip().lower()

    # Select appropriate list based on input
    # User can also go back instead of searching

    # If feature a is chosen, then list all jobs by default
    if feature_choice == "a":
        list_all_jobs(username)

    # Else if feature b is chosen, then list all jobs the user applied to
    elif feature_choice == "b":
        list_applied_jobs(username)

    # Else if feature c is chosen, then list all jobs the user did NOT applied to
    elif feature_choice == "c":
        list_unapplied_jobs(username)

    # Else if feature d is chosen, then list all jobs that the user has saved
    elif feature_choice == "d":
        show_saved_jobs(username)

    elif feature_choice == "e":
        show_unsaved_jobs(username)

    # Else if feature e is chosen, then prompt user to go back to feature select or quit
    elif feature_choice == "f":
        if go_back():
            choose_features(username)

    # Else, prompt user to go back to feature select or quit
    else:
        if go_back():
            choose_features(username)


def show_saved_jobs(username):
    """show saved jobs page"""
    draw_line(message="SHOW_SAVED_JOBS")

    saved_jobs = get_saved_jobs(username)
    if saved_jobs:
        print("Here are the jobs you saved for later:\n")
        for idx, job in enumerate(saved_jobs):
            print(f"{idx + 1} - {job}")
    else:
        print("There are no jobs you saved for later.")

    # Go back to feature select by default
    if go_back():
        choose_features(username)


def show_unsaved_jobs(username):
    """show unsaved jobs page"""
    draw_line(message="SHOW_UNSAVED_JOBS")

    unsaved_jobs = [
        unsaved_job
        for unsaved_job in all_jobs_list(username)
        if unsaved_job not in get_saved_jobs(username)
    ]
    if unsaved_jobs:
        print("Here are the jobs you have not saved for later:\n")
        for idx, job in enumerate(unsaved_jobs):
            print(f"{idx + 1} - {job}")
    else:
        print("You have saved all the jobs")

    # Go back to feature select by default
    if go_back():
        choose_features(username)


# Function designed to list all available jobs
def list_all_jobs(username):
    """job selection page"""
    draw_line(message="LIST_ALL_JOBS")

    # Get all jobs from database
    all_jobs = all_jobs_list(username)
    applied_jobs = applied_jobs_list(username)

    # Print all jobs and prompt user if they wish to apply to any of the jobs listed
    if all_jobs:
        print("\nHere are all jobs available:\n")
        for job in all_jobs:
            if job in applied_jobs:
                print(f"[Applied] {job}")
            else:
                print(f"[] {job}")

        print("\n")

        view_info = input(
            "Do you want to apply to any of the jobs on this list? y/n?: "
        ).lower()

        # If user selects yes, have them search for the job
        if view_info == "y":
            apply_for_job(username)

        # If you select no or other options, then prompt user to go back to feature select
        else:
            if go_back():
                choose_features(username)

    # Else, inform user that there are no jobs listed
    else:
        print("\nThere are no jobs opening on inCollege.")
        choose_features(username)


# Function designed to list all jobs the user has applied to
def list_applied_jobs(username):
    """job selection page"""
    draw_line(message="LIST_APPLIED_JOBS")
    # Get all job applications the user has made from the database
    applied_jobs = applied_jobs_list(username)

    # Print all jobs and prompt user if they wish to apply to any of the jobs listed
    if applied_jobs:
        print("\nListing all jobs you've applied for:\n")

        for job in applied_jobs:
            print(f"[Applied] {job}")

        print("\n")

        print(
            "You have already applied to these jobs, and cannot resend an application.\n"
        )
        if go_back():
            choose_features(username)

    # Else, inform user that there are no jobs listed
    else:
        print("\nThere are no jobs you've applied for.")
        choose_features(username)


# Function designed to list all jobs the user has NOT applied to
def list_unapplied_jobs(username):
    """job selection page"""
    draw_line(message="LIST_UNAPPLIED_JOBS")
    # Get all job applciations the user has made from the database
    applied_jobs = applied_jobs_list(username)

    # If there is atleast one job the user has applied to...
    if applied_jobs:
        # Make a set containing the titles of all jobs the user has applied to
        s = set(applied_jobs)

        # Get all jobs from the database
        # Keep only the titles of the jobs that the user has not applied to
        unapplied_jobs = [job for job in all_jobs_list(username) if job not in s]

        # If there are job titles that the user hasn't applied to...
        # Print them and prompt user if they wish to apply to any of the jobs listed
        if unapplied_jobs:
            print("\nListing all jobs you have NOT applied for:\n")

            for job in unapplied_jobs:
                print(f"[] {job}")

            print("\n")

            view_info = input(
                "Do you want to apply to any of the jobs on this list? y/n?: "
            ).lower()

            # If user selects yes, have them search for the job
            if view_info == "y":
                apply_for_job(username)

            # If you select no or other options, then prompt user to go back to feature select
            else:
                if go_back():
                    choose_features(username)

        # Else, inform user that there are no jobs listed
        else:
            print("\nThere are no jobs you have NOT applied for.")
            choose_features(username)

    # Else, if there are no job applications, then the user has not applied to any jobs.
    # This means all of the jobs are unapplied: and the user can apply to any of them
    else:
        all_jobs = all_jobs_list(username)
        print("\nListing all jobs you have NOT applied for:\n")
        for job in all_jobs:
            if job in applied_jobs:
                print(f"[Applied] {job}")
            else:
                print(f"[] {job}")

        print("\n")
        view_info = input(
            "Do you want to apply to any of the jobs on this list? y/n?: "
        ).lower()

        # If user selects yes, have them search for the job
        if view_info == "y":
            apply_for_job(username)

        # If you select no or other options, then prompt user to go back to feature select
        else:
            if go_back():
                choose_features(username)


# Function designed to select a job to apply (list all available jobs by default)
def job_select(username):
    """job selection page"""
    draw_line(message="JOB_SELECT")
    # Get all jobs from database
    all_jobs = all_jobs_list(username)
    applied_jobs = applied_jobs_list(username)

    # Print all jobs and prompt user if they wish to apply to any of the jobs listed
    if all_jobs:
        print("\nHere are all jobs available:\n")
        for job in all_jobs:
            if job in applied_jobs:
                print(f"[Applied] {job}")
            else:
                print(f"[] {job}")

        print("\n")
        view_info = input(
            "Do you want to apply to any of the jobs on this list? y/n?: "
        ).lower()

        # If user selects yes, have them search for the job
        if view_info == "y":
            apply_for_job(username)

        # If you select no or other options, then prompt user to go back to feature select
        else:
            if go_back():
                choose_features(username)
    # Else, upon a failed search, inform the user that no account has that last name
    else:
        print("\nThere are no jobs opening on inCollege.")
        choose_features(username)


# Function designed to search for a job title, then confirm their selectiom
def apply_for_job(username):
    draw_line(message="JOB_CONFIRM")
    """Promopt the user to search by job title , inform them, and ask for confirmation"""
    job_title = input("\nEnter the title of the job you want to apply for: ")

    # Check if the job title exist
    job_info = get_job(job_title)

    # If the job title exists, inform the user about the job
    if job_info:
        print("\nThis is the current job information for this title:")
        print(f"\nTitle: {job_info[0]}")
        print(f"Description: {job_info[1]}")
        print(f"Employer: {job_info[2]}")
        print(f"Location: {job_info[3]}")
        print(f"Salary: {job_info[4]}")
        print("\n")

        # Prompt user to confirm their selection
        confirm_apply = input(
            "Confirm this job and send the application? y/n?: "
        ).lower()

        # If user selects yes, peform the send application function
        if confirm_apply == "y":
            send_application(username, job_title)

        # If you select no or other options, then prompt user to go back to feature select
        else:
            if go_back():
                choose_features(username)

    # Else, inform the user that the user does not exist, then repeat job select
    else:
        print("There is no job with that title, please try again.")
        job_select(username)


# Function designed to store and sav application
def send_application(username, job_title):
    # First, check and see if the user has already applied to this job
    application_check = search_application(username, job_title)
    # Second, check and see if the user had posted this job
    origin_check = user_made_job(
        get_first_name(username), get_last_name(username), job_title
    )

    # If the user has applied to this job, inform them that they have already applied
    # Nothing happens, and they are sent to the feature select
    if application_check is True:
        print(
            "\nYou have already applied to this job, and cannot resend an application."
        )
        choose_features(username)

    # If user created this job, inform them that they can't apply to a job they created
    elif origin_check is True:
        print("\nYou can't hire yourself for a job you posted!")
        choose_features(username)

    # If the user has not applied to this job, and they don't own it, then send the application
    elif application_check is False:
        # Take user's predicted graduaton date
        print("\n")
        graduation = input("Please enter your predicted graduation date(mm/dd/yyyy): ")

        # Take user's predicted starting date or first day of work
        print("\n")
        start = input("Please enter your predicted start date(mm/dd/yyyy): ")

        # Take user's reason why they'd be fit for this job
        print("\n")
        description = input("Please explain why you'd be a great fit for this job: ")

        # Take user's information and save as an application
        print("\n")
        verify_apply = create_application(
            username, job_title, graduation, start, description
        )

        # If the user's application saves successfully, inform them that their application has been sent
        if verify_apply:
            print("Application sent. We wish you luck on obtaining the position!\n")
            # num_days_since_applied resets to 0 upon the application being saved successfully
            # as to reset the 7 day timer for the notificaiton
            reset_days(username)
            choose_features(username)


# Function that helps you search for friends
def friend_search(username):
    """Friend search page"""
    draw_line(message="FRIEND_SEARCH")

    # Prompt user for how they'd like to search for friends
    print("How would you like to search for friends?")
    for key, value in FRIEND_OPTIONS.items():
        print(f"{key}. {value}")
    feature_choice = (
        input(f"Choose one of {list(FRIEND_OPTIONS.keys())}:").strip().lower()
    )

    # Select appropriate search based on input, then return to feature select
    # User can also go back instead of searching
    if feature_choice == "a":
        last_name_search(username)
        choose_features(username)
    if feature_choice == "b":
        university_search(username)
        choose_features(username)
    if feature_choice == "c":
        major_search(username)
        choose_features(username)
    elif feature_choice == "d":
        if go_back():
            choose_features(username)


# Function designed to search the name of someone you knoe
def name_search():
    """name search page"""
    draw_line(message="NAME_SEARCH")

    # prompt the user for a first and last name
    friend_firstname = input("Please enter your friend's first name: ")
    friend_lastname = input("Please enter your friend's last name: ")

    # Use search name function to see if the person exist
    # *** This function is in database_helper
    result = search_name(friend_firstname, friend_lastname)

    # If result works, then inform the user they exist.
    if result:
        print(
            f"\n{friend_firstname} {friend_lastname} is an existing user on inCollege."
        )

    # Else inform the user they don't exist.
    else:
        print(
            f"\n{friend_firstname} {friend_lastname} is not yet an existing user on inCollege."
        )


# Function searches for name based on last name
def last_name_search(username):
    """last name search page"""
    draw_line(message="LAST_NAME_SEARCH")

    # Prompt user for last name
    friend_lastname = input("Please enter a last name: ")

    # Check to see if a user has this last name
    friend_username = get_username_from_last_name(friend_lastname)

    # If you find them, then you can prompt the user to send them as a friend request
    if friend_username != False:
        print(f"\nPrinting usernames of users with the last name {friend_lastname}")
        print(f"\n{', '.join(friend_username)}")
        choice = input(
            "Do you want to request to connect with someone from this list? y/n?: "
        ).lower()

        # If you select yes, send them a friend request
        if choice == "y":
            send_friend_request(username)
        # If you select no or other options, then prompt user to go back to feature select
        else:
            if go_back():
                choose_features(username)
    # Else, upon a failed search, inform the user that no account has that last name
    else:
        print(
            f"\nThere are no users that have the last name {friend_lastname} on inCollege."
        )


# Function that searches users based off university
def university_search(username):
    """university search page"""
    draw_line(message="UNIVERSITY_SEARCH")

    # Prompt the user for a university to search for
    friend_university = input("Please enter a university: ")

    # Check the university, then compare the users with this university
    friend_username = get_username_from_university(friend_university)

    # If at least one student is associated with this unversity, show the list of students
    if friend_username != False:
        print(f"\nPrinting usernames of users attending {friend_university}")
        print(f"\n{', '.join(friend_username)}")

        # Prompt user to send friend request
        choice = input(
            "Do you want to request to connect with someone from this list? y/n?: "
        ).lower()

        # If yes, then send frend request
        if choice == "y":
            send_friend_request(username)

        # Else, prompt user to go back to feature select
        else:
            if go_back():
                choose_features(username)

    # Else, inform the user that no student is associated with this university
    else:
        print(f"\nThere are no users that attend {friend_university} on inCollege.")


# Function that searches for students based off major
def major_search(username):
    """major search page"""
    draw_line(message="MAJOR_SEARCH")

    # Prompt the user for a major to search for
    friend_major = input("Please enter a major: ")

    # Check the major, then compare the users with this major
    friend_username = get_username_from_major(friend_major)

    # If at least one student is associated with this major, show the list of students
    if friend_username != False:
        print(
            f"\nPrinting usernames of users who are taking this major: {friend_major}"
        )
        print(f"\n{', '.join(friend_username)}")

        # Prompt user to send friend request
        choice = input(
            "Do you want to request to connect with someone from this list? y/n?: "
        ).lower()

        # If yes, then send frend request
        if choice == "y":
            send_friend_request(username)

        # Else, prompt user to go back to feature select
        else:
            if go_back():
                choose_features(username)
    # Else, inform the user that no student is associated with this major
    else:
        print(
            f"\nThere are no users that are taking this major: {friend_major} on inCollege."
        )


# Function sends friend request out to a specific user
def send_friend_request(sender_username):
    """Send a friend request to another user"""
    friend_username = input("Enter the username of the user you want to connect with: ")

    # Check if the user exists
    add_friend(sender_username, friend_username)

    # If the user exists, inform the user that the request has been sent
    if add_friend:
        print(f"Friend request sent to {friend_username}!")

    # Else, inform the user that the user does not exist
    else:
        print("Invalid input, please try again")
        send_friend_request(sender_username)


# Function that prints the skills learned
def learn_skill(username):
    """Learn skill page"""
    draw_line(message=FEATURES["c"])

    # Print to the user all of the skills they can learn
    print("Here are some skills you can learn:")
    for i, skill in enumerate(SKILLS):
        print(f"{i + 1}. {skill}")

    # Print the option to go back to feature select
    print("6. Go back")

    # Prompt the user to choose a skill to learn
    skill_choice = input(f"Enter integers from 1 to {len(SKILLS) + 1}: ").strip()

    # If the user chooses a skill, then go to that skill's page (not implemented yet)
    if skill_choice.isdigit() and 1 <= int(skill_choice) <= len(SKILLS):
        single_skill(username, int(skill_choice))

    # Else if skill choic is 6, prompt user to go back to feature select
    elif skill_choice.isdigit() and int(skill_choice) == 6:
        print("Not picking to learn a new skill?")
        if go_back():
            choose_features(username)

    # Else, inform the user that the input is invalid
    else:
        print("Invalid input, please try again")
        learn_skill(username)


# Function that prints the skills learned
def single_skill(username, skill_choice):
    """Learn skill page"""
    draw_line(message=SKILLS[skill_choice - 1])

    # Print to the user that the skill is under construction (not implemented)
    print("under construction")

    # Prompt the option to go back to feature select
    if go_back():
        learn_skill(username)


# Function that determines if you want to sign in or login
def options(input_d):
    """Options page"""
    # Prompt the user to choose if they want to sign in or login
    if input_d in ["S", "L"]:
        return input_d
    # Else, inform the user that the input is invalid and return none type
    print("Invalid input, please try again")
    return None


# Function that controls navigation link feature
def choose_navigation_link():
    """Display navigation links and get user's choice"""
    draw_line(message="Navigation Links")
    print("What link would you like to go to?")
    for key, value in NAVIGATION_LINKS_GROUP.items():
        print(f"{key}. {value}")

    # Prompt the user to choose a link
    navigation_link_choice = (
        input(f"Choose one of {list(NAVIGATION_LINKS_GROUP.keys())}: ").strip().lower()
    )
    # If the user chooses a link, then go to that link
    if navigation_link_choice in NAVIGATION_LINKS_GROUP:
        print(f"You selected {NAVIGATION_LINKS_GROUP[navigation_link_choice]}")
        navigation_link_direct(navigation_link_choice)
    # Else, inform the user that the input is invalid then try again
    else:
        print("Link not identfied. Please try again")
        return choose_navigation_link()


# Function that directs user to correct navigation link feature
def navigation_link_direct(navigation_link_choice, username="test"):
    """Direct user to the naviagation link they chose"""
    if navigation_link_choice == "a":
        choose_useful_links()
    elif navigation_link_choice == "b":
        choose_incollege_important_links()
    elif navigation_link_choice == "c":
        if go_back():
            if signed_in == True:
                choose_features(username)
            else:
                links_or_login()


# Function that selects the useful links
def choose_useful_links():
    """Display useful links and get user's choice"""
    draw_line(message="Useful Links")
    print("What link would you like to go to?")
    for key, value in USEFUL_LINKS_GROUP.items():
        print(f"{key}. {value}")

    # Prompt the user to choose a link
    useful_link_choice = (
        input(f"Choose one of {list(USEFUL_LINKS_GROUP.keys())}: ").strip().lower()
    )

    # If the user chooses a link, then go to that link
    if useful_link_choice in USEFUL_LINKS_GROUP:
        print(f"You selected {USEFUL_LINKS_GROUP[useful_link_choice]}")
        useful_link_direct(useful_link_choice)

    # Else, inform the user that the input is invalid then try again
    else:
        print("Link not identfied. Please try again")
        return choose_useful_links()


# Function that directs user to correct useful link feature
def useful_link_direct(useful_link_choice):
    """Direct user to the useful link they chose"""
    if useful_link_choice == "a":
        general()
    elif useful_link_choice == "b":
        browse_incollege()
    elif useful_link_choice == "c":
        business_solutions()
    elif useful_link_choice == "d":
        directories()
    elif useful_link_choice == "e":
        if go_back():
            choose_navigation_link()


# Function that selects the incollege important links
def important_link_direct(important_link_choice):
    """Direct user to the useful link they chose"""
    if important_link_choice == "a":
        copyright_notice()
    elif important_link_choice == "b":
        about_important()
    elif important_link_choice == "c":
        accessibility()
    elif important_link_choice == "d":
        user_agreement()
    elif important_link_choice == "e":
        privacy_policy()
    elif important_link_choice == "f":
        cookie_policy()
    elif important_link_choice == "g":
        copyright_policy()
    elif important_link_choice == "h":
        brand_policy()
    elif important_link_choice == "i":
        languages()
    elif important_link_choice == "j":
        if go_back():
            choose_navigation_link()


# Function that selects the incollege important links
def choose_incollege_important_links():
    draw_line(message="InCollege Important Links")
    print("What link would you like to go to?")
    for key, value in INCOLLEGE_IMPORTANT_LINKS_GROUP.items():
        print(f"{key}. {value}")

    # Prompt the user to choose a link
    important_link_choice = (
        input(f"Choose one of {list(INCOLLEGE_IMPORTANT_LINKS_GROUP.keys())}: ")
        .strip()
        .lower()
    )

    # If the user chooses a link, then go to that link
    if important_link_choice in INCOLLEGE_IMPORTANT_LINKS_GROUP:
        print(f"You selected {INCOLLEGE_IMPORTANT_LINKS_GROUP[important_link_choice]}")
        important_link_direct(important_link_choice)

    # Else, inform the user that the input is invalid then try again
    else:
        print("Link not identified. Please try again")
        return choose_incollege_important_links()


# Function that prints the copyright notice
def copyright_notice():
    draw_line(message="A Copyright Notice")

    print("© Team_Arizona_2023_forever")
    print("All rights reserved")

    # Prompt the user to return to the main menu or quit
    if go_back():
        choose_incollege_important_links()


# Function that prints the accesibility information
def accessibility():
    draw_line(message="Accessibility")

    print(
        "We are committed to ensuring that our platform is accessible to all users,including those with disabilities. Here are some of the features we have implemented to enhance accessibility: "
    )
    print("Coming Soon🙂")
    print(
        "If you encounter any accessibility issues or have suggestions for improvement,please contact us at Team Arizona."
    )

    # Prompt the user to return to the main menu or quit
    if go_back():
        choose_incollege_important_links()


# Function that prints the user agreement information
def user_agreement():
    draw_line(message="User Agreement")

    print(
        "By using our platform, you agree to abide by the following terms and conditions: \n <Respect the rights of other users> \n <Do not engage in any unlawful activities on our platform.> \n <Abide by our community guidelines.> \n <Protect your account credentials and personal information.> \n <Report any suspicious or inappropriate content.> \n \n \n <Failure to comply with these terms may result in account suspension or termination.>"
    )

    # Prompt the user to return to the main menu or quit
    if go_back():
        choose_incollege_important_links()


# Function that prints the privacy policy information
def privacy_policy():
    draw_line(message="Privacy Policy")

    print("a. Guest Controls")
    print("b. Go Back")

    # Prompt the user to choose a guest control
    option = input(f"Choose one of {list(GUEST_CONTROLS.keys())}:").strip().lower()

    # If the user chooses a guest control, then go to that guest control
    if option == "a":
        guest_controls()

    # Else, prompt the user to return to the main menu or quit
    else:
        if go_back():
            choose_incollege_important_links()


# Function that prints the cookie policy information
def cookie_policy():
    draw_line(message="Cookie Policy")

    print(
        "Our website uses cookies to improve your experience. By continuing to use our site, you accept our use of cookies."
    )

    # Prompt the user to return to the main menu or quit
    if go_back():
        choose_incollege_important_links()


# Function that prints the copyright policy information
def copyright_policy():
    draw_line(message="Copyright Policy")

    print(
        "All content on this platform is protected by copyright laws. The content includes but is not limited to text, images, logos, and graphics \n You may not reproduce, distribute, or modify our content without explicit written permission from us \n For copyright-related inquiries, please contact: legal@incollege.com."
    )

    # Prompt the user to return to the main menu or quit
    if go_back():
        choose_incollege_important_links()


# Function that prints the brand policy information
def brand_policy():
    draw_line(message="Brand Policy")

    print(
        "Our brand is a valuable asset, including our name, logo, and visual identity. To maintain consistency and integrity, we have established guidelines for the use of our brand elements. \n \n You may not use our brand elements without prior written permission. Any use must adhere to our brand guidelines \n \n If you require the use of our brand for any purpose, please contact us to request approval."
    )

    # Prompt the user to return to the main menu or quit
    if go_back():
        choose_incollege_important_links()


# Function to choose guess controls and how you'll turn it on and off
def guest_controls():
    draw_line(message="Guest Controls")

    # If user is signed in: Prompt the user to choose a guest control
    if signed_in:
        for key, value in GUEST_CONTROLS.items():
            print(f"{key}. {value}")
        option = input(f"Choose one of {list(GUEST_CONTROLS.keys())}:").strip().lower()

    # Apply the appropriate option and control if it gets turned on or off
    # Note this that if a user isn't logged in, this is designed to skip guest control changes
    change = turn_on_off(option)

    # Prompt the user to return to the main menu or quit
    if go_back():
        choose_incollege_important_links()


# Function designed to turn guest controls on or off
def turn_on_off(x):
    """ "List and prompt the option to turn on and off a guest control"""
    for key, value in TURN_ON_OFF.items():
        print(f"{key}. {value}")
    option = input(f"Choose one of {list(TURN_ON_OFF.keys())}:").strip().lower()

    # If option a, control email on/off status
    if x == "a":
        if option == "a":
            email = 1
        else:
            email = 0

        return email

    # Else if option b, control SMS on/off status
    elif x == "b":
        if option == "a":
            SMS = 1
        else:
            SMS = 0

        return SMS

    # Else if option c, control targeted ads on/off status
    elif x == "c":
        if option == "a":
            target_ads = 1
        else:
            target_ads = 0

        return target_ads


# Function designed to control language preference
def languages():
    draw_line(message="Languages")

    # If user is signed in: Prompt the user to choose a language
    # Note this that if a user isn't logged in, this is designed to skip language changes
    if signed_in:
        for key, value in LANGUAGES.items():
            print(f"{key}. {value}")
        language = LANGUAGES[
            input(f"Choose one of {list(LANGUAGES.keys())}:").strip().lower()
        ]
    # Apply the appropriate language preference if it gets changed
    print(f"Congratulations, the app language has been changed to {language}")

    # Prompt the user to return to the main menu or quit
    if go_back():
        choose_incollege_important_links()


# Function designed to check friend request
def check_friend_request(username):
    """Check if friend request table is filled, if yes ask to accept or reject, if no continue"""
    draw_line(message="Pending Friend Requests")
    friend_request = pending_friend_request_list(username)
    if friend_request is False:
        print("You have no friend requests!")
        choose_features(username)
    else:
        print("You have a pending friend request from:")
        for i, name in enumerate(friend_request):
            print(f"{name[0]}")

        print("\nWhat would you like to do with these requests?")
        for key, value in FRIEND_REQUEST.items():
            print(f"{key}. {value}")
        friend_request_choice = (
            input(f"Choose one of {list(FRIEND_REQUEST.keys())}: ").strip().lower()
        )

        # If option a, accept the friend request
        if friend_request_choice == "a":
            accept_friend_request(username)
            choose_features(username)
        # Else if option r, reject the friend request
        if friend_request_choice == "r":
            reject_friend_request(username)
            choose_features(username)
        # Else if option b, prompt return to the main menu or quit
        elif friend_request_choice == "b":
            if go_back():
                choose_features(username)

        # Else inform user of invalid input and try again
        else:
            print("Character not identified. Please try again")
            return check_friend_request(username)


# funciton designed to accept friend request
def accept_friend_request(username):
    # prompt user to enter friend request name to add
    friend_user = input("Which user would you like to add?")
    user_exists = does_friend_request_match(username, friend_user)

    # If user exists, add friend to friend table
    if user_exists:
        add_to_friend_list(username, friend_user)
        delete_friend_request(username, friend_user)
        print("Friend Added!")

    # Else inform user that user doesn't exist and try again
    else:
        print("Username does not exist in friend requests. Try again!")
        accept_friend_request(username)


# Function designed to reject friend request
def reject_friend_request(username):
    # prompt user to enter friend request name to reject
    friend_user = input("Which user would you like to reject?")
    user_exists = does_friend_request_match(username, friend_user)

    # If user exists, reject friend request
    if user_exists:
        delete_friend_request(username, friend_user)
        print("Friend Rejected!\n")

    # Else inform user that user doesn't exist and try again
    else:
        print("Username does not exist in friend requests. Try again!\n")
        reject_friend_request(username)


# Function designed to show network list to user
def show_network(username):
    # Print friend list text
    draw_line(message="Friend List")
    # Check the friend list of the user
    friend_list = list_of_friends(username)

    # If friend list is empty, inform user that they have no friends
    # Send user back to feature select
    if friend_list is False:
        print("You have no friends!")
        choose_features(username)

    # Else print friend list
    else:
        print("Here's a list of your friends:")
        for i, name in enumerate(friend_list):
            print(f"{name[1]}")

        # Prompt user if they want to remove someone
        choice = (
            input("Would you like to disconnect from one of these friends? (y/n):")
            .strip()
            .lower()
        )

        # if yes, prompt user to enter username to remove and go back to feature select
        if choice == "y":
            delete_friend(username)
            choose_features(username)

        # else if no, prompt user to return to feature select
        elif choice == "n":
            if go_back():
                choose_features(username)

        # else inform user of invalid input and try again
        else:
            print("Character not identified. Please try again")
            return show_network(username)


# Function designed to delete a person from friends list
def delete_friend(username):
    # Prompt user to enter username to remove
    friend_user = input("Which user would you like to delete?")
    user_exists = does_friend_match(username, friend_user)

    # If user exists, delete friend from friend table
    if user_exists:
        delete_friend_from_list(username, friend_user)
        print("Friend Deleted!\n")

    # Else inform user that user doesn't exist and prompt user to try again
    else:
        print("Username does not exist in friend requests. Try again!\n")
        delete_friend(username)


# Function designed to print the about page information
def about_important():
    """Browse About page"""
    draw_line(message="About")

    print(
        "In College: Welcome to In College, the world's largest college student network with many users in many countries and territories worldwide"
    )

    # Prompt user to return to feature select
    if go_back():
        choose_incollege_important_links()


# Functioned designed to select general links
def general():
    """Display general links and get user's choice"""
    draw_line(message="General")
    print("What link would you like to go to?")
    global signed_in

    # If user is not logged in, use the not logged in general links and have user select an option
    if signed_in == False:
        for key, value in NOT_SIGNED_IN_GENERAL_LINKS_GROUP.items():
            print(f"{key}. {value}")
        general_link_choice = (
            input(f"Choose one of {list(NOT_SIGNED_IN_GENERAL_LINKS_GROUP.keys())}: ")
            .strip()
            .lower()
        )

        # If user chooses a proper general link, go to that link choice
        if general_link_choice in NOT_SIGNED_IN_GENERAL_LINKS_GROUP:
            print(
                f"You selected {NOT_SIGNED_IN_GENERAL_LINKS_GROUP[general_link_choice]}"
            )
            return non_signed_in_general_direct(general_link_choice)

        # Else inform user of invalid input and repeat this functio
        else:
            print("Link not identfied. Please try again")
            return general()

    # Else if you are signed in, display the signed in general choices
    else:
        for key, value in SIGNED_IN_GENERAL_LINKS_GROUP.items():
            print(f"{key}. {value}")
        general_link_choice = (
            input(f"Choose one of {list(SIGNED_IN_GENERAL_LINKS_GROUP.keys())}: ")
            .strip()
            .lower()
        )

        # if user chooses a proper general link, go to that link choice
        if general_link_choice in SIGNED_IN_GENERAL_LINKS_GROUP:
            print(f"You selected {SIGNED_IN_GENERAL_LINKS_GROUP[general_link_choice]}")
            return signed_in_general_direct(general_link_choice)

        # Else inform user of invalid input and repeat this function
        else:
            print("Link not identfied. Please try again")
            return general()


# Function designed to direct user to the correct general link they've choosen
# Designed for when user is not signed into an account
def non_signed_in_general_direct(general_link_choice):
    """Direct user to the general link they chose if not signed in"""
    if general_link_choice == "a":
        main_helper()
    elif general_link_choice == "b":
        help_center()
    elif general_link_choice == "c":
        about()
    elif general_link_choice == "d":
        press()
    elif general_link_choice == "e":
        blog()
    elif general_link_choice == "f":
        careers()
    elif general_link_choice == "g":
        developers()
    elif general_link_choice == "h":
        if go_back():
            choose_useful_links()


# Function designed to direct user to the correct general link they've choosen
# Designed for when user is signed into an account
def signed_in_general_direct(general_link_choice):
    """Direct user to the general link they chose if signed in"""
    if general_link_choice == "a":
        help_center()
    elif general_link_choice == "b":
        about()
    elif general_link_choice == "c":
        press()
    elif general_link_choice == "d":
        blog()
    elif general_link_choice == "e":
        careers()
    elif general_link_choice == "f":
        developers()
    elif general_link_choice == "g":
        if go_back():
            choose_useful_links()


# Function designed to display help center page
def help_center():
    """Browse Help Center page"""
    draw_line(message="Help Center")

    print("We're here to help")

    # Ask user if they want to go back to general links or log out
    if go_back():
        general()


# Function designed to display about page
def about():
    """Browse About page"""
    draw_line(message="Press")

    print(
        "In College: Welcome to In College, the world's largest college student network with many users in many countries and territories worldwide"
    )

    # Ask user if they want to go back to general links or log out
    if go_back():
        general()


# Funtion designed to display press page
def press():
    """Browse Press page"""
    draw_line(message="Press")

    print("In College Pressroom: Stay on top of the latest news, updates, and reports")

    # Ask user if they want to go back to general links or log out
    if go_back():
        general()


# Function designed to display blog page
def blog():
    """Browse Blog page"""
    draw_line(message="Blog")

    # Display page is under construction
    print("Under construction")

    # Ask user if they want to go back to general links or log out
    if go_back():
        general()


# Function designed to display careers page
def careers():
    """Browse Careers page"""
    draw_line(message="Careers")

    # Display page is under construction
    print("Under construction")

    # Ask user if they want to go back to general links or log out
    if go_back():
        general()


# Function designed to display developers page
def developers():
    """Browse Developers page"""
    draw_line(message="Developers")

    # Display page is under construction
    print("Under construction")

    # Ask user if they want to go back to general links or log out
    if go_back():
        general()


# Function designed to display developers page
def browse_incollege():
    """Browse InCollege page"""
    draw_line(message="Browse InCollege")

    # Display page is under construction
    print("Under construction")

    # Ask user if they want to go back to useful links or log out
    if go_back():
        choose_useful_links()


# Function designed to display business solutions page
def business_solutions():
    """Business Solutions page"""
    draw_line(message="Business Solutions")

    # Display page is under construction
    print("Under construction")

    # Ask user if they want to go back to useful links or log out
    if go_back():
        choose_useful_links()


# Function designed to display directories page
def directories():
    """Directories page"""
    draw_line(message="Directories")

    # Display page is under construction
    print("Under construction")

    # Ask user if they want to go back to useful links or log out
    if go_back():
        choose_useful_links()


# Function designed to display profile navigation and choose profile to view
def display_profile_navigation(username):
    """Profile page"""
    draw_line(message="PROFILE_OPTIONS")

    # List profile options and prompt user to select a feature
    print("What would you like to do with the profiles?")
    for key, value in PROFILE_OPTIONS.items():
        print(f"{key}. {value}")
    feature_choice = (
        input(f"Choose one of {list(PROFILE_OPTIONS.keys())}:").strip().lower()
    )

    # If user selects option to create their profile, go to create user profile
    if feature_choice == "a":
        create_user_profile(username)

    # If user selects option to view their profile, go to display user profile
    if feature_choice == "b":
        display_user_profile(username)

    # If user selects option to view a friend's profile, go to display friend profile
    elif feature_choice == "c":
        display_friend_profile(username)

    # If user wants to go back, ask if they want to go back to feature select or log out
    elif feature_choice == "d":
        if go_back():
            choose_features(username)


# Function designed to create user's profile
def create_user_profile(username):
    """Get user's information to create or update a profile"""
    draw_line(message="Create/Update Profile")

    # If user does not have a profile, create one
    if not get_profile(username):
        print(
            """You have no profile. So let's create one!\nIf you don't want to fill up certain fields, just press enter"""
        )

        # Take in user's information
        # They can press enter to skip a field
        university = input("Please enter your university: ").title()
        major = input("Please enter your major: ").title()
        years_attended = input(f"How many years did you attend {university}: ")
        degree = input("Please enter your degree: ")
        title = input("Please enter your title: ")
        about_me = input("Please enter a short description about yourself: ")

        # If system successfully created a profile, inform user
        if create_profile(username, university, major, title, about_me):
            print("Profile created!")

        # Else inform user that there was an error and prompt user to return to profile navigation
        else:
            print("Error creating profile")
            if go_back():
                display_profile_navigation(username)
            else:
                create_user_profile(username)

        # If education is created succesfully, inform the user
        if create_education(username, university, degree, years_attended):
            print("Education created!")

        # Else inform the user that there was an error and prompt user to return to profile navigation
        else:
            print("Error creating education")
            if go_back():
                display_profile_navigation(username)
            else:
                create_user_profile(username)

        # inform user that they'll be adding experience
        print("Let's add some experience!")
        count = 0

        # while less than 3 experiences shown
        while count < 3:
            # Take in information for experience
            experienceId = count
            title = input("Please enter your experience title: ")
            employer = input("Please enter your employer: ")
            started_date = input("Please enter your start date: ")
            end_date = input("Please enter your end date: ")
            location = input("Please enter your location: ")
            description = input("Please enter your description: ")

            # If system successfully created experience, inform user
            if create_experience(
                username,
                experienceId,
                title,
                employer,
                started_date,
                end_date,
                location,
                description,
            ):
                print("Experience created!")
                count += 1
                stop = ""

                # While response is no yes or no (starts blank)
                while stop not in ["Y", "N"]:
                    # Ask user if they want to add another experience
                    stop = (
                        input("Do you want to add another experience? (Y/N): ")
                        .strip()
                        .upper()
                    )

                    # If no, exit experience adding loop
                    if stop == "N":
                        count = 3
                        break

                    # If yes, see if they've reached the limit for adding another experience
                    elif stop == "Y":
                        # If limit is reached, exit loop
                        if count == 3:
                            print("You have reached the maximum number of experiences!")
                        break

                    # If response is not yes or no, prompt user to try again
                    else:
                        print("Invalid input, please try again")

            # Else inform user that there was an error and prompt user to return to profile navigation
            else:
                print("Error creating experience")
                if go_back():
                    display_profile_navigation(username)
                else:
                    create_user_profile(username)

    # If user already has profile, the ddisplay profile navigation
    else:
        print("Here is your current profile:")
        user_profile = get_profile(username)
        print_profile_only(user_profile)
        print("You can update your profile here:")
        university = input("Please enter your university: ").title()
        major = input("Please enter your major: ").title()
        degree = input("Please enter your degree: ")
        years_attended = input(f"How many years did you attend {university}: ")
        title = input("Please enter your title: ")
        about_me = input("Please enter a short description about yourself: ")

        # If profile is updated succesfully, inform user
        if update_profile(username, university, major, title, about_me):
            print("Profile updated!")

        # Else if there was an error, inform user that there was an error and prompt user to return to profile navigation
        else:
            print("Error updating profile")
            if go_back():
                display_profile_navigation(username)
            else:
                create_user_profile(username)

        # If update education is successful, inform user
        if update_education(username, university, degree, years_attended):
            print("Education updated!")

        # Else if there was an error, inform user that there was an error and prompt user to return to profile navigation
        else:
            print("Error updating education")
            if go_back():
                display_profile_navigation(username)
            else:
                create_user_profile(username)

        # Inform user that experience will be updated experience
        print("Let's update some experience!")
        count = 0

        # While count is less than 3
        while count < 3:
            # Prompt user to enter experience
            experienceId = count
            title = input("Please enter your experience title: ")
            employer = input("Please enter your employer: ")
            started_date = input("Please enter your start date: ")
            end_date = input("Please enter your end date: ")
            location = input("Please enter your location: ")
            description = input("Please enter your description: ")

            # If experience is created succesfully, inform user
            if update_experience(
                username,
                experienceId,
                title,
                employer,
                started_date,
                end_date,
                location,
                description,
            ):
                print("Experience updated!")
                count += 1
                stop = ""

                # While stop is not yes or no
                # Stop is not set at the begining
                while stop not in ["Y", "N"]:
                    # prompt user if they wanna add another experience
                    stop = (
                        input("Do you want to update another experience? (Y/N): ")
                        .strip()
                        .upper()
                    )

                    # If no, break out of loop
                    if stop == "N":
                        count = 3
                        break

                    # Else if yes, check if number of experience limit is reached
                    elif stop == "Y":
                        if count == 3:
                            print("You have reached the maximum number of experiences!")
                        break

                    # Else inform user that input was invalid and prompt them to try again
                    else:
                        print("Invalid input, please try again")

            # Else if there was an error, inform user that there was an error and prompt user to return to profile
            else:
                print("Error updating experience")
                if go_back():
                    display_profile_navigation(username)
                # else:
                #     create_user_profile(username)

    # Go to display choice function to direct user to profile display (for themselves)
    display_choice(username)
    # else:
    #     create_user_profile(username)


# Function designed to direct user to profile display (for themselves)
def display_choice(username):
    # While true, display choice
    while True:
        # Prompt user for choice
        user_input = (
            input("Do you want to see what your profile looks like (Y/N)? ")
            .strip()
            .upper()
        )

        # If user wants to see their own profile, display the user's profile
        if user_input == "Y":
            display_user_profile(username)
            break

        # Else if user doesn't want to see their own profile, go back to the profile navigation
        elif user_input == "N":
            if go_back():
                display_profile_navigation(username)
                break

        # Else, display error message and prompt user to try again
        else:
            print("Invalid choice! Try Again!")


# Function designed to display user's profile
def display_user_profile(username):
    first = get_first_name(username)
    last = get_last_name(username)
    draw_line(message="PROFILE")
    print(f"Here's {first} {last}'s profile:")
    if user_profile := get_profile(username):
        print_profile_only(user_profile)
    else:
        print("You have no profile. Please create one!")
    if go_back():
        display_profile_navigation(username)
    # else:
    #     display_user_profile(username)


# Function displays user's friend profile
def display_user_friend_profile(username):
    draw_line(message=f"{username.upper()}'S PROFILE")
    print("Here's your friend's profile:")

    # If friend has profile, print profile
    if user_profile := get_profile(username):
        print_profile_only(user_profile)

    # else print friend has no profile
    else:
        print(f"{username} has no profile. Encourage them to make one!")


# Function designed to print out the profile of a user
# Function also prints out all of that user's experience
def print_profile_only(user_profile):
    print("Username: ", user_profile["user"])
    print("Title: ", user_profile["title"])
    print("About Me: ", user_profile["about"])
    print("\nEducation:")
    print("University: ", user_profile["university"])
    print("Major: ", user_profile["major"])
    print("Degree: ", user_profile["degree"])
    print("Years Attended: ", user_profile["years_attended"])
    print("\nExperience:")
    for idx, experience in enumerate(user_profile["experience"]):
        print(f"Experience {idx + 1}:")
        print("Title: ", experience["title"])
        print("Employer: ", experience["employer"])
        print("Location: ", experience["location"])
        print("Start Date: ", experience["date_started"])
        print("End Date: ", experience["date_ended"])
        print("Description: ", experience["description"])
        print("\n")


# Function to display friend profile
def display_friend_profile(username):
    # Display friend list and search user's list of friends
    draw_line(message="Friend List")
    friend_list = list_of_friends(username)

    # If friend list is empty, display message showing they have no friends
    if friend_list is False:
        print("You have no friends!")
        display_profile_navigation(username)

    # Else If friend list is not empty, display friend list
    else:
        print("Here's a list of your friends:")
        for i, name in enumerate(friend_list):
            if len(name) > 1 and not get_profile(name[1]):
                print(f"{name[1]}")
            else:
                print(f"{name[0]} - PROFILE")

        # Ask user to select a friend to view their profile
        choice = input(
            "Would you like to display the profile from one of these friends? (y/n):"
        )

        # If user chooses to view friend profile, prompt user which friend to view
        if choice == "y":
            friend_name = input("Which friend's profile would you like to see?:")
            user_exists = does_friend_match(username, friend_name)

            # If user exist, display friend profile and go back to feature select
            if user_exists:
                display_user_friend_profile(friend_name)
                choose_features(username)

            # Else if user does not exist, inform user that friend doesn't exist
            # Then repeat this function
            else:
                print("Username does not exist in friend requests. Try again!")
                display_friend_profile(username)

        # Else if user chooses not to view friend profile, Prompt user to go back to feature select
        elif choice == "n":
            if go_back():
                choose_features(username)

        # Else if user enters invalid input, prompt user to try again
        # Repeat this function if this occurs
        else:
            print("Character not identified. Please try again")
            return display_friend_profile(username)


# Function designed to prompt user to log out of their account
def logout(username):
    """Ask user if they want to log out"""
    decision = input("Do you want to log out (Y / N)? ").strip().upper()

    # if user selects yes, log out
    if decision == "Y":
        # using the global variable num_days_since_applied
        # each login counts as a day that has passed since they last applied
        update_days(username)
        global num_days_since_applied
        num_days_since_applied = get_days(username)
        return 0

    # Else if user selects no, return to feature select
    elif decision == "N":
        choose_features(username)

    # Else if user selects anything else, display error message and prompt user to try again
    else:
        print("Invalid input, please try again")
        logout(username)


# Function designed to determine if user would like to sign up or log in
def main_entry():
    """Welcome page and get the user into the system through login or signup"""
    draw_line(message="In College")
    print("Welcome to InCollege! Would you like to sign up or log in?")

    # Ask user if they want to sign up or log in
    decision_in = input("Enter S to sign up or L to log in: ").strip().upper()

    # Execute options function and make choice based on user input
    decision = options(decision_in)

    # While decision is invalid, ask user to try again
    while decision is None:
        decision_in = input("Enter S to sign up or L to log in: ").strip().upper()
        decision = options(decision_in)

    # Return the decision the user has made
    return decision


# Function that ask if user wants to log out or go to feature select menu
def go_back():
    """Ask user if they want to go back to the previous page"""
    decision = input("Do you want to go back (Y / N)? ").strip().upper()

    # if user wants to go back, return True
    if decision == "Y":
        return True

    # else if user wants to log out, return False
    elif decision == "N":
        return False

    # else, inform user of invalid input and repeat this function
    else:
        print("Invalid input, please try again")
        return go_back()


# Function that determines login attempt limit has been reached
def change_limit_login():
    """Determine if the user has exceeded the number of login attempts"""
    global limit_login
    global login_attempts

    # If the number of login attempts is greater than the limit, return True
    if login_attempts > LOGIN_NUM_LIMIT:
        limit_login = True

    # Else, increment log in attempy by 1
    else:
        login_attempts += 1

    # return limit login regardless of condition/limit-cap
    return limit_login


# Function that is used when user fails log in and counts the number of login attempts
def try_again():
    """Ask user if they want to try to login again after failed attempt. Currently the user has unlimited attempts to try again"""

    # Prompt user to try again
    decision = input("Do you want to try again (Y / N)? ").strip().upper()
    limit = change_limit_login()

    # If user says yes, try again
    if decision == "Y" and limit == False:
        return True

    # If user says yes, but runs out of attempts, end the program
    elif decision == "Y" and limit == True:
        print("Ran out of attempts! Try again later")
        return False

    # If user says no, end the program
    elif decision == "N":
        return False

    # If user inputs invalid input, try again
    else:
        print("Invalid input, please try again")
        try_again()


# HELPERS for printing the headers of each section
# Makes it easier to know which section you're in while navigating Incollege
def draw_line(message):
    """Draw a line with the message in the middle. The line dynamically adjusts to the terminal width"""
    terminal_width, _ = shutil.get_terminal_size()
    print()
    print("-" * terminal_width)
    print(message.upper())
    print("-" * terminal_width)


# Function for when the web page opens,and greets user
def web_opening():
    """Opening page for the web application"""

    # Print the inspirational message
    print(
        '"I found making a career difficult, but thanks to inCollege: I was able to find the help that I needed!" - Hoff Reidman\n'
    )

    # Prompt user if they want to watch a video
    video_prompt = input("Would you like to watch their story (Y/N)? ")

    # if they want to watch the video, print the video
    if video_prompt == "y" or video_prompt == "Y":
        print("Video is now playing...\n")
        time.sleep(5)
        print("Video is complete.\n")


# Function that prompts user to use navigation links or head to login page
def links_or_login():
    """Prompts user to either use the navigation links or to login page"""
    links_prompt = input(
        "Do you want to navigate and explore InCollege while logged out (Y/N)? "
    )

    if links_prompt == "y" or links_prompt == "Y":
        choose_navigation_link()


# Main Function/Driver helper, which decides the first steps of the program
def main_helper():
    decision = main_entry()

    username = None
    while decision is None:
        decision = main_entry()
    if decision == "S":
        username = signup()
    elif decision == "L":
        prompt_person_search()
        username = login()

    if username is None:
        sys.exit()

    choose_features(username)

    print("Thank you for using InCollege!")

    draw_line(message="End of Program")
    exit()


# Main Function/Driver
def main():
    """Main function that controls the flow of the program"""

    web_opening()
    links_or_login()
    main_helper()


if __name__ == "__main__":
    main()
