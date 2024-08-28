import customtkinter as ctk
import threading
from CTkMessagebox import CTkMessagebox
from main import start_scraping

def run_gui():
    app = ctk.CTk()
    app.geometry("400x300")
    app.title("Manga Scraper")

    def on_scrape_button_click():
        url = url_entry.get()
        file_path = file_entry.get()
        if url:
            threading.Thread(target=scrape_and_notify, args=([url],)).start()
        elif file_path:
            with open(file_path, 'r') as f:
                urls = [line.strip() for line in f.readlines()]
            threading.Thread(target=scrape_and_notify, args=(urls,)).start()
        else:
            CTkMessagebox(title="Error", message="Please enter a URL or select a file.", icon="cancel")

    def scrape_and_notify(urls):
        try:
            start_scraping(urls)
            CTkMessagebox(title="Download Complete", message="All chapters have been downloaded successfully!")
        except Exception as e:
            CTkMessagebox(title="Error", message=f"An error occurred: {e}", icon="cancel")

    guide_label = ctk.CTkLabel(app, text="Visit Manganato.com to get the manga link.")
    guide_label.pack(pady=10)

    url_label = ctk.CTkLabel(app, text="Enter the URL of the manga to scrape:")
    url_label.pack(pady=10)

    url_entry = ctk.CTkEntry(app, width=300)
    url_entry.pack(pady=10)

    file_label = ctk.CTkLabel(app, text="Or select a file with manga URLs:")
    file_label.pack(pady=10)

    file_entry = ctk.CTkEntry(app, width=300)
    file_entry.pack(pady=10)

    scrape_button = ctk.CTkButton(app, text="Scrape", command=on_scrape_button_click)
    scrape_button.pack(pady=10)

    app.mainloop()

if __name__ == "__main__":
    run_gui()
