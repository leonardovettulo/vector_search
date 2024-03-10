import os

import requests


def download_html_page(url: str, save_folder: str) -> str | None:
    """
    Downloads and saves the HTML content of a webpage to a specified folder.

    Args:
        url (str): The URL of the webpage to download.
        save_folder (str): The path to the folder where the file should be saved.

    Returns:
        str | None: The filename where the HTML content was saved,
        or None if the download failed.
    """
    try:
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)

        # Get the last part of the url to get the file name
        filename = f"{url.split('/')[-1]}.html"
        filepath = os.path.join(save_folder, filename)

        response = requests.get(url)

        if response.status_code == 200:
            with open(filepath, "w", encoding="utf-8") as file:
                file.write(response.text)
            print(f"HTML content of {url} has been saved to {filepath}")
            return filepath
        else:
            print(
                f"Failed to retrieve the website. Status code: {response.status_code}"
            )
            return None
    except requests.RequestException as e:
        print(f"Request Exception error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    return None


if __name__ == "__main__":

    url_to_download = "https://en.wikipedia.org/wiki/Rules_of_chess"
    save_directory = "./data"
    download_html_page(url_to_download, save_directory)
