import os
from typing import Any

from bs4 import BeautifulSoup


def get_html_files(folder_path: str) -> list[str]:
    """
    Retrieves a list of all HTML files within a given folder and its subdirectories.

    Parameters:
    - folder_path (str): The path to the folder where to search for HTML files.

    Returns:
    - list[str]: A list of paths to the HTML files found within the specified folder.
    """
    html_files: list[str] = []

    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".html"):
                html_files.append(file)

    return html_files


def parse_html_to_chunks(filename: str, folder: str) -> list[dict[str, str]]:
    """
    Parses HTML content from a file and extracts chunks of information
    including title, subtitles, and content.

    Parameters:
    - filename (str): The name of the HTML file to be parsed.
    - folder (str): The path of the file

    Returns:
    - list[dict[str, str]]: A list of dictionaries containing the title,
      subtitle, and content for each extracted chunk.
    """
    chunks: list[dict[str, str]] = []

    filename = os.path.join(folder, filename)

    try:
        with open(filename, "r", encoding="utf-8") as file:
            html_content = file.read()

        soup = BeautifulSoup(html_content, "lxml")

        title: str = soup.title.string if soup.title else "No title found"

        ignore_subtitles = [
            "External links",
            "External links[edit]",
            "Further reading",
            "Bibliography",
            "References",
            "See also",
            "Contents",
        ]

        current_subtitle: str | None = None
        content_started: bool = False

        for node in soup.find(id="bodyContent").find_all(["h2", "h3", "p", "ul", "ol"]):
            if node.name in ["h2", "h3"]:
                current_subtitle = (
                    node.text.strip()
                    if node.text.strip() not in ignore_subtitles
                    else None
                )
                content_started = True
            elif current_subtitle or not content_started:
                content_text: str = ""
                if node.name == "p":
                    content_text = node.text.strip()
                elif node.name in ["ul", "ol"]:
                    content_text = " ".join(
                        li.text.strip() for li in node.find_all("li")
                    )

                # We are extracting chunks that contain at least 50 chars
                if content_text and len(content_text) > 50:
                    chunks.append(
                        {
                            "title": title,
                            "subtitle": (
                                current_subtitle
                                if current_subtitle
                                else f"{title} - Introduction"
                            ),
                            "content": content_text,
                        }
                    )

    except Exception as e:
        raise RuntimeError(f"Failed to parse HTML content: {e}") from e

    return chunks


if __name__ == "__main__":

    PATH = "./data"

    chunks = []
    for file in get_html_files(folder_path=PATH):
        chunks.extend(parse_html_to_chunks(filename=file, folder=PATH))

    print(chunks)
