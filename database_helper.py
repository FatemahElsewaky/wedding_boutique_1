import sqlite3

conn = sqlite3.connect("account.db")
c = conn.cursor()

# Create accounts table if it doesn't already exist
c.execute(
    """CREATE TABLE IF NOT EXISTS accounts (

          user text ,
          pass text,
          first text,
          last text,
          university text,
          major text,
          tier int,
          days int

          )"""
)

c.execute(
    """CREATE TABLE IF NOT EXISTS jobs (

          title text,
          description text,
          employer text,
          location text,
          salary text,
          first text,
          last text

          )"""
)


c.execute(
    """CREATE TABLE IF NOT EXISTS job_applications (

          title text,
          user text,
          graduation text,
          start text,
          description text

          )"""
)


c.execute(
    """CREATE TABLE IF NOT EXISTS jobs_saved (

          title text,
          user text

          )"""
)

c.execute(
    """CREATE TABLE IF NOT EXISTS friends (

          user text,
          friend_user text 

          )"""
)

c.execute(
    """CREATE TABLE IF NOT EXISTS friends_list (

          user text,
          friend_user text 

          )"""
)

c.execute(
    """CREATE TABLE IF NOT EXISTS profile (

          user text ,
          university text,
          major text,
          title text,
          about text

          )"""
)

c.execute(
    """CREATE TABLE IF NOT EXISTS experience (

          user text,
          experienceId text,
          title text,
          employer text,
          date_started text,
          date_ended text,
          location text,
          description text

          )"""
)

c.execute(
    """CREATE TABLE IF NOT EXISTS education (

          user text ,
          school_name text,
          degree text,
          years_attended text

          )"""
)


c.execute(
    """CREATE TABLE IF NOT EXISTS message (

          message text ,
          sender text,
          receiver text

          )"""
)

c.execute(
    """CREATE TABLE IF NOT EXISTS message_notification (

          message text ,
          sender text,
          receiver text

          )"""
)


c.execute(
    """CREATE TABLE IF NOT EXISTS notification (

          message text ,
          sender text,
          receiver text

          )"""
)


def save_job_for_user(username, saved_job_title):
    """Returns True if the job was successfully saved, False otherwise"""
    try:
        with conn:
            # Insert username, password, first name, and last name into database
            c.execute(
                "INSERT INTO jobs_saved VALUES (:title, :user)",
                {"title": saved_job_title, "user": username},
            )
        return True
    except sqlite3.Error as error:
        print("Failed to add job into sqlite table:", error)
        return False


def get_saved_jobs(username):
    """Returns a list of all jobs saved by the user"""
    try:
        with conn:
            c.execute("SELECT * FROM jobs_saved WHERE user = :user", {"user": username})
            jobs = c.fetchall()
            if jobs:
                return [job[0] for job in jobs]
            else:
                return []
    except sqlite3.Error as error:
        print("Failed to get jobs from sqlite table:", error)
        return []


def clean_saved_jobs_when_job_deleted(title):
    """ "Return true if all the deleted jobs were successfully deleted from the saved jobs table"""
    try:
        with conn:
            # Delete the job with the provided title
            c.execute("DELETE FROM jobs_saved WHERE title = ?", (title,))
        return True
    except sqlite3.Error as error:
        print("Failed to delete job from the sqlite table:", error)
        return False


def delete_saved_job(username, saved_job_title):
    """Returns True if the job was successfully deleted, False otherwise"""
    try:
        with conn:
            # Delete the job with the provided title
            c.execute(
                "DELETE FROM jobs_saved WHERE title = ? AND user = ?",
                (
                    saved_job_title,
                    username,
                ),
            )
        return True
    except sqlite3.Error as error:
        print("Failed to delete job from the sqlite table:", error)
        return False


def create_profile(username, university, major, title, about):
    """Returns True if the profile was successfully created, False otherwise"""
    try:
        with conn:
            # Insert username, password, first name, and last name into database
            c.execute(
                "INSERT INTO profile VALUES (:user, :university, :major, :title, :about)",
                {
                    "user": username,
                    "university": university,
                    "major": major,
                    "title": title,
                    "about": about,
                },
            )
        return True
    except sqlite3.Error as error:
        print("Failed to add profile into sqlite table:", error)
        return False


def get_profile(username):
    """Get the combined profile from profile, education, and experience tables"""
    profile, education, experience = None, None, None
    final_profile = {}
    try:
        with conn:
            c.execute("SELECT * FROM profile WHERE user = :user", {"user": username})
            profile = c.fetchone()
            c.execute("SELECT * FROM education WHERE user = :user", {"user": username})
            education = c.fetchone()
            c.execute("SELECT * FROM experience WHERE user = :user", {"user": username})
            jobs = c.fetchall()

            if not profile and not education and not experience:
                return None

            if profile is not None:
                final_profile["user"] = profile[0]
                final_profile["university"] = profile[1]
                final_profile["major"] = profile[2]
                final_profile["title"] = profile[3]
                final_profile["about"] = profile[4]
            if education is not None:
                final_profile["school_name"] = education[1]
                final_profile["degree"] = education[2]
                final_profile["years_attended"] = education[3]
            if jobs is not None:
                final_profile["experience"] = []
                for job in jobs:
                    final_profile["experience"].append(
                        {
                            "experienceId": job[1],
                            "title": job[2],
                            "employer": job[3],
                            "date_started": job[4],
                            "date_ended": job[5],
                            "location": job[6],
                            "description": job[7],
                        }
                    )
            return final_profile
    except sqlite3.Error as error:
        print("Failed to get profile from sqlite table:", error)
        return None


def update_profile(username, university, major, title, about):
    """Returns True if the profile was successfully updated, False otherwise"""
    try:
        with conn:
            # Update the profile with the provided username
            c.execute(
                "UPDATE profile SET university = ?, major = ?, title = ?, about = ? WHERE user = ?",
                (university, major, title, about, username),
            )
        return True
    except sqlite3.Error as error:
        print("Failed to update profile from the sqlite table:", error)
        return False


def delete_profile(username):
    """Returns True if the user was successfully deleted, False otherwise"""
    """Used to delete profiles that are currently made for testing purposes in our tests"""
    try:
        with conn:
            # Delete the user with the provided username
            c.execute("DELETE FROM profile WHERE user = ?", (username,))
        return True
    except sqlite3.Error as error:
        print("Failed to delete profile from the sqlite table:", error)
        return False


def create_experience(
    user, experienceId, title, employer, date_started, date_ended, location, description
):
    """Returns True if the experience was successfully created, False otherwise"""
    try:
        with conn:
            # Insert username, password, first name, and last name into database
            c.execute(
                "INSERT INTO experience VALUES (:user, :experienceId, :title, :employer, :date_started, :date_ended, :location, :description)",
                {
                    "user": user,
                    "experienceId": experienceId,
                    "title": title,
                    "employer": employer,
                    "date_started": date_started,
                    "date_ended": date_ended,
                    "location": location,
                    "description": description,
                },
            )
        return True
    except sqlite3.Error as error:
        print("Failed to add experience into sqlite table:", error)
        return False


def update_experience(
    user, experienceId, title, employer, date_started, date_ended, location, description
):
    """Returns True if the experience was successfully updated, False otherwise"""
    try:
        with conn:
            # Update the experience with the provided username
            c.execute(
                "UPDATE experience SET title = ?, employer = ?, date_started = ?, date_ended = ?, location = ?, description = ? WHERE user = ? AND experienceId = ?",
                (
                    title,
                    employer,
                    date_started,
                    date_ended,
                    location,
                    description,
                    user,
                    experienceId,
                ),
            )
        return True
    except sqlite3.Error as error:
        print("Failed to update experience from the sqlite table:", error)
        return False


def delete_experience(username):
    """Returns True if the experience was successfully deleted, False otherwise"""
    """Used to delete the user profile's experiences that are currently made for testing purposes in our tests"""
    try:
        with conn:
            # Delete the user with the provided username
            c.execute("DELETE FROM experience WHERE user = ?", (username,))
        return True
    except sqlite3.Error as error:
        print("Failed to delete experience from the sqlite table:", error)
        return False


def create_education(user, school_name, degree, years_attended):
    """Returns True if the education was successfully created, False otherwise"""
    try:
        with conn:
            # Insert username, password, first name, and last name into database
            c.execute(
                "INSERT INTO education VALUES (:user, :school_name, :degree, :years_attended)",
                {
                    "user": user,
                    "school_name": school_name,
                    "degree": degree,
                    "years_attended": years_attended,
                },
            )
        return True
    except sqlite3.Error as error:
        print("Failed to add education into sqlite table:", error)
        return False


def update_education(user, school_name, degree, years_attended):
    """ "Returns True if the education was successfully updated, False otherwise"""
    try:
        with conn:
            # Update the education with the provided username
            c.execute(
                "UPDATE education SET school_name = ?, degree = ?, years_attended = ? WHERE user = ?",
                (school_name, degree, years_attended, user),
            )
        return True
    except sqlite3.Error as error:
        print("Failed to update education from the sqlite table:", error)
        return False


def delete_education(username):
    """Returns True if the education was successfully deleted, False otherwise"""
    """Used to delete the user profile's education that are currently made for testing purposes in our tests"""
    try:
        with conn:
            # Delete the user with the provided username
            c.execute("DELETE FROM education WHERE user = ?", (username,))
        return True
    except sqlite3.Error as error:
        print("Failed to delete education from the sqlite table:", error)
        return False


def create_user(username, password, first, last, university, major, tier, days):
    """Returns True if the user was successfully created, False otherwise"""
    try:
        with conn:
            # Insert username, password, first name, and last name into database
            c.execute(
                "INSERT INTO accounts VALUES (:user, :pass, :first, :last, :university, :major, :tier, :days)",
                {
                    "user": username,
                    "pass": password,
                    "first": first,
                    "last": last,
                    "university": university,
                    "major": major,
                    "tier": tier,
                    "days": days,
                },
            )
        return True
    except sqlite3.Error as error:
        print("Failed to add user into sqlite table:", error)
        return False


def get_user(username):
    """Returns the user information for a given username."""
    try:
        with conn:
            c.execute("SELECT * FROM accounts WHERE user = :user", {"user": username})
            user = c.fetchone()
            if user is not None:
                # User found, return it as a dictionary
                return {
                    "user": user[0],
                    "pass": user[1],
                    "first": user[2],
                    "last": user[3],
                    "university": user[4],
                    "major": user[5],
                }
            else:
                # User not found
                return None
    except sqlite3.Error as error:
        print("Failed to get user from sqlite table:", error)
        return None


## EPIC #8 PT.1 Start ########################
def get_days(username):
    """Returns the user information for a given username."""
    try:
        with conn:
            c.execute(
                "SELECT days FROM accounts WHERE user = :user", {"user": username}
            )
            user = c.fetchone()
            if user is not None:
                # User found, return it as a dictionary
                return user[0]
            else:
                return 0
    except sqlite3.Error as error:
        print("Failed to get days from sqlite table:", error)
        return 0


def reset_days(username):
    """Returns the user information for a given username."""
    try:
        with conn:
            c.execute(
                "UPDATE accounts SET days = 0 WHERE user = :user", {"user": username}
            )

        return True

    except sqlite3.Error as error:
        print("Failed to reset days from sqlite table:", error)
        return False


def update_days(username):
    """Returns the user information for a given username."""
    try:
        with conn:
            c.execute(
                "UPDATE accounts SET days = days + 1 WHERE user = :user",
                {"user": username},
            )

        return True

    except sqlite3.Error as error:
        print("Failed to reset days from sqlite table:", error)
        return False


## EPIC #8 PT.2 End ########################


def delete_user(username):
    """Returns True if the user was successfully deleted, False otherwise"""
    try:
        with conn:
            # Delete the user with the provided username
            c.execute("DELETE FROM accounts WHERE user = ?", (username,))
        return True
    except sqlite3.Error as error:
        print("Failed to delete user from the sqlite table:", error)
        return False


def does_username_exist(username):
    """Returns True if the username already exists in the database, False otherwise"""
    c.execute("SELECT * FROM accounts WHERE user=:user", {"user": username})
    user_entry = c.fetchone()
    return user_entry is not None


def create_job(title, description, employer, location, salary, first, last):
    """Returns True if the user was successfully created, False otherwise"""
    try:
        with conn:
            # Insert username, password, first name, and last name into database
            c.execute(
                "INSERT INTO jobs VALUES (:title, :description, :employer, :location,:salary, :first, :last)",
                {
                    "title": title,
                    "description": description,
                    "employer": employer,
                    "location": location,
                    "salary": salary,
                    "first": first,
                    "last": last,
                },
            )
        return True
    except sqlite3.Error as error:
        print("Failed to add job into sqlite table:", error)
        return False


def get_all_job_titles():
    """Returns a list of all jobs"""
    try:
        with conn:
            c.execute("SELECT * FROM jobs")
            return [job[0] for job in c.fetchall()]
    except sqlite3.Error as error:
        print("Failed to get jobs from sqlite table:", error)
        return []


def get_job_list_posted_by_user(first, last):
    """Returns a list of jobs posted by the user"""
    try:
        with conn:
            # Insert username, password, first name, and last name into database
            # return a list of job titles
            c.execute(
                "SELECT title FROM jobs WHERE first = ? AND last = ?", (first, last)
            )
            return [job[0] for job in c.fetchall()]
    except sqlite3.Error as error:
        print("Failed to get jobs from sqlite table:", error)
        return []


def delete_job(title):
    """Returns True if the job was successfully deleted, False otherwise"""
    try:
        with conn:
            # Delete the job with the provided title
            c.execute("DELETE FROM jobs WHERE title = ?", (title,))
        return True
    except sqlite3.Error as error:
        print("Failed to delete job from the sqlite table:", error)
        return False


def add_friend(username, friend_username):
    """Returns True if the friend was successfully added into the database, False otherwise"""
    try:
        with conn:
            c.execute(
                "INSERT INTO friends VALUES (:user, :friend_user)",
                {"user": username, "friend_user": friend_username},
            )
        return True
    except sqlite3.Error as error:
        print("Failed to add friend to the sqlite table:", error)
        return False


def search_name(firstname, lastname):
    """Returns True if the username already exists in the database, False otherwise"""
    c.execute(
        "SELECT * FROM accounts WHERE first=:first AND last=:last",
        {"first": firstname, "last": lastname},
    )
    user_entry = c.fetchone()
    return user_entry is not None


def get_username_from_last_name(lastname):
    """Returns a list of usernames if found with the friend's last name in the database, an empty list otherwise"""
    c.execute("SELECT user FROM accounts WHERE last=:last", {"last": lastname})
    users = c.fetchall()
    if users:
        return [user[0] for user in users]
    else:
        return []


def get_username_from_university(university):
    """Returns a list of username if found with the friend's university in the database, an empty list otherwise"""
    c.execute(
        "SELECT user FROM accounts WHERE university=:university",
        {"university": university},
    )
    users = c.fetchall()
    if users:
        return [user[0] for user in users]
    else:
        return []


def get_username_from_major(major):
    """Returns a list of username if found with the friend's major in the database, an empty list otherwise"""
    c.execute("SELECT user FROM accounts WHERE major=:major", {"major": major})
    users = c.fetchall()
    if users:
        return [user[0] for user in users]
    else:
        return []


def get_first_name(username):
    """Returns True if the username already exists in the database, False otherwise"""
    c.execute("SELECT * FROM accounts WHERE user=:user", {"user": username})
    user_entry = c.fetchone()
    return user_entry[2]


def get_last_name(username):
    """Returns True if the username already exists in the database, False otherwise"""
    c.execute("SELECT * FROM accounts WHERE user=:user", {"user": username})
    user_entry = c.fetchone()
    return user_entry[3]


def check_login(username, password):
    """Returns True if the username and password match a user in the database, False otherwise"""
    c.execute(
        "SELECT * FROM accounts WHERE user=:user AND pass=:pass",
        {"user": username, "pass": password},
    )
    accEntry = c.fetchone()
    return accEntry is not None


def get_num_of_users():
    """Returns the number of users in the database"""
    c.execute("SELECT COUNT(*) FROM accounts")
    result = c.fetchone()
    if result:
        return result[0]  # Extract the count from the result
    else:
        return 0  # Return 0 if there are no users in the database


def get_num_of_jobs():
    """Returns the number of users in the database"""
    c.execute("SELECT COUNT(*) FROM jobs")
    result = c.fetchone()
    if result:
        return result[0]  # Extract the count from the result
    else:
        return 0  # Return 0 if there are no users in the database


def does_friend_request_match(username, friend_username):
    """Returns friend username if the username already exists in the friends, False otherwise"""
    c.execute(
        "SELECT * FROM friends WHERE user=:user AND friend_user=:friend_user",
        {"user": friend_username, "friend_user": username},
    )
    user_entry = c.fetchone()
    if user_entry:
        return True
    else:
        return False


def pending_friend_request_list(username):
    """Returns friend username if the username already exists in the friends, False otherwise"""
    c.execute(
        "SELECT * FROM friends WHERE friend_user=:friend_user",
        {"friend_user": username},
    )
    user_entry = c.fetchall()

    if user_entry:
        return user_entry
    else:
        return False


def add_to_friend_list(username, friend_username):
    """Returns True if the friend was successfully added into the database, False otherwise"""
    try:
        with conn:
            c.execute(
                "INSERT INTO friends_list VALUES (:user, :friend_user)",
                {"user": username, "friend_user": friend_username},
            )
            c.execute(
                "INSERT INTO friends_list VALUES (:user, :friend_user)",
                {"user": friend_username, "friend_user": username},
            )
        return True
    except sqlite3.Error as error:
        print("Failed to add friend to the sqlite table:", error)
        return False


def delete_friend_request(username, friend_username):
    """Returns True if the friend was successfully deleted, False otherwise"""
    try:
        with conn:
            # Delete the friend with the provided username
            c.execute(
                "DELETE FROM friends WHERE user = ? AND friend_user = ?",
                (
                    friend_username,
                    username,
                ),
            )
        return True
    except sqlite3.Error as error:
        print("Failed to delete user from the sqlite table:", error)
        return False


def list_of_friends(username):
    """Returns friend username if the username already exists in the friends, False otherwise"""
    c.execute("SELECT * FROM friends_list WHERE user=:user", {"user": username})
    user_entry = c.fetchall()

    if user_entry:
        return user_entry
    else:
        return False


def does_friend_match(username, friend_username):
    """Returns friend username if the username already exists in the friends, False otherwise"""
    c.execute(
        "SELECT * FROM friends_list WHERE user=:user AND friend_user=:friend_user",
        {"user": username, "friend_user": friend_username},
    )
    user_entry = c.fetchone()
    if user_entry:
        return True
    else:
        return False


def delete_friend_from_list(username, friend_username):
    """Returns True if the friend was successfully deleted, False otherwise"""
    try:
        with conn:
            # Delete the friend with the provided username
            c.execute(
                "DELETE FROM friends_list WHERE user = ? AND friend_user = ?",
                (
                    friend_username,
                    username,
                ),
            )
            c.execute(
                "DELETE FROM friends_list WHERE user = ? AND friend_user = ?",
                (
                    username,
                    friend_username,
                ),
            )
        return True
    except sqlite3.Error as error:
        print("Failed to delete user from the sqlite table:", error)
        return False


def all_jobs_list(username):
    """Returns all jobs"""
    c.execute("SELECT * FROM jobs")
    jobs = c.fetchall()

    if jobs:
        return [job[0] for job in jobs]
    else:
        return []


# Function gets the info of the job that matches the title searched
def get_job(job_title):
    """Returns the info of the job title you searched for, and returns False if no information on job title is saved"""
    c.execute(
        "SELECT * FROM jobs WHERE title=:title",
        {
            "title": job_title,
        },
    )
    info = c.fetchone()

    if info:
        return info
    else:
        return False


def create_application(username, job_title, graduation, start, description):
    """Returns True if the application was successfully created, False otherwise"""
    try:
        with conn:
            # Insert username, password, first name, and last name into database
            c.execute(
                "INSERT INTO job_applications VALUES (:title, :user,:graduation,:start,:description)",
                {
                    "title": job_title,
                    "user": username,
                    "graduation": graduation,
                    "start": start,
                    "description": description,
                },
            )
        return True
    except sqlite3.Error as error:
        print("Failed to add job application into sqlite table:", error)
        return False


def search_application(username, job_title):
    """Returns the info of the job title you searched for, and returns False if no information on job title is saved"""
    c.execute(
        "SELECT * FROM job_applications WHERE user=:user AND title=:title",
        {
            "user": username,
            "title": job_title,
        },
    )
    info = c.fetchone()

    if info:
        return True
    else:
        return False


def delete_application(username, job_title):
    """Returns True if the application was successfully deleted, False otherwise"""
    try:
        with conn:
            c.execute(
                "DELETE FROM job_applications WHERE user = ? AND title = ?",
                (
                    username,
                    job_title,
                ),
            )
        return True
    except sqlite3.Error as error:
        print("Failed to delete job application from the sqlite table:", error)
        return False


def user_made_job(first, last, job_title):
    """checks if job belongs to user. If so, they can't apply for it"""
    c.execute(
        "SELECT * FROM jobs WHERE first=:first AND last=:last AND title=:title",
        {"first": first, "last": last, "title": job_title},
    )
    info = c.fetchone()

    if info:
        return True
    else:
        return False


def applied_jobs_list(username):
    """Returns the info of the job title you applied for, and returns False if no information on job title is saved"""
    c.execute(
        "SELECT * FROM job_applications WHERE user=:user",
        {
            "user": username,
        },
    )
    jobs = c.fetchall()

    if jobs:
        return [job[0] for job in jobs]
    else:
        return []


def create_new_message(message, sender, receiver):
    """Returns True if message was successfully created, False otherwise"""
    try:
        with conn:
            # Insert message, sender, receiver, and new into database
            c.execute(
                "INSERT INTO message_notification VALUES (:message, :sender, :receiver)",
                {
                    "message": message,
                    "sender": sender,
                    "receiver": receiver,
                },
            )
        return True
    except sqlite3.Error as error:
        print("Failed to add new message into sqlite table:", error)
        return False


def get_new_message(receiver):
    """Returns the info of the message you searched for, and returns False if the user has no messages for them inside of the message database"""
    c.execute(
        "SELECT * FROM message_notification WHERE receiver=:receiver",
        {
            "receiver": receiver,
        },
    )
    info = c.fetchall()

    if info:
        return info
    else:
        return []


def remove_new_message(username, receiver, message):
    """Returns True if the application was successfully deleted, False otherwise"""
    try:
        with conn:
            c.execute(
                "DELETE FROM message_notification WHERE sender = ? AND receiver = ? AND message = ?",
                (
                    receiver,
                    username,
                    message,
                ),
            )
        return True
    except sqlite3.Error as error:
        print("Failed to delete new message from the sqlite table:", error)
        return False


## EPIC #8 Pt.2 Start ########################


def create_notification(message, sender, receiver):
    """Returns True if message was successfully created, False otherwise"""
    try:
        with conn:
            # Insert message, sender, receiver, and new into database
            c.execute(
                "INSERT INTO notification VALUES (:message, :sender, :receiver)",
                {
                    "message": message,
                    "sender": sender,
                    "receiver": receiver,
                },
            )
        return True
    except sqlite3.Error as error:
        print("Failed to add new message into sqlite table:", error)
        return False


def get_notification(receiver):
    """Returns the info of the message you searched for, and returns False if the user has no messages for them inside of the message database"""
    c.execute(
        "SELECT * FROM notification WHERE receiver=:receiver",
        {
            "receiver": receiver,
        },
    )
    info = c.fetchall()

    if info:
        return info
    else:
        return []


def remove_notification(username, receiver, message):
    """Returns True if the application was successfully deleted, False otherwise"""
    try:
        with conn:
            c.execute(
                "DELETE FROM notification WHERE sender = ? AND receiver = ? AND message = ?",
                (
                    receiver,
                    username,
                    message,
                ),
            )
        return True
    except sqlite3.Error as error:
        print("Failed to delete new message from the sqlite table:", error)
        return False


## EPIC #8 Pt.2 END ########################


def create_message(message, sender, receiver):
    """Returns True if message was successfully created, False otherwise"""
    try:
        with conn:
            # Insert message, sender, receiver, and new into database
            c.execute(
                "INSERT INTO message VALUES (:message, :sender, :receiver)",
                {
                    "message": message,
                    "sender": sender,
                    "receiver": receiver,
                },
            )
        return True
    except sqlite3.Error as error:
        print("Failed to add message into sqlite table:", error)
        return False


def get_message(receiver):
    """Returns the info of the message you searched for, and returns False if the user has no messages for them inside of the message database"""
    c.execute(
        "SELECT * FROM message WHERE receiver=:receiver",
        {
            "receiver": receiver,
        },
    )
    info = c.fetchall()

    if info:
        return info
    else:
        return []


def remove_message(username, receiver, message):
    """Returns True if message was successfully deleted, False otherwise"""
    try:
        with conn:
            c.execute(
                "DELETE FROM message WHERE sender = ? AND receiver = ? AND message = ?",
                (
                    receiver,
                    username,
                    message,
                ),
            )
        return True
    except sqlite3.Error as error:
        print("Failed to delete message from the sqlite table:", error)
        return False


def get_transaction(receiver, sender):
    """Returns where there was messaging between you and another person and returns False if no information is saved in messages. Sender in this case refers to the person the user is replying to, and receiver is the user looking into their inbox"""
    c.execute(
        "SELECT * FROM message WHERE receiver=:receiver AND sender=:sender",
        {
            "receiver": receiver,
            "sender": sender,
        },
    )
    info = c.fetchall()

    if info:
        return True
    else:
        return False


def is_plus_tier(username):
    """Returns the tier value of the account. 1 if the user is a plus tier user, 0 if the user is a standard tier user, and False if neither"""
    c.execute(
        "SELECT tier FROM accounts WHERE user=:user",
        {
            "user": username,
        },
    )
    info = c.fetchone()

    if info:
        return info[0]
    else:
        return False


def is_friend(username, receiver):
    """Returns True if the username and receiver of the message are friends, False otherwise"""
    c.execute(
        "SELECT * FROM friends_list WHERE user=:user AND friend_user=:friend_user",
        {"user": username, "friend_user": receiver},
    )
    user_entry = c.fetchone()

    if user_entry:
        return True
    else:
        return False


def list_of_users(username):
    """Returns a list of all the users in the system currently, False otherwise"""
    c.execute("SELECT user FROM accounts")
    user_entry = c.fetchall()

    if user_entry:
        return user_entry
    else:
        return False


def get_applicants_for_job(job_title):
    """Returns list of users who applied for the given job title"""

    try:
        with conn:
            c.execute("SELECT user FROM job_applications WHERE title = ?", (job_title,))
            applicants = [row[0] for row in c.fetchall()]
            return applicants

    except sqlite3.Error as error:
        print("Failed to get applicants:", error)
        return []
