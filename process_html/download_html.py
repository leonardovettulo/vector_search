import os

import requests


def download_html_page(url_list: list[str], save_folder: str):
    """
    Downloads and saves the HTML content of a webpage to a specified folder.

    Args:
        url (str): The URL of the webpage to download.
        save_folder (str): The path to the folder where the file should be saved.

    Returns:
        None
    """
    try:
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)

        for url in url_list:
            # Get the last part of the url to get the file name
            filename = f"{url.split('/')[-1]}.html"
            filepath = os.path.join(save_folder, filename)

            response = requests.get(url)
            print(filepath)
            if response.status_code == 200:
                with open(filepath, "w", encoding="utf-8") as file:
                    file.write(response.text)
                print(f"HTML content of {url} has been saved to {filepath}")
            else:
                print(
                    f"Failed to retrieve the website. Status code: {response.status_code}"
                )
    except requests.RequestException as e:
        print(f"Request Exception error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    return None


if __name__ == "__main__":

    url_list = [
        "https://en.wikipedia.org/wiki/Rules_of_chess",
        "https://en.wikipedia.org/wiki/Abstract_strategy_game",
        "https://en.wikipedia.org/wiki/Checkmate",
        "https://en.wikipedia.org/wiki/History_of_chess",
        "https://en.wikipedia.org/wiki/Fischer_random_chess",
    ]

    save_directory = "./data"
    download_html_page(url_list, save_directory)
