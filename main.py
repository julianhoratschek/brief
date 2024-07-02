from loaders.config_loader import ConfigurationLoader
from brief import generate_brief

from pathlib import Path
import argparse


if __name__ == '__main__':

    # Load Configurations
    configs: ConfigurationLoader = ConfigurationLoader(Path("./config.txt"))

    # Create command line arguments
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        prog="brief",
        description="Generiere Briefe aus Aufnahmebögen"
    )

    with_choices: list[str] = ["body-data", "midas", "whodas-cats", "whodas", "treatments", "afflictions", "bdi", "f45"]
    parser.add_argument("-w", "--with-blocks", action="extend", nargs="+", choices=with_choices,
                        help="definiert Absätze, die beim Generieren abgefragt werden")
    parser.add_argument("-o", "--omit-blocks", action="extend", nargs="+", choices=with_choices,
                        help="definiert Absätze, die beim Generieren nicht abgefragt werden. Überschreibt Argumente"
                             "von --with")

    # Parse arguments
    args = parser.parse_args()

    # Set Include Blocks
    if args.with_blocks:
        configs.set_blocks(args.with_blocks, [True] * len(args.with_blocks))

    # Set Exclude Blocks
    if args.omit_blocks:
        configs.set_blocks(args.omit_blocks, [False] * len(args.omit_blocks))

    # Generate Letter
    generate_brief(configs)

