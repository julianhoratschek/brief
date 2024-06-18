from zipfile import ZipFile
import re


from patient import Patient, get_patient_file_matches
from gimme import ui_get_patient_file


def extract_text(pre_match: str) -> str:
    pattern = re.compile(r"<w:t(?:\s.*?)?>(.*?)</w:t>")
    return "".join([text.group(1) for text in pattern.finditer(pre_match)])


def show_all_fields():
    with ZipFile(r"D:\projects\python\leterip\Bali, Korinna 29032024.docx") as zip_file:
        with zip_file.open("word/document.xml") as docx_file:
            pattern = re.compile(r"<w:tc>.*?<w:p(?:\s.*?)?>(.*?)</w:p>")
            for i, m in enumerate(pattern.finditer(docx_file.read().decode("utf-8"))):
                print(f"{i}: {extract_text(m.group(1))}")


# show_all_fields()

if __name__ == '__main__':
    d1 = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5}
    d2 = {"1": 1, "2": 2, "3": 3, "4": 4, "5": 5}

    d3 = {**d1, **d2}

    print(d3)

