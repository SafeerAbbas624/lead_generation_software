import csv
import re
import datetime



def write_to_csv(contact_details):
    fieldnames = ['Company Name', 'Url Link', 'Keyword Selected', 'Phone', 'Email', 'Address', 'Person Name']
    if not contact_details:
        print("No data to write to CSV file")
        return
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    csv_file = f"output_{current_datetime}.csv"
    with open(csv_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        for detail in contact_details:
            cleaned_detail = {}
            for key, value in detail.items():
                if isinstance(value, list):
                    value = ', '.join(str(v) for v in value)  # Join list elements with commas
                cleaned_detail[key] = value
            writer.writerow(cleaned_detail)
    print(f"Contact details written to {csv_file}")