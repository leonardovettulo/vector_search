import json
from unittest.mock import mock_open, patch

from search.vectorizer.parse_html import (
    get_html_files,
    parse_html_files_to_chunks,
    parse_html_to_chunks,
)


def test_get_html_files_with_mixed_content(tmp_path):
    html_file = tmp_path / "test.html"
    non_html_file = tmp_path / "test.txt"
    html_file.write_text("<html></html>")
    non_html_file.write_text("This is a text file.")

    result = get_html_files(str(tmp_path))

    assert len(result) == 1
    assert "test.html" in result


def test_parse_html_to_chunks_valid_content():
    html_content = """
<html>
<head><title>Test Page</title></head>
<body id="bodyContent">
<h2>Subtitle 1</h2>
<p>This is a paragraph with more than fifty characters to ensure it's captured.</p>
</body>
</html>
"""
    with patch("builtins.open", mock_open(read_data=html_content)):
        result = parse_html_to_chunks("dummy.html", "/dummy/path")

    assert len(result) == 1
    assert result[0]["title"] == "Test Page"
    assert "This is a paragraph" in result[0]["content"]


def test_parse_html_files_to_chunks_integration(tmp_path):
    # Setup: Create a mock HTML file in a temporary directory
    html_file_path = tmp_path / "test.html"
    html_file_path.write_text(
        """
<html>
<head><title>Test Page</title></head>
<body id="bodyContent">
<h2>Subtitle 1</h2>
<p>This is a paragraph with more than fifty characters to ensure it's captured.</p>
</body>
</html>
"""
    )

    # Mocking the output JSON file path
    output_json_path = tmp_path / "chunks.json"

    # Call the adjusted function with the output JSON file path
    chunks_count = parse_html_files_to_chunks(
        folder_path=str(tmp_path), output_json_path=str(output_json_path)
    )

    # Assertions
    assert output_json_path.exists(), "The output JSON file was not created."
    assert chunks_count > 0, "No chunks were processed."

    # Read the generated JSON file
    with open(output_json_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    assert len(data) == 1, "Unexpected number of chunks processed."
    assert data[0]["title"] == "Test Page", "The title in the chunk does not match."
    assert (
        "This is a paragraph" in data[0]["content"]
    ), "The content in the chunk does not match expected text."
