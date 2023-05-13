import asyncio

import httpx
from bs4 import BeautifulSoup


def parse_search_response(response):
    soup = BeautifulSoup(response.text, 'html.parser')
    all_jobs_html = soup.find_all('div', class_='base-card')
    jobs = []
    for job_html in all_jobs_html:
        job = {}
        link = job_html.find('a', class_='base-card__full-link').get('href')
        card_info = job_html.find('div', class_='base-search-card__info')
        title = card_info.find('h3', class_='base-search-card__title').text.strip()
        location = card_info.find('span', class_='job-search-card__location').text.strip()
        time = card_info.find('time', class_='job-search-card__listdate')
        company = card_info.find('h4', class_='base-search-card__subtitle').text.strip()
        job.update({
            'link': link,
            'title': title,
            'location': location,
            'company': company,
            'time': time if time is None else time.text.strip()
        })
        jobs.append(job)
    return jobs


async def send_detail_request(session, job):
    response = await session.get(job['link'])
    soup = BeautifulSoup(response.text, 'html.parser')
    des = soup.find('div', class_='show-more-less-html__markup')
    job['description'] = des if des is None else des.text.strip()
    return job


async def get_detail_responses(jobs):
    async with httpx.AsyncClient() as session:
        tasks = [send_detail_request(session, job) for job in jobs]
        result = await asyncio.gather(*tasks, return_exceptions=False)
    return result
