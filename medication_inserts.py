from patient import Patient
from docx import (DocxTableRow, DocxTableCellProperties, DocxTableCellWidthProperty,
                  DocxFontProperty, DocxJustificationProperty, DocxSizeProperty, DocxRunProperties, melt)


def get_medication_inserts(patient: Patient):
    c1 = DocxTableCellProperties([DocxTableCellWidthProperty(3686, "dxa")])
    c2 = DocxTableCellProperties([DocxTableCellWidthProperty(1276, "dxa")])
    crest = [DocxTableCellProperties([DocxTableCellWidthProperty(992, "dxa")]),
             DocxTableCellProperties([DocxTableCellWidthProperty(992, "dxa")]),
             DocxTableCellProperties([DocxTableCellWidthProperty(992, "dxa")]),
             DocxTableCellProperties([DocxTableCellWidthProperty(1134, "dxa")])]
    ppr = [DocxJustificationProperty(), DocxRunProperties([DocxFontProperty(), DocxSizeProperty(18)])]

    base_medication_rows = []
    other_medication_rows = []

    for meds in patient.current_basis_medication:
        row = DocxTableRow()
        row.cell(c1).p(ppr).run(meds.name)
        row.cell(c2).p(ppr).run(f'{meds.amount} {meds.unit}')
        for cr, t in zip(crest, meds.destructure_taken()):
            row.cell(cr).p(ppr).run(t)

        base_medication_rows.append(row)

    for meds in patient.current_other_medication:
        row = DocxTableRow()
        row.cell(c1).p(ppr).run(meds.name)
        row.cell(c2).p(ppr).run(f'{meds.amount} {meds.unit}')
        for cr, t in zip(crest, meds.destructure_taken()):
            row.cell(cr).p(ppr).run(t)

        other_medication_rows.append(row)

    return {
        'base_medication': melt(base_medication_rows),
        'other_medication': melt(other_medication_rows)
    }

