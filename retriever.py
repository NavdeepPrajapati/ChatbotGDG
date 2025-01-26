import os
import json
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc # type: ignore

BASE_DIR = "scraped_data"
PROBLEMS_DIR = os.path.join(BASE_DIR, "problems")
EDITORIALS_DIR = os.path.join(BASE_DIR, "editorials")
os.makedirs(PROBLEMS_DIR, exist_ok=True)
os.makedirs(EDITORIALS_DIR, exist_ok=True)

# Selenium setup
def get_selenium_driver():
    try:
        driver = uc.Chrome()
        return driver
    except Exception as e:
        print(f"Error initializing ChromeDriver: {e}")
        exit(1)

def create_problem_directory(problem_id, contest_name, base_path=PROBLEMS_DIR):
    problem_dir = os.path.join(base_path, contest_name)
    os.makedirs(problem_dir, exist_ok=True)
    return {
        "statement": os.path.join(problem_dir, f"{problem_id}_statement.txt"),
        "metadata": os.path.join(problem_dir, f"{problem_id}_metadata.json")
    }

def update_metadata(metadata_path, data):
    if os.path.exists(metadata_path):
        with open(metadata_path, 'r') as f:
            existing_data = json.load(f)
    else:
        existing_data = {}
    existing_data.update(data)
    with open(metadata_path, 'w') as f:
        json.dump(existing_data, f, indent=4)

def scrape_problem(problem_url, problem_id, contest_name):
    driver = get_selenium_driver()
    driver.get(problem_url)

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "problem-statement"))
        )
    except Exception as e:
        print(f"Problem page loading failed for {problem_url}: {e}")
        driver.quit()
        return

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Extract elements 
    title = soup.find("div", class_="title")
    title_text = title.text if title else f"Problem {problem_id}"
    
    statement = soup.select_one("#pageContent > div.problemindexholder > div.ttypography > div > div:nth-child(2)")
    input_spec = soup.find("div", class_="input-specification")
    output_spec = soup.find("div", class_="output-specification")
    sample_texts = soup.find("div", class_="sample-test")
    tags = [tag.get_text(strip=True) for tag in soup.find_all("span", class_="tag-box")] if soup.find_all("span", class_="tag-box") else []
    time_limit = soup.find("div", class_="time-limit")
    memory_limit = soup.find("div", class_="memory-limit")

    paths = create_problem_directory(problem_id, contest_name)

    # Write problem details
    with open(paths["statement"], 'w', encoding='utf-8') as f:
        if statement:
            f.write(statement.get_text() + "\n")
        if input_spec:
            f.write(input_spec.get_text() + "\n")
        if output_spec:
            f.write(output_spec.get_text() + "\n")
        if sample_texts:
            for lines in sample_texts.find_all("div"):
                f.write(lines.get_text() + "\n")

    update_metadata(paths["metadata"], {
        "title": title_text,
        "tags": tags,
        "time_limit": time_limit.get_text(strip=True) if time_limit else "N/A",
        "memory_limit": memory_limit.get_text(strip=True) if memory_limit else "N/A"
    })
    print(f"Problem {problem_id} saved successfully.")

    driver.quit()

if __name__ == "__main__":
    contest_url = "https://codeforces.com/contest/2044"
    scrape_problem(contest_url, "A", "contest_2044")
