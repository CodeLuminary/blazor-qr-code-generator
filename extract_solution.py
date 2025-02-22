import re
from typing import List, Tuple


def extract_code_blocks(
    markdown_text: str,
    languages: List[str] = ['javascript', 'jsx', 'css', 'xaml', 'xml', 'csharp', 'razor', 'html'],
    include_markers: bool = False
) -> List[Tuple[str, str]]:
    """
    Extracts code blocks and their associated filenames from markdown text for specified languages.

    Args:
        markdown_text (str): The text containing code blocks.
        languages (List[str]): A list of languages to extract. Defaults to ['javascript', 'jsx', 'css'].
        include_markers (bool): Whether to include the code block markers. Defaults to False.

    Returns:
        List[Tuple[str, str]]: A list of tuples, each containing the filename and the extracted code block.
    """
    language_pattern = '|'.join(map(re.escape, languages))
    code_block_pattern = re.compile(
        rf'```({language_pattern})\s*\n(.*?)```', re.DOTALL)

    matches = code_block_pattern.findall(markdown_text)

    extracted_blocks = []
    for lang, block in matches:
        block = block.strip()
        filename = f'unknown.{lang}'
        code = block

        if lang in languages:
            # Look for single-line comments starting with //
            lines = block.split('\n')
            if lines and lines[0].strip().startswith('//'):
                # Extract filename from the comment
                filename_match = re.match(r'//\s*(.+)', lines[0].strip())
                if filename_match:
                    filename = filename_match.group(1).strip()
                    code = '\n'.join(lines[1:]).strip()
            # hanlde comments like /* --- */
            elif lines and lines[0].strip().startswith('/*'):
                # Extract filename from the comment
                filename_match = re.match(
                    r'\/\*\s*\.\/(.+?)\s*\*\/', lines[0].strip())
                if filename_match:
                    filename = filename_match.group(1).strip()
                    code = '\n'.join(lines[1:]).strip()

        if include_markers:
            code = f"```{lang}\n{code}\n```"

        extracted_blocks.append((filename, code))

    return extracted_blocks


def extract_solution(llm_response: str) -> List[Tuple[str, str]]:
    """
    Extracts a list of file paths and code file contents from the LLM's response.

    Args:
        llm_response (str): The response containing code blocks.

    Returns:
        List[Tuple[str, str]]: A list of tuples (file_path, file_content).
    """
    extracted_blocks = extract_code_blocks(llm_response)
    return [
        (f"{filename}", code)
        for filename, code in extracted_blocks
    ]
