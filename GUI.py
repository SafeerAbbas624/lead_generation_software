# Import tkinter library for GUI
import tkinter as tk
# Import ttk module for themed widgets
from tkinter import ttk
# Import crawl function from crawler module
from crawler import crawl
from crawler import export_to_csv


# Define global results list
results = []
# Global variable to store the current offset
current_offset = 0
# Define search_keywords function
def search_keywords():
    global current_offset, unique_urls
    keywords = keywords_entry.get()
    filters = filters_entry.get()
    unique_urls, current_offset = crawl(keywords, filters, current_offset)
    if len(unique_urls) == 0:
        print('\n This is to inform you that your Bing API is not responding due to Quota Exceeded Error.\nPlease upgrade your plan or buy new plan.\n')
        raise Exception
    else:
        show_page(current_page)
    total_count_label.config(text=f"Total URLs: {len(unique_urls)}\nThere are 50 URLs on each page.")

# Generate popup on completion of CSV export
def generate_popup(message):
    popup = tk.Toplevel(root)
    popup.title("Completed")
    label = tk.Label(popup, text=message)
    label.pack(fill="x", pady=10)
    button = tk.Button(popup, text="OK", command=popup.destroy)
    button.pack(fill="x", pady=10)

# CSV export file button
def export_to_csv_button():
    gui_keyword = keywords_entry.get()
    export_to_csv(unique_urls, gui_keyword)
    generate_popup("CSV file exported successfully. \nGo to the same directory to find the output file.")

# Create Tkinter root window
root = tk.Tk()
# Set window title
root.title("Lead generation software (v1.2)")
# Set window size
root.geometry("800x850")

# Create main frame with padding
main_frame = ttk.Frame(root, padding="10")
# Pack main frame to fill window
main_frame.pack(fill="both", expand=True)

# Create label for keywords
keywords_label = ttk.Label(main_frame, text="Keywords: \nWrite your keywords with commas in between if there are more than one.")
# Pack label with padding
keywords_label.pack(fill="x", pady=10)
# Create entry field for keywords
keywords_entry = ttk.Entry(main_frame, width=50)
# Pack entry field with padding
keywords_entry.pack(fill="x", pady=10)

# Create label for filters
filters_label = ttk.Label(main_frame, text="Filter: \nThis field is for negative words.")
# Pack label with padding
filters_label.pack(fill="x", pady=10)
# Create entry field for filters
filters_entry = ttk.Entry(main_frame, width=50)
# Pack entry field with padding
filters_entry.pack(fill="x", pady=10)

# Create search button
search_button = ttk.Button(main_frame, text="Search", command=search_keywords)
# Pack button with padding
search_button.pack(fill="x", pady=10)

# Create label for results
results_label = ttk.Label(main_frame, text="Results:")
# Pack label with padding
results_label.pack(fill="x", pady=10)
# Create text area for results
results_text = tk.Text(main_frame, width=80, height=20)
# Pack text area with padding
results_text.pack(fill="both", expand=True, pady=10)

# Export button
export_button = ttk.Button(main_frame, text="Export as CSV", command=export_to_csv_button)
export_button.pack(fill="x", pady=10)


# Create a label for total count
total_count_label = ttk.Label(main_frame, text="Total URLs: 0\nThere are 50 URLs on each page.")
total_count_label.pack(fill="x", pady=10)


# progress bar for page pagination 
def create_progress_bar(parent):
    progress_bar = tk.Canvas(parent, width=300, height=20, bg="light gray")
    progress_bar.progress_fill = progress_bar.create_rectangle(0, 0, 0, 20, fill="green")
    progress_bar.progress_text = progress_bar.create_text(300, 10, anchor="w", text="Page progress bar", justify="center", fill='white')
    return progress_bar

# Update progress bar function
def update_progress_bar(progress_bar, value, total):
    width = progress_bar.winfo_width()*2
    fill_width = int(width * value / total)
    progress_bar.itemconfig(progress_bar.progress_fill, width=fill_width,)
    progress_bar.itemconfig(progress_bar.progress_text, text=f"{value}/{total}", fill="white")
    # Force GUI update
    progress_bar.update()

# Create a progress bar
progress_bar = create_progress_bar(main_frame)
progress_bar.pack(fill="x", pady=10)



current_page = 1
results_per_page = 50

def show_page(page_number):
    global current_page
    current_page = page_number
    start_index = (page_number - 1) * results_per_page
    end_index = start_index + results_per_page

    # Update progress bar
    update_progress_bar(progress_bar, start_index + 1, len(unique_urls))

    # Clear results text area
    results_text.delete(1.0, tk.END)

    # Display results for the current page
    for url in unique_urls[start_index:end_index]:
        results_text.insert(tk.END, url + '\n')
def previous_page():
    global current_page
    if current_page > 1:
        current_page -= 1
        show_page(current_page)

def next_page():
    global current_page
    total_pages = (len(unique_urls) + results_per_page - 1) // results_per_page
    if current_page < total_pages:
        current_page += 1
        show_page(current_page)

# Create buttons for pagination
previous_button = ttk.Button(main_frame, text="Previous", command=previous_page)
previous_button.pack(side=tk.LEFT)
next_button = ttk.Button(main_frame, text="Next", command=next_page)
next_button.pack(side=tk.LEFT)


# Start Tkinter event loop
root.mainloop()