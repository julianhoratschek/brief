from typing import Self, Optional
from .util import melt


class DocxParagraphProperty:
    """Base class for Paragraph properties."""
    pass


class DocxRunProperty:
    """Base class for Run properties."""
    pass


class DocxFontProperty(DocxRunProperty):
    """Font property. Should be added to DocxRunProperties."""

    def __init__(self, font_name: str = "Lucida Sans Unicode"):
        self.font_name = font_name

    def __str__(self):
        return f'<w:rFonts w:ascii="{self.font_name}" w:hAnsi="{self.font_name}" w:cs="{self.font_name}"/>'


class DocxSizeProperty(DocxRunProperty):
    """Font Size property. Should be added to DocxRunProperties."""

    def __init__(self, value: int = 18):
        self.value = value

    def __str__(self):
        return f'<w:sz w:val="{self.value}"/><w:szCs w:val="{self.value}"/>'


class DocxBigProperty(DocxRunProperty):
    """Font Weight property. Should be added to DocxRunProperties."""

    def __str__(self):
        return "<w:b/><w:bCs/>"


class DocxHighlightProperty(DocxRunProperty):
    """Background Highlight property. Should be added to DocxRunProperties."""

    def __init__(self, value: str = "yellow"):
        self.value = value

    def __str__(self):
        return f'<w:highlight w:val="{self.value}"/>'


class DocxRunProperties(DocxParagraphProperty):
    """Collection of DocxRunProperties. Can be added to Runs or Paragraphs."""

    def __init__(self, properties: list[DocxRunProperty]):
        self.properties = properties

    def having(self, prop: DocxRunProperty) -> Self:
        """Copies this DocxRunProperties instance, but adds or modifies properties-list using prop.
        Returns the copied instance"""

        properties = list(self.properties)
        for i, p in enumerate(properties):
            if type(prop) is type(p):
                properties[i] = p
                break
        else:
            properties.append(prop)

        return DocxRunProperties(properties)

    def __str__(self):
        return ("<w:rPr>"
                + (melt(self.properties) if self.properties else "")
                + "</w:rPr>")


class DocxRun:
    """A Run contains the text elements of a paragraph."""

    def __init__(self, text: str = "", properties: DocxRunProperties = None):
        self.text: str = text
        self.properties: DocxRunProperties = properties

    def __str__(self):
        # Only insert preserve-spaces when text begins or ends with whitespace.
        preserver_space: str = (' xml:space="preserve"'
                                if len(self.text) and (self.text[0] == ' ' or self.text[-1] == ' ')
                                else "")

        # Cannot handle tabs in the string, but expects tabs to be presented in separate Runs.
        return (f'<w:r>'
                + (str(self.properties) if self.properties else "")
                + ('<w:tab/>' if self.text == "\t" else f'<w:t{preserver_space}>{self.text}</w:t>')
                + '</w:r>')


class DocxNumberingProperty(DocxParagraphProperty):
    """Declares Paragraph as a numbering"""

    def __init__(self, level: int, number_id: int):
        self.level = level
        self.number_id = number_id

    def __str__(self):
        return f'<w:numPr><w:ilvl w:val="{self.level}"/><w:numId w:val="{self.number_id}"/></w:numPr>'


class DocxTab:
    """Define Tabstops for this Paragraph. This is a property used in DocxTabsProperty, not a representation of \t!"""

    def __init__(self, value: str, position: int):
        self.value = value
        self.position = position

    def __str__(self):
        return f'<w:tab w:val="{self.value}" w:pos="{self.position}"/>'


class DocxTabsProperty(DocxParagraphProperty):
    """Property defining all tabstops for a paragraph."""

    def __init__(self, tabs_positions: list[int]):
        """Defines a DocxTab for each element in tabs_positions. DocxTabs will have a standard value of "left"."""

        self.tabs = [DocxTab("left", pos) for pos in tabs_positions]

    def __str__(self):
        return ('<w:tabs>'
                + melt(self.tabs)
                + '</w:tabs>')


class DocxIndentationProperty(DocxParagraphProperty):
    """Paragraph indentation property."""

    def __init__(self, left: int, hanging: int = 0):
        self.left = left
        self.hanging = hanging

    def __str__(self):
        return f'<w:ind w:left="{self.left}" w:hanging="{self.hanging}"/>'


class DocxJustificationProperty(DocxParagraphProperty):
    """Paragraph justification property."""

    def __init__(self, value: str = "both"):
        self.value = value

    def __str__(self):
        return f'<w:jc w:val="{self.value}"/>'


class DocxParagraph:
    """Defines a single paragraph"""

    def __init__(self, properties: list[DocxParagraphProperty]):
        self.properties: list[DocxParagraphProperty] = properties

        # Select the DocxRunProperties property, if present, to add to each run, as Microsoft demands it.
        self.run_properties: DocxRunProperties | None = None
        for p in filter(lambda x: isinstance(x, DocxRunProperties), self.properties):
            self.run_properties = p

        self.runs: list = []

    def run(self, text: str, properties: DocxRunProperties = None) -> Self:
        """Creates a run containing text and appends it to the paragraph. text will be split at \t, each tab will be
        included as a separate run. If properties is set, it will be used for this run, otherwise self.run_properties
        will be used (even if set to None)."""

        props = properties if properties is not None else self.run_properties

        while text:
            text_before, tab, text = text.partition("\t")
            self.runs.append(DocxRun(text_before, props))
            if tab:
                self.runs.append(DocxRun(tab, props))

        return self

    def __str__(self):
        return ("<w:p>"
                + (f"<w:pPr>{melt(self.properties)}</w:pPr>" if self.properties else "")
                + (melt(self.runs))
                + "</w:p>")

