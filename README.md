# **UKLawCaseScraper**
------
`UKLawCaseScraper` is a module, allows you to retrieve judgments and decisions information from 2003 onwards, from [Find case law](https://caselaw.nationalarchives.gov.uk/)  in a friendly, Pythonic way without having to solve CAPTCHAs.

## Installation
-----
UKLawCaseScraper can be installed with `pip`. To install using `pip`, simply run:
```python
pip install UKLawCaseScraper
```
or `pip` to install from `github`:
```python
pip install git+https://github.com/mrjoneidi/UKLawCaseScraper.git@main
```
This package has 3 main modules:
* CaseInfoScraper
* CaseHeaderScraper
* FullTextScraper
* Save_to_json  (For version <= `0.4.2`)

In versions prior to `0.4.2`, it is necessary to use the `save_to_json` function to manually save each output separately. However, starting from version `0.4.3`, each output class automatically records its data to a JSON file.

### 1- CaseInfoScraper
---
This module contains 2 functions. These functions scrape Link, Name of the Case, judgment-listing__court, judgment-listing__neutralcitation and Datetime for a page or multipages.
Funcrions:
* `scrape_judgments`
* `scrape_all_judgments_info`
* `get_response`

### 2- CaseHeaderScraper
---
This module has 3 functions. First module give us just page's urls that use in second and third functions. (So you have to run `scrape_judgment_urls` first) then, second function gives us direct download case's PDFs and the last one, scrape case header info :)
Functions:
* `scrape_judgment_urls`
* `judgment_Dlink`
* `scrape_header_info`
* `get_response`

### 3- FullTextScraper
---
This module has 3 function. It gets output of scrape_header_info and scrape all text of each cases.
Functions:
* `load_json`
* `scrape_full_text`
* `OutputScraper`
* `get_response`

### Usage Example
----
#### **CaseInfoScraper**
```python
from UKLawCaseScraper.CaseInfoScraper import CaseInfoScraper

base_url = "https://caselaw.nationalarchives.gov.uk/judgments/search?query="

## Any name you want
Case_info_path = "CaseInfo.json"
scraper = CaseInfoScraper(base_url, Case_info_path)
str_page = 1
end_page = 5

scraper.scrape_all_judgments_info(str_page, end_page)
```
#### **CaseHeaderScraper**
```python
from UKLawCaseScraper.CaseHeaderScraper import CaseHeaderScraper

base_url = "https://caselaw.nationalarchives.gov.uk/judgments/search"
str_page = 1
end_page = 5
scraper = CaseHeaderScraper(base_url)

url_path =  "judgment_urls1.json"
linkd = "judgment_dlinks1.json"
header_info = "header_info.json"

urls = scraper.scrape_judgment_urls(str_page, end_page,url_path)
scraper.judgment_Dlink(urls , linkd )
scraper.scrape_header_info(urls , header_info )
```

#### **FullTextScraper**
```python
# This is output of `scrape_all_judgments_info` function from CaseInfoScraper module
from UKLawCaseScraper.FullTextScraper import FullTextScraper
input_file_path = "CaseInfo.json"
output_file_path = 'judgment_full_text.json'

scraper = FullTextScraper(input_file_path)
scraped_data = scraper.output_scraper(output_file_path)
```
### 4- get_response
----
The `get_response` function is an essential component of the all classes. Here's an explanation of why it is included and its role in the class:
* Network Requests Handling
* Retry Mechanism

The `get_response` function is crucial for managing HTTP requests within the all classes. It ensures that web pages are fetched reliably, handles network errors gracefully, and retries requests when necessary. This design improves the robustness, maintainability, and readability of the scraper code.

## Contributing
---
* Specify preferred methods for reporting issues, suggesting features, or submitting pull requests
* Provide details on coding style, testing practices, and any other expectations you have for contributors.
* Test and provide feedback: Help us ensure quality by testing the code and providing feedback on usability.

## Author(s)
----
* Mohammadreza Joneidi Jafari 
* Amir Souroush Farzin

## Contact Us
---
If you have any questions or feedback, please get in touch in m.r.joneidi.02@gmail.com


