import os
import tempfile

from src.main import read_and_concat_interviews_content
from src.main import write_result_to_file


def test_read_and_concat_interviews_content():
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "tests/interviews")
    result = read_and_concat_interviews_content(directory_path=path)
    assert result == """--- BEGIN INTERVIEW ---
Florian:
    Hello everyone, this is the second interview, how are you doing?

Interviewer2:
    I'm doing well, thank you for asking.
--- END INTERVIEW ---
--- BEGIN INTERVIEW ---
Florian:
    Hello everyone, this is the first interview, how are you doing?

Interviewer1:
    I'm doing great, thank you for asking. How about you?
--- END INTERVIEW ---
"""


def test_write_result_to_file():
    with tempfile.TemporaryDirectory() as temp_dir:
        write_result_to_file(result="test", path=temp_dir)

        expected_file_path = os.path.join(temp_dir, "out", "extract_and_summarize_interviews_content.md")

        with open(expected_file_path, 'r') as file:
            content = file.read()
            assert content == "test"
