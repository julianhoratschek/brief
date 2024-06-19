from .util import melt
from .paragraph import DocxParagraph, DocxParagraphProperty


class DocxTableProperty:
    pass


class DocxTableCellWidthProperty(DocxTableProperty):
    def __init__(self, width: int, w_type: str = "dxa"):
        self.width = width
        self.w_type = w_type

    def __str__(self):
        return f'<w:tcW w:w="{self.width}" w:type="{self.w_type}"/>'


class DocxTableCellProperties:
    def __init__(self, properties: list[DocxTableProperty]):
        self.properties = properties

    def __str__(self):
        return f'<w:tcPr>{melt(self.properties)}</w:tcPr>'


class DocxTableCell:
    def __init__(self, properties: DocxTableCellProperties):
        self.properties = properties
        self.paragraphs: list[DocxParagraph] = []

    def p(self, properties: list[DocxParagraphProperty]) -> DocxParagraph:
        paragraph = DocxParagraph(properties)
        self.paragraphs.append(paragraph)
        return paragraph

    def __str__(self):
        return f'<w:tc>{self.properties}{melt(self.paragraphs)}</w:tc>'


class DocxTableRow:
    def __init__(self):
        self.cells: list[DocxTableCell] = []

    def cell(self, properties: DocxTableCellProperties) -> DocxTableCell:
        cell = DocxTableCell(properties)
        self.cells.append(cell)
        return cell

    def __str__(self):
        return f'<w:tr>{melt(self.cells)}</w:tr>'

