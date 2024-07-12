from loaders.config_loader import ConfigurationLoader
from brief import generate_brief, generate_employer_note

from pathlib import Path
import argparse


def log_configs(loaded_configuration: ConfigurationLoader):
    path_names: dict[str, str] = {
        "db": "Datenbank (Ordner mit Aufnahmebögen)",
        "output": "Ausgabe-Ordner",
        "docx": "Docx-Schablone",
        "header": "Seiten-Header Schablone",
        "document": "Dokument-Inhalt Schablone",
        "inserts": "Einzufügende Blöcke",
        "employer": "Schablone für Arbeitgebervorlage"
    }

    block_names: dict[str, str] = {
        "body-data": "Untersuchungsdaten",
        "midas": "MIDAS-Score",
        "whodas-cats": "WHODAS Kategorien",
        "whodas": "WHODAS-Score",
        "treatments": "Vorbehandlungen (ärztlich und nicht-medizinisch)",
        "afflictions": "Körperliche und psychische Beschwerden",
        "bdi": "BDI-II",
        "f45": "Chronische Schmerzerkrankung: Score"
    }

    print("Folgende Pfade wurden geladen:")
    for path_name, path in loaded_configuration.paths.items():
        print(f"\t* {path_names[path_name]}: {path.absolute()}")

    print("Folgende Schablonen werden NICHT abgefragt:")
    for block, display in loaded_configuration.blocks.items():
        if display:
            continue

        print(f"\t* {block_names[block]}")


if __name__ == '__main__':

    # Load Configurations
    configs: ConfigurationLoader = ConfigurationLoader(Path("./config.txt"))
    log_configs(configs)

    # Create command line arguments
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        prog="brief",
        description="Generiere Briefe aus Aufnahmebögen"
    )

    with_choices: list[str] = ["body-data", "midas", "whodas-cats", "whodas", "treatments", "afflictions", "bdi", "f45"]
    parser.add_argument("-e", "--employer", action="store_true",
                        help="Schreibe Bescheinigung für den Arbeitgeber")
    parser.add_argument("-w", "--with-blocks", action="extend", nargs="+", choices=with_choices,
                        help="definiert Absätze, die beim Generieren abgefragt werden")
    parser.add_argument("-o", "--omit-blocks", action="extend", nargs="+", choices=with_choices,
                        help="definiert Absätze, die beim Generieren nicht abgefragt werden. Überschreibt Argumente"
                             "von --with")

    # Parse arguments
    args = parser.parse_args()

    # Generate letter to employer
    if args.employer:
        generate_employer_note(configs)
        exit(0)

    # Set Include Blocks
    if args.with_blocks:
        configs.set_blocks(args.with_blocks, [True] * len(args.with_blocks))

    # Set Exclude Blocks
    if args.omit_blocks:
        configs.set_blocks(args.omit_blocks, [False] * len(args.omit_blocks))

    # Generate Letter
    generate_brief(configs)
