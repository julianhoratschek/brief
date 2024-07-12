from loaders.patient import Patient
from loaders.medication import Medication
from loaders.insert_loader import XmlTemplateLoader
from loaders.config_loader import ConfigurationLoader
from shutil import copy
from pathlib import Path
from zipfile import ZipFile
import re


def get_medication(templates: XmlTemplateLoader, medication: list[Medication]) -> str:
    """
    Returns medication formatted to match xml templates.
    :param templates: XmlTemplateLoader instance with loaded template "medication"
    :param medication: List of Medication objects
    :return: String produced by applying templates to medication
    """

    return "".join([templates.apply_template("medication",
                                             name=med.name,
                                             dosage=f"{med.amount} {med.unit}",
                                             **med.times())
                    for med in medication])


def get_diagnoses(templates: XmlTemplateLoader, diagnoses: dict[str, str]) -> str:
    """
    Returns diagnoses formatted to match xml templates.
    :param templates: XmlTemplateLoader instance with loaded template "diagnoses"
    :param diagnoses: Dictionary mapping icd10 codes to diagnose names.
    :return: Text produced by applying templates to diagnoses
    """

    return "".join([templates.apply_template("diagnosis",
                                             icd10=icd10,
                                             name=name)
                    for icd10, name in diagnoses.items()])


def create_output_file(output_path: Path, docx_template_path: Path, document_text: str, header_text: str):
    """
    Generate DOCX-File from templates.
    :param output_path: Path to output file
    :param docx_template_path: Path to docx template file
    :param document_text: Text to write into word/document.xml
    :param header_text: Text to write into word/header1.xml
    """

    # If Output path does not exist, create it
    if not output_path.parent.exists():
        output_path.parent.mkdir()

    # Copy ZIP file to output location
    patch_path: Path = copy(docx_template_path,
                            output_path)

    # Write missing document.xml and header1.xml files to ZIP archive
    with ZipFile(patch_path, "a") as zip_file:
        zip_file.writestr("word/document.xml", document_text.encode("utf-8"))
        zip_file.writestr("word/header1.xml", header_text.encode("utf-8"))


def generate_header(configs: ConfigurationLoader, patient: Patient) -> str:
    """Read header-data from template file and insert text fields
    :param configs: ConfigurationLoader
    :param patient: Patient object
    :return: String containing xml data for docx header
    """

    with open(configs.paths["header"], "rb") as xml_file:
        return xml_file.read().decode("utf-8").format(**{
            "patient_data": f"{patient.last_name}, {patient.first_name}, *{patient.birth_date.strftime('%d.%m.%Y')}",
        })


def write_data(configs: ConfigurationLoader, patient: Patient,
               midas_text: str, whodas_text: str,
               treatments: str,
               self_eval_text: str):
    """
    Insert template string into document_template.xml, generate docx
    :param configs: ConfigurationLoader containing all needed paths
    :param patient: Patient object with loaded data
    :param midas_text: Text to write into {midas} block
    :param whodas_text: Text to write into {whodas} block
    :param treatments: Text to write into {prev_treatments} block
    :param self_eval_text: Text to write into {self_eval_text} block
    """

    # Load templates and inserts
    templates: XmlTemplateLoader = XmlTemplateLoader(configs.paths["inserts"])

    # Read the document text from document template, insert text fields
    with open(configs.paths["document"], "rb") as xml_file:
        document_text: str = xml_file.read().decode("utf-8").format(**{
            **patient.get_data(),

            "midas": patient.gender.apply(midas_text),
            "whodas": patient.gender.apply(whodas_text),
            "prev_treatments": patient.gender.apply(treatments),
            "self_evaluation": patient.gender.apply(self_eval_text),

            "insert_diagnoses": get_diagnoses(templates, patient.diagnosis),

            **templates.get_inserts(list(patient.diagnosis.keys())),

            'base_medication': get_medication(templates, patient.current_basis_medication),
            'other_medication': get_medication(templates, patient.current_other_medication),

            **patient.gender.gender_dict
        })

    # Write data
    create_output_file(output_path=configs.paths["output"] / patient.file_name(),
                       docx_template_path=configs.paths["docx"],
                       document_text=document_text,
                       header_text=generate_header(configs, patient))


def patch_data(configs: ConfigurationLoader, patient: Patient):
    """
    Reload an already generated docx-file and re process its content, adding text blocks which were omitted before.
    This only works for inserting new insert templates depending on diagnoses read from patient.
    :param configs: ConfigurationLoader containing all needed paths
    :param patient: Patient object with loaded data
    """

    # Load Templates
    templates: XmlTemplateLoader = XmlTemplateLoader(configs.paths["inserts"])

    # Get generated file path
    file_path: Path = configs.paths["output"] / patient.file_name()

    # Do not proceed if file was not created
    if not file_path.exists():
        return

    with ZipFile(file_path, 'r') as zip_file:
        with zip_file.open('word/document.xml') as document_xml:
            # Replace commented insert hooks with working ones
            full_document_text: str = (re.sub(
                r"<!-- insert_id: \[(.*?)] !-->",
                r"{\1}",

                # In the text read from the loaded docx file
                document_xml.read().decode('utf-8'))

                # Then reformat string
                .format(**templates.get_inserts(list(patient.diagnosis.keys()))))

        # Load already generated header from docx-file
        with zip_file.open('word/header1.xml') as header_xml:
            full_header_text: str = header_xml.read().decode('utf-8')

    # Write everything into new file
    create_output_file(output_path=file_path.with_stem(f"{file_path.stem} patch"),
                       docx_template_path=configs.paths["docx"],
                       document_text=full_document_text,
                       header_text=full_header_text)


def write_employer_note(configs: ConfigurationLoader, patient: Patient):
    """Create a document with a recommendation for the employer
    """

    # Read the document text from employer note template
    with open(configs.paths["employer"], "rb") as xml_file:
        document_text: str = xml_file.read().decode("utf-8").format(**{
            **patient.get_data(),
            **patient.gender.gender_dict
        })

    # Write data
    create_output_file(
        output_path=configs.paths["output"] / f"A-{patient.last_name}, {patient.first_name} Arbeitgebervorlage.docx",
        docx_template_path=configs.paths["docx"],
        document_text=document_text,
        header_text=generate_header(configs, patient))
