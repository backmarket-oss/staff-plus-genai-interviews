import logging
import os

from src.llm import configure

from langchain.prompts import load_prompt

logging.basicConfig(level=logging.INFO)


def read_and_concat_interviews_content(
    directory_path: str = f"{os.path.dirname(os.path.dirname(os.path.realpath(__file__)))}/interviews/refinement",
) -> str:
    """
    Read and concatenate all the interviews content from the directory.

    :param directory_path: The directory path where the interviews content is stored.
    :return: The concatenated interviews content.
    """
    logging.info(f"Reading and concatenating interviews content from {directory_path}")
    interviews_content = []
    for file_name in os.listdir(directory_path):
        if file_name.endswith(".txt"):
            with open(os.path.join(directory_path, file_name), "r") as file:
                interviews_content.append("--- BEGIN INTERVIEW ---\n")
                interviews_content.append(file.read())
                interviews_content.append("--- END INTERVIEW ---\n")
    return "".join(interviews_content)


def write_result_to_file(result: str, path: str = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))) -> None:
    """
    Write the result to a file.

    :param path: The path to write the file.
    :param result: The result to write to a file.
    """
    logging.info(f"Write the results to: {path}")
    out_dir = os.path.join(path, "out")
    os.makedirs(out_dir, exist_ok=True)
    with open(f"{path}/out/extract_and_summarize_interviews_content.md", "w") as file:
        file.write(result)


def main() -> None:
    """
    Main function top run the script.
    """
    path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    prompt_file_path = f"{path}/prompts/extract_and_summarize_interviews_content.yaml"
    logging.info(f"Load the prompt from: {prompt_file_path}")
    prompt_template = load_prompt(path=prompt_file_path)

    interviews_content = read_and_concat_interviews_content()
    client = configure()
    model = os.environ.get("GENAI_MODEL", "google/gemini-1.5-pro")
    logging.info(f"Configure the OpenAI client with model: {model}  ")
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt_template.format(interviews_content=interviews_content),
            }
        ],
        temperature=float(os.environ.get("GENAI_TEMPERATURE", 1.0)),
        max_tokens=int(os.environ.get("GENAI_MAX_TOKENS", 8192)),
    )
    write_result_to_file(result=response.choices[0].message.content)


if __name__ == "__main__":
    main()
