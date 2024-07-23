import requests
from bs4 import BeautifulSoup
import datetime
import json
import time

class CaseInfoScraper:
    """Scrapes judgment information from the National Archives website."""

    def __init__(self, base_url, output_file):
        """Initializes the scraper with a base URL for search results and a string to prepend to hrefs."""
        prefix_string = "https://caselaw.nationalarchives.gov.uk/"
        self.base_url = base_url
        self.prefix_string = prefix_string
        self.output_file = output_file
        self.judgments_data = {}

    def get_response(self, url, retries=5, backoff_factor=1.0):
        """Gets the response from a URL with retry mechanism.

        Args:
            url: The URL to get the response from.
            retries: Number of retries in case of failure.
            backoff_factor: Factor by which the wait time increases after each retry.

        Returns:
            The response object if the request is successful, None otherwise.
        """
        for attempt in range(retries):
            try:
                response = requests.get(url)
                response.raise_for_status()  # Raise HTTPError for bad responses
                return response
            except requests.RequestException as e:
                if attempt < retries - 1:
                    sleep_time = backoff_factor * (2 ** attempt)
                    print(f"Request failed: {e}. Retrying in {sleep_time} seconds...")
                    time.sleep(sleep_time)
                else:
                    print(f"Request failed after {retries} attempts: {e}")
                    return None

    def save_to_file(self):
        """Saves the data to the JSON file in a pretty-printed format."""
        with open(self.output_file, 'w') as f:
            json.dump(self.judgments_data, f, default=str, indent=4)

    def scrape_judgments(self, url):
        """Scrapes judgment information from a single page.

        Args:
            url: The URL of the search results page.
        """
        response = self.get_response(url)
        if response is None:
            return  # Return if the response failed

        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all containers holding judgment information
        judgements = soup.find_all("div", class_="results__result-list-container")

        for judgement in judgements:
            judgements_list = judgement.find("ul", class_="judgment-listing__list")
            for li in judgements_list.find_all("li"):
                data = {}

                # Extract judgment information
                anchor = li.find("a")
                if anchor and anchor.get("href"):
                    data["link"] = self.prefix_string + anchor["href"]
                    data["Name of the Case"] = anchor.text.strip()
                else:
                    continue  # Skip if anchor or href is not found

                court_span = li.find("span", class_="judgment-listing__court")
                if court_span:
                    data["judgment-listing__court"] = court_span.text.strip()
                else:
                    data["judgment-listing__court"] = "N/A"  # Default value if not found

                neutral_citation_span = li.find("span", class_="judgment-listing__neutralcitation")
                if neutral_citation_span:
                    data["judgment-listing__neutralcitation"] = neutral_citation_span.text.strip()
                else:
                    data["judgment-listing__neutralcitation"] = "N/A"  # Default value if not found

                date_span = li.find("time", class_="judgment-listing__date")
                if date_span and date_span.get("datetime"):
                    try:
                        data["datetime"] = datetime.datetime.strptime(date_span["datetime"], "%d %b %Y, midnight")
                    except ValueError:
                        data["datetime"] = "Invalid Date"  # Default value if parsing fails
                else:
                    data["datetime"] = "N/A"  # Default value if not found

                # Store each judgment data in the dictionary
                case_name = data["Name of the Case"].strip()
                self.judgments_data[case_name] = data

    def scrape_all_judgments_info(self, start_page, end_page):
        """Scrapes judgment information from all specified pages.

        Args:
            start_page: The starting page number.
            end_page: The ending page number.
        """
        for page_number in range(start_page, end_page + 1):
            url = f"{self.base_url}&page={page_number}"
            self.scrape_judgments(url)

        # Save all the gathered data to file
        self.save_to_file()