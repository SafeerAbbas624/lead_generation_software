# Import libraries
import requests
from bs4 import BeautifulSoup
import re
import time
import random
import csv
import output
from nltk.corpus import names
import urllib.parse
from fake_useragent import UserAgent


import nltk
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree



nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')



# Function to crawl over internet to get url list using bing API.
def crawl(keywords, filters, offset=0):
    api_key = "Write your bing.microsoft.com API key here."
    keywords_list = re.split(r'[,\s]+', keywords)
    filters_list = re.split(r'[,\s]+', filters)
    # Combine contact-related keywords with original keywords
    contact_keywords = ['impressum', 'about us', 'contact', 'kontakt'] 
    combined_keywords = '+'.join(urllib.parse.quote(word) for word in keywords_list + contact_keywords)
    filters_encoded = '+'.join(urllib.parse.quote(word) for word in filters_list)

    search_url = f"https://api.bing.microsoft.com/v7.0/search?q={combined_keywords}&mkt=de-DE&setLang=de&cc=DE&count=10"
    headers = {
        'Ocp-Apim-Subscription-Key': api_key,
    }
    urls = []

    for start in range(offset, offset + 200, 10):
        try:
            response = requests.get(search_url + f"&offset={start}", headers=headers)
            response.raise_for_status()  # Raise an exception for error HTTP statuses
            data = response.json()
            if 'webPages' in data:
                for link in data['webPages']['value']:
                    urls.append(link['url'])
            else:
                print("No 'webPages' key found in the response.")
        except requests.exceptions.RequestException as e:
            print(f"Error fetching URLs: {e}")
            break  # Stop fetching if an error occurs

        # Add a delay between requests to avoid rate limiting
        time.sleep(0.3)

    unique_urls = []
    seen_domains = {}

    for url in urls:
        domain = urllib.parse.urlparse(url).netloc

        if domain not in seen_domains:
            seen_domains[domain] = url
            unique_urls.append(url)

    return unique_urls, offset + 200





# Function to extract addresses from the text 
def extract_addresses_from_text(web_text):
    # Define a regex pattern for German addresses
    address_pattern = re.compile(r'\b[A-Za-zäöüÄÖÜß]+\s+\d{1,4}\b,\s*\d{5}\s+[A-Za-zäöüÄÖÜß]+\b')
    addresses = address_pattern.findall(web_text)
    return addresses




# Function to extract names from the text using NLTK library
def extract_names_from_text(webtext):
    nltk_results = ne_chunk(pos_tag(word_tokenize(webtext)))
    person_names = []
    for nltk_result in nltk_results:
        if type(nltk_result) == Tree and nltk_result.label() == 'PERSON':
            name = ' '.join([leaf[0] for leaf in nltk_result.leaves()])
            person_names.append(name)
    return person_names




# Function to extract text from url smartly
def fetch_url(url):
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    session = requests.Session()
    retries = 3

    for _ in range(retries):
        try:
            response = session.get(url, headers=headers)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            soup = BeautifulSoup(response.content, 'html.parser')
            text = soup.get_text()
            return text
        except requests.exceptions.RequestException as e:
            print(f"Error processing URL {url}: {e}")
            time.sleep(random.uniform(1, 3))  # Random delay before retrying

    return None



# Find impressum links in url
def find_impressum_links(url):
    """
    Extracts potential Impressum URLs from a given website.

    Args:
        url (str): The URL of the website to search.

    Returns:
        list: A list of potential Impressum URLs found on the website.
    """
    impressum_links = []
    try:
        ua = UserAgent()
        headers = {'User-Agent': ua.random}
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise exception for bad responses
        soup = BeautifulSoup(response.content, 'html.parser')

        # Look for common Impressum link text patterns (case-insensitive)
        if 'impressum' or 'about' or 'contact' or 'kontakt' in url:
            impressum_links.append(url)
        else:
            for pattern in ['impressum', 'about us', 'contact', 'kontakt']:
                impressum_links.extend(link['href'] for link in soup.find_all('a', text=re.compile(pattern, re.IGNORECASE)))

        return impressum_links

    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return []




# Extract Company name from the URL
def extract_company_name(url):
    try:
        parsed_url = urllib.parse.urlparse(url)
        domain = parsed_url.netloc
        # Remove subdomains and top-level domains
        company_name = domain.split('.')[-2]
        # Basic cleaning (replace underscores with spaces, capitalize first letter)
        company_name = company_name.replace('_', ' ').title()
        return company_name
    except Exception as e:
        print(f"Error extracting company name from URL: {e}")
        return None






# Function to scrape data from a list of URLs and dumb data into csv
def export_to_csv(unique_urls, gui_keyword):
    number = 0
    contact_details = []
    impressum_urls = []
    for url in unique_urls:
        if any(social in url for social in ['linkedin', 'youtube', 'facebook', 'reddit', 'instagram']):
            print(f'This {url} is skipping. \nIt is a social link.')
            continue
        else:
            # Find potential Impressum URLs for the current website
            number += 1
            print(f'Processing {url}...\nThis is {number} link\n\n')
            potential_impressums = find_impressum_links(url)
            impressum_urls.extend(potential_impressums)


    print(len(impressum_urls))
    print(impressum_urls)
    number = 0

# Process the extracted Impressum URLs (replace with your data extraction logic)
    for impressum_url in impressum_urls:
            number += 1
            print(f'Processing {impressum_url}...\nThis is {number} link\n\n')
            text = fetch_url(impressum_url)
            if text is None:
                print(f'No data in this url \n {impressum_url}')
                continue

            try:
                # Extract Names from the text
                extracted_names = extract_names_from_text(webtext=text)

            except Exception as e:
                print(f"Names can't be extracted from this URL.\nError processing URL {url}: {e}")
                extracted_names = []

            try:
                # Extract addresses from the text
                addresses = extract_addresses_from_text(web_text=text)
            except Exception as e:
                print(f"Address can't be extracted from this URL.\nError processing URL {url}: {e}")
                addresses = []

            try:
                # Extract Phone number from the text
                phone_regex = re.compile(r'\+?\d{1,4}[\s-]?\d{1,4}[\s-]?\d{1,4}[\s-]?\d{1,4}[\s-]?\d{1,4}[\s-]?\d{1,4}')
                extracted_phone_numbers = phone_regex.findall(text)
            except Exception as e:
                print(f"Phone Number can't be extracted from this URL.\nError processing URL {url}: {e}")
                extracted_phone_numbers = []

            try:
                # Extract Email address from the text
                email_regex = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
                extracted_emails = email_regex.findall(text)
            except Exception as e:
                print(f"Emails can't be extracted from this URL.\nError processing URL {url}: {e}")
                extracted_emails = []

            try:
                # Extract company name from URL
                company_name = extract_company_name(impressum_url)
            except Exception as e:
                print(f"Company name can't be extracted from this URL.\nError processing URL {url}: {e}")
                company_name = ''

            # Create a dictionary to store the extracted information
            detail = {
                'Company Name': company_name,
                'Url Link': impressum_url,
                'Keyword Selected': gui_keyword,
                'Phone': extracted_phone_numbers,
                'Email': extracted_emails,
                'Address': addresses,
                'Person Name': extracted_names,
                }

            contact_details.append(detail)
            print(contact_details)

    # Write the contact details to a CSV file using output.py
    print(f'This is the detail \n {contact_details}\n \n \n This is the end of detail.')
    output.write_to_csv(contact_details)
