import requests
from bs4 import BeautifulSoup
import datetime
import re
from tabulate import tabulate
from openai import OpenAI
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from environment
LLM_MODEL = "gpt-4-turbo-preview"  # Using GPT-4 Turbo

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def get_movies_from_year(year):
    """
    (No Changes Here)
    Scrapes the "List of Telugu films of {year}" Wikipedia page.
    Returns a list of dictionaries with keys: title, release_date, url.
    """
    url = f"https://en.wikipedia.org/wiki/List_of_Telugu_films_of_{year}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Page not found or error for year {year}.", file=sys.stderr)
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    movies = []
    # Look for tables with class "wikitable"
    tables = soup.find_all("table", class_="wikitable")
    for table in tables:
        headers = [th.get_text(strip=True).lower() for th in table.find_all("th")]
        if not any("release" in header for header in headers):
            continue
        try:
            release_idx = next(i for i, header in enumerate(headers) if "release" in header)
        except StopIteration:
            continue
        # Try to identify a title column; if not found, default to first column.
        try:
            title_idx = next(i for i, header in enumerate(headers) if "title" in header)
        except StopIteration:
            title_idx = 0

        for row in table.find_all("tr")[1:]:
            cols = row.find_all(["td", "th"])
            if len(cols) <= release_idx:
                continue
            release_text = cols[release_idx].get_text(" ", strip=True)
            # Look for a date pattern like "23 March 1979"
            date_match = re.search(r'(\d{1,2})\s+([A-Za-z]+)\s+(\d{4})', release_text)
            if date_match:
                day, month_str, year_str = date_match.groups()
                try:
                    release_date = datetime.datetime.strptime(f"{day} {month_str} {year_str}", "%d %B %Y").date()
                except ValueError:
                    continue
                # Get movie title and URL if available.
                title_cell = cols[title_idx]
                a_tag = title_cell.find("a")
                title = title_cell.get_text(" ", strip=True)
                movie_url = None
                if a_tag and a_tag.get("href", "").startswith("/wiki/"):
                    movie_url = "https://en.wikipedia.org" + a_tag["href"]
                movies.append({
                    "title": title,
                    "release_date": release_date,
                    "url": movie_url
                })
    return movies

def get_all_text_from_page(soup):
    """
    Extracts all text content from the main content area of the Wikipedia page.
    """
    content_div = soup.find("div", class_="mw-parser-output")
    if not content_div:
        return "Not available"

    all_text = []
    for element in content_div.find_all(['p', 'ul', 'ol', 'table']):
        all_text.append(element.get_text(" ", strip=True))

    return " ".join(all_text)

def get_llm_movie_summary(text):
    """
    Uses OpenAI's API to generate a comprehensive summary of the movie info,
    including songs, music director, and other interesting details.
    """
    prompt = (
        "Summarize the following information about a movie, providing a rich and detailed description. "
        "Include the plot, major production details, reception, cast, "
        "songs featured in the movie, the music director, and any other interesting details. "
        "Provide a concise, paragraph-style summary. Do not include headers, just include the summary:\n\n"
        f"{text}"
    )
    try:
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=750,  # Increased token limit for more detailed summary
            temperature=0.7
        )
        movie_summary = response.choices[0].message.content.strip()
        return movie_summary
    except Exception as e:
        print(f"LLM summarization failed: {e}", file=sys.stderr)
        return "LLM summarization failed."

def get_movie_summary(movie_url):
    """
    Visits the movie's Wikipedia page (if available) and gets a summary
    either by LLM processing or by simply reading all text.
    """
    if not movie_url:
        return "Not available"

    try:
        response = requests.get(movie_url)
        if response.status_code != 200:
            return "Not available"
    except Exception as e:
        print(f"Error fetching URL {movie_url}: {e}", file=sys.stderr)
        return "Not available"

    soup = BeautifulSoup(response.text, 'html.parser')

    all_text = get_all_text_from_page(soup)
    if all_text == "Not available":
        return "Not available"

    movie_summary = get_llm_movie_summary(all_text)
    if movie_summary == "LLM summarization failed.":
        return all_text

    return movie_summary

def get_movies_for_date_or_month(target_date):
    """
    Iterates through years, scraping movie lists. First checks for movies
    on the exact date. If none found, expands to find movies released in the same month.
    """
    movies_highlight = []
    found_on_date = False
    for year in range(1947, target_date.year + 1):
        movies = get_movies_from_year(year)
        for movie in movies:
            rd = movie["release_date"]
            if rd.month == target_date.month and rd.day == target_date.day:
                found_on_date = True
                movie_summary = get_movie_summary(movie["url"])
                movie.update({"Summary": movie_summary})
                movies_highlight.append(movie)

    # If no movies were found for the exact date, search the entire month
    if not found_on_date:
        for year in range(1947, target_date.year + 1):
            movies = get_movies_from_year(year)
            for movie in movies:
                rd = movie["release_date"]
                if rd.month == target_date.month:
                    movie_summary = get_movie_summary(movie["url"])
                    movie.update({"Summary": movie_summary})
                    movies_highlight.append(movie)

    return movies_highlight

if __name__ == "__main__":
    user_input = input("Enter a date (mm/dd/yyyy): ")
    try:
        target_date = datetime.datetime.strptime(user_input, "%m/%d/%Y").date()
    except ValueError:
        print("Invalid date format. Please use mm/dd/yyyy.", file=sys.stderr)
        exit(1)

    highlights = get_movies_for_date_or_month(target_date)

    if highlights:
        if any(movie["release_date"].day == target_date.day for movie in highlights):
            print(f"\nMovies released on {target_date.strftime('%B %d')} from 1947 to {target_date.year}:\n")
        else:
            print(f"\nNo movies found released on {target_date.strftime('%B %d')}. Here are movies released in {target_date.strftime('%B')} from 1947 to {target_date.year}:\n")
        table_data = []
        for movie in highlights:
            table_data.append([
                movie["title"],
                movie["release_date"],
                movie.get("Summary", "Not available") 
            ])
        headers = ["Title", "Release Date", "Summary"]
        print(tabulate(table_data, headers=headers, tablefmt="grid", maxcolwidths=[None, None, 80])) # Changed line
    else:
        print("No movies found with a matching release date in the specified range.")
