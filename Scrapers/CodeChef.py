import os
import sys
import time
import logging

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from extensions import EXTENSIONS
from UploadToGitHub import upload_to_github

from selenium import webdriver
from selenium.webdriver.common.by import By


def handle_profile_page(codechef_username):
    driver = webdriver.Chrome()
    driver.implicitly_wait(40)

    # Profile page handle
    driver.get(f"https://www.codechef.com/users/{codechef_username}")
    time.sleep(3)

    return driver


def get_submission_links(driver):
    number_of_pages = int(driver.find_element_by_class_name("pageinfo").text.split()[-1])

    submission_links = []

    while True:
        rows = driver.find_elements_by_xpath("//table[@class='dataTable']/tbody/tr")

        for row in rows:
            spans = row.find_elements_by_xpath(".//span")
            has_accepted = any(span.get_attribute("title") == "accepted" for span in spans)
            
            td_elements = row.find_elements_by_tag_name('td')
            contains_1_pts = any("1 pts" in td_element.get_attribute('title') for td_element in td_elements)

            if has_accepted or contains_1_pts:
                element = row.find_element_by_css_selector('td.centered a.centered')
                submission_links.append(element.get_attribute("href"))
        
        page_num = driver.find_element(By.CSS_SELECTOR, ".pageinfo").text
        
        if page_num==f'{number_of_pages} of {number_of_pages}':
            break
        
        btn = driver.find_element(By.XPATH, "//td/a[@onclick=\"onload_getpage_recent_activity_user('next');\"]")
        driver.execute_script("arguments[0].click();", btn)
        time.sleep(2)

    return submission_links



def codechef_uploader(codechef_username, repo):
    ac_submission_cnt = 0
    
    driver = handle_profile_page(codechef_username)
    submission_links = get_submission_links(driver)

    links = submission_links[0]
    for i in range(1, len(submission_links)):
        links += ',' + submission_links[i]

    with open("codechef_links.txt", "w") as f:
        f.write(links)
        f.close()

    submission_links = []
    with open("codechef_links.txt", "r") as f:
        submission_links = list(f.read().split(','))
        f.close()

    i = 0

    while i < len(submission_links):
        submission_link = submission_links[i]
        driver.get(submission_link)
        time.sleep(5)

        # verdict = driver.find_element_by_css_selector("div._status_container_1gitb_99 span").text
        
        solution_code = driver.find_element(By.CSS_SELECTOR, '.ace_content')
        solution_code = solution_code.text
        if len(solution_code) == 0:
            print("got one bad")
            continue
        
        elements = driver.find_elements_by_xpath("//a[contains(@class, '_link_1gitb_44')]")

        # Extract the text from the elements
        problem_id = elements[0].text.strip()
        contest_id = elements[1].text.strip()

        language = driver.find_element_by_class_name("_ideLanguageName_1jy8z_268").text
        language = language[language.index(":")+1:].strip()
        
        name = driver.find_element_by_class_name("_problem_title_1gitb_58").text
        solution_id = submission_link[-8:]

        try:
            path = f'CodeChef/{contest_id}/{problem_id} - {name}/{solution_id}.{EXTENSIONS[language]}'
            upload_to_github(repo, path, solution_code)

        except Exception as e:
            logging.error(f'{e} for {i}')
            continue
        
        print(f"done: {i}")
        i += 1
        ac_submission_cnt += 1

    return ac_submission_cnt