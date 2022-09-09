import argparse
from PyPDF2 import PdfFileReader, PdfFileWriter
import os
from os import listdir
from os.path import isfile, join

def get_page(pdf, i):
    current_page = pdf.getPage(i)
    text = current_page.extractText()
    page = text[len(text)-5:]
    return page

def simplify(args, file_name):
    with open(os.path.join(args.pdf_dir, file_name), 'rb') as f:
        pdf = PdfFileReader(f)
        num_pages = pdf.numPages
        saved_page = []
        i = 0
        while i < num_pages:
            start = i
            p_page = get_page(pdf, i)
            page = p_page
            while page == p_page:
                i += 1
                if i >= num_pages-1: break
                page = get_page(pdf, i)
            # first page
            saved_page.append(start)
            # last page
            if start != i-1: saved_page.append(i-1)

        # create a new pdf object
        new_pdf = PdfFileWriter()
        for p in saved_page:
            new_pdf.addPage(pdf.getPage(p))

        with open(os.path.join(args.output_dir, file_name), 'wb') as output_file:
            new_pdf.write(output_file)

        print(f"simplified pdf created: {args.output_dir}/{file_name}, Pages: {num_pages} -> {len(saved_page)}")

    return 


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--pdf_dir', type=str, default='./origin_file')
    parser.add_argument('--output_dir', type=str, default='./sim_file')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    files = [f for f in listdir(args.pdf_dir) if isfile(join(args.pdf_dir, f))]
    for file_name in files:
        simplify(args, file_name)