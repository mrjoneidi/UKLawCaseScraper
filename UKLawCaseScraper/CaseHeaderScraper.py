import requests
from bs4 import BeautifulSoup
import json
import time
import os

class CaseHeaderScraper:
    """A class to scrape judgment information from the National Archives website."""

    def __init__(self, base_url):
        """Initializes the scraper with a base URL for search results."""
        self.base_url = base_url

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

    def save_to_file(self, filename, case_name, data):
        """Saves the data to the JSON file."""
        if not os.path.exists(filename):
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump({}, f)

        with open(filename, 'r+', encoding='utf-8') as f:
            try:
                file_data = json.load(f)
            except json.JSONDecodeError:
                file_data = {}

            file_data[case_name] = data

            f.seek(0)
            json.dump(file_data, f, ensure_ascii=False, indent=4, default=str)
            f.truncate()

    def scrape_judgment_urls(self, start_page, end_page, output_file):
        """Scrapes judgment URLs from the National Archives website.

        Args:
            start_page: The starting page number.
            end_page: The ending page number.
            output_file: The output file to save URLs.

        Returns:
            A list of modified URLs for each judgment.
        """
        res = []
        for page in range(start_page, end_page + 1):
            # Construct the URL for the current page
            url = f"{self.base_url}?query=&page={page}"
            # Fetch the page content
            response = self.get_response(url)
            if response is None:
                continue  # Skip to the next page if the response failed

            soup = BeautifulSoup(response.content, 'html.parser')
            job_elements = soup.find_all("div", class_="results__result-list-container")

            for job_element in job_elements:
                links = job_element.find_all("a")
                for link in links:
                    link_url = link.get("href")
                    if link_url:
                        res.append(link_url)

        string_to_add = 'https://caselaw.nationalarchives.gov.uk/'
        filtered_list = [item for item in res if "query" not in item]
        modified_list = [string_to_add + item for item in filtered_list]

        # Save URLs to a file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(modified_list, f, ensure_ascii=False, indent=4, default=str)

        return modified_list

    def judgment_Dlink(self, modified_list, output_file):
        """Scrapes download links and other details from the specified URLs.

        Args:
            modified_list: A list of modified URLs to scrape.
            output_file: The output file to save judgment details.

        Returns:
            A list of dictionaries containing download link and other details for each judgment.
        """
        judgment_details = []

        for url in modified_list:
            response = self.get_response(url)
            if response is None:
                continue  # Skip to the next URL if the response failed

            soup = BeautifulSoup(response.content, 'html.parser')

            # Find all containers holding judgment information
            judgments = soup.find_all("div", class_="judgment-toolbar__container")

            for judgment in judgments:
                data = {}

                # Extract title of the case
                title_element = judgment.find("h1", class_="judgment-toolbar__title")
                if title_element:
                    data["title"] = title_element.text.strip()

                # Extract judgment reference
                reference_element = judgment.find("p", class_="judgment-toolbar__reference")
                if reference_element:
                    data["judgment_reference"] = reference_element.text.strip()

                # Extract download link
                download_element = judgment.find("a", class_="judgment-toolbar-buttons__option--pdf")
                if download_element and "href" in download_element.attrs:
                    data["download_link"] = download_element["href"]

                # Add the data to the list if it contains valid data
                if data:
                    judgment_details.append(data)

                # Save each judgment data to file immediately
                self.save_to_file(output_file, data["title"], data)

        return judgment_details

    def scrape_header_info(self, modified_list, output_file):
        """Scrapes header information from the specified URLs.

        Args:
            modified_list: A list of modified URLs to scrape.
            output_file: The output file to save header information.

        Returns:
            A dictionary containing header information for each judgment.
        """
        header_info_dict = {}

        for url in modified_list:
            response = self.get_response(url)
            if response is None:
                continue  # Skip to the next URL if the response failed

            soup = BeautifulSoup(response.content, 'html.parser')

            # Find the judgment article
            judgment_article = soup.find("article", class_="judgment")

            if not judgment_article:
                continue

            data = {}

            # Extract all text within all headers with class="judgment-header"
            all_headers = judgment_article.find_all("header", class_="judgment-header")
            all_header_text = " ".join([header.get_text(separator=' ', strip=True) for header in all_headers])
            data["all_header_text"] = all_header_text

            # Extract specific information from the first header
            if all_headers:
                header_element = all_headers[0]

                # Extract judgment title
                title_element = header_element.find("p")
                if title_element:
                    data["title"] = title_element.text.strip()

                # Extract neutral citation number
                citation_element = header_element.find("div", class_="judgment-header__neutral-citation")
                if citation_element:
                    data["neutral_citation"] = citation_element.text.replace('Neutral Citation Number: ', '').strip()

                # Extract case number
                case_number_element = header_element.find("div", class_="judgment-header__case-number")
                if case_number_element:
                    data["case_number"] = case_number_element.text.replace('Case No: ', '').strip()

                # Extract court name
                court_element = header_element.find("div", class_="judgment-header__court")
                if court_element:
                    data["court"] = court_element.text.strip()

                # Extract location
                location_elements = header_element.find_all("p", class_="judgment-header__pr-right")
                if location_elements:
                    data["location"] = " ".join([element.text.strip() for element in location_elements])

                # Extract judgment date
                date_element = header_element.find("div", class_="judgment-header__date")
                if date_element:
                    data["date"] = date_element.text.replace('Date: ', '').strip()

                # Ensure that there is a title before saving to file
                if "title" in data:
                    # Add the URL to the data
                    data["url"] = url
                    self.save_to_file(output_file, data["title"], data)
                    header_info_dict[url] = data
                else:
                    print(f"No title found for URL: {url}")

        return header_info_dict