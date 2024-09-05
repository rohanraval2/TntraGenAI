import itertools
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTTextLineHorizontal, LTChar
import time
import pandas as pd
import numpy as np
from pypdf import PdfReader
import os

start = time.time()

class PDFDetails:
    def __init__(self, path):
        self.path = path
        self.start = 1
        stop_pages = PdfReader(path)
        self.stop = len(stop_pages.pages)

    def start_stop_page(self, start=1, stop=0.1):
        self.start = start
        if stop != 0.1:
            self.stop = stop

    def extract_text_with_font_styles(self):
        text_with_font_styles = []

        for page_number, page_layout in enumerate(
            itertools.islice(extract_pages(self.path), self.start - 1, self.stop), start=self.start
        ):
            for element in page_layout:
                if isinstance(element, LTTextContainer):
                    for text_line in element:
                        if isinstance(text_line, LTTextLineHorizontal):
                            line_text = ""
                            line_fonts = set()
                            total_characters = 0
                            bold_characters = 0
                            previous_x1 = None
                            has_one_alpha = False

                            for character in text_line:
                                if isinstance(character, LTChar):
                                    total_characters += 1
                                    if previous_x1 is not None:
                                        gap = character.x0 - previous_x1
                                        if gap > character.size * 0.1:
                                            # Adjust this threshold as needed
                                            line_text += " "

                                    line_text += character.get_text()
                                    line_fonts.add(character.size)
                                    previous_x1 = character.x1

                                    if character.get_text().isalpha():
                                        has_one_alpha = True

                                    if not character.get_text().isalpha():
                                        total_characters -= 1

                                    if ('Bold' in character.fontname and character.get_text().isalpha()):
                                        bold_characters += 1


                            is_bold = bold_characters > 0 and  bold_characters == total_characters and has_one_alpha

                            if line_text.strip():
                                text_with_font_styles.append({
                                    'page': page_number,
                                    'text': line_text.strip(),
                                    'font_sizes': sorted(line_fonts),
                                    'is_bold': is_bold
                                })

        return text_with_font_styles

    def get_excel(self, name=None, with_ml=False):
        text_font_styles = self.extract_text_with_font_styles()
        new_sentences = []
        if not os.path.exists("TrainData"):
            os.mkdir("TrainData")

        for item in text_font_styles:
            item['font_sizes'] = np.mean(item['font_sizes'])
            new_sentences.append(item["text"])

        df = pd.DataFrame(text_font_styles)
        df = df.set_index("page")

        if not with_ml:
            all_zeros = [0] * len(text_font_styles)
            df = df.assign(Title=all_zeros)
        else:
            pass

        if name is None:
            name = f"TrainData/{self.path.replace('.pdf', '.xlsx')}"
        else:
            name = f"TrainData/{name}.xlsx"

        df.to_excel(name)
        print("Excel file created!")
        print(df)

    def get_pd(self):
        text_font_styles = self.extract_text_with_font_styles()

        new_sentences = []

        for item in text_font_styles:
            item['font_sizes'] = np.mean(item['font_sizes'])
            new_sentences.append(item["text"])

        df = pd.DataFrame(text_font_styles)
        df = df.set_index("page")

        return df

# Sample PDF input
pdf_path = "/Users/rohanraval/Downloads/COURSE6_RS (1).pdf"

pdf_path = ("/Users/rohanraval/Downloads/RelevantCollegeNotes/JupyterNBs"
            "/lec17.pdf")

#pdf_path = ("/Users/rohanraval/Downloads/RelevantCollegeNotes/COURSE6_RS (1)"
 #          ".pdf")

#pdf_path = ("/Users/rohanraval/Desktop/Summer_Internship/nlp"
#            "/NewsDataCollection/javanotes5.pdf")

#obj = PDFDetails(pdf_path)

#obj.start_stop_page()

# Create Excel file from the extracted text and font styles
#obj.get_excel("lec17EDIT")

#print(obj.get_pd())

stop = time.time()

print(f"Time taken: {stop - start} seconds")
