# Code Review Automation Tool

This program is designed to assist developers by automating the process of code review. By leveraging a pre-trained standalone machine learning model (e.g., GPT-4), it reads source code files and provides suggestions for improvements.

## Features

- **File Scanning:** Ability to scan a single file or all files in the current directory.
- **Multiple Output Formats:** Results can be exported as plain text, JSON, or XML files.
- **Customizable Model:** Utilizes a customizable language model, allowing users to select the appropriate model for their needs.

## Installation

Make sure you have Python 3.x installed.

```bash
pip install -r requirements.txt
```
or
```bash
pip3 install -r requirements.txt
```

## Usage

You can run the program from the command line with various options:

```bash
gpt4all_code_review --file <file_path> --all
```

### Options

- `h`, `--help`: Show this help message and exit
- `--model`: Specifies the model name. Default is `"orca-mini-3b.ggmlv3.q4_0.bin"`.
- `--file`: Specifies the file path to analyze. If not provided, all files in the current directory will be analyzed.
- `--all`: Includes all files and folders in the current directory for scanning.
- `--output`: Output type (default: `txt`). Options: `txt`, `json`, `xml`.
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

- **Text:** A human-readable table with file paths and suggestions.
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
