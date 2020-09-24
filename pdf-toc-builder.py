''' PDF TOC Builder
    For more information see: https://github.com/mattbriggs/pdf-toc-builder
    pdf_extract_headings.py compiles a TOC for a PDF based on the H1s in a markdown repo.

    Release V0.0.1 2020.9.23
'''

import csv
import os
from io import StringIO
import PyPDF2 as pypdf
import markdown
from bs4 import BeautifulSoup
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

import config


def get_text_from_file(path):
    '''Return text from a text filename path'''
    textout = ""
    fh = open(path, "r")
    try:
        for line in fh:
            try:
                textout += line
            except:
                print("Bad char in " + path)
    except:
        print("Bad char in " + path)
    fh.close()
    return textout


def clear_docs_repo_metadata(inrawbody, d_format="html"):
    '''With raw markdown file and docs metadata block, turn just the body as the
    indicated format, html, text, or markown'''
    meta_flag = "---"
    mleng = len(meta_flag)
    meta_end = inrawbody[inrawbody.find(meta_flag)+mleng:].find(meta_flag)+(mleng*2)
    body = inrawbody[meta_end:]
    if d_format == "html":
        out_file = markdown.markdown(body)
    elif d_format == "txt":
        html_doc = markdown.markdown(body)
        soup = BeautifulSoup(html_doc, 'html.parser')
        out_file = soup.get_text()
    else:
        out_file = body
    return out_file


def write_text(outbody, path):
    '''Write text file to the path.'''
    out_file = open(path, "w")
    for line in outbody:
        out_file.write(line)
    out_file.close()


def get_files(in_path, extension):
    '''With the directory path, returns a list of markdown file paths.'''
    outlist = []
    for (path, dirs, files) in os.walk(in_path):
        for filename in files:
            ext_index = filename.find(".")
            if filename[ext_index+1:] == extension:
                entry = path + "\\" + filename
                outlist.append(entry)
    return outlist


def get_heading(intext):
    '''With markdown text, return a list of all headings as flat list.'''
    html_doc = markdown.markdown(intext)
    soup = BeautifulSoup(html_doc, 'html.parser')
    headings_htm = soup.findAll("h1")
    headings = []
    for i in headings_htm:
        headings.append(i.text)
    if headings:
        return headings[0]
    else:
        return ""


def get_text_from_page(path_to_pdf):
    '''With a PDF path and page number, return the text.
    PDF base 0. Whereas the PDF reader is base 1. 39 is 40.'''
    # get length of PDF
    pdfobj = open(path_to_pdf, 'rb')
    pdfread = pypdf.PdfFileReader(pdfobj)
    total_pages_zerobase = pdfread.numPages
    print("Processing length: " + str(total_pages_zerobase))

    # retrieve contents as dict
    text_dict = {}
    for px in range(total_pages_zerobase):
        print("Processing.... page {}".format(px))

        # create device
        rsrcmgr = PDFResourceManager()
        retstr = StringIO()
        codec = 'utf-8'
        laparams = LAParams()
        device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        fp = open(path_to_pdf, 'rb')

        maxpages = 0
        caching = True
        pagenos = {px, px}

        for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password="", caching=caching, check_extractable=True):
            interpreter.process_page(page)

        text = retstr.getvalue()

        #close device
        fp.close()
        device.close()
        retstr.close()

        text_escape = text.replace("\n", "\\n")
        text_dict[px] = text_escape

    return text_dict


def write_csv(outbody, path):
    '''Write CSV file to the path.'''
    csvout = open(path, 'w', newline="")
    csvwrite = csv.writer(csvout)
    for r in outbody:
        csvwrite.writerow(r)
    csvout.close()


def get_titles_from_repo_paths(list_of_paths):
    '''Crawl the repository and get the titles'''
    list_of_file_paths = []
    list_of_h1s = []
    for subfolder in list_of_paths:
        new_list = get_files(subfolder, "md")
        list_of_file_paths += new_list
    for path in list_of_file_paths:
        body_all = get_text_from_file(path)
        body_content = clear_docs_repo_metadata(body_all)
        heading = get_heading(body_content)
        if heading:
            list_of_h1s.append(heading)
    dedup = set(list_of_h1s)
    list_of_headings = list(dedup)
    return list_of_h1s


def create_table_of_contents(pdf_file):
    '''get the list of headings, get the body texts from PDF, creating headings table.'''
    toc_table = [["title", "page"]]
    list_of_headings = get_titles_from_repo_paths(SUBFOLDERS)
    page_content = get_text_from_page(pdf_file)
    page_count = list(page_content.keys())
    used = []
    for p in page_count:
        for h in list_of_headings:
            if h in page_content[p]:
                if h not in used:
                    toc_table.append([h, p+1])
                    used.append(h)
    return toc_table


def main():
    '''Main logic of the script:
    1. Get the H1 from the repo branch and save as a text file.
    2. Get the PDF and create a dictionary of key values, key page number
       value page contnet.
    3. For each H1 find the page it occurs on. If it has a page, add to the TOC table.
    4. Sort the TOC table by page number.
    5. Save the TOC Table.
    5. Second phase: Add the TOC table to a word doc save the word doc.
    '''

    print("Starting")

    print("Before your run this script, you will need to update the config.py file.\n")

    pdf_file = input("Add PDF file to create PDFs > ")
    report_out = input("Path and file to save TOC (CSV) > ")
    table_of_contents = create_table_of_contents(pdf_file)

    print("Done: {}".format(report_out))

    # Generate CSV output

    csvout = open(report_out, 'w', newline="")
    csvwrite = csv.writer(csvout)
    for r in table_of_contents:
        csvwrite.writerow(r)
    csvout.close()

if __name__ == "__main__":
    main()
