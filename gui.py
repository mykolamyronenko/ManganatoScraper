import customtkinter as ctk
import threading
from CTkMessagebox import CTkMessagebox
from main import start_scraping
import os

def run_gui():
    app = ctk.CTk()
    app.geometry("400x300")
    app.title("Manga Scraper")

    def on_scrape_button_click():
        input_text = url_or_file_entry.get()
        if os.path.isfile(input_text):
            with open(input_text, 'r') as f:
                urls = [line.strip() for line in f.readlines()]
            threading.Thread(target=scrape_and_notify, args=(urls,)).start()
        else:
            threading.Thread(target=scrape_and_notify, args=([input_text],)).start()

    def scrape_and_notify(urls):
        try:
            start_scraping(urls, update_progress)
            CTkMessagebox(title="Download Complete", message="All chapters have been downloaded successfully!")
        except Exception as e:
            CTkMessagebox(title="Error", message=f"An error occurred: {e}", icon="cancel")

    def update_progress(value, max_value):
        progress_bar.set(value / max_value)

    guide_label = ctk.CTkLabel(app, text="Enter the URL of the manga or the path to a file with URLs:")
    guide_label.pack(pady=10)

    url_or_file_entry = ctk.CTkEntry(app, width=300)
    url_or_file_entry.pack(pady=10)

    scrape_button = ctk.CTkButton(app, text="Scrape", command=on_scrape_button_click)
    scrape_button.pack(pady=10)

    progress_bar = ctk.CTkProgressBar(app, width=300)
    progress_bar.pack(pady=10)
    progress_bar.set(0)

    app.mainloop()

if __name__ == "__main__":
    run_gui()
