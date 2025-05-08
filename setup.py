from setuptools import setup, find_packages

setup(
    name="gpt4all-code-review",
    version="2025.5.9.1718",
    packages=find_packages(),
    install_requires=[
        "argparse",
        "gpt4all",
        "prettytable",
        "datetime",
        "console_progressbar",
    ],
    author="Evgenii Evstafev",
    author_email="chigwel@gmail.com",
    description="A self-contained tool for code review powered by GPT4ALL.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/chigwell/gpt4all-code-review",
    entry_points={
        "console_scripts": [
            "gpt4all_code_review = gpt4all_code_review.gpt4all_code_review:main",
        ],
    },
)
