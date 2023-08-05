import os
import json
import argparse
from gpt4all import GPT4All
from prettytable import PrettyTable
from datetime import datetime
from console_progressbar import ProgressBar


def main():
    parser = argparse.ArgumentParser(description="check.py")
    parser.add_argument(
        "--model",
        help="Model name",
        default="orca-mini-3b.ggmlv3.q4_0.bin"
    )
    parser.add_argument(
        "--file",
        help="File path to analyze"
    )
    parser.add_argument(
        "--all",
        help="Include all files and folders",
        action='store_true'
    )
    parser.add_argument(
        "--output",
        help="Output type",
        default="text"
    )
    parser.add_argument(
        "--export",
        help="Export to file"
    )
    parser.add_argument(
        "--export-folder",
        help="Export to folder"
    )

    args = parser.parse_args()
    model_name = args.model
    scan_all = args.all
    output_type = args.output
    export = args.export
    export_folder = args.export_folder
    if export_folder is None and export is not None:
        export_folder = "code_review_results"
    else:
        export_folder = None
    model = GPT4All(model_name)


    all_files = gather_files(args.file, scan_all)
    print("Number of scanning files:", len(all_files))

    results = process_files(all_files, model)
    export_results(results, export_folder, output_type)


def export_as_text(results, export_folder):
    t = PrettyTable(['File path', 'Suggestions'])
    for result in results:
        t.add_row(result)
    t.align = "l"
    t._max_width = {"File path": 50, "Suggestions": 100}
    print(t)
    if export_folder:
        filename = f"review-{datetime.now().strftime('%Y%m%d-%H%M%S')}.txt"
        with open(os.path.join(export_folder, filename), "w") as f:
            f.write(t.get_string())

def export_as_json(results, export_folder):
    print(json.dumps(results))
    if export_folder:
        filename = f"review-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
        with open(os.path.join(export_folder, filename), "w") as f:
            json.dump(results, f)

def export_as_xml(results, export_folder):
    xml_content = "<results>" + "".join(f"<result><file_path>{result[0]}</file_path><suggestions>{result[1]}</suggestions></result>" for result in results) + "</results>"
    print(xml_content)
    if export_folder:
        filename = f"review-{datetime.now().strftime('%Y%m%d-%H%M%S')}.xml"
        with open(os.path.join(export_folder, filename), "w") as f:
            f.write(xml_content)

def export_results(results, export_folder, output_type):
    if export_folder and not os.path.exists(export_folder):
        os.makedirs(export_folder)

    if output_type == "text":
        export_as_text(results, export_folder)
    elif output_type == "json":
        export_as_json(results, export_folder)
    elif output_type == "xml":
        export_as_xml(results, export_folder)
    else:
        print("Unknown output type")

def process_files(all_files, model):
    results = []
    system_template = 'Imagine that you are a developer, and you are reviewing the code of a junior. You should give short suggestions for improving the code.'


    total_files = len(all_files)
    current_file = 0
    pb_files = ProgressBar(total=100, prefix='Files', suffix='', decimals=3, length=100, fill='X',
                     zfill='-')

    for file_path in all_files:
        try:
            current_file += 1
            print("Processing file: " + file_path + " (" + str(current_file) +"/"+ str(total_files) + ")")
            if current_file == 1:
                current_progress_files = 0
            pb_files.print_progress_bar(current_progress_files)

            with open(file_path, "r", encoding='utf-8', errors='replace') as f:
                file_content = f.read()
                file_name = os.path.basename(file_path)
                content_chunks = [file_content[i:i+1900] for i in range(0, len(file_content), 1900)]
                print(" number of chunks:", len(content_chunks))
                suggestions = []
                chunk_number = 0
                total_chunks = len(content_chunks)
                pb_chunks = ProgressBar(total=100, prefix='Chunks', suffix='', decimals=3,
                                       length=100, fill='X',
                                       zfill='-')
                for chunk in content_chunks:
                    chunk_number += 1
                    if chunk_number == 1:
                        current_progress_chunks = 0

                    pb_chunks.print_progress_bar(current_progress_chunks)
                    print("     chunk number:", chunk_number)
                    prompt = f"The file '{file_name}' (chunk '{str(chunk_number)}') contains: {chunk}. Could you give some recommendations for improving the code? and sorting suggestions list by priority from hight to low"

                    with model.chat_session(system_template):
                        response = model.generate(prompt=prompt, temp=0, max_tokens=1000)
                        current_progress_chunks = chunk_number / total_chunks * 100
                        suggestion = response.lstrip().replace("Sure", "").replace("Sure, ", "").replace("!", "")
                        suggestions.append(suggestion)
                pb_chunks.print_progress_bar(100)
                combined_suggestion = ""
                for i in range(len(suggestions)):
                    combined_suggestion += str(i+1) + ". " + suggestions[i] + "\n"
                current_progress_files = current_file / total_files * 100
                pb_files.print_progress_bar(current_progress_files)
                results.append([file_path.replace(os.getcwd(), ""), combined_suggestion])

        except Exception as e:
            print(e)

    return results

def gather_files(scan_file, scan_all):
    all_files = []

    if scan_all:
        for path, _, files in os.walk(os.getcwd()):
            all_files.extend(
                os.path.join(path, name) for name in files
            )

    if scan_file:
        all_files.append(os.path.join(os.getcwd(), scan_file))

    return all_files

if __name__ == "__main__":
    main()
