from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import cloudscraper
import os
import json
from urllib.parse import urljoin
import time


CHROME_DRIVER_PATH = "C:\\Program Files (x86)\\chromedriver.exe"


PROBLEM_DIR = "data/problems"
EDITORIAL_DIR = "data/editorials"
os.makedirs(PROBLEM_DIR, exist_ok=True)
os.makedirs(EDITORIAL_DIR, exist_ok=True)


BASE_URL = "https://codeforces.com"


def scrape_problems(contest_url):
    """Scrape problems from the given contest URL."""
    scraper = cloudscraper.create_scraper()
    response = scraper.get(contest_url)
    soup = BeautifulSoup(response.text, "html.parser")

   
    problems_table = soup.find("table", class_="problems")
    if not problems_table:
        print("No problems table found.")
        return

    problem_links = []
    for row in problems_table.find_all("tr")[1:]:  
        problem_cell = row.find("td", class_="id")
        if problem_cell:
            link = problem_cell.find("a", href=True)
            if link:
                problem_links.append(f"{BASE_URL}{link['href']}")

    print(f"Found {len(problem_links)} problems in the contest.")

    
    for problem_url in problem_links:
        print(f"Scraping problem: {problem_url}")
        response = scraper.get(problem_url)
        problem_soup = BeautifulSoup(response.text, "html.parser")

        
        title_div = problem_soup.find("div", class_="title")
        title = title_div.text.strip() if title_div else "No Title"

        
        statement_div = problem_soup.find("div", class_="problem-statement")
        statement = statement_div.text.strip() if statement_div else "No Statement"

        
        tags = []
        tags_section = problem_soup.find("div", class_="roundbox sidebox borderTopRound ")
        if tags_section:
            for tag in tags_section.find_all("span", class_="tag-box"):
                tags.append(tag.text.strip())

       
        problem_filename = os.path.join(PROBLEM_DIR, f"{title.replace(' ', '_')}.txt")
        with open(problem_filename, "w", encoding="utf-8") as f:
            f.write(statement)

       
        metadata = {
            "title": title,
            "tags": tags
        }
        metadata_filename = os.path.join(PROBLEM_DIR, f"{title.replace(' ', '_')}.json")
        with open(metadata_filename, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=4)

        print(f"Saved problem: {title}")


def scrape_editorial_with_all_problems(contest_url):
    """Scrape editorial content including solutions and code for all problems."""
    options = Options()
    options.headless = True
    service = Service(CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)

    try:
        print(f"Fetching contest page: {contest_url}")
        driver.get(contest_url)
        time.sleep(3)  

       
        soup = BeautifulSoup(driver.page_source, "html.parser")

       
        tutorial_tags = []
        for tag in soup.find_all("a", href=True):
            if "Tutorial" in tag.get("title", "") or "Tutorial" in tag.text:
                tutorial_tags.append(tag)

        if not tutorial_tags:
            print("No anchor tag with 'Tutorial' found.")
            return

        for tag in tutorial_tags:
            tutorial_url = tag.get('href')
            full_tutorial_url = urljoin(BASE_URL, tutorial_url)
            print(f"Full Tutorial URL: {full_tutorial_url}")

            
            scraper = cloudscraper.create_scraper()
            tutorial_response = scraper.get(full_tutorial_url)

            if tutorial_response.status_code == 200:
                tutorial_soup = BeautifulSoup(tutorial_response.text, "html.parser")
                content_section = tutorial_soup.find("div", class_="ttypography")
                if content_section:
                    contest_id = contest_url.split("/")[-1]
                    editorial_path = os.path.join(EDITORIAL_DIR, f"contest_{contest_id}_editorial.txt")

                    with open(editorial_path, "w", encoding="utf-8") as f:
                        
                        for problem_section in content_section.find_all("h4"):
                            problem_title = problem_section.text.strip()
                            f.write(f"\n### Problem: {problem_title}\n")

                         
                            solution_div = problem_section.find_next("div", class_="spoiler-content")
                            solution = solution_div.text.strip() if solution_div else "No Solution Found"
                            f.write("\n#### Solution Explanation\n")
                            f.write(solution)

                          
                            code_div = solution_div.find_next("div", class_="spoiler-content")
                            code = code_div.text.strip() if code_div else "No Code Found"
                            f.write("\n#### Code\n")
                            f.write(code)

                    print(f"Editorial content saved to: {editorial_path}")
                else:
                    print("No content found in the tutorial page.")
            else:
                print(f"Failed to fetch tutorial page: {full_tutorial_url}")

    except Exception as e:
        print(f"Error during scraping: {e}")
    finally:
        driver.quit()



def scrape_contest(contest_url):
    print(f"Starting scraping for contest: {contest_url}")
    scrape_problems(contest_url)
    scrape_editorial_with_all_problems(contest_url)
    print(f"Scraping completed for contest: {contest_url}")



contest_url = "https://codeforces.com/contest/2044"
scrape_contest(contest_url)




