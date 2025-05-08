import os
import json
import argparse
from gpt4all import GPT4All
from prettytable import PrettyTable
from datetime import datetime
from console_progressbar import ProgressBar

DEFAULT_MODEL_NAME = "orca-mini-3b.ggmlv3.q4_0.bin"
SYSTEM_TEMPLATE = (
    "Imagine that you are a developer, and you are reviewing the code of a junior. "
    "You should give short suggestions for improving the code."
)


class CodeAnalyzer:
    def __init__(self, model_name, scan_all, output, export, export_folder):
        self.model_name = model_name
        self.scan_all = scan_all
        self.output_type = output
        self.export = export
        self.export_folder = export_folder or "code_review_results" if export else None
        self.model = GPT4All(model_name)

    def gather_files(self, scan_file):
        all_files = []

        if self.scan_all:
            for path, _, files in os.walk(os.getcwd()):
                all_files.extend(os.path.join(path, name) for name in files)

        if scan_file:
            all_files.append(os.path.join(os.getcwd(), scan_file))

        return all_files

    def process_files(self, all_files):
        results = []
        total_files = len(all_files)
        pb_files = ProgressBar(
            total=100,
            prefix="Files",
            suffix="",
            decimals=3,
            length=100,
            fill="X",
            zfill="-",
        )

        for idx, file_path in enumerate(all_files, 1):
            print(f"Processing file: {file_path} ({idx}/{total_files})")
            results.append(self.process_file(file_path, idx, total_files, pb_files))

        return results

    def process_file(self, file_path, file_index, total_files, pb_files):
        try:
            with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                file_content = f.read()
            file_name = os.path.basename(file_path)
            content_chunks = self.get_chunks(file_content)
            suggestions = self.get_suggestions(file_name, content_chunks)

            pb_files.print_progress_bar((file_index / total_files) * 100)
            return [file_path.replace(os.getcwd(), ""), "\n".join(suggestions)]
        except Exception as e:
            print(e)

    @staticmethod
    def get_chunks(file_content, chunk_size=1900):
        return [
            file_content[i : (i + chunk_size)] for i in range(0, len(file_content), chunk_size)
        ]

    def get_suggestions(self, file_name, content_chunks):
        total_chunks = len(content_chunks)
        pb_chunks = ProgressBar(
            total=100,
            prefix="Chunks",
            suffix="",
            decimals=3,
            length=100,
            fill="X",
            zfill="-",
        )
        suggestions = []

        for idx, chunk in enumerate(content_chunks, 1):
            pb_chunks.print_progress_bar((idx / total_chunks) * 100)
            prompt = (
                f"The file '{file_name}' (chunk '{str(idx)}') contains: {chunk}. "
                f"Could you give some recommendations for improving the code? "
                f"and sorting suggestions list by priority from hight to low"
            )

            with self.model.chat_session(SYSTEM_TEMPLATE):
                response = self.model.generate(prompt=prompt, temp=0, max_tokens=1000)
                suggestion = (
                    response.lstrip().replace("Sure", "").replace("Sure, ", "").replace("!", "")
                )
                suggestions.append(suggestion)

        return suggestions

    def export_results(self, results):
        if self.export_folder and not os.path.exists(self.export_folder):
            os.makedirs(self.export_folder)

        exporters = {
            "plain": self.export_as_plain_text,
            "txt": self.export_as_text_table,
            "json": self.export_as_json,
            "xml": self.export_as_xml,
        }
        export_func = exporters.get(self.output_type, lambda *args: print("Unknown output type"))
        export_func(results)

    def export_as_plain_text(self, results):
        print("\n".join(f"{result[0]}: {result[1]}" for result in results))
        if self.export_folder:
            self.write_to_file(
                "\n".join(f"{result[0]}: {result[1]}" for result in results), ".txt"
            )

    def export_as_text_table(self, results):
        t = PrettyTable(["File path", "Suggestions"])
        for result in results:
            t.add_row(result)
        t.align = "l"
        t._max_width = {"File path": 50, "Suggestions": 100}
        print(t)
        if self.export_folder:
            self.write_to_file(t.get_string(), ".txt")

    def export_as_json(self, results):
        print(json.dumps(results))
        if self.export_folder:
            self.write_to_file(json.dumps(results), ".json")

    def export_as_xml(self, results):
        xml_content = (
            "<results>"
            + "".join(
                f"<result><file_path>{result[0]}</file_path>"
                f"<suggestions>{result[1]}</suggestions></result>"
                for result in results
            )
            + "</results>"
        )
        print(xml_content)
        if self.export_folder:
            self.write_to_file(xml_content, ".xml")

    def write_to_file(self, content, extension):
        filename = f"review-{datetime.now().strftime('%Y%m%d-%H%M%S')}{extension}"
        with open(os.path.join(self.export_folder, filename), "w") as f:
            f.write(content)


def parse_arguments():
    parser = argparse.ArgumentParser(description="gpt4all_code_review")
    parser.add_argument(
        "--model",
        help="Specifies the model name. Default is orca-mini-3b.ggmlv3.q4_0.bin",
        default=DEFAULT_MODEL_NAME,
    )
    parser.add_argument(
        "--file",
        help="Specifies the file path to analyze. If not provided, "
        "all files in the current directory will be analyzed",
    )
    parser.add_argument(
        "--all",
        help="Includes all files and folders in the current directory for scanning",
        action="store_true",
    )
    parser.add_argument(
        "--output",
        help="Output type (default: plain). Options: plain, txt (prettytable), json, xml",
        default="plain",
    )
    parser.add_argument("--export", help="Export to file (default: False)")
    parser.add_argument(
        "--export-folder", help="Export to folder (default: ./code_review_results)"
    )

    return parser.parse_args()


def main():
    args = parse_arguments()
    analyzer = CodeAnalyzer(args.model, args.all, args.output, args.export, args.export_folder)

    all_files = analyzer.gather_files(args.file)
    print("Number of scanning files:", len(all_files))

    results = analyzer.process_files(all_files)
    analyzer.export_results(results)


if __name__ == "__main__":
    main()
