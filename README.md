[![PyPI version](https://badge.fury.io/py/gpt4all-code-review.svg)](https://badge.fury.io/py/gpt4all-code-review)
[![Downloads](https://static.pepy.tech/personalized-badge/gpt4all-code-review?period=total&units=international_system&left_color=black&right_color=green&left_text=Downloads)](https://pepy.tech/project/gpt4all-code-review)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![PyPI format](https://img.shields.io/pypi/format/gpt4all-code-review.svg)](https://pypi.python.org/pypi/gpt4all-code-review/)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-blue)](https://www.linkedin.com/in/eugene-evstafev-716669181/)

# Code Review Automation Tool

This program is designed to assist developers by automating the process of code review. By leveraging a pre-trained standalone machine learning model (e.g., GPT-4), it reads source code files and provides suggestions for improvements.

## Features

- **File Scanning:** Ability to scan a single file or all files in the current directory.
- **Multiple Output Formats:** Results can be exported as plain text, JSON, or XML files.
- **Customizable Model:** Utilizes a customizable language model, allowing users to select the appropriate model for their needs.

## Installation

Make sure you have Python 3.x installed.

```bash
pip install gpt4all-code-review
```

For updates, use:

```bash
pip install gpt4all-code-review --upgrade
```

## Usage

You can run the program from the command line with various options:

```bash
gpt4all_code_review --file <file_path>
```

### Options

- `h`, `--help`: Show this help message and exit
- `--model`: Specifies the model name. Default is `"orca-mini-3b.ggmlv3.q4_0.bin"`.
- `--file`: Specifies the file path to analyze. If not provided, all files in the current directory will be analyzed.
- `--all`: Includes all files and folders in the current directory for scanning.
- `--output`: Output type (default: `plain`). Options: `plain`, `txt` (prettytable), `json`, `xml`.
- `--export`: Export to file (default: `False`).
- `--export-folder`: Export to folder (default: `./code_review_results`).
### Example

To analyze a single file:

```bash
gpt4all_code_review --file=./path/to/yourfile.py
```

To analyze all files in the current directory:

```bash
gpt4all_code_review --all
```

## Output Formats

- **PLAIN:** A human-readable plain txt file.
- **TXT:** A human-readable table (prettytable) with file paths and suggestions.
- **JSON:** A machine-readable format that can be parsed programmatically.
- **XML:** An alternative machine-readable format.

## Dependencies

-   `os`: Standard Python library for interacting with the operating system.
-   `json`: Standard Python library for working with JSON data.
-   `argparse`: Standard Python library for parsing command-line arguments.
-   `gpt4all`: A Python library for interfacing with GPT-4 models. Used to apply the AI models to the code.
-   `prettytable`: A Python library to print tabular data in a visually appealing ASCII table format.
-   `datetime`: Standard Python library for working with dates and times.
-   `console_progressbar`: A Python library for displaying progress bars in the console.

## License

MIT License
