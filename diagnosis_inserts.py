from patient import Patient
from docx import (DocxParagraph, DocxRunProperties,
                  DocxIdentationProperty, DocxJustificationProperty,
                  DocxFontProperty, DocxSizeProperty, melt)


def get_inserts(patient: Patient):
    ident = DocxIdentationProperty(1134, 1134)
    jc = DocxJustificationProperty()
    rpr = DocxRunProperties([DocxFontProperty(), DocxSizeProperty(18)])
    ppr = [ident, jc, rpr]

    return {
        "insert_diagnoses": melt([DocxParagraph(ppr).run(f"{icd10}\t{name}") for name, icd10 in patient.diagnosis])
    }

