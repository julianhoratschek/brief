from pathlib import Path
import re


class ConfigurationLoader:
    def __init__(self, config_path: Path):
        configuration_pattern: re.Pattern = re.compile(r'(?P<key>.*?)\s*=\s*(?P<path>.*)')

        self.paths: dict[str, Path] = {}

        for m in configuration_pattern.finditer(config_path.read_text(encoding='utf-8')):
            self.paths[m.group('key')] = Path(m.group('path'))

    def get_path(self, key: str) -> Path:
        return self.paths[key] if key in self.paths else Path()
