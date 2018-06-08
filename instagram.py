from selenium import webdriver
import urllib.request
import time
import os
import re


def create_directory(input_dir: str) -> None:
    """ Function to create a new empty directory with given name,
        if it does not already exist

    Args:
        input_dir (str): The path of the new empty directory to be created
            if it does not already exist at the specified location.
    """
    try:
        if not os.path.exists(input_dir):
            os.makedirs(input_dir)
    except OSError:
        print("Error: Creating directory, " + input_dir)


def validate_username() -> str:
    """ Function to get a username input and validate it with a regular expression
        according to the constraints for instagram username """

    while True:
        # Get the username as input from the user
        username_local = input("Enter the Instagram username: ")
        match = re.search(r"^([A-Za-z0-9_](?:(?:[A-Za-z0-9_]|(?:\.(?!\.))){0,28}(?:[A-Za-z0-9_]))?)$", username_local)

        if match:
            break
        else:
            print("Please enter a valid username.\n")
    return username_local


if __name__ == "__main__":
    username = validate_username()

    # Create a directory with same name as the username
    # if it does not exist already.
    create_directory(username)

    # Create a new driver object for Google Chrome
    browser_object = webdriver.Chrome("C:\\Users\\chromedriver.exe")
    # Create the url string for the username specified
    browser_object.get("https://www.instagram.com/{}/?hl=en".format(username))

    # This is the number of seconds for which the browser will wait
    # while the page loads.
    SCROLL_PAUSE_TIME = 3
    # This variable measures the number of seconds elapsed since the initial loading.
    time_elapsed = 0

    # This set will include the urls for all the images.
    image_url_set = set()

    # After the initial loading only the first 12 images are available.
    # The rest are loaded in batches after scrolling down. So the browser is
    # scrolled after every SCROLL_PAUSE_TIME seconds, to give time for the images to load.

    # Get scroll height
    last_height = browser_object.execute_script("return document.body.scrollHeight")

    while True:
        # Get all the images which are available currently.
        image_divs = browser_object.find_elements_by_css_selector(".FFVAD")

        # For each image get the url and add it to the set,
        # thus any url previously fetched will not be present more than once.
        for image_div in image_divs:
            url = image_div.get_attribute('src')
            image_url_set.add(url)

        # Scroll down to the bottom
        browser_object.execute_script("window.scrollTo(0, document.body.scrollHeight)")

        # Wait to load the page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate the new scroll height and compare it with the last scroll height.
        new_height = browser_object.execute_script("return document.body.scrollHeight")

        # At most 100 scrolls are allowed(may be omitted) if the profile is
        # still not fully loaded.
        if (time_elapsed == 300 * SCROLL_PAUSE_TIME) or (new_height == last_height):
            break
        else:
            last_height = new_height
            time_elapsed += SCROLL_PAUSE_TIME

    # Close the current browser window
    browser_object.close()

    # Now, process the urls in the set one by one and store them
    # as .jpg files in the specified directory.
    i = 1
    for image in image_url_set:
        try:
            urllib.request.urlretrieve(image, "{}\\{}.jpg".format(username, str(i)))
        except TypeError:
            print("Error: {}".format(i))
        i += 1

    # end
