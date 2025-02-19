import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime,date
from tqdm import tqdm
from pydantic_ai import Agent
from pydantic_ai.models import KnownModelName
import os
from pydantic import BaseModel
from typing import cast

# URL base
BASE_URL = "https://www.berghain.berlin/en/program/archive/{year}/{month}/"

class EventModel(BaseModel):
    date: date  
    title: str  
    location: str  
    artists: list[str]  
    labels: list[str]  

def fetch_html(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return BeautifulSoup(response.content, 'html.parser')
        else:
            print(f"Error al obtener {url}: {response.status_code}")
            return None
    except Exception as e:
        print(f"Excepción al obtener {url}: {e}")
        return None

def process_month(year, month):
    url = BASE_URL.format(year=year, month=f"{month:02d}")
    soup = fetch_html(url)
    if not soup:
        return []
    
    events_data = []
    events = soup.find_all('a', class_='upcoming-event')
    
    for event in events:
        model = cast(KnownModelName, os.getenv('PYDANTIC_AI_MODEL', 'openai:gpt-3.5-turbo'))
        agent = Agent(model, result_type=EventModel)
        try:
            result = agent.run_sync(str(event))
            result = result.data
            _datetime = result.date
            title = result.title
            location = result.location
            artists = result.artists
            
            # Add each artist as a separate entry
            for artist in artists:
                events_data.append([_datetime, title, location, artist])
                
        except Exception as e:
            print(f"Error processing event: {e}")
            continue
    
    return events_data


def save_to_csv(file_name, data, headers=None):
    with open(file_name, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if headers and file.tell() == 0:  # Write headers only if the file is empty
            writer.writerow(headers)
        writer.writerows(data)

# Main function to iterate from 2010 to the current month
def main():
    file_name = 'berghain.csv'
    headers = ['date', 'title', 'location', 'artist'] # Headers for the CSV file
    start_year = 2010
    end_date = datetime.now()
    total_months = (end_date.year - start_year) * 12 + end_date.month + 1

    with tqdm(total=total_months, desc="Processing Months") as pbar:    
        for year in range(start_year, end_date.year + 1):
            for month in range(1, 13):
                if year == end_date.year and month > end_date.month +1:
                    break
                events_data = process_month(year, month)
                if events_data:
                    save_to_csv(file_name, events_data, headers=headers)
                pbar.update(1)

    print(f"File {file_name} created successfully")

if __name__ == "__main__":
    main()
