#!/usr/bin/env python3

# This script automates the process of generating and validating redirects for k8s.io.
# Generate [_redirects] file based on [gen-redirects.csv]
# [step 1] Read gen-redirects.csv and remove incomplete redirects
# [step 2] Validate availability of the redirection target(to) URLs
# [step 3] Validate any localization redirect exists (and remove)
# [step 4] Localize redirects for each language (replicate redirects)
# [step 5] Update [_redirects] file

# Refer to https://www.netlify.com/docs/redirects/ for the redirect rules when updating gen-redirects.csv

import csv
import requests
import os
from concurrent.futures import ThreadPoolExecutor

# Base URL
BASE_URL = "https://kubernetes.io"

# List of URL prefixes that are used to classify redirects (main sections).
URL_CONTENT_PREFIX = ["blog", "case-studies", "community", "docs", "partners", "releases"]

# Dynamically load directory names for localization from the 'content' directory, excluding 'en'
content_dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'content')
directories = os.listdir(content_dir_path)
URL_LOCALIZATION_PREFIX = [
    d for d in directories 
    if os.path.isdir(os.path.join(content_dir_path, d)) 
    and d != "en"
]

# Reads redirects from a given CSV file and returns a list of redirects. 
# Skips rows with empty 'from' or 'to' URLs.
def read_redirects_from_csv(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        return [(i+1, *row) for i, row in enumerate(reader) if row[0].strip() and row[1].strip()]

# Checks the availability of a given URL. 
# If the URL ends with ":splat", it trims that part before checking. 
# Returns True if the URL is accessible, otherwise False.
def check_url_availability(url):
    print(f"Checking redirection target URL: {url}")
    if url.endswith(":splat"):
        url = url[:-6]
    try:
        response = requests.get(url)
        return response.status_code == 200
    except requests.RequestException:
        return False

# Writes a list of redirects to a given CSV file.
def write_redirects_to_csv(redirects, filename):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        for redirect in redirects:
            writer.writerow(redirect[1:])  # Exclude line number

# Writes a list of redirects to the specified file in the Netlify redirects format.
def write_redirects_to_file(redirects, filename):
    with open(filename, 'w') as f:
        f.write("# Autogenerated file based on [gen-redirects.csv] by [gen-redirects.py]\n")
        f.write("# Do not manually change this file. Modify [gen-redirects.csv] and run [gen-redirects.py] to update\n")
        for _, from_url, to_url, status in redirects:
            # Format the line with appropriate spacing
            f.write(f"{from_url.ljust(70)} {to_url.ljust(70)} {status}\n")

def main():
    # Read the redirects from the CSV file
    print("\n[Step 1] Reading gen-redirects.csv and removing incomplete redirects...")
    redirects = read_redirects_from_csv('gen-redirects.csv')
    
    # Sort the redirects based on the from_url URL for better readability
    redirects.sort(key=lambda x: x[1])
    
    # Check the availability of the target URLs in parallel
    print("\n[Step 2] Validating the availability of redirection target URLs...\n")

    with ThreadPoolExecutor() as executor:
        results = list(executor.map(lambda x: (x, check_url_availability(BASE_URL + x[2] if x[2].startswith('/') else x[2])), redirects))

    unavailable_redirects = []
    available_redirects = []

    for (line_num, from_url, to_url, status), is_available in results:
        if not is_available:
            print(f"[{line_num}] to_url is NOT available: {BASE_URL + to_url if to_url.startswith('/') else to_url} \t (from_url: {from_url})")
            unavailable_redirects.append((line_num, from_url, to_url, status))
        else:
            available_redirects.append((line_num, from_url, to_url, status))

    combined_redirects = available_redirects

    # Ask the user if they want to delete the unavailable redirects
    if unavailable_redirects:
        user_input = input("\nDo you want to delete the unavailable redirects? (y/n): ")
        if user_input.lower() == 'y':
            # Write the combined list back to the CSV file
            write_redirects_to_csv(combined_redirects, 'gen-redirects.csv')
        else:
            # Combine the lists with a blank line in between
            combined_redirects = available_redirects + [(None, '', '', '')] + unavailable_redirects
            print("\nThe unavailable redirects will be placed at the bottom of the gen-redirects.csv file with a blank line separating them.")
            # Write the combined list back to the CSV file
            write_redirects_to_csv(combined_redirects, 'gen-redirects.csv')
            print("[Please clean up the unavailable redirects in the gen-redirects.csv and then run the program again]")
            exit()
    else:
        print("\nAll redirection target URLs are accessible. Proceeding to the next step.\n")

    print("\n[Step 3] Validating and removing any existing localization redirects....\n")

    # Add '/' to the beginning and end of each prefix for matching
    content_prefixes = [f"/{prefix}/" for prefix in URL_CONTENT_PREFIX]
    localization_prefixes = [f"/{prefix}/" for prefix in URL_LOCALIZATION_PREFIX]

    # Classify the redirects based on the three criteria
    content_redirects = [redirect for redirect in combined_redirects if redirect[1].startswith(tuple(content_prefixes))]
    localization_redirects = [redirect for redirect in combined_redirects if redirect[1].startswith(tuple(localization_prefixes))]
    other_redirects = [redirect for redirect in combined_redirects if redirect not in content_redirects and redirect not in localization_redirects]

    # Reordering groups
    combined_redirects = content_redirects + other_redirects

    # If there are localization redirects, inform the user and ask for action
    if localization_redirects:
        print("\nThe following localization redirects were detected and need to be removed.")
        for line_num, from_url, _, _ in localization_redirects:
            print(f"Line {line_num}: {from_url}")

        user_input = input("\nDo you want to delete these localization redirects? (y/n): ")
        if user_input.lower() == 'y':
            print("Localization redirects have been removed.")
        else:
            combined_redirects += localization_redirects
            print("Localization redirects were retained.")
    else:
        print("\nNo localization redirects (good to go).\n")

    # Write the combined list back to the CSV file  
    write_redirects_to_csv(combined_redirects, 'gen-redirects.csv')

    # Localize redirections for each language (replicate redirects for English URL)
    print("\n[Step 4] Localizing redirects for each language... (by replicating redirects).\n")
    localized_content_redirects = []

    for prefix in URL_LOCALIZATION_PREFIX:
        for line_num, from_url, to_url, status in content_redirects:
            if to_url.startswith("/"):
                localized_from_url = f"/{prefix}{from_url}"
                localized_to_url = f"/{prefix}{to_url}"
                localized_content_redirects.append((line_num, localized_from_url, localized_to_url, status))

    # Combine all the redirect lists for the _redirects file
    print("\n[Step 5] Updating [_redirects] file.\n")
    all_redirects_for_file = content_redirects + localized_content_redirects + other_redirects
    write_redirects_to_file(all_redirects_for_file, '_redirects')

    print("\n[Process Completed Successfully]")
    with open('_redirects', 'r') as file:
        line_count = sum(1 for _ in file)
        print(f"Total: {line_count} redirects. (see _redirects file for details)\n")

if __name__ == "__main__":
    main()