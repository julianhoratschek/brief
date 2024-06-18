from typing import Self, Optional


def melt(it) -> str:
    return "".join(map(str, it))


class DocxParagraphProperty:
    pass


class DocxRunProperty:
    pass


class DocxFontProperty(DocxRunProperty):
    def __init__(self, font_name: str = "Lucida Sans Unicode"):
        self.font_name = font_name

    def __str__(self):
        return f'<w:rFonts w:ascii="{self.font_name}" w:hAnsi="{self.font_name}" w:cs="{self.font_name}"/>'


class DocxSizeProperty(DocxRunProperty):
    def __init__(self, value: int = 18):
        self.value = value

    def __str__(self):
        return f'<w:sz w:val="{self.value}"/><w:szCs w:val="{self.value}"/>'


class DocxRunProperties(DocxParagraphProperty):
    def __init__(self, properties: list[DocxRunProperty]):
        self.properties = properties

    def __str__(self):
        return ("<w:rPr>"
                + (melt(self.properties) if self.properties else "")
                + "</w:rPr>")


class DocxRun:
    def __init__(self, text: str = "", properties: DocxRunProperties = None):
        self.text: str = text
        self.properties: DocxRunProperties = properties

    def __str__(self):
        return (f'<w:r>'
                + (str(self.properties) if self.properties else "")
                + ('<w:tab/>' if self.text == "\t" else f'<w:t>{self.text}</w:t>')
                + '</w:r>')


class DocxIdentationProperty(DocxParagraphProperty):
    def __init__(self, left: int, hanging: int = 0):
        self.left = left
        self.hanging = hanging

    def __str__(self):
        return f'<w:ind w:left="{self.left}" w:hanging="{self.hanging}"/>'


class DocxJustificationProperty(DocxParagraphProperty):
    def __init__(self, value: str = "both"):
        self.value = value

    def __str__(self):
        return f'<w:jc w:val="{self.value}"/>'


class DocxParagraph:
    def __init__(self, properties: list[DocxParagraphProperty]):
        self.properties: list[DocxParagraphProperty] = properties
        self.run_properties: DocxRunProperties | None = None
        for p in filter(lambda x: isinstance(x, DocxRunProperties), self.properties):
            self.run_properties = p
        self.runs: list = []

    def run(self, text: str, properties: DocxRunProperties = None) -> Self:
        props = self.run_properties if self.run_properties is not None else properties

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

