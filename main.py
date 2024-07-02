from loaders.config_loader import ConfigurationLoader
from brief import generate_brief

from pathlib import Path
import argparse

if __name__ == '__main__':
    configs: ConfigurationLoader = ConfigurationLoader(Path("./config.txt"))
    print(configs.blocks)

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
    args = parser.parse_args()

    if args.with_blocks:
        configs.set_blocks(args.with_blocks, [True] * len(args.with_blocks))

    if args.omit_blocks:
        configs.set_blocks(args.omit_blocks, [False] * len(args.omit_blocks))

    generate_brief(configs)

