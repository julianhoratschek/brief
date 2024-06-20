from .util import melt
from .paragraph import DocxParagraph, DocxParagraphProperty


# DocxTable implementation omitted as it won't be used in this project


class DocxTableProperty:
    """Base class for Table properties."""
    pass


class DocxTableCellWidthProperty(DocxTableProperty):
    """Width property used for table cells. Should be added to DocxTableCellProperties."""

    def __init__(self, width: int, w_type: str = "dxa"):
        self.width = width
        self.w_type = w_type

    def __str__(self):
        return f'<w:tcW w:w="{self.width}" w:type="{self.w_type}"/>'


class DocxTableCellProperties:
    """Collection of Properties for Table cells."""
    def __init__(self, properties: list[DocxTableProperty]):
        self.properties = properties

    def __str__(self):
        return f'<w:tcPr>{melt(self.properties)}</w:tcPr>'


class DocxTableCell:
    """Table cell class."""

    def __init__(self, properties: DocxTableCellProperties):
        self.properties = properties
        self.paragraphs: list[DocxParagraph] = []

    def p(self, properties: list[DocxParagraphProperty]) -> DocxParagraph:
        """Generate DocxParagraph and add it to this cell. Returns the created paragraph."""

        paragraph = DocxParagraph(properties)
        self.paragraphs.append(paragraph)
        return paragraph

    def __str__(self):
        return f'<w:tc>{self.properties}{melt(self.paragraphs)}</w:tc>'


class DocxTableRow:
    """Table row class"""

    def __init__(self):
        self.cells: list[DocxTableCell] = []

    def cell(self, properties: DocxTableCellProperties) -> DocxTableCell:
        """Creates a DocxTableCell and adds it to this row. Returns the created cell."""

        cell = DocxTableCell(properties)
        self.cells.append(cell)
        return cell

    def __str__(self):
        return f'<w:tr>{melt(self.cells)}</w:tr>'

