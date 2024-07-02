from pathlib import Path
import re


class ConfigurationLoader:
    def __init__(self, config_path: Path):
        configuration_pattern: re.Pattern = re.compile(r'(?P<key>.*?)\s*=\s*(?P<path>.*)')

        # Default Paths
        self.paths: dict[str, Path] = {
            "db": Path(),
            "output": Path(r"./output/"),
            "docx": Path(r"./templates/template.docx"),
            "header": Path(r"./templates/header1_template.xml"),
            "document": Path(r"./templates/document_template.xml"),
            "inserts": Path(r"./templates/insert_template.xml")
        }

        # Default: prompt user for all blocks
        self.blocks: dict[str, bool] = {
            "body-data": True,
            "midas": True,
            "whodas-cats": True,
            "whodas": True,
            "treatments": True,
            "afflictions": True,
            "bdi": True,
            "f45": True
        }

        # Iterate over configurations
        for m in configuration_pattern.finditer(config_path.read_text(encoding='utf-8')):
            key, value = map(lambda s: s.strip(), m.groups())

            # Process block-exclusion configuration
            if key == "without":
                values: list[str] = list(map(lambda s: s.strip(), value.split()))
                self.set_blocks(values, [False] * len(values))

            # Otherwise overwrite paths
            else:
                self.paths[key] = Path(value)

    def get_path(self, key: str) -> Path:
        return self.paths[key] if key in self.paths else Path()

    def include_block(self, block_name: str) -> bool:
        """Returns true if user should be prompted for block described by block_name."""

        return block_name in self.blocks and self.blocks[block_name]

    def set_blocks(self, block_names: list[str], value_list: list[bool]):
        """Sets configuration to include/ignore block prompts according to values in value_list"""

        for key, val in zip(block_names, value_list):
            self.blocks[key] = val
