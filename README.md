# lead_generation_software

## Introduction

This Python-based lead generation software (v1.2) is designed to automate the process of finding potential leads by crawling websites using the Bing Search API and extracting contact information. It features a user-friendly GUI built with Tkinter for efficient interaction.

## Images:
![Lead Generation Software](https://github.com/SafeerAbbas624/lead_generation_software/blob/main/Screenshot1.JPG)

**This is the Graphical User Interface of the software.**

![Lead Generation Software Running image](https://github.com/SafeerAbbas624/lead_generation_software/blob/main/Screenshot2.JPG)

**Software showing result against the given keywords. This software is designed to get result from German domains first.**

![CSV file results](https://github.com/SafeerAbbas624/lead_generation_software/blob/main/Screenshot3.JPG)

**This is the csv file snippet to show the contact information scraped.**

## Key Features

- <b>Keyword Targeting:</b> Specify relevant keywords and software will show urls against those keywords.
- <b>Filter Negative Words:</b> Exclude irrelevant websites using negative keywords.
- <b>Bing Search Integration:</b> Leverage the Bing Search API for efficient crawling. Note that Google API doesnt work good as Bing API.
- <b>Pagination:</b> Navigate through large result sets effortlessly. It shows 50 urls per page and designed to get 200 urls max. If the search button is pressed again it will give next 200 results.
- <b>Progress Bar:</b> Monitor the crawling progress in real time. It shows progress in terminal also when running.
- <b>CSV Export:</b> Export extracted contact data in a structured CSV format.
- <b>Error Handling:</b> Gracefully handle potential errors during crawling and data extraction.
  
## Installation

**1. Prerequisites:**

- Python 3.x
- Install required libraries:
```Bash
pip install tkinter requests beautifulsoup4 bs4 nltk fake_useragent urllib.parse re csv output
```

**2. Clone or Download:**

- Clone the repository: git clone https://github.com/SafeerAbbas624/lead-generation-software.git
- Or download the ZIP archive.
- 
**3. API Key:**
  
- Obtain a Bing Search API key from Microsoft Azure Bing Search API Services. 
- Put the API in ```crawler.py``` file under ```api_key```string.
``` python
def crawl(keywords, filters, offset=0):
    api_key = "Write your bing.microsoft.com API key here."
```

## Usage

**1 Navigate to the project directory.**

**2 Run the application: python GUI.py**

**3 GUI Interface:**

- Enter keywords and filters.
- Click "Search."
- Navigate through results using "Next/Previous" buttons.
- Export data using "Export as CSV."
  
### How the Code Works

```GUI.py:``` Handles user interaction, built with Tkinter widgets.

```crawler.py:``` Encapsulates crawling logic using Bing Search API and extracts contact information.

```output.py:``` Exports extracted data to a CSV file.

### Additional Notes

This project can be used on lead generation purposes, it is mendatory to get API first and store it under ```api_key``` string. 

**Contributing:**

- If you wish to contribute to this project, please feel free to contact and please put the star. 
