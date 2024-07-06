from pathlib import Path
from zipfile import ZipFile
from shutil import copy
import re

from .config_loader import ConfigurationLoader


def create_output_file(file_name: str, configs: ConfigurationLoader, document_text: str, header_text: str):
    """
    Generate DOCX-File from templates.
    :param file_name: Filename with extension
    :param configs: Instance of ConfigurationLoader containing paths to templates and output directories
    :param document_text: Text to write into word/document.xml
    :param header_text: Text to write into word/header1.xml
    """

    output_path: Path = configs.get_path("output")

    # If Output path does not exist, create it
    if not output_path.exists():
        output_path.mkdir()

    # Copy ZIP file to output location
    patch_path: Path = copy(configs.get_path("docx"),
                            output_path / file_name)

    # Write missing document.xml and header1.xml files to ZIP archive
    with ZipFile(patch_path, "a") as zip_file:
        zip_file.writestr("word/document.xml", document_text.encode("utf-8"))
        zip_file.writestr("word/header1.xml", header_text.encode("utf-8"))


def patch_inserts(file_path: Path, configs: ConfigurationLoader, format_dict: dict[str, str]):
    """
    Reloads generated docx file and fills in patches. Can only add inserts, not remove them.

    :param file_path: Path to generated docx-file
    :param configs: Instance of ConfigurationLoader containing paths to templates and output directories
    :param format_dict: dictionary to be passed to str format
    """

    with ZipFile(file_path, 'r') as zip_file:
        with zip_file.open('word/document.xml') as document_xml:
            # Replace commented insert hooks with working ones
            full_document_text: str = (re.sub(
                r"<!-- insert_id: (.*?)\s !-->",
                r"\1",
                document_xml.read().decode('utf-8'))

                # Reformat string
                .format(**format_dict))

        # Load already generated header from docx-file
        with zip_file.open('word/header1.xml') as header_xml:
            full_header_text: str = header_xml.read().decode('utf-8')

    # Write everything into new file
    create_output_file(f"Patch {file_path.stem}.docx", configs, full_document_text, full_header_text)





