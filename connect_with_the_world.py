import requests
import os
import time
import html
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


def main():
    driver = start_driver()
    try:
        for page in range(1, 101):
            # Replace this link with the one you're interested in
            address = f"https://www.linkedin.com/search/results/people/?facetGeoRegion=%5B%22gb%3A0%22%5D&facetIndustry=%5B%22137%22%2C%22104%22%5D&facetNetwork=%5B%22F%22%2C%22S%22%5D&keywords=Recruiter&origin=FACETED_SEARCH&page={page}"

            # Getting the html
            driver = get_html(driver, address)

            # Scrolling down
            scroll_down(driver)

            # Analyzing the html and getting the infos of the recruiters.
            html_text = driver.page_source
            soup = bs(html_text, "lxml")
            recruiters_names_divs = soup.findAll('span', {'class': 'name actor-name'})
            status_divs = soup.findAll('p', {'class': 'subline-level-1 t-14 t-black t-normal search-result__truncate'})
            location_divs = soup.findAll('p', {'class': 'subline-level-2 t-12 t-black--light t-normal search-result__truncate'})

            # Sending an invitation with a personalized message.
            for name_div, status, location in zip(recruiters_names_divs,status_divs, location_divs):
                full_name = name_div.text
                status = status.text.strip()
                location = location.text.strip()
                try:
                    add_recruiter(driver, full_name, status, location)
                except Exception as e:
                    print(e)
                    # print("Adding the recruiter failed... Might have been already added, can't be added, or a technical problem happened.")
    except:
        driver.quit()
        exit(1)

    driver.quit()


def start_driver():
    """
    Starts the selenium chrome driver.
    Add --headless option if you do not want a browser to pop up.
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--user-data-dir=C:/Users/Qnouro/AppData/Local/Google/Chrome/User\ Data/Default")
    print("Starting the driver...")
    driver = webdriver.Chrome(options=options)  # Headless + using your firefox's cookies
    return driver


def get_html(driver, addr):
    """
    Retrieving the html page of the given address
    """
    driver.get(addr)
    return driver


def scroll_down(driver):
    """
    Scrolling down the page. This is useful (and necessary) in order to trigger
    the JS scripts of the page which generates the "CONNECT" button amongst
    other things.
    """
    print("Scrolling...")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight/3);")
    time.sleep(1)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)


def click_button(driver, button):
    """
    Clicks on the given button.
    @param button: xpath of the button to click on.
    """
    time.sleep(2)
    elem = driver.find_element_by_xpath(button)
    print(elem)
    actions = ActionChains(driver)
    actions.click(elem).perform()


def add_recruiter(driver, full_name, status, location):
    """
    Adds the given recruiter.
    """
    first_name = full_name.split(" ")[0]

    # Creating the message with customized first name
    message = f"""Hi {first_name}"""

    aria_label = full_name + ". " + status + ", " + location
    aria_label = html.escape(aria_label, quote=True)  # Conversion to html compatible string for special characters

    button = f"//*[@aria-label='Connect with {aria_label}']"
    click_button(driver, button)

    time.sleep(1)

    add_note_button = "//*[@aria-label='Add a note']"
    click_button(driver, add_note_button)

    time.sleep(2)

    send_message(driver, message)


def send_message(driver, message):
    """
    Inserts the given message in the textarea and sends it.
    """
    element = driver.find_element_by_tag_name("textarea")
    element.send_keys(Keys.TAB)
    element.clear()
    element.send_keys(message)
    button = f"//*[@aria-label='Done']"
    click_button(driver, button)


if __name__ == "__main__":
    main()
