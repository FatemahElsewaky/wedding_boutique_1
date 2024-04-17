from unittest.mock import Mock, patch

from main import *

# will connect to database, use these values for testing
# username: testuser
# password: ValidPass1!
# first name: Test
# last name: User


# Test 1: Test whether main_entry() reads user's input correctly
# with test cases = ['g', 'G', 'ss', '1', '$', 's', 'l'] all should fail
# with test cases = ['S', 'L'] all should pass
def test_options_success():
    input_tests = ["S", "L"]
    for i in input_tests:
        entry = options(i)
        assert entry is not None


def test_options_fail():
    input_tests = ["g", "G", "ss", "1", "$", "s", "l"]
    for i in input_tests:
        entry = options(i)
        assert entry is None


def test_ten_acc_made_fail():
    """check if the number of users reached the limit of 5"""
    assert reached_user_limit(10) is True


def test_five_acc_made_success():
    """check that the number of users is less than 5"""
    for i in range(0, 5):
        assert reached_user_limit(i) is False


# test 3: Error message when 6th account is created
def test_error_message_for_sixth_acc_success(capsys):
    reached_user_limit(10)
    captured = capsys.readouterr()
    assert (
        "All permitted accounts have been created, please come back later"
        in captured.out
    )


def test_error_message_for_eleventh_acc_fail(capsys):
    for i in range(0, 10):
        reached_user_limit(i)
        captured = capsys.readouterr()
        assert (
            "All permitted accounts have been created, please come back later"
            not in captured.out
        )


# test 4: Secure password
# all cases should pass this test which means the passwords were invalid in main
def test_validate_password_fails():
    password_list = [
        "Games1$",  # less than 8 characters
        "Games&cats123",  # more than 12 characters
        "games&cats12",  # no capitalized character
        "Games&cats$#",  # no digits
        "Games3cats47",  # no special characters
    ]
    for i in password_list:
        password = validate_password(i)
        assert password is None


# all cases should pass this test which means the passwords were valid in main
def test_validate_password_success():
    password_list = [
        "Gamess&1",  # 8 character success
        "Gamess&12",  # 9 character success
        "Gamess&123",  # 10 character success
        "Gamess&1234",  # 11 character success
        "Gamess&12345",  # 12 character success
    ]
    for i in password_list:
        password = validate_password(i)
        assert password is not None


"---------------------------------------------------------------------------"


def mock_success_input(prompt):
    if "Enter your username: " in prompt:
        return "testuser"
    elif "Enter your password: " in prompt:
        return "ValidPass1!"


def mock_failed_input(prompt):
    if "Enter your username: " in prompt:
        return "usernotindb"
    elif "Enter your password: " in prompt:
        return "invalidpassword"
    elif "Do you want to try again (Y / N)? " in prompt:
        return "N"


def mock_try_again_input(prompt):
    if "Do you want to try again (Y / N)? " in prompt:
        return "Y"


def mock_features_input(prompt):
    if "Choose one of ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']: " in prompt:
        return "a"
    if "Choose one of ['a', 'b', 'c', 'd', 'e', 'f']:" in prompt:
        return "f"
    if "Do you want to go back (Y / N)? " in prompt:
        return "N"


def mock_go_back_input(prompt):
    if "Do you want to go back (Y / N)? " in prompt:
        return "N"


def mock_learn_skill_input(prompt):
    if "Enter integers from 1 to 6: " in prompt:
        return "1"
    if "Do you want to go back (Y / N)? " in prompt:
        return "N"


def mock_no_selected_skill_input(prompt):
    if "Enter integers from 1 to 6: " in prompt:
        return "6"
    if "Do you want to go back (Y / N)? " in prompt:
        return "N"


def test_successful_login(monkeypatch, capsys):
    # Mock user input for successful login
    create_user("testuser", "ValidPass1!", "Test", "User", "USF", "Major", 0, 0)
    monkeypatch.setattr("builtins.input", mock_success_input)

    # Call the login function
    username = login()

    # Capture the printed output
    captured = capsys.readouterr()

    # Assert the expected output and username
    assert "You have successfully logged in" in captured.out
    assert username == "testuser"


def test_failed_login(monkeypatch, capsys):
    # Mock user input for failed login
    monkeypatch.setattr("builtins.input", mock_failed_input)

    # Call the login function
    login()

    # Capture the printed output
    captured = capsys.readouterr()

    # Assert the expected output
    assert "Incorrect username / password, please try again" in captured.out
    assert try_again() is False


def test_unlimited_logins(monkeypatch):
    # Mock user input for try_again function
    monkeypatch.setattr("builtins.input", mock_try_again_input)

    # Call the try_again function and assert the expected output
    assert try_again() is True


def test_features(monkeypatch, capsys):
    # Mock user input for choose_features function
    monkeypatch.setattr("builtins.input", mock_features_input)

    # Call the choose_features function
    choose_features("testuser")

    # Capture the printed output
    captured = capsys.readouterr()

    # Assert that the expected message is printed
    assert "a. Search for a job" in captured.out
    assert "b. Find someone you know" in captured.out
    assert "c. Learn a new skill" in captured.out
    assert "d. Go to Navigation Links" in captured.out
    assert "e. Show My Network" in captured.out
    assert "f. Check Pending Friend Requests" in captured.out
    assert "g. Display Profiles" in captured.out
    assert "h. Messenger" in captured.out
    assert "i. Log Out" in captured.out


def test_learn_skill(monkeypatch, capsys):
    # Mock user input for learn_skill function
    monkeypatch.setattr("builtins.input", mock_learn_skill_input)

    # Call the learn_skill function
    learn_skill("testuser")

    # Capture the printed output
    captured = capsys.readouterr()

    # Assert that the expected message is printed
    assert "1. Python" in captured.out
    assert "2. Java" in captured.out
    assert "3. C++" in captured.out
    assert "4. JavaScript" in captured.out
    assert "5. SQL" in captured.out
    assert "6. Go back" in captured.out


def test_no_selected_skill(monkeypatch, capsys):
    # Mock user input for no selected skill
    monkeypatch.setattr("builtins.input", mock_no_selected_skill_input)

    # Call the learn_skill function
    learn_skill("testuser")

    # Capture the printed output
    captured = capsys.readouterr()

    # Assert that the expected message is printed
    assert "Not picking to learn a new skill?" in captured.out


"-----------------------------EPIC 2 Tests------------------------------------------"


def mock_watch_video(prompt):
    if "Would you like to watch their story (Y/N)? " in prompt:
        return "Y"


def mock_not_watch_video(prompt):
    if "Would you like to watch their story (Y/N)? " in prompt:
        return "N"


def mock_name_search_success(prompt):
    if "Please enter your friend's first name: " in prompt:
        return "Test"
    elif "Please enter your friend's last name: " in prompt:
        return "User"


def mock_name_search_fail(prompt):
    if "Please enter your friend's first name: " in prompt:
        return "Test"
    elif "Please enter your friend's last name: " in prompt:
        return "NotUser"


def mock_signup(prompt):
    if "Enter your username: " in prompt:
        return "anothertestuser"
    elif "Enter your password: " in prompt:
        return "ValidPass1!"
    elif "Please insert your first name: " in prompt:
        return "anotherTest"
    elif "Please insert your last name: " in prompt:
        return "anotherUser"
    elif "Would you like to upgrade your account? (Y / N): " in prompt:
        return "N"


def test_signup(monkeypatch, capsys):
    # Mock user input for successful signup
    monkeypatch.setattr("builtins.input", mock_signup)

    # Call the signup function
    signup()

    # Capture the printed output
    captured = capsys.readouterr()

    # Assert the expected output
    assert "Signup successful!" in captured.out
    assert delete_user("anothertestuser") is True


def test_name_search_success(monkeypatch, capsys):
    create_user("testuser", "ValidPass1!", "Test", "User", "USF", "Major", 0, 0)
    # Mock user input for successful name search
    monkeypatch.setattr("builtins.input", mock_name_search_success)

    # Call the name_search function
    name_search()

    # Capture the printed output
    captured = capsys.readouterr()

    # Assert the expected output
    assert "Test User is an existing user on inCollege." in captured.out


def test_name_search_fail(monkeypatch, capsys):
    # Mock user input for failed name search
    monkeypatch.setattr("builtins.input", mock_name_search_fail)

    # Call the name_search function
    name_search()

    # Capture the printed output
    captured = capsys.readouterr()

    # Assert the expected output
    assert "Test NotUser is not yet an existing user on inCollege." in captured.out


def test_watch_video(monkeypatch, capsys):
    # Mock user input for watching the video
    monkeypatch.setattr("builtins.input", mock_watch_video)

    # Call the web_opening function
    web_opening()

    # Capture the printed output
    captured = capsys.readouterr()

    # Assert the expected output
    assert "Video is now playing..." in captured.out


def test_not_watch_video(monkeypatch, capsys):
    # Mock user input for not watching the video
    monkeypatch.setattr("builtins.input", mock_not_watch_video)

    # Call the web_opening function
    web_opening()

    # Capture the printed output
    captured = capsys.readouterr()

    # Assert the expected output
    assert "Video is now playing..." not in captured.out


def friend_search_pass_input(prompt):
    if "Please enter your friend's first name: " in prompt:
        return "Test"
    if "Please enter your friend's last name: " in prompt:
        return "User"


def friend_search_fail_input(prompt):
    if "Please enter your friend's first name: " in prompt:
        return "test"
    if "Please enter your friend's last name: " in prompt:
        return "user"


def friend_search_fail_input_2(prompt):
    if "Please enter your friend's first name: " in prompt:
        return "jack"
    if "Please enter your friend's last name: " in prompt:
        return "mack"


def test_friend_search_pass(monkeypatch, capsys):
    create_user(
        username="testuser",
        password="ValidPass1!",
        first="Test",
        last="User",
        university="USF",
        major="Major",
        tier=0,
        days=0,
    )
    monkeypatch.setattr("builtins.input", friend_search_pass_input)
    name_search()
    captured = capsys.readouterr()
    assert "is an existing user on inCollege." in captured.out
    assert search_name("Test", "User") is True


def test_friend_search_fail_1(monkeypatch, capsys):
    create_user(
        username="testuser",
        password="ValidPass1!",
        first="Test",
        last="User",
        university="USF",
        major="Major",
        tier=0,
        days=0,
    )
    monkeypatch.setattr("builtins.input", friend_search_fail_input)
    name_search()
    captured = capsys.readouterr()

    assert "is not yet an existing user on inCollege." in captured.out
    assert search_name("test", "user") is False


def test_friend_search_fail_2(monkeypatch, capsys):
    create_user(
        username="testuser",
        password="ValidPass1!",
        first="Test",
        last="User",
        university="USF",
        major="Major",
        tier=0,
        days=0,
    )
    monkeypatch.setattr("builtins.input", friend_search_fail_input_2)
    name_search()
    captured = capsys.readouterr()

    assert "is not yet an existing user on inCollege." in captured.out
    assert search_name("test", "user") is False


def go_back_pass_input(prompt):
    if "Choose one of" in prompt:
        return "f"
    if "Do you want to go back (Y / N)? " in prompt:
        return "N"


def go_back_learn_skill_pass_input(prompt):
    if "Enter integers from 1 to " in prompt:
        return "6"
    if "Do you want to go back (Y / N)? " in prompt:
        return "N"


def test_job_search_go_back(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", go_back_pass_input)
    job_search("testuser")
    captured = capsys.readouterr()
    assert "Go back" in captured.out


def test_friend_search_go_back(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", go_back_pass_input)
    friend_search("testuser")
    captured = capsys.readouterr()
    assert "Go back" in captured.out


def test_learn_skill_go_back(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", go_back_learn_skill_pass_input)
    learn_skill("testuser")
    captured = capsys.readouterr()
    assert "Go back" in captured.out


def test_check_ten_jobs_pass(capsys):
    for i in range(0, 10):
        assert reached_job_limit(i) is False


def test_check_ten_jobs_fail(capsys):
    assert reached_job_limit(10) is True
    captured = capsys.readouterr()
    assert (
        "All permitted jobs have been created, please come back later" in captured.out
    )


def create_job_pass_input(prompt):
    if "Please enter the job's title: " in prompt:
        return "Software Engineer"
    if "Please enter the job's description: " in prompt:
        return "Code accurate and fast software"
    if "Please enter the job's employer: " in prompt:
        return "Google"
    if "Please enter the job's location: " in prompt:
        return "Los Angeles, CA"
    if "Please enter the job's salary: " in prompt:
        return "$125,000"
    if "Choose one of" in prompt:
        return "a"
    if "Choose one of" in prompt:
        return "b"
    if "Do you want to go back (Y / N)? " in prompt:
        return "N"


def test_create_job_pass(monkeypatch, capsys):
    create_job(
        title="a",
        description="b",
        employer="c",
        location="d",
        salary="e",
        first="f",
        last="g",
    )
    create_job(
        title="a",
        description="b",
        employer="c",
        location="d",
        salary="e",
        first="f",
        last="g",
    )
    create_job(
        title="a",
        description="b",
        employer="c",
        location="d",
        salary="e",
        first="f",
        last="g",
    )
    create_job(
        title="a",
        description="b",
        employer="c",
        location="d",
        salary="e",
        first="f",
        last="g",
    )
    create_job(
        title="a",
        description="b",
        employer="c",
        location="d",
        salary="e",
        first="f",
        last="g",
    )
    create_job(
        title="a",
        description="b",
        employer="c",
        location="d",
        salary="e",
        first="f",
        last="g",
    )
    create_job(
        title="a",
        description="b",
        employer="c",
        location="d",
        salary="e",
        first="f",
        last="g",
    )
    create_job(
        title="a",
        description="b",
        employer="c",
        location="d",
        salary="e",
        first="f",
        last="g",
    )
    create_job(
        title="a",
        description="b",
        employer="c",
        location="d",
        salary="e",
        first="f",
        last="g",
    )

    monkeypatch.setattr("builtins.input", create_job_pass_input)
    job_posting("testuser")
    captured = capsys.readouterr()
    assert "JOB_POSTING" in captured.out
    assert (
        "title" or "description" or "employer" or "location" or "salary" in captured.out
    )
    assert "Failed to insert Python variable into sqlite table" not in captured.out
    assert (
        "\nJob created: Thank You for posting. We hope you'll find great employees!\n"
        in captured.out
    )
    assert delete_job("a") is True
    assert delete_job("Software Engineer") is True


"------------------ EPIC #3 ---------------------------------------------------"


def mock_choose_useful_links(prompt):
    if "Choose one of ['a', 'b', 'c', 'd', 'e']: " in prompt:
        return "a"


def test_choose_useful_links(monkeypatch, capsys):
    """Mock user input for useful_links function"""
    monkeypatch.setattr("builtins.input", mock_choose_useful_links)
    monkeypatch.setattr("main.useful_link_direct", Mock())

    # Call the useful_links function
    choose_useful_links()

    # Capture the printed output
    captured = capsys.readouterr()

    # Assert that the expected message is printed
    assert "a. General" in captured.out
    assert "b. Browse InCollege" in captured.out
    assert "c. Business Solutions" in captured.out
    assert "d. Directories" in captured.out
    assert "e. Go back" in captured.out


def mock_general_signed_in(prompt):
    if "Choose one of ['a', 'b', 'c', 'd', 'e', 'f', 'g']: " in prompt:
        return "a"


@patch("main.signed_in", True)
def test_general_signed_in(monkeypatch, capsys):
    """Mock user input for general function"""
    monkeypatch.setattr("builtins.input", mock_general_signed_in)
    monkeypatch.setattr("main.signed_in_general_direct", Mock())

    # Call the general function
    general()

    # Capture the printed output
    captured = capsys.readouterr()

    # Assert that the expected message is printed
    assert "a. Help Center" in captured.out
    assert "b. About" in captured.out
    assert "c. Press" in captured.out
    assert "d. Blog" in captured.out
    assert "e. Careers" in captured.out
    assert "f. Developers" in captured.out
    assert "g. Go back" in captured.out


def mock_general_not_signed_in(prompt):
    if "Choose one of ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']: " in prompt:
        return "a"


@patch("main.signed_in", False)
def test_general_not_signed_in(monkeypatch, capsys):
    """Mock user input for general function"""
    monkeypatch.setattr("builtins.input", mock_general_not_signed_in)
    monkeypatch.setattr("main.non_signed_in_general_direct", Mock())

    # Call the general function
    general()

    # Capture the printed output
    captured = capsys.readouterr()

    # Assert that the expected message is printed
    assert "a. Sign Up" in captured.out
    assert "b. Help Center" in captured.out
    assert "c. About" in captured.out
    assert "d. Press" in captured.out
    assert "e. Blog" in captured.out
    assert "f. Careers" in captured.out
    assert "g. Developers" in captured.out
    assert "h. Go back" in captured.out


def test_help_center(monkeypatch, capsys):
    """Mock user input for help_center function"""
    monkeypatch.setattr("main.go_back", Mock())
    monkeypatch.setattr("main.general", Mock())
    # Call the help_center function
    help_center()

    # Capture the printed output
    captured = capsys.readouterr()

    # Assert that the expected message is printed
    assert "We're here to help" in captured.out


def test_about(monkeypatch, capsys):
    """Mock user input for about function"""
    monkeypatch.setattr("main.go_back", Mock())
    monkeypatch.setattr("main.general", Mock())
    # Call the about function
    about()

    # Capture the printed output
    captured = capsys.readouterr()

    # Assert that the expected message is printed
    assert (
        "In College: Welcome to In College, the world's largest college student network with many users in many countries and territories worldwide"
        in captured.out
    )


def test_press(monkeypatch, capsys):
    """Mock user input for press function"""
    monkeypatch.setattr("main.go_back", Mock())
    monkeypatch.setattr("main.general", Mock())
    # Call the press function
    press()

    # Capture the printed output
    captured = capsys.readouterr()

    # Assert that the expected message is printed
    assert (
        "In College Pressroom: Stay on top of the latest news, updates, and reports"
        in captured.out
    )


def test_blog(monkeypatch, capsys):
    """Mock user input for blog function"""
    monkeypatch.setattr("main.go_back", Mock())
    monkeypatch.setattr("main.general", Mock())
    # Call the blog function
    blog()

    # Capture the printed output
    captured = capsys.readouterr()

    # Assert that the expected message is printed
    assert "Under construction" in captured.out


def test_careers(monkeypatch, capsys):
    """Mock user input for careers function"""
    monkeypatch.setattr("main.go_back", Mock())
    monkeypatch.setattr("main.general", Mock())
    # Call the careers function
    careers()

    # Capture the printed output
    captured = capsys.readouterr()

    # Assert that the expected message is printed
    assert "Under construction" in captured.out


def test_developers(monkeypatch, capsys):
    """Mock user input for developers function"""
    monkeypatch.setattr("main.go_back", Mock())
    monkeypatch.setattr("main.general", Mock())
    # Call the developers function
    developers()

    # Capture the printed output
    captured = capsys.readouterr()

    # Assert that the expected message is printed
    assert "Under construction" in captured.out


def test_browse_incollege(monkeypatch, capsys):
    """Mock user input for browse_incollege function"""
    monkeypatch.setattr("main.go_back", Mock())
    monkeypatch.setattr("main.choose_useful_links", Mock())

    browse_incollege()

    captured = capsys.readouterr()

    assert "Under construction" in captured.out


def test_business_solutions(monkeypatch, capsys):
    """Mock user input for business_solutions function"""
    monkeypatch.setattr("main.go_back", Mock())
    monkeypatch.setattr("main.choose_useful_links", Mock())

    business_solutions()

    captured = capsys.readouterr()

    assert "Under construction" in captured.out


def test_directories(monkeypatch, capsys):
    """Mock user input for directories function"""
    monkeypatch.setattr("main.go_back", Mock())
    monkeypatch.setattr("main.choose_useful_links", Mock())

    directories()

    captured = capsys.readouterr()

    assert "Under construction" in captured.out


# Designed to mock the transition from navigation to imporant links
def mock_navi_to_important_input(prompt):
    if "Choose one of ['a', 'b', 'c']: " in prompt:
        return "b"
    if "Choose one of ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']: " in prompt:
        return "j"
    if "Do you want to go back (Y / N)? " in prompt:
        return "N"


# Designed to mock selecting the copyright notice option
def mock_copyright_notice_input(prompt):
    if "Choose one of ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']: " in prompt:
        return "a"
    if "Do you want to go back (Y / N)? " in prompt:
        return "N"


# Designed to mock selecting the about option
def mock_about_input(prompt):
    if "Choose one of ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']: " in prompt:
        return "b"
    if "Do you want to go back (Y / N)? " in prompt:
        return "N"


# Designed to mock selecting the accessibiltity option
def mock_accessibility_input(prompt):
    if "Choose one of ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']: " in prompt:
        return "c"
    if "Do you want to go back (Y / N)? " in prompt:
        return "N"


# Designed to mock selecting the user agreement option
def mock_user_agreement_input(prompt):
    if "Choose one of ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']: " in prompt:
        return "d"
    if "Do you want to go back (Y / N)? " in prompt:
        return "N"


# Designed to mock selecting the privacy policy option, and turning email off
def mock_privacy_policy_input(prompt):
    if "Choose one of ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']: " in prompt:
        return "e"
    if "Choose one of ['a', 'b']:" in prompt:
        return "a"
    if "Choose one of ['a', 'b', 'c']:" in prompt:
        return "a"
    if "Do you want to go back (Y / N)? " in prompt:
        return "N"


# Designed to mock selecting the cookie policy option
def mock_cookie_policy_input(prompt):
    if "Choose one of ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']: " in prompt:
        return "f"
    if "Do you want to go back (Y / N)? " in prompt:
        return "N"


# Designed to mock selecting the copyright policy option
def mock_copyright_policy_input(prompt):
    if "Choose one of ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']: " in prompt:
        return "g"
    if "Do you want to go back (Y / N)? " in prompt:
        return "N"


# Designed to mock selecting the brand policy option
def mock_brand_policy_input(prompt):
    if "Choose one of ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']: " in prompt:
        return "h"
    if "Do you want to go back (Y / N)? " in prompt:
        return "N"


# Designed to mock selecting the language option and changing it to spanish
def mock_language_input(prompt):
    if "Choose one of ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']: " in prompt:
        return "i"
    if "Choose one of ['a', 'b']:" in prompt:
        return "b"
    if "Do you want to go back (Y / N)? " in prompt:
        return "N"


# Designed to mock turning something on
def mock_turn_on_input(prompt):
    if "Choose one of ['a', 'b']:" in prompt:
        return "a"
    if "Do you want to go back (Y / N)? " in prompt:
        return "N"


# Designed to mock turning something off
def mock_turn_off_input(prompt):
    if "Choose one of ['a', 'b']:" in prompt:
        return "b"
    if "Do you want to go back (Y / N)? " in prompt:
        return "N"


# Testing to see if navigation can move to important link, and print all the options
def test_navigation_to_important_link(monkeypatch, capsys):
    # Mock user input for choosing important link
    monkeypatch.setattr("builtins.input", mock_navi_to_important_input)

    # Call the choose navigation link function
    choose_navigation_link()

    # Capture the printed output
    captured = capsys.readouterr()

    # Assert that the expected message is printed
    assert "a. Useful Links" in captured.out
    assert "b. InCollege Important Links" in captured.out
    assert "c. Go back" in captured.out

    assert "a. A Copyright Notice" in captured.out
    assert "b. About" in captured.out
    assert "c. Accessibility" in captured.out
    assert "d. User Agreement" in captured.out
    assert "e. Privacy Policy" in captured.out
    assert "f. Cookie Policy" in captured.out
    assert "g. Copyright Policy" in captured.out
    assert "h. Brand Policy" in captured.out
    assert "i. Languages" in captured.out
    assert "j. Go back" in captured.out


# Testing to see if the copyright notice text is printed
def test_copyright_notice(monkeypatch, capsys):
    # Mock user input for choosing copyright notice
    monkeypatch.setattr("builtins.input", mock_copyright_notice_input)

    # Call the choose incollege important links function
    choose_incollege_important_links()

    # Capture the printed output
    captured = capsys.readouterr()

    # Assert that the expected message is printed
    assert "© Team_Arizona_2023_forever" in captured.out
    assert "All rights reserved" in captured.out


# Testing to see if the about text is printed
def test_about(monkeypatch, capsys):
    # Mock user input for  choosing about
    monkeypatch.setattr("builtins.input", mock_about_input)

    # Call the choose incollege important links function
    choose_incollege_important_links()

    # Capture the printed output
    captured = capsys.readouterr()

    # Assert that the expected message is printed
    assert (
        "In College: Welcome to In College, the world's largest college student network with many users in many countries and territories worldwide"
        in captured.out
    )


# Testing to see if the accessibility text is printed
def test_accessibility(monkeypatch, capsys):
    # Mock user input for choosing accessibility
    monkeypatch.setattr("builtins.input", mock_accessibility_input)

    # Call the choose incollege important links function
    choose_incollege_important_links()

    # Capture the printed output
    captured = capsys.readouterr()

    # Assert that the expected messages are printed
    assert (
        "We are committed to ensuring that our platform is accessible to all users,including those with disabilities. Here are some of the features we have implemented to enhance accessibility:"
        in captured.out
    )

    assert (
        "If you encounter any accessibility issues or have suggestions for improvement,please contact us at Team Arizona."
        in captured.out
    )


# Testing to see if the user agreement text is printed
def test_user_agreement(monkeypatch, capsys):
    # Mock user input for choosing user agreement
    monkeypatch.setattr("builtins.input", mock_user_agreement_input)

    # Call the choose incollege important links function
    choose_incollege_important_links()

    # Capture the printed output
    captured = capsys.readouterr()

    # Assert that the expected messages are printed
    assert (
        "By using our platform, you agree to abide by the following terms and conditions: \n <Respect the rights of other users> \n <Do not engage in any unlawful activities on our platform.> \n <Abide by our community guidelines.> \n <Protect your account credentials and personal information.> \n <Report any suspicious or inappropriate content.> \n \n \n <Failure to comply with these terms may result in account suspension or termination.>"
        in captured.out
    )


# Testing to see if the privacy policy is printing the proper options
def test_privacy_policy(monkeypatch, capsys):
    # Mock user input for choosing privacy policy
    monkeypatch.setattr("builtins.input", mock_privacy_policy_input)

    # Call the choose incollege important links function
    choose_incollege_important_links()

    # Capture the printed output
    captured = capsys.readouterr()

    assert "a. Guest Controls" in captured.out
    assert "b. Go Back" in captured.out
    assert "a. Email" in captured.out
    assert "b. SMS" in captured.out
    assert "c. Target_Advertising" in captured.out
    assert "a. Turn On" in captured.out
    assert "b. Turn Off" in captured.out


# Testing to see if the cookie policy text is printed
def test_cookie_policy(monkeypatch, capsys):
    # Mock user input for choosing cookie policy
    monkeypatch.setattr("builtins.input", mock_cookie_policy_input)

    # Call the choose incollege important links function
    choose_incollege_important_links()

    # Capture the printed output
    captured = capsys.readouterr()

    assert (
        "Our website uses cookies to improve your experience. By continuing to use our site, you accept our use of cookies."
        in captured.out
    )


# Testing to see if the copyright policy text is printed
def test_copyright_policy(monkeypatch, capsys):
    # Mock user input for choosing copyright policy
    monkeypatch.setattr("builtins.input", mock_copyright_policy_input)

    # Call the choose incollege important links function
    choose_incollege_important_links()

    # Capture the printed output
    captured = capsys.readouterr()

    assert (
        "All content on this platform is protected by copyright laws. The content includes but is not limited to text, images, logos, and graphics \n You may not reproduce, distribute, or modify our content without explicit written permission from us \n For copyright-related inquiries, please contact: legal@incollege.com."
        in captured.out
    )


# Testing to see if the brand policy text is printed
def test_brand_policy(monkeypatch, capsys):
    # Mock user input for choosing brand policy
    monkeypatch.setattr("builtins.input", mock_brand_policy_input)

    # Call the choose incollege important links function
    choose_incollege_important_links()

    # Capture the printed output
    captured = capsys.readouterr()

    assert (
        "Our brand is a valuable asset, including our name, logo, and visual identity. To maintain consistency and integrity, we have established guidelines for the use of our brand elements. \n \n You may not use our brand elements without prior written permission. Any use must adhere to our brand guidelines \n \n If you require the use of our brand for any purpose, please contact us to request approval."
        in captured.out
    )


# Testing to see if the language options are presented and can change to spanish
def test_language_setting(monkeypatch, capsys):
    # Mock user input for choosing language options
    monkeypatch.setattr("builtins.input", mock_language_input)

    # Call the choose incollege important links function
    choose_incollege_important_links()

    # Capture the printed output
    captured = capsys.readouterr()

    assert "You selected Languages" in captured.out
    assert "a. English" in captured.out
    assert "b. Spanish" in captured.out
    assert (
        "Congratulations, the app language has been changed to Spanish" in captured.out
    )


# Testing to see if email is turned on
def test_turn_on_email(monkeypatch, capsys):
    # Mock user input for choosing guest policy
    monkeypatch.setattr("builtins.input", mock_turn_on_input)

    # Call the turn on and off function
    change = turn_on_off("a")

    # Capture the printed output
    captured = capsys.readouterr()

    assert "a. Turn On" in captured.out
    assert "b. Turn Off" in captured.out
    assert change == 1


# Testing to see if email is turned off
def test_turn_off_email(monkeypatch, capsys):
    # Mock user input for choosing guest policy
    monkeypatch.setattr("builtins.input", mock_turn_off_input)

    # Call the turn on and off function
    change = turn_on_off("a")

    # Capture the printed output
    captured = capsys.readouterr()

    assert "a. Turn On" in captured.out
    assert "b. Turn Off" in captured.out
    assert change == 0


# Testing to see if SMS is turned on
def test_turn_on_SMS(monkeypatch, capsys):
    # Mock user input for choosing guest policy
    monkeypatch.setattr("builtins.input", mock_turn_on_input)

    # Call the turn on and off function
    change = turn_on_off("b")

    # Capture the printed output
    captured = capsys.readouterr()

    assert "a. Turn On" in captured.out
    assert "b. Turn Off" in captured.out
    assert change == 1


# Testing to see if SMS is turned off
def test_turn_off_SMS(monkeypatch, capsys):
    # Mock user input for choosing guest policy
    monkeypatch.setattr("builtins.input", mock_turn_off_input)

    # Call the turn on and off function
    change = turn_on_off("b")

    # Capture the printed output
    captured = capsys.readouterr()

    assert "a. Turn On" in captured.out
    assert "b. Turn Off" in captured.out
    assert change == 0


# Testing to see if targeted Ads are turned on
def test_turn_on_ads(monkeypatch, capsys):
    # Mock user input for choosing guest policy
    monkeypatch.setattr("builtins.input", mock_turn_on_input)

    # Call the turn on and off function
    change = turn_on_off("c")

    # Capture the printed output
    captured = capsys.readouterr()

    assert "a. Turn On" in captured.out
    assert "b. Turn Off" in captured.out
    assert change == 1


# Testing to see if targeted Ads are turned off
def test_turn_off_ads(monkeypatch, capsys):
    # Mock user input for choosing guest policy
    monkeypatch.setattr("builtins.input", mock_turn_off_input)

    # Call the turn on and off function
    change = turn_on_off("c")

    # Capture the printed output
    captured = capsys.readouterr()

    assert "a. Turn On" in captured.out
    assert "b. Turn Off" in captured.out
    assert change == 0


"///////////////////////   Epic #4   //////////////////////////////////////////////"


# Helper function to make a friend request
def friend_request_helper(monkeypatch, capsys):
    # Perform mock friend request
    monkeypatch.setattr("builtins.input", mock_send_friend_request_input)

    # Start from friend request function
    send_friend_request("TestFriend")


# Helper function to accept friend request
def accept_friend_request_helper(monkeypatch, capsys):
    # Perform mock accepting friend request
    monkeypatch.setattr("builtins.input", mock_accept_request_input)

    # Start from friend request function
    check_friend_request("TestUser")


# Helper function to accept friend request
def delete_friend_request_helper(monkeypatch, capsys):
    # Perform mock accepting friend request
    monkeypatch.setattr("builtins.input", mock_delete_request_input)

    # Start from friend request function
    check_friend_request("TestUser")


# Mocks quiting the program if network has no friends
def mock_quit_from_network_input_V1(prompt):
    if "Choose one of ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']: " in prompt:
        return "i"

    if "Do you want to log out (Y / N)? " in prompt:
        return "Y"


# Mocks quiting the program if you don't remove friends
def mock_quit_from_network_input_V2(prompt):
    if "Would you like to disconnect from one of these friends? (y/n):" in prompt:
        return "n"

    if "Do you want to go back (Y / N)? " in prompt:
        return "N"


# Mocks quiting the program if you remove a friend
def mock_quit_from_network_input_V3(prompt):
    if "Would you like to disconnect from one of these friends? (y/n):" in prompt:
        return "y"

    if "Which user would you like to delete?" in prompt:
        return "TestFriend"

    if "Choose one of ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']: " in prompt:
        return "i"

    if "Do you want to log out (Y / N)? " in prompt:
        return "Y"


# Mocks sending a friend request and then quit
def mock_send_friend_request_input(prompt):
    if "Enter the username of the user you want to connect with: " in prompt:
        return "TestUser"


# Mocks leaving from the pending friend request menu and then quit
def mock_quit_Friend_request_input(prompt):
    if "Choose one of ['a', 'r', 'b']: " in prompt:
        return "b"

    if "Do you want to go back (Y / N)? " in prompt:
        return "N"


# Mocks leaving from the pending friend request menu and then quit
def mock_accept_request_input(prompt):
    if "Choose one of ['a', 'r', 'b']: " in prompt:
        return "a"

    if "Which user would you like to add?" in prompt:
        return "TestFriend"

    if "Choose one of ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']: " in prompt:
        return "i"

    if "Do you want to log out (Y / N)? " in prompt:
        return "Y"


# Mocks rejecting a friend request and then quit
def mock_delete_request_input(prompt):
    if "Choose one of ['a', 'r', 'b']: " in prompt:
        return "r"

    if "Which user would you like to reject?" in prompt:
        return "TestFriend"

    if "Choose one of ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']: " in prompt:
        return "i"

    if "Do you want to log out (Y / N)? " in prompt:
        return "Y"


# Test to see if friends list returns empty and informs the user
def test_empty_friends_list(monkeypatch, capsys):
    # mock the first scenerio for the network menu, when friends list is empty
    monkeypatch.setattr("builtins.input", mock_quit_from_network_input_V1)

    # Call the check friend request function
    show_network("TestUser")

    # Capture the printed output
    captured = capsys.readouterr()

    assert "You have no friends!" in captured.out


# Test to see if a single friend request passes through
def test_one_friend_request(monkeypatch, capsys):
    # use helper to add a single friend
    friend_request_helper(monkeypatch, capsys)

    # Capture the printed output
    captured = capsys.readouterr()
    assert "Friend request sent to TestUser!" in captured.out

    # Mock quitting immediately after checking friend request
    monkeypatch.setattr("builtins.input", mock_quit_Friend_request_input)

    # Call the check friend request function
    check_friend_request("TestUser")

    # Capture the printed output
    captured = capsys.readouterr()

    assert "You have a pending friend request from:" in captured.out
    assert "TestFriend" in captured.out

    # Delete the friend request to refresh the list to none
    delete_friend_request_helper(monkeypatch, capsys)


# Test to see if three friend request pass through
def test_three_friend_request(monkeypatch, capsys):
    # use helper to add three friends
    friend_request_helper(monkeypatch, capsys)
    friend_request_helper(monkeypatch, capsys)
    friend_request_helper(monkeypatch, capsys)

    # Capture the printed output
    captured = capsys.readouterr()
    assert "Friend request sent to TestUser!" in captured.out

    # Mock quitting immediately after checking friend request
    monkeypatch.setattr("builtins.input", mock_quit_Friend_request_input)

    # Call the check friend request function
    check_friend_request("TestUser")

    # Capture the printed output
    captured = capsys.readouterr()

    assert "You have a pending friend request from:" in captured.out
    assert "TestFriend" in captured.out
    assert "TestFriend" in captured.out
    assert "TestFriend" in captured.out

    # Delete the friend request to refresh the list to none
    delete_friend_request_helper(monkeypatch, capsys)
    delete_friend_request_helper(monkeypatch, capsys)
    delete_friend_request_helper(monkeypatch, capsys)


# Test to see if a single friend request is accepted
def test_accept_friend(monkeypatch, capsys):
    # Create another friend request
    friend_request_helper(monkeypatch, capsys)

    # Capture output to see if friend request is sent
    captured = capsys.readouterr()
    assert "Friend request sent to TestUser!" in captured.out

    # Mock accepting the friend request, then quitting
    monkeypatch.setattr("builtins.input", mock_accept_request_input)

    # Call the check friend request function
    check_friend_request("TestUser")

    # Capture the printed output
    captured = capsys.readouterr()

    assert "You have a pending friend request from:" in captured.out
    assert "TestFriend" in captured.out
    assert "Friend Added!" in captured.out


# Test to see if a single friend request is rejected
def test_reject_friend(monkeypatch, capsys):
    # Create a friend request to send over to use
    friend_request_helper(monkeypatch, capsys)

    # Capture output to see if friend request is sent
    captured = capsys.readouterr()
    assert "Friend request sent to TestUser!" in captured.out

    # Mock rejecting a request, then quitting
    monkeypatch.setattr("builtins.input", mock_delete_request_input)

    # Call the check friend request function
    check_friend_request("TestUser")

    # Capture the printed output
    captured = capsys.readouterr()

    assert "You have a pending friend request from:" in captured.out
    assert "TestFriend" in captured.out
    assert "Friend Rejected!" in captured.out


# Test to see if a friend is added to the user's friend list.
def test_user_add_friend_list(monkeypatch, capsys):
    # Check to see if the user's friend list has the friend he accepted earlier
    monkeypatch.setattr("builtins.input", mock_quit_from_network_input_V2)

    # Show friends list
    show_network("TestUser")

    # Capture the printed output
    captured = capsys.readouterr()

    assert "Here's a list of your friends:" in captured.out
    assert "TestFriend" in captured.out


# Test to see if the user is added to the user's friend list.
def test_friend_add_friend_list(monkeypatch, capsys):
    # Checkt to siff the the friend's friend last had the user who accepted him
    monkeypatch.setattr("builtins.input", mock_quit_from_network_input_V2)

    # Show friends list
    show_network("TestFriend")

    # Capture the printed output
    captured = capsys.readouterr()

    assert "Here's a list of your friends:" in captured.out
    assert "TestUser" in captured.out


# Test to remove a friend from the friends list
def test_remove_friend(monkeypatch, capsys):
    # Mock removing a friend from the friend's list
    monkeypatch.setattr("builtins.input", mock_quit_from_network_input_V3)

    # Show friends list, so to remove friend
    show_network("TestUser")

    # Capture the printed output
    captured = capsys.readouterr()

    assert "Here's a list of your friends:" in captured.out
    assert "TestFriend" in captured.out
    assert "Friend Deleted" in captured.out


# Test to see if the user is removed from the user's friend list.
def test_user_remove_friend_list(monkeypatch, capsys):
    # Mock quitting after noticing no friends in the friends list
    monkeypatch.setattr("builtins.input", mock_quit_from_network_input_V1)

    # Show friends list
    show_network("TestUser")

    # Capture the printed output
    captured = capsys.readouterr()

    assert "You have no friends!" in captured.out


# Test to see if the user is removed from the user's friend list.
def test_friend_remove_friend_list(monkeypatch, capsys):
    # Mock quitting after noticing no friends in the friends list
    monkeypatch.setattr("builtins.input", mock_quit_from_network_input_V1)

    # Show friend's list
    show_network("TestFriend")

    # Capture the printed output
    captured = capsys.readouterr()

    assert "You have no friends!" in captured.out


def test_friends_list_initially_empty():
    # Create a new user
    username = "test_user"
    password = "password123"
    create_user(
        username, password, "John", "Doe", "Test University", "Computer Science", 0, 0
    )

    # Check that new user has empty friends list
    friends = list_of_friends(username)
    assert friends == False

    # Clean up test user
    delete_user(username)


def test_find_someone_you_know():
    # Create some test users
    create_user("alice", "pw123", "Alice", "Smith", "State U", "Computer Science", 0, 0)
    create_user("bob", "pw456", "Bob", "Jones", "State U", "Biology", 0, 0)

    logged_in_user = "charlie"

    # Search by last name
    results = get_username_from_last_name("Smith")
    assert results == ["alice"]

    # Search by university
    results = get_username_from_university("State U")
    assert set(results) == {"alice", "bob"}

    # Search by major
    results = get_username_from_major("Computer Science")
    assert results == ["alice"]

    # Send connection request
    add_friend(logged_in_user, "alice")

    # Verify request was sent
    request = pending_friend_request_list("alice")
    assert any(logged_in_user in req for req in request)

    # Clean up test users
    delete_user("alice")
    delete_user("bob")
    delete_user("charlie")


"///////////////////////   Epic #5   //////////////////////////////////////////////"


def mock_profile_choice_and_features_input(prompt):
    if "Choose one of ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']: " in prompt:
        return "g"
    if "Choose one of ['a', 'b', 'c', 'd']:" in prompt:
        return "d"
    if "Do you want to go back (Y / N)? " in prompt:
        return "N"


def test_profile_choice_and_features(monkeypatch, capsys):
    # Mock user input for choose_features and display_profile_navigation functions
    monkeypatch.setattr("builtins.input", mock_profile_choice_and_features_input)

    # Call the choose_features function
    choose_features("testuser")

    # Capture the printed output
    captured = capsys.readouterr()

    # Assert that the feature to make, update, display, or search for a profile is shown in when a user logs in
    assert "g. Display Profiles" in captured.out

    # Assert the features for profiles are available in the program
    assert "a. Create or Update Your Profile" in captured.out
    assert "b. Display Your Profile" in captured.out
    assert "c. Display Your Friend's Profile" in captured.out
    assert "d. Go Back" in captured.out


def mock_create_user_profile_V1(prompt):
    # Tests user profile that is entirely filled out
    if "Please enter your university: " in prompt:
        return "university of south florida"
    if "Please enter your major: " in prompt:
        return "computer science"
    if "How many years did you attend University Of South Florida: " in prompt:
        return "3"
    if "Please enter your degree: " in prompt:
        return "Bachelors"
    if "Please enter your title: " in prompt:
        return "3rd Year Computer Science Student"
    if "Please enter a short description about yourself: " in prompt:
        return "I am a third year computer science student that is looking for a job!"
    if "Please enter your experience title: " in prompt:
        return "Intern"
    if "Please enter your employer: " in prompt:
        return "Boeing"
    if "Please enter your start date: " in prompt:
        return "October 1st, 2020"
    if "Please enter your end date: " in prompt:
        return "December 30th, 2021"
    if "Please enter your location: " in prompt:
        return "New York"
    if "Please enter your description: " in prompt:
        return "Worked at Boeing as an intern to fix up airline website"
    if "Do you want to add another experience? (Y/N): " in prompt:
        return "N"
    if "Do you want to see what your profile looks like (Y/N)? " in prompt:
        return "Y"
    if "Do you want to go back (Y / N)? " in prompt:
        return "N"


def mock_create_user_profile_V2(prompt):
    # Tests user profile that has education info but no lines of experience info
    if "Please enter your university: " in prompt:
        return "university of florida"
    if "Please enter your major: " in prompt:
        return "biology"
    if "How many years did you attend University Of Florida: " in prompt:
        return "6"
    if "Please enter your degree: " in prompt:
        return "Masters"
    if "Please enter your title: " in prompt:
        return "1st Year Biology Student"
    if "Please enter a short description about yourself: " in prompt:
        return "I am a first year biology student that is looking for a job!"
    if "Please enter your experience title: " in prompt:
        return ""
    if "Please enter your employer: " in prompt:
        return ""
    if "Please enter your start date: " in prompt:
        return ""
    if "Please enter your end date: " in prompt:
        return ""
    if "Please enter your location: " in prompt:
        return ""
    if "Please enter your description: " in prompt:
        return ""
    if "Do you want to add another experience? (Y/N): " in prompt:
        return "N"
    if "Do you want to see what your profile looks like (Y/N)? " in prompt:
        return "Y"
    if "Do you want to go back (Y / N)? " in prompt:
        return "N"


def mock_create_user_profile_V3(prompt):
    # Tests user profile that contains only 1 line about their education but no lines of experience info or profile info
    if "Please enter your university: " in prompt:
        return "university of central florida"
    if "Please enter your major: " in prompt:
        return ""
    if "How many years did you attend University Of Central Florida: " in prompt:
        return ""
    if "Please enter your degree: " in prompt:
        return ""
    if "Please enter your title: " in prompt:
        return ""
    if "Please enter a short description about yourself: " in prompt:
        return ""
    if "Please enter your experience title: " in prompt:
        return ""
    if "Please enter your employer: " in prompt:
        return ""
    if "Please enter your start date: " in prompt:
        return ""
    if "Please enter your end date: " in prompt:
        return ""
    if "Please enter your location: " in prompt:
        return ""
    if "Please enter your description: " in prompt:
        return ""
    if "Do you want to add another experience? (Y/N): " in prompt:
        return "N"
    if "Do you want to see what your profile looks like (Y/N)? " in prompt:
        return "Y"
    if "Do you want to go back (Y / N)? " in prompt:
        return "N"


def mock_create_user_profile_V4(prompt):
    # Tests user profile that contains only 1 line about their education but no lines of experience info or profile info
    if "Please enter your university: " in prompt:
        return "florida state university"
    if "Please enter your major: " in prompt:
        return ""
    if "How many years did you attend Florida State University: " in prompt:
        return ""
    if "Please enter your degree: " in prompt:
        return ""
    if "Please enter your title: " in prompt:
        return ""
    if "Please enter a short description about yourself: " in prompt:
        return ""
    if "Please enter your experience title: " in prompt:
        return "title"
    if "Please enter your employer: " in prompt:
        return "employer"
    if "Please enter your start date: " in prompt:
        return "start"
    if "Please enter your end date: " in prompt:
        return "end"
    if "Please enter your location: " in prompt:
        return "location"
    if "Please enter your description: " in prompt:
        return "desc"
    if "Do you want to add another experience? (Y/N): " in prompt:
        return "Y"
    if "Do you want to see what your profile looks like (Y/N)? " in prompt:
        return "Y"
    if "Do you want to go back (Y / N)? " in prompt:
        return "N"


def test_create_user_profile_V1(monkeypatch, capsys):
    # Mock user input for create_user_profile function
    monkeypatch.setattr("builtins.input", mock_create_user_profile_V1)

    # Call the create_user_profile function
    create_user_profile("testuser")

    # Capture the printed output
    captured = capsys.readouterr()

    # Assert that the messages where the profile is sucessfully created and
    # shows the correct capitalization for the user's university and major and fully filled out info
    assert "Profile created!" in captured.out
    assert "Education created!" in captured.out
    assert "Experience created!" in captured.out
    assert "Username:  testuser" in captured.out
    assert "Title:  3rd Year Computer Science Student" in captured.out
    assert (
        "About Me:  I am a third year computer science student that is looking for a job!"
        in captured.out
    )
    assert "University:  University Of South Florida" in captured.out
    assert "Major:  Computer Science" in captured.out
    assert "Degree:  Bachelors" in captured.out
    assert "Years Attended:  3" in captured.out

    user_profile = get_profile("testuser")
    for i, experience in enumerate(user_profile["experience"]):
        title = experience["title"]
        employer = experience["employer"]
        location = experience["location"]
        start_date = experience["date_started"]
        end_date = experience["date_ended"]
        description = experience["description"]

    assert title == "Intern"
    assert employer == "Boeing"
    assert location == "New York"
    assert start_date == "October 1st, 2020"
    assert end_date == "December 30th, 2021"
    assert description == "Worked at Boeing as an intern to fix up airline website"

    # Clean up test user profile
    delete_profile("testuser")
    delete_education("testuser")
    delete_experience("testuser")


def test_create_user_profile_V2(monkeypatch, capsys):
    # Mock user input for create_user_profile function
    monkeypatch.setattr("builtins.input", mock_create_user_profile_V2)

    # Call the create_user_profile function
    create_user_profile("testuser")

    # Capture the printed output
    captured = capsys.readouterr()

    # Assert that the messages where the profile is sucessfully created and
    # shows the user's profile info and education info but with experience info empty
    assert "Profile created!" in captured.out
    assert "Education created!" in captured.out
    assert "Experience created!" in captured.out
    assert "Username:  testuser" in captured.out
    assert "Title:  1st Year Biology Student" in captured.out
    assert (
        "About Me:  I am a first year biology student that is looking for a job!"
        in captured.out
    )
    assert "University:  University Of Florida" in captured.out
    assert "Major:  Biology" in captured.out
    assert "Degree:  Masters" in captured.out
    assert "Years Attended:  6" in captured.out

    user_profile = get_profile("testuser")
    for i, experience in enumerate(user_profile["experience"]):
        title = experience["title"]
        employer = experience["employer"]
        location = experience["location"]
        start_date = experience["date_started"]
        end_date = experience["date_ended"]
        description = experience["description"]

    assert title == ""
    assert employer == ""
    assert location == ""
    assert start_date == ""
    assert end_date == ""
    assert description == ""

    # Clean up test user profile
    delete_profile("testuser")
    delete_education("testuser")
    delete_experience("testuser")


def test_create_user_profile_V3(monkeypatch, capsys):
    # Mock user input for create_user_profile function
    monkeypatch.setattr("builtins.input", mock_create_user_profile_V3)

    # Call the create_user_profile function
    create_user_profile("testuser")

    # Capture the printed output
    captured = capsys.readouterr()

    # Assert that the messages where the profile is sucessfully created and
    # shows the profile successfully created but with only 1 line of education info
    assert "Profile created!" in captured.out
    assert "Education created!" in captured.out
    assert "Experience created!" in captured.out
    assert "Username:  testuser" in captured.out
    assert "Title:  " in captured.out
    assert "About Me:  " in captured.out
    assert "University:  University Of Central Florida" in captured.out
    assert "Major:  " in captured.out
    assert "Degree:  " in captured.out
    assert "Years Attended:  " in captured.out

    user_profile = get_profile("testuser")
    for i, experience in enumerate(user_profile["experience"]):
        title = experience["title"]
        employer = experience["employer"]
        location = experience["location"]
        start_date = experience["date_started"]
        end_date = experience["date_ended"]
        description = experience["description"]

    assert title == ""
    assert employer == ""
    assert location == ""
    assert start_date == ""
    assert end_date == ""
    assert description == ""

    # Clean up test user profile
    delete_profile("testuser")
    delete_education("testuser")
    delete_experience("testuser")


def test_create_user_profile_V4(monkeypatch, capsys):
    # Mock user input for create_user_profile function
    monkeypatch.setattr("builtins.input", mock_create_user_profile_V4)

    # Call the create_user_profile function
    create_user_profile("testuser")

    # Capture the printed output
    captured = capsys.readouterr()

    # Assert that the messages where the profile is sucessfully created and
    # that it allows up to 3 past experiences to be created
    assert "Profile created!" in captured.out
    assert "Education created!" in captured.out
    assert "Experience created!" in captured.out
    assert "You have reached the maximum number of experiences!" in captured.out

    user_profile = get_profile("testuser")
    for i, experience in enumerate(user_profile["experience"]):
        title = experience["title"]
        employer = experience["employer"]
        location = experience["location"]
        start_date = experience["date_started"]
        end_date = experience["date_ended"]
        description = experience["description"]

    assert title == "title"
    assert employer == "employer"
    assert location == "location"
    assert start_date == "start"
    assert end_date == "end"
    assert description == "desc"

    # Clean up test user profile
    delete_profile("testuser")
    delete_education("testuser")
    delete_experience("testuser")


def mock_update_user_profile(prompt):
    # Tests user profile that will be updated with new values and fills in missing sections in previous
    # version of the student's profile
    if "Please enter your university: " in prompt:
        return "university of south florida"
    if "Please enter your major: " in prompt:
        return "Business"
    if "How many years did you attend University Of South Florida: " in prompt:
        return "1"
    if "Please enter your degree: " in prompt:
        return "Bachelors"
    if "Please enter your title: " in prompt:
        return "1st Year Business Student"
    if "Please enter a short description about yourself: " in prompt:
        return "I am a first year business student that is looking for a job!"
    if "Please enter your experience title: " in prompt:
        return "Intern"
    if "Please enter your employer: " in prompt:
        return "Boeing"
    if "Please enter your start date: " in prompt:
        return "October 1st, 2020"
    if "Please enter your end date: " in prompt:
        return "December 30th, 2021"
    if "Please enter your location: " in prompt:
        return "New York"
    if "Please enter your description: " in prompt:
        return "Worked at Boeing as an intern to write a blog for their website"
    if "Do you want to update another experience? (Y/N): " in prompt:
        return "N"
    if "Do you want to see what your profile looks like (Y/N)? " in prompt:
        return "Y"
    if "Do you want to go back (Y / N)? " in prompt:
        return "N"


def test_update_user_profile(monkeypatch, capsys):
    # Mock user input for create_user_profile function
    monkeypatch.setattr("builtins.input", mock_update_user_profile)

    # Call the create_user_profile function
    create_profile(
        "testuser", "University of South Florida", "Computer Science", "", ""
    )
    create_education("testuser", "University of South Florida", "", 3)
    create_experience(
        "testuser",
        1,
        "Intern",
        "Boeing",
        "October 1st, 2020",
        "December 30th, 2021",
        "New York",
        "Worked at Boeing as an intern to write a blog for their website",
    )

    # Call the create_user_profile function
    create_user_profile("testuser")

    # Capture the printed output
    captured = capsys.readouterr()

    # Assert that the messages where the profile is sucessfully updated and
    # updates and fills in the remaining sections that the student wanted to add
    assert "Profile updated!" in captured.out
    assert "Education updated!" in captured.out
    assert "Experience updated!" in captured.out
    assert "Username:  testuser" in captured.out
    assert "Title:  1st Year Business Student" in captured.out
    assert (
        "About Me:  I am a first year business student that is looking for a job!"
        in captured.out
    )
    assert "University:  University Of South Florida" in captured.out
    assert "Major:  Business" in captured.out
    assert "Degree:  Bachelors" in captured.out
    assert "Years Attended:  1" in captured.out

    user_profile = get_profile("testuser")
    for i, experience in enumerate(user_profile["experience"]):
        title = experience["title"]
        employer = experience["employer"]
        location = experience["location"]
        start_date = experience["date_started"]
        end_date = experience["date_ended"]
        description = experience["description"]

    assert title == "Intern"
    assert employer == "Boeing"
    assert location == "New York"
    assert start_date == "October 1st, 2020"
    assert end_date == "December 30th, 2021"
    assert (
        description == "Worked at Boeing as an intern to write a blog for their website"
    )

    # Clean up test user profile
    delete_profile("testuser")
    delete_education("testuser")
    delete_experience("testuser")


def test_display_user_profile(monkeypatch, capsys):
    create_user("test", "pwd123", "Test", "User", "Test U", "CS", 0, 0)

    monkeypatch.setattr("builtins.input", lambda x: "Y")

    display_user_profile("test")

    captured = capsys.readouterr()
    assert "Here's Test User's profile:" in captured.out
    assert "You have no profile" in captured.out


def test_display_user_friend_profile(monkeypatch, capsys):
    def mock_get_profile(username):
        return {
            "user": "friend",
            "title": "Engineer",
            "about": "Test about me section.",
            "university": "Test U",
            "major": "CS",
            "degree": "Bachelor",
            "years_attended": "2010-2014",
            "experience": [
                {
                    "title": "Software Engineer",
                    "employer": "Tech Corp",
                    "location": "Tech City",
                    "date_started": "2015-01",
                    "date_ended": "2020-12",
                    "description": "Worked on various tech projects.",
                }
            ],
        }

    monkeypatch.setattr("main.get_profile", mock_get_profile)

    def mock_draw_line(message):
        print(message)

    monkeypatch.setattr("main.draw_line", mock_draw_line)

    display_user_friend_profile("friend")

    captured = capsys.readouterr()

    assert "FRIEND'S PROFILE" in captured.out
    assert "Engineer" in captured.out
    assert "Test about me section." in captured.out
    assert "Test U" in captured.out
    assert "CS" in captured.out
    assert "Bachelor" in captured.out
    assert "2010-2014" in captured.out
    assert "Software Engineer" in captured.out
    assert "Tech Corp" in captured.out
    assert "Tech City" in captured.out
    assert "2015-01" in captured.out
    assert "2020-12" in captured.out
    assert "Worked on various tech projects." in captured.out


def test_display_friend_no_friends(monkeypatch, capsys):
    monkeypatch.setattr("main.list_of_friends", lambda x: False)

    monkeypatch.setattr("builtins.input", lambda _: "n")

    display_friend_profile("test")

    captured = capsys.readouterr()
    assert "You have no friends!" in captured.out


def mock_get_profile(username):
    if username == "friend1":
        return {
            "user": "friend1",
            "university": "Some University",
            "major": "Some Major",
            "title": "Some Title",
            "about": "About friend1",
        }
    return None


def test_display_friend_invalid(monkeypatch, capsys):
    def mock_friends(username):
        return [("friend1",), ("friend2",)]

    monkeypatch.setattr("main.list_of_friends", mock_friends)

    def mock_get_profile(username):
        if username == "friend1":
            return {
                "user": "friend1",
                "university": "Some University",
                "major": "Some Major",
                "title": "Some Title",
                "about": "About friend1",
            }
        return None

    monkeypatch.setattr("main.get_profile", mock_get_profile)

    input_values = ["x", "n", "n"]
    monkeypatch.setattr("builtins.input", lambda x: input_values.pop(0))
    display_friend_profile("test")

    captured = capsys.readouterr()
    assert "Character not identified" in captured.out
    monkeypatch.setattr("main.display_friend_profile", Mock())


"///////////////////////   Epic #6   //////////////////////////////////////////////"


def mock_signup_helper(prompt):
    if "Enter your username: " in prompt:
        return "mockuser"
    elif "Enter your password: " in prompt:
        return "ValidPass1!"
    elif "Please insert your first name: " in prompt:
        return "Test"
    elif "Please insert your last name: " in prompt:
        return "User"
    elif "Would you like to upgrade your account? (Y / N): " in prompt:
        return "N"


# Tests to check that the system can support up to ten job listings are in lines 450 to 578
# as they were tested during Epic #2 but has been modified to test support from five job listings
# to ten job listings


def mock_job_delete_success(prompt):
    # Mock input for a user deleting a job posting
    if "Would you like to delete a job? y/n: " in prompt:
        return "y"
    if "Please enter the job title you want to delete: " in prompt:
        return "a"
    if "Do you want to go back (Y / N)? " in prompt:
        return "N"


def test_job_delete_success(monkeypatch, capsys):
    # Creatjng a job listing for the test
    create_job(
        title="a",
        description="b",
        employer="c",
        location="d",
        salary="e",
        first="Test",
        last="User",
    )

    # Mock user input for job_delete function
    monkeypatch.setattr("builtins.input", mock_job_delete_success)

    # Call the job_delete function
    job_delete("testuser")

    # Capture the printed output
    captured = capsys.readouterr()

    # Assert that the job listing the user has chosen is deleted
    assert "Here are the jobs you posted that you can delete:\n" in captured.out
    assert "1 - a" in captured.out
    assert "Job deleted successfully!" in captured.out


def mock_job_delete_notification(prompt):
    # Mock input to test for job deleted notification
    if "Would you like to delete a job? y/n: " in prompt:
        return "y"

    elif "Please enter the job title you want to delete: " in prompt:
        return "a"

    elif "Do you want to go back (Y / N)? " in prompt:
        return "n"


def mock_job_creation_V2(prompt):
    if "Please enter the job's title: " in prompt:
        return "a"
    elif "Please enter the job's description: " in prompt:
        return "b"
    elif "Please enter the job's employer: " in prompt:
        return "c"
    elif "Please enter the job's location: " in prompt:
        return "d"
    elif "Please enter the job's salary: " in prompt:
        return "e"
    elif "Choose one of ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']: " in prompt:
        return "i"

    elif "Do you want to log out (Y / N)? " in prompt:
        return "Y"


def test_job_delete_notification(monkeypatch, capsys):
    # Creating a job listing, job application, and deleted created job listing for the test

    create_user("test", "pwd123", "f", "g", "Test U", "CS", 0, 0)

    # Mock user input for create_job function
    monkeypatch.setattr("builtins.input", mock_job_creation_V2)

    job_posting("test")

    create_application(
        username="testuser",
        job_title="a",
        graduation="b",
        start="c",
        description="d",
    )

    # Mock user input for delete job function
    monkeypatch.setattr("builtins.input", mock_job_delete_notification)

    job_delete("test")

    # Mock user input for exiting choose feature function
    monkeypatch.setattr("builtins.input", mock_quit_from_network_input_V1)

    # Call the job_delete function
    choose_features("testuser")

    # Capture the printed output
    captured = capsys.readouterr()

    # Assert that the job listing the user has chosen is deleted
    assert "A job you applied for, a, has been deleted" in captured.out

    delete_user("test")
    delete_application(username="testuser", job_title="a")


# Testing that the job_search function can now be called from the top level menu is tested
# in lines 180 to 198 as it was tested in Epic #1 but was modified to add this feature choice


def mock_job_options(prompt):
    # Mocks input for job options and viewing features
    if "Choose one of ['a', 'b', 'c', 'd', 'e', 'f']:" in prompt:
        return "f"
    if "Do you want to go back (Y / N)? " in prompt:
        return "N"


def test_job_options(monkeypatch, capsys):
    # Mock user input for testing job_search feature
    monkeypatch.setattr("builtins.input", mock_job_options)

    # Call the job_search function
    job_search("testuser")

    # Capture the printed output
    captured = capsys.readouterr()

    # Assert that the options avaliable to the user when job searching
    assert "a. Post a job" in captured.out
    assert "b. Apply for a Job" in captured.out
    assert "c. View Jobs" in captured.out
    assert "d. Delete a job" in captured.out
    assert "e. Save/unsave a job for later" in captured.out
    assert "f. Go back" in captured.out


def test_view_jobs_options(monkeypatch, capsys):
    # Mock user input for testing job_listing feature
    monkeypatch.setattr("builtins.input", mock_job_options)

    # Call the job_listing function
    job_listing("testuser")

    # Capture the printed output
    captured = capsys.readouterr()

    # Asserts the options avaliable to the user when viewing jobs
    assert "a. List all jobs available" in captured.out
    assert "b. List only applied jobs" in captured.out
    assert "c. List only not applied jobs" in captured.out
    assert "d. List only saved jobs" in captured.out
    assert "e. List only unsaved jobs" in captured.out
    assert "f. Go back" in captured.out


def mock_view_all_jobs(prompt):
    # Mocks input for a user that doesn't want to apply for any of jobs in the system
    # while allows showing that it allows the user to apply for one on the system
    if "Do you want to apply to any of the jobs on this list? y/n?: " in prompt:
        return "n"
    if "Do you want to go back (Y / N)? " in prompt:
        return "N"


def test_view_all_jobs(monkeypatch, capsys):
    # Creatjng job listings and a test application for the test
    create_job(
        title="a",
        description="b",
        employer="c",
        location="d",
        salary="e",
        first="f",
        last="g",
    )
    create_job(
        title="b",
        description="b",
        employer="c",
        location="d",
        salary="e",
        first="f",
        last="g",
    )
    create_job(
        title="c",
        description="b",
        employer="c",
        location="d",
        salary="e",
        first="f",
        last="g",
    )

    create_application(
        username="testuser",
        job_title="c",
        graduation="b",
        start="c",
        description="d",
    )

    # Mock user input for testing list_all_jobs and job_select feature
    monkeypatch.setattr("builtins.input", mock_view_all_jobs)

    # Call the list_all_jobs function
    list_all_jobs("testuser")

    # Capture the printed output
    captured = capsys.readouterr()

    print("Captured Output:", captured.out)

    # Asserts that the system displays all of the avaliable jobs in the system and as well as
    # jobs in the system that they already applied for
    assert "\nHere are all jobs available:\n" in captured.out
    assert "[] a" in captured.out
    assert "[] b" in captured.out
    assert "[Applied] c" in captured.out

    # Call the job_select function
    job_select("testuser")

    # Capture the printed output
    captured = capsys.readouterr()

    print("Captured Output:", captured.out)

    # Asserts that the system displays all of the avaliable jobs in the system and as well as
    # jobs in the system that they already applied for on the job_select function as it also
    # by default lists all of the jobs in the system
    assert "\nHere are all jobs available:\n" in captured.out
    assert "[] a" in captured.out
    assert "[] b" in captured.out
    assert "[Applied] c" in captured.out

    # Calling delete_job functions for test clean up
    delete_job("a")
    clean_saved_jobs_when_job_deleted("a")
    delete_job("b")
    clean_saved_jobs_when_job_deleted("b")
    delete_job("c")
    clean_saved_jobs_when_job_deleted("c")

    delete_user("testuser")
    delete_application("testuser", "c")


def mock_job_information(prompt):
    # Mocks input for a user looking up the job they want to apply for and declining to apply
    if "\nEnter the title of the job you want to apply for: " in prompt:
        return "a"
    if "Confirm this job and send the application? y/n?: " in prompt:
        return "n"
    if "Do you want to go back (Y / N)? " in prompt:
        return "N"


def test_job_information(monkeypatch, capsys):
    # Creatjng job listing for the test
    create_job(
        title="a",
        description="b",
        employer="c",
        location="d",
        salary="e",
        first="f",
        last="g",
    )

    # Mock user input for testing apply_for_job feature
    monkeypatch.setattr("builtins.input", mock_job_information)

    # Call the apply_for_job function
    apply_for_job("testuser")

    # Capture the printed output
    captured = capsys.readouterr()

    # Asserts that the system displays the job information for job they are considering to apply for
    assert "\nThis is the current job information for this title:" in captured.out
    assert "\nTitle: a" in captured.out
    assert "Description: b" in captured.out
    assert "Employer: c" in captured.out
    assert "Location: d" in captured.out
    assert "Salary: e" in captured.out

    # Calling delete_job functions for test clean up
    delete_job("a")
    clean_saved_jobs_when_job_deleted("a")


def mock_job_application_success(prompt):
    # Mocks input for a user looking up the job they want to apply for and applying for it
    if "\nEnter the title of the job you want to apply for: " in prompt:
        return "a"
    if "Confirm this job and send the application? y/n?: " in prompt:
        return "y"
    if "Please enter your predicted graduation date(mm/dd/yyyy): " in prompt:
        return "01/01/1990"
    if "Please enter your predicted start date(mm/dd/yyyy): " in prompt:
        return "01/02/1990"
    if "Please explain why you'd be a great fit for this job: " in prompt:
        return "I think I would be a great candidate"
    if "Choose one of ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']: " in prompt:
        return "i"
    if "Do you want to log out (Y / N)? " in prompt:
        return "Y"


def mock_job_application_fail(prompt):
    # Mocks input for a user looking up the job but failing to apply for the job
    if "\nEnter the title of the job you want to apply for: " in prompt:
        return "a"
    if "Confirm this job and send the application? y/n?: " in prompt:
        return "y"
    if "Choose one of ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']: " in prompt:
        return "i"
    if "Do you want to log out (Y / N)? " in prompt:
        return "Y"


def test_job_application_success(monkeypatch, capsys):
    create_user("testuser", "ValidPass1!", "Mock", "User", "USF", "CS", 0, 0)

    # Creatjng job listing for the test
    create_job(
        title="a",
        description="b",
        employer="c",
        location="d",
        salary="e",
        first="f",
        last="g",
    )

    # Mock user input for testing apply_for_job feature
    monkeypatch.setattr("builtins.input", mock_job_application_success)

    # Call the apply_for_job function
    apply_for_job("testuser")

    # Capture the printed output
    captured = capsys.readouterr()

    print("Captured Output:", captured.out)

    # Asserts that the user has successfully sent their application
    assert (
        "Application sent. We wish you luck on obtaining the position!\n"
        in captured.out
    )

    # Calling delete_job functions for test clean up
    delete_job("a")
    clean_saved_jobs_when_job_deleted("a")
    delete_application("testuser", "a")
    delete_user("testuser")

    print("Captured Output:", captured.out)


def test_job_application_fail_V1(monkeypatch, capsys):
    create_user("testuser", "ValidPass1!", "Mock", "User", "USF", "CS", 0, 0)

    # Creatjng job listing and application for the test
    create_job(
        title="a",
        description="b",
        employer="c",
        location="d",
        salary="e",
        first="f",
        last="g",
    )

    create_application(
        username="testuser",
        job_title="a",
        graduation="b",
        start="c",
        description="d",
    )
    # Mock user input for testing apply_for_job feature
    monkeypatch.setattr("builtins.input", mock_job_application_fail)

    # Call the apply_for_job function
    apply_for_job("testuser")

    # Capture the printed output
    captured = capsys.readouterr()

    # Asserts that the user can't reapply for a job they already sent an application for
    assert (
        "\nYou have already applied to this job, and cannot resend an application."
        in captured.out
    )

    # Calling delete_job functions for test clean up
    delete_job("a")
    clean_saved_jobs_when_job_deleted("a")
    delete_application("testuser", "a")
    delete_user("testuser")


def test_job_application_fail_V2(monkeypatch, capsys):
    # Creatjng job listing for the test
    create_job(
        title="a",
        description="b",
        employer="c",
        location="d",
        salary="e",
        first="Test",
        last="User",
    )

    monkeypatch.setattr("builtins.input", mock_signup_helper)

    # Call the signup function
    signup()

    # Mock user input for testing apply_for_job feature
    monkeypatch.setattr("builtins.input", mock_job_application_fail)

    # Call the apply_for_job function
    apply_for_job("mockuser")

    # Capture the printed output
    captured = capsys.readouterr()

    # Asserts that the user can't apply for job they posted
    assert "\nYou can't hire yourself for a job you posted!" in captured.out

    # Calling delete_job functions for test clean up
    delete_job("a")
    clean_saved_jobs_when_job_deleted("a")
    assert delete_user("mockuser") is True
    delete_application("mockuser", "a")


def mock_display_applied_jobs(prompt):
    # Mocks input for a user displaying list of applied jobs
    if "Do you want to go back (Y / N)? " in prompt:
        return "N"


def test_display_applied_jobs(monkeypatch, capsys):
    # Creatjng job listings and a test application for the test
    create_job(
        title="a",
        description="b",
        employer="c",
        location="d",
        salary="e",
        first="f",
        last="g",
    )

    create_application(
        username="testuser",
        job_title="a",
        graduation="b",
        start="c",
        description="d",
    )

    # Mock user input for testing list_applied_jobs
    monkeypatch.setattr("builtins.input", mock_display_applied_jobs)

    # Call the list_applied_jobs function
    list_applied_jobs("testuser")

    # Capture the printed output
    captured = capsys.readouterr()

    print("Captured Output:", captured.out)

    # Asserts that the system displays all of the applied jobs in the system
    assert "\nListing all jobs you've applied for:\n" in captured.out
    assert "[Applied] a" in captured.out

    delete_job("a")
    clean_saved_jobs_when_job_deleted("a")
    delete_application("testuser", "a")
    delete_user("testuser")


def test_display_not_applied_jobs(monkeypatch, capsys):
    # Creatjng job listings for the test
    create_job(
        title="e",
        description="b",
        employer="c",
        location="d",
        salary="e",
        first="f",
        last="g",
    )

    # Mock user input for testing list_unapplied_jobs
    monkeypatch.setattr("builtins.input", mock_view_all_jobs)

    # Call the list_unapplied_jobs function
    list_unapplied_jobs("testuser")

    # Capture the printed output
    captured = capsys.readouterr()

    # Asserts that the system displays all of the unapplied jobs in the system
    assert "\nListing all jobs you have NOT applied for:\n" in captured.out
    assert "[] e" in captured.out

    delete_job("e")
    clean_saved_jobs_when_job_deleted("e")


def mock_save_unsave_jobs(prompt):
    # Mocks input for a user saving and unsaving jobs
    if "Would you like to save a job? y/n: " in prompt:
        return "y"
    if "Please enter the job title you want to save: " in prompt:
        return "f"
    if "\nWould you like to unsave a job? y/n: " in prompt:
        return "y"
    if "Please enter the job title you want to unsave: " in prompt:
        return "f"
    if "Do you want to go back (Y / N)? " in prompt:
        return "N"


def test_save_unsave_jobs(monkeypatch, capsys):
    # Creatjng job listings for the test
    create_job(
        title="f",
        description="b",
        employer="c",
        location="d",
        salary="e",
        first="f",
        last="g",
    )

    # Mock user input for testing save_job
    monkeypatch.setattr("builtins.input", mock_save_unsave_jobs)

    # Call the save_job function
    save_job("testuser")

    # Capture the printed output
    captured = capsys.readouterr()

    # Asserts that the system saves and unsaves jobs in the system
    assert "1 - f" in captured.out
    assert "Job saved successfully!" in captured.out
    assert "Job unsaved successfully!" in captured.out

    delete_job("f")
    clean_saved_jobs_when_job_deleted("f")


def test_display_saved_jobs(monkeypatch, capsys):
    # Creatjng saved job  for the test
    save_job_for_user(username="testuser", saved_job_title="g")

    # Mock user input for testing show_saved_jobs and job_select feature
    monkeypatch.setattr("builtins.input", mock_display_applied_jobs)

    # Call the show_saved_jobs function
    show_saved_jobs("testuser")

    # Capture the printed output
    captured = capsys.readouterr()

    # Asserts that the system displays all of the saved jobs in the system
    assert "Here are the jobs you saved for later:\n" in captured.out
    assert "1 - g" in captured.out

    delete_job("g")
    clean_saved_jobs_when_job_deleted("g")


def test_display_unsaved_jobs(monkeypatch, capsys):
    # Creatjng job listings for the test
    create_job(
        title="h",
        description="b",
        employer="c",
        location="d",
        salary="e",
        first="f",
        last="g",
    )

    # Mock user input for testing show_unsaved_jobs and job_select feature
    monkeypatch.setattr("builtins.input", mock_display_applied_jobs)

    # Call the show_unsaved_jobs function
    show_unsaved_jobs("testuser")

    # Capture the printed output
    captured = capsys.readouterr()

    print("Captured Output:", captured.out)

    # Asserts that the system displays all of the unsaved jobs in the system
    assert "Here are the jobs you have not saved for later:\n" in captured.out
    assert "1 - h" in captured.out

    delete_job("h")
    clean_saved_jobs_when_job_deleted("h")


def mock_display_applied_saved_jobs(prompt):
    # Mocks input for a user displaying list of applied and unsaved jobs after logging out
    if "Do you want to log out (Y / N)? " in prompt:
        return "y"


def test_display_applied_saved_jobs(monkeypatch, capsys):
    # Creatjng job listings, a test application, and saved job for the test
    create_job(
        title="i",
        description="b",
        employer="c",
        location="d",
        salary="e",
        first="f",
        last="g",
    )

    create_job(
        title="j",
        description="b",
        employer="c",
        location="d",
        salary="e",
        first="f",
        last="g",
    )

    create_application(
        username="testuser",
        job_title="i",
        graduation="b",
        start="c",
        description="d",
    )

    save_job_for_user(username="testuser", saved_job_title="j")

    # Mock user input for testing logout
    monkeypatch.setattr("builtins.input", mock_display_applied_saved_jobs)

    # Call the logout function
    return_stm = logout("testuser")

    # Asserts that the system logs user out
    assert return_stm == 0

    # Mock user input for testing list_applied_jobs
    monkeypatch.setattr("builtins.input", mock_display_applied_jobs)

    # Call the list_applied_jobs function
    list_applied_jobs("testuser")

    # Capture the printed output
    captured = capsys.readouterr()

    assert "\nListing all jobs you've applied for:\n" in captured.out
    assert "[Applied] i" in captured.out

    # Mock user input for testing show_saved_jobs
    monkeypatch.setattr("builtins.input", mock_display_applied_jobs)

    # Call the show_saved_jobs function
    show_saved_jobs("testuser")

    # Capture the printed output
    captured = capsys.readouterr()

    assert "Here are the jobs you saved for later:\n" in captured.out
    assert "1 - j" in captured.out

    delete_job("i")
    clean_saved_jobs_when_job_deleted("i")
    delete_job("j")
    clean_saved_jobs_when_job_deleted("j")


"-----------------------------EPIC 7 Tests------------------------------------------"


def mock_test_signup_premium_tier_helper(prompt):
    if "Enter your username: " in prompt:
        return "mockuser"
    elif "Enter your password: " in prompt:
        return "ValidPass1!"
    elif "Please insert your first name: " in prompt:
        return "Mock"
    elif "Please insert your last name: " in prompt:
        return "User"
    elif "Please insert the university you are attending: " in prompt:
        return "University of South Florida"
    elif "Please insert your major: " in prompt:
        return "Computer Science"
    elif "Would you like to upgrade your account? (Y / N): " in prompt:
        return "Y"


def test_signup_premium_tier(monkeypatch, capsys):
    """Mock signup function to test if user is given tier options"""
    monkeypatch.setattr("builtins.input", mock_test_signup_premium_tier_helper)
    signup()

    # Capture the printed output
    captured = capsys.readouterr()

    # Assert that the expected message is printed
    assert (
        "\nHere at Incollege, we offer the ability for accounts to be upgraded to plus tier. For $10 a month, you can message and contact all users on this site without them being on your friend's list.\n"
        in captured.out
    )
    assert "\nYou have upgraded your account to plus tier. Thank you!\n" in captured.out

    assert delete_user("mockuser") is True


def mock_test_signup_free_tier_helper(prompt):
    if "Enter your username: " in prompt:
        return "mockuser"
    elif "Enter your password: " in prompt:
        return "ValidPass1!"
    elif "Please insert your first name: " in prompt:
        return "Mock"
    elif "Please insert your last name: " in prompt:
        return "User"
    elif "Please insert the university you are attending: " in prompt:
        return "University of South Florida"
    elif "Please insert your major: " in prompt:
        return "Computer Science"
    elif "Would you like to upgrade your account? (Y / N): " in prompt:
        return "N"


def test_signup_free_tier(monkeypatch, capsys):
    """Mock signup function to test if user is given tier options"""
    monkeypatch.setattr("builtins.input", mock_test_signup_free_tier_helper)
    signup()

    # Capture the printed output
    captured = capsys.readouterr()

    # Assert that the expected message is printed
    assert (
        "\nHere at Incollege, we offer the ability for accounts to be upgraded to plus tier. For $10 a month, you can message and contact all users on this site without them being on your friend's list.\n"
        in captured.out
    )
    assert "\nYou have chosen to stay as a standard user. Thank you!\n" in captured.out

    assert delete_user("mockuser") is True


def mock_test_free_tier_messaging_with_no_friends(prompt):
    if (
        "\nWould you like to list your friends before choosing a recepient?(y/n): "
        in prompt
    ):
        return "y"
    elif "Please enter the username of who you wish to send a message to: " in prompt:
        return "mockuser2"
    elif "Enter your message: " in prompt:
        return "Hello!"
    elif "\nAre you sure you want to send this message to mockuser2? (y/n): " in prompt:
        return "y"


def test_free_tier_messaging_with_no_friends(monkeypatch, capsys):
    create_user("mockuser", "ValidPass1!", "Mock", "User", "USF", "CS", 0, 0)
    create_user("mockuser2", "ValidPass1!", "Mock", "User", "USF", "CS", 0, 0)

    monkeypatch.setattr("builtins.input", mock_test_free_tier_messaging_with_no_friends)
    monkeypatch.setattr("main.choose_features", Mock())
    standard_messenger("mockuser")

    # Capture the printed output
    captured = capsys.readouterr()

    assert (
        "\nYou have no friends! Please be aware that you can't message anyone as a standard user if you have no friends.\n"
        in captured.out
    )
    assert "\nI'm sorry, you are not friends with that person.\n" in captured.out

    assert delete_user("mockuser") is True
    assert delete_user("mockuser2") is True


def mock_test_messaging_non_existing_user(prompt):
    if (
        "\nWould you like to list your friends before choosing a recepient?(y/n): "
        in prompt
    ):
        return "y"
    elif "Please enter the username of who you wish to send a message to: " in prompt:
        return "mockuser2"


def test_messaging_non_existing_user(monkeypatch, capsys):
    create_user("mockuser", "ValidPass1!", "Mock", "User", "USF", "CS", 0, 0)

    monkeypatch.setattr("builtins.input", mock_test_messaging_non_existing_user)
    monkeypatch.setattr("main.choose_features", Mock())
    standard_messenger("mockuser")

    # Capture the printed output
    captured = capsys.readouterr()

    assert "The user doesn't exist, please try again" in captured.out

    assert delete_user("mockuser") is True


def mock_test_generate_friend_list(prompt):
    if (
        "\nWould you like to list your friends before choosing a recepient?(y/n): "
        in prompt
    ):
        return "y"
    if "Please enter the username of who you wish to send a message to: " in prompt:
        return "non_existing_user"


def test_generate_friend_list(monkeypatch, capsys):
    create_user("mockuser", "ValidPass1!", "Mock", "User", "USF", "CS", 0, 0)
    create_user("mockuser2", "ValidPass1!", "Mock", "User", "USF", "CS", 0, 0)
    add_to_friend_list("mockuser", "mockuser2")

    monkeypatch.setattr("builtins.input", mock_test_generate_friend_list)
    monkeypatch.setattr("main.choose_features", Mock())
    standard_messenger("mockuser")

    # Capture the printed output
    captured = capsys.readouterr()

    assert "\nHere's a list of your friends: \n" in captured.out
    assert "mockuser2" in captured.out

    assert delete_user("mockuser") is True
    assert delete_user("mockuser2") is True
    assert delete_friend_from_list("mockuser", "mockuser2") is True


def test_free_tier_messaging_with_friends(monkeypatch, capsys):
    create_user("mockuser", "ValidPass1!", "Mock", "User", "USF", "CS", 0, 0)
    create_user("mockuser2", "ValidPass1!", "Mock", "User", "USF", "CS", 0, 0)
    add_to_friend_list("mockuser", "mockuser2")

    monkeypatch.setattr("builtins.input", mock_test_free_tier_messaging_with_no_friends)
    monkeypatch.setattr("main.choose_features", Mock())
    standard_messenger("mockuser")

    # Capture the printed output
    captured = capsys.readouterr()
    assert "\nMessage sent!\n" in captured.out

    assert delete_user("mockuser") is True
    assert delete_user("mockuser2") is True
    assert delete_friend_from_list("mockuser", "mockuser2") is True
    assert remove_message("mockuser", "mockuser2", "Hello!") is True


def test_new_message_notification(monkeypatch, capsys):
    create_user("mockuser", "ValidPass1!", "Mock", "User", "USF", "CS", 0, 0)
    create_user("mockuser2", "ValidPass1!", "Mock", "User", "USF", "CS", 0, 0)
    create_new_message("Hello!", "mockuser", "mockuser2")
    create_message("Hello!", "mockuser", "mockuser2")

    new_message_check("mockuser2")

    # Capture the printed output
    captured = capsys.readouterr()
    assert "You have messages waiting for you!\n" in captured.out

    assert delete_user("mockuser") is True
    assert delete_user("mockuser2") is True
    assert remove_message("mockuser", "mockuser2", "Hello!") is True


def test_empty_inbox(monkeypatch, capsys):
    create_user("mockuser", "ValidPass1!", "Mock", "User", "USF", "CS", 0, 0)

    monkeypatch.setattr("main.choose_features", Mock())
    inbox("mockuser")

    # Capture the printed output
    captured = capsys.readouterr()
    assert "Your inbox is empty" in captured.out

    assert delete_user("mockuser") is True


def mock_test_non_empty_inbox(prompt):
    if "\nChoose one of ['a', 'b', 'c']:" in prompt:
        return "c"
    elif "Do you want to go back (Y / N)? " in prompt:
        return "Y"


def test_non_empty_inbox(monkeypatch, capsys):
    create_user("mockuser", "ValidPass1!", "Mock", "User", "USF", "CS", 0, 0)
    create_user("mockuser2", "ValidPass1!", "Mock", "User", "USF", "CS", 0, 0)
    create_message("Hello!", "mockuser", "mockuser2")

    monkeypatch.setattr("builtins.input", mock_test_non_empty_inbox)
    monkeypatch.setattr("main.choose_features", Mock())

    inbox("mockuser2")

    # Capture the printed output
    captured = capsys.readouterr()
    assert "You have messages: \n" in captured.out
    assert "From mockuser: Hello!\n" in captured.out
    assert "\nWhat would you like to do with these messages?" in captured.out
    assert "a. Reply" in captured.out
    assert "b. Delete" in captured.out
    assert "c. Go Back" in captured.out

    assert delete_user("mockuser") is True
    assert delete_user("mockuser2") is True
    assert remove_message("mockuser", "mockuser2", "Hello!") is True


def mock_test_reply_message_standard(prompt):
    if "\nPlease enter the name of the user you wish to reply to: " in prompt:
        return "mockuser"
    if "\nPlease enter your reply: " in prompt:
        return "Hello! How are you?"
    if "\nAre you sure you want to send this message to mockuser? (y/n): " in prompt:
        return "Y"
    if "Choose one of" in prompt:
        return "i"
    if "Do you want to log out (Y / N)? " in prompt:
        return "y"


def mock_test_reply_message_plus(prompt):
    if "\nPlease enter the name of the user you wish to reply to: " in prompt:
        return "mockuser2"
    if "\nPlease enter your reply: " in prompt:
        return "Hello! How are you?"
    if "\nAre you sure you want to send this message to mockuser2? (y/n): " in prompt:
        return "Y"
    if "Choose one of" in prompt:
        return "i"
    if "Do you want to log out (Y / N)? " in prompt:
        return "y"


def test_reply_message_standard(monkeypatch, capsys):
    create_user("mockuser", "ValidPass1!", "Mock", "User", "USF", "CS", 0, 0)
    create_user("mockuser2", "ValidPass1!", "Mock", "User", "USF", "CS", 0, 0)
    create_message("Hello!", "mockuser", "mockuser2")

    monkeypatch.setattr("builtins.input", mock_test_reply_message_standard)
    reply_message("mockuser2")

    # Capture the printed output
    captured = capsys.readouterr()
    assert "\nMessage sent!\n" in captured.out

    assert delete_user("mockuser") is True
    assert delete_user("mockuser2") is True
    assert remove_message("mockuser", "mockuser2", "Hello!") is True
    assert remove_message("mockuser2", "mockuser", "Hello! How are you?") is True


def test_reply_message_plus(monkeypatch, capsys):
    create_user("mockuser", "ValidPass1!", "Mock", "User", "USF", "CS", 1, 0)
    create_user("mockuser2", "ValidPass1!", "Mock", "User", "USF", "CS", 0, 0)
    create_message("Hello!", "mockuser2", "mockuser")

    monkeypatch.setattr("builtins.input", mock_test_reply_message_plus)
    reply_message("mockuser")

    # Capture the printed output
    captured = capsys.readouterr()
    assert "\nMessage sent!\n" in captured.out

    assert delete_user("mockuser") is True
    assert delete_user("mockuser2") is True
    assert remove_message("mockuser", "mockuser2", "Hello!") is True
    assert remove_message("mockuser2", "mockuser", "Hello! How are you?") is True


def mock_test_plus_messenger(prompt):
    if (
        "\nWould you like to list all users in the system before choosing a recepient?(y/n): "
        in prompt
    ):
        return "y"
    if "Please enter the username of who you wish to send a message to: " in prompt:
        return "mockuser2"
    if "Enter your message: " in prompt:
        return "Hello! How are you?"
    if "\nAre you sure you want to send this message to mockuser2? (y/n): " in prompt:
        return "Y"
    if "Choose one of" in prompt:
        return "i"
    if "Do you want to log out (Y / N)? " in prompt:
        return "y"


def test_plus_messenger(monkeypatch, capsys):
    create_user("mockuser", "ValidPass1!", "Mock", "User", "USF", "CS", 1, 0)
    create_user("mockuser2", "ValidPass1!", "Mock", "User", "USF", "CS", 0, 0)
    create_user("mockuser3", "ValidPass1!", "Mock", "User", "USF", "CS", 0, 0)

    # create_message("Hello!", "mockuser", "mockuser")

    monkeypatch.setattr("builtins.input", mock_test_plus_messenger)
    plus_messenger("mockuser")

    # Capture the printed output
    captured = capsys.readouterr()
    assert "\nHere's a list of every user in the system:\n" in captured.out
    assert "mockuser2" in captured.out
    assert "mockuser3" in captured.out
    assert "\nMessage sent!\n" in captured.out

    assert delete_user("mockuser") is True
    assert delete_user("mockuser2") is True
    assert delete_user("mockuser3") is True
    assert remove_message("mockuser", "mockuser2", "Hello! How are you?") is True


########### EPIC #8 ###########################################################


# Mocks quiting the program if network has no friends
def mock_quit_from_jobs_input_V1(prompt):
    if "Choose one of ['a', 'b', 'c', 'd', 'e', 'f']:" in prompt:
        return "f"

    if "Do you want to go back (Y / N)? " in prompt:
        return "N"


# Function that test if a message warns the user to apply for jobs if they haven't applied in 7 days


# Please keep in mind that 7 days is too long for testing, so days means "log-ins" for this circumstance to allow for testing.
def test_7_day_application_delay(monkeypatch, capsys):
    create_user("mockuser9", "ValidPass1!", "Mock", "User", "USF", "CS", 0, 0)

    # Use monkeypatch to constantly log out the user
    monkeypatch.setattr("builtins.input", mock_quit_from_network_input_V1)

    # Log in and out multiple times
    for _ in range(8):
        choose_features("mockuser9")

    # Capture the printed output
    captured = capsys.readouterr()

    # Print the entire captured output for inspection
    print("Captured Output:", captured.out)

    # Now you can assert for the presence of the specific line
    assert (
        "Remember - you're going to want to have a job when you graduate. Make sure that you start to apply for jobs today!"
        in captured.out
    )

    delete_user("mockuser9")


# Function that test to make sure the warning doesn't go off if less than 7 log outs: an edge case.


# Please keep in mind that 7 days is too long for testing, so days means "log-ins" for this circumstance to allow for testing.
def test_6_day_application_delay(monkeypatch, capsys):
    create_user("mockuser9", "ValidPass1!", "Mock", "User", "USF", "CS", 0, 0)

    # Use monkeypatch to constantly log out the user
    monkeypatch.setattr("builtins.input", mock_quit_from_network_input_V1)

    # Log in and out multiple times
    for _ in range(7):
        choose_features("mockuser9")

    # Capture the printed output
    captured = capsys.readouterr()

    # Print the entire captured output for inspection
    print("Captured Output:", captured.out)

    # Now you can assert for the presence of the specific line
    assert (
        "Remember - you're going to want to have a job when you graduate. Make sure that you start to apply for jobs today!"
        not in captured.out
    )

    delete_user("mockuser9")


# Test to see if notification will show for user who hasn't made profile
def test_profile_notification(monkeypatch, capsys):
    create_user("mockuser7", "ValidPass1!", "Mock", "User", "USF", "CS", 0, 0)

    # Use monkeypatch to constantly log out the user
    monkeypatch.setattr("builtins.input", mock_quit_from_network_input_V1)

    # Log in and out multiple times

    choose_features("mockuser7")

    # Capture the printed output
    captured = capsys.readouterr()

    # Print the entire captured output for inspection
    print("Captured Output:", captured.out)

    # Now you can assert for the presence of the specific line
    assert "Don't forget to create a profile!" in captured.out

    delete_user("mockuser7")


# Test to see if notificantion doesn't show if profile is made.
def test_no_profile_notification(monkeypatch, capsys):
    create_user("testuser", "ValidPass1!", "Mock", "User", "USF", "CS", 0, 0)

    # Mock user input for create_user_profile function
    monkeypatch.setattr("builtins.input", mock_update_user_profile)

    # Call the create_user_profile function
    create_profile(
        "testuser", "University of South Florida", "Computer Science", "", ""
    )
    create_education("testuser", "University of South Florida", "", 3)
    create_experience(
        "testuser",
        1,
        "Intern",
        "Boeing",
        "October 1st, 2020",
        "December 30th, 2021",
        "New York",
        "Worked at Boeing as an intern to write a blog for their website",
    )

    # Call the create_user_profile function
    create_user_profile("testuser")

    # Capture the printed output
    captured = capsys.readouterr()

    # Assert that the messages where the profile is sucessfully updated and
    # updates and fills in the remaining sections that the student wanted to add
    assert "Profile updated!" in captured.out
    assert "Education updated!" in captured.out
    assert "Experience updated!" in captured.out
    assert "Username:  testuser" in captured.out
    assert "Title:  1st Year Business Student" in captured.out
    assert (
        "About Me:  I am a first year business student that is looking for a job!"
        in captured.out
    )
    assert "University:  University Of South Florida" in captured.out
    assert "Major:  Business" in captured.out
    assert "Degree:  Bachelors" in captured.out
    assert "Years Attended:  1" in captured.out

    user_profile = get_profile("testuser")
    for i, experience in enumerate(user_profile["experience"]):
        title = experience["title"]
        employer = experience["employer"]
        location = experience["location"]
        start_date = experience["date_started"]
        end_date = experience["date_ended"]
        description = experience["description"]

    assert title == "Intern"
    assert employer == "Boeing"
    assert location == "New York"
    assert start_date == "October 1st, 2020"
    assert end_date == "December 30th, 2021"
    assert (
        description == "Worked at Boeing as an intern to write a blog for their website"
    )

    # Clean up test user profile

    create_user("testuser", "ValidPass1!", "Mock", "User", "USF", "CS", 0, 0)

    # Use monkeypatch to constantly log out the user
    monkeypatch.setattr("builtins.input", mock_quit_from_network_input_V1)

    # Log in and out multiple times

    choose_features("testuser")

    # Capture the printed output
    captured = capsys.readouterr()

    # Print the entire captured output for inspection
    print("Captured Output:", captured.out)

    # Now you can assert for the presence of the specific line
    assert "Don't forget to create a profile!" not in captured.out

    delete_user("testuser")
    delete_profile("testuser")
    delete_education("testuser")
    delete_experience("testuser")


# Test to see if the user is notified of any new messages sent.
def test_message_notification(monkeypatch, capsys):
    create_user("mockuser", "ValidPass1!", "Mock", "User", "USF", "CS", 0, 0)
    create_user("mockuser2", "ValidPass1!", "Mock", "User", "USF", "CS", 0, 0)
    create_new_message("Hello!", "mockuser", "mockuser2")
    create_message("Hello!", "mockuser", "mockuser2")

    # Use monkeypatch to constantly log out the user
    monkeypatch.setattr("builtins.input", mock_quit_from_network_input_V1)

    choose_features("mockuser2")

    # Capture the printed output
    captured = capsys.readouterr()
    assert "You have messages waiting for you!\n" in captured.out

    assert delete_user("mockuser") is True
    assert delete_user("mockuser2") is True
    assert remove_message("mockuser", "mockuser2", "Hello!") is True


def test_no_applications_notification(monkeypatch, capsys):
    create_user("mockuser15", "ValidPass1!", "Mock", "User", "USF", "CS", 0, 0)

    # Use monkeypatch to constantly log out the user
    monkeypatch.setattr("builtins.input", mock_quit_from_jobs_input_V1)

    job_search("mockuser15")

    # Capture the printed output
    captured = capsys.readouterr()

    # Assert that the no applications notification triggered sucessfully.

    assert "You have not applied for any jobs yet" in captured.out

    delete_user("mockuser15")


def test_num_applications_notification(monkeypatch, capsys):
    create_user("test", "pwd123", "f", "g", "Test U", "CS", 0, 0)
    create_user("testuser5", "pwd123", "f", "g", "Test U", "CS", 0, 0)

    # Mock user input for create_job function
    monkeypatch.setattr("builtins.input", mock_job_creation_V2)

    job_posting("test")

    create_application(
        username="testuser5",
        job_title="a",
        graduation="b",
        start="c",
        description="d",
    )

    # Mock user input for create_job function
    monkeypatch.setattr("builtins.input", mock_quit_from_jobs_input_V1)

    # Capture the output after setting up the scenario and searching for jobs
    captured_before_search = capsys.readouterr()
    job_search("testuser5")

    # Capture the output after searching for jobs
    captured_after_search = capsys.readouterr()

    assert "You have currently applied for 1 job(s) total." in captured_after_search.out

    delete_user("test")
    delete_user("testuser5")
    delete_application("testuser5", "a")
    delete_job("a")


def test_notify_new_job(monkeypatch, capsys):
    # create a user
    create_user("job_applicant", "ValidPass1!", "Job", "Applicant", "USF", "CS", 0, 0)

    # create another user who posts a job
    create_user("job_poster", "ValidPass1!", "Job", "Poster", "USF", "CS", 0, 0)

    # post a job
    create_job(
        title="test job",
        description="test job description",
        employer="test employer",
        location="test location",
        salary="test salary",
        first="Job",
        last="Poster",
    )
    notify_new_job("job_poster", "test job")
    notifications_on_login("job_applicant")

    # Capture the printed output
    captured = capsys.readouterr()

    assert "A new job for test job has been posted" in captured.out

    # clean up
    assert delete_user("job_applicant") is True
    assert delete_user("job_poster") is True
    delete_job("test job") is True


def test_notify_deleted_applied_job(monkeypatch, capsys):
    # create a user
    create_user("job_applicant", "ValidPass1!", "Job", "Applicant", "USF", "CS", 0, 0)

    # create another user who posts a job
    create_user("job_poster", "ValidPass1!", "Job", "Poster", "USF", "CS", 0, 0)

    # post a job
    create_job(
        title="test job",
        description="test job description",
        employer="test employer",
        location="test location",
        salary="test salary",
        first="Job",
        last="Poster",
    )

    # create an application
    create_application(
        username="job_applicant",
        job_title="test job",
        graduation="May 2024",
        start="August 2024",
        description="overqualified",
    )

    delete_job("test job")
    notify_deleted_applied_job("job_poster", "test job")
    notifications_on_login("job_applicant")

    # Capture the printed output
    captured = capsys.readouterr()

    assert "A job you applied for, test job, has been deleted" in captured.out

    # clean up
    assert delete_user("job_applicant") is True
    assert delete_user("job_poster") is True
    assert delete_application("job_applicant", "test job") is True


def test_notify_new_user(monkeypatch, capsys):
    # create a user
    create_user("user1", "ValidPass1!", "Mock1", "User1", "USF", "CS", 0, 0)

    # create another user
    create_user("user2", "ValidPass1!", "Mock2", "User2", "USF", "CS", 0, 0)
    notify_new_user("user2", "Mock2", "User2")

    notifications_on_login("user1")

    # Capture the printed output
    captured = capsys.readouterr()

    assert "Mock2 User2 has joined InCollege" in captured.out
    assert get_notification("user1") == []

    # clean up
    assert delete_user("user1") is True
    assert delete_user("user2") is True
