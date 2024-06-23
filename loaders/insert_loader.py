import re
from pathlib import Path


class XmlTemplateLoader:
    """Loads xml templates from ./templates/insert_template.xml."""

    def __init__(self, insert_template_file: Path):
        # Load templates for inserts
        insert_pattern: re.Pattern = re.compile(
            r'<insert for="(?P<for>.*?)" name="(?P<name>.*?)">(?P<text>.*?)</insert>',
            re.DOTALL)

        # Load templates for repeating patterns
        template_pattern: re.Pattern = re.compile(r'<template name="(?P<name>.*?)">(?P<text>.*?)</template>',
                                                  re.DOTALL)

        full_text: str = insert_template_file.read_text(encoding='utf-8')

        # Get all templates from the file
        self.templates: dict[str, str] = {m.group('name'): m.group('text')
                                          for m in template_pattern.finditer(full_text)}

        # Get all inserts from the file.
        self.inserts: dict[str, dict[str, str]] = {}
        for m in insert_pattern.finditer(full_text):
            for_id: str = m.group('for')
            if for_id not in self.inserts:
                self.inserts[for_id] = {}
            self.inserts[for_id][m.group('name')] = m.group('text')

    def get_inserts(self, for_ids: list[str]) -> dict[str, str]:
        """Looks for the keys for_ids in inserts and returns them as a dict mapping the template name
        onto the insert string. If an insert is defined but not present in for_ids its name will also be
        keyes in the result, but will be mapped onto an empty string."""

        result: dict[str, str] = {}

        # Do not change object
        buffer: dict[str, dict[str, str]] = self.inserts.copy()

        # Insert every block with a corresponding id in ids.
        for n in for_ids:
            if n in buffer:
                result.update(buffer.pop(n))

        # For every other key only insert an empty string
        result.update({key: "" for key, _ in buffer.values()})

        return result

    def apply_template(self, template_name: str, **kwargs) -> str:
        return self.templates[template_name].format(**kwargs) if template_name in self.templates else ""

