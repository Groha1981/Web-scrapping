import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
import json

host = "https://spb.hh.ru/search/vacancy?text=python&area=1&area=2"
keywords = ["Django", "Flask"]
headers = Headers(browser="chrome", os="wim")
response = requests.get(host, headers=headers.generate())

html = response.text
soup = BeautifulSoup(html, "html.parser")
vacancies = soup.find_all(class_="vacancy-serp-item")
results = []
for vacancy in vacancies:
    link = vacancy.find("a", class_="bloko-link")["href"]
    company = vacancy.find("a", class_="bloko-link").text
    city = vacancy.find(class_="vacancy-serp-item__meta-info").text
    salary = vacancy.find(class_="vacancy-serp-item__compensation")
    if salary:
        salary = salary.text.strip()
    else:
        salary = "Not specified"
    description = vacancy.find(class_="g-user-content").text
    if any(keyword.lower() in description.lower() for keyword in keywords):
        vacancy_info = {
            "link": link,
            "company": company,
            "city": city,
            "salary": salary,
        }
        results.append(vacancy_info)

with open("vacancies.json", "w", encoding="utf-8") as file:
    json.dump(results, file, ensure_ascii=False, indent=4)

print(results)
