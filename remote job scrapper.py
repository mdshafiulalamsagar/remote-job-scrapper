import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://remoteok.com/remote-dev-jobs"
headers = {"User-Agent": "Mozilla/5.0"}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

jobs = soup.find_all('tr', class_='job')

job_data = []

for job in jobs:
    try:
        # Job categories (tags)
        tags = job.find_all('div', class_='tag')
        categories = [tag.h3.text.strip() for tag in tags if tag.h3]
        role = ", ".join(categories) if categories else "N/A"

        # Date posted
        time_tag = job.find('time')
        posted = time_tag['datetime'] if time_tag else "N/A"

        # Apply link from "source" <td>
        apply_section = job.find('td', class_='source')
        link = "N/A"
        if apply_section:
            apply_tag = apply_section.find('a', href=True)
            if apply_tag:
                href = apply_tag['href']
                if href.startswith('/l/'):
                    link = "https://remoteok.com" + href

        job_data.append({
            'Role': role,
            'Posted': posted,
            'Apply Link': link
        })

    except Exception as e:
        continue


# Save to Excel
df = pd.DataFrame(job_data)
df.to_excel('remoteok_updated_jobs.xlsx', index=False)
print("✅ Jobs saved to remoteok_updated_jobs.xlsx")
