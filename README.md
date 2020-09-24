# PDF TOC Builder
PDF TOC miner compiles a list of headings from a list of markdown docs repositories and then cross references those headings with a PDF file in order to build a table of contents as a CSV. 

## Overview

In this repository is a config.py file. Open the file and add the path to the folders containing markdown content files for a static site builder such as Hugo or DocFX. The main script parses the files to create a list of H1 level headings (`# heading`). The script then parses the PDF and then cross references each heading with it's corresponding page in the PDF and produces a CSV file that you can use to create a table of contents based on the headings in the PDF.

**Input**:

Markdown repository path in a file name `config.py`.

**Output**:

A CSV file with the following output:

| title | page |
| --- | --- |
| heading 1 one | 1 |
| heading 1 two | 2 |
| heading 1 three | 3 |

## To run this script

1. You will need Python 3.6 or greater and the Python package manager Pip. Pip is usually installed with Python.

2. Install the modules in the` requiements.txt` file using **pip**.

    ```
    pip install -r /path/to/requirements.txt
    ```

3. Create a file named `config.py` in the project with the following global variable:

    ```python
    SUBFOLDERS = [r"\path-to-repo1",
                  r"C\path-to-repo2",
                  r"\path-to-repo3"]
    ```

3. Run the script.

    ```
    python pdf-toc-builder.py
    ```

4. Type the path and filename, and type the CSV output. The script prints in the terminal its progress in the PDF.

## Issues and stuff

If you have issues, please make an issue in this repo. Thanks.
