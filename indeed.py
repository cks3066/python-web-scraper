import requests
from bs4 import BeautifulSoup

LIMIT = 50
SEARCH_TARGET= "python"
URL = f"https://kr.indeed.com/%EC%B7%A8%EC%97%85?q={SEARCH_TARGET}&limit={LIMIT}&filter=0&vjk=e742db63ad7e269f"

def convert_string_with_comma_to_number(some_string):
  for n in range(len(some_string)):
    string_replaced = some_string.replace(',','')
  return int(string_replaced)

def extract_job(html):
    title = html.find("span", title=True).string
    company = html.find("span", {"class": "companyName"})
    if company is not None:
      company_anchor = company.find("a")
      if company.find("a") is not None:
        company = company_anchor.string
      else:
        company = company.string
    location = html.find("div", {"class", "companyLocation"}).string
    job_id = html["data-jk"]
    return {'title': title, 'company': company, 'location': location, 'link': f"https://kr.indeed.com/%EC%B1%84%EC%9A%A9%EB%B3%B4%EA%B8%B0?jk={job_id}&from=serp&vjs=3"}

def extract_indeed_pages():
  result = requests.get(URL)
  soup = BeautifulSoup(result.text, "html.parser")
  search_count_pages = soup.find("div", {"id": "searchCountPages"})

  # search_count_pages.string.split()[-1] => ex) "123건" or "123,123건"
  # search_count_pages.string.split()[-1][:-1] => ex) "123" or "123,123"
  number_jobs_searched_string = search_count_pages.string.split()[-1][:-1]

  # ex) "123,123" => 123123
  number_jobs_searched = convert_string_with_comma_to_number(number_jobs_searched_string)

  max_pages = number_jobs_searched // LIMIT + 1
  return max_pages

def extract_indeed_jobs(last_page):
  jobs = []
  for page in range(last_page):
    print(f"Scrapping page {page}")
    result = requests.get(f"{URL}&start={page*LIMIT}")
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find_all("a", {"class": "result"})
    for result in results:
      job = extract_job(result)
      jobs.append(job)
  return jobs

def get_jobs():
  last_page = extract_indeed_pages()
  jobs = extract_indeed_jobs(last_page)
  return jobs
