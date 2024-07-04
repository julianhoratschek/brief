import re
from pathlib import Path


class XmlTemplateLoader:
    """Loads xml templates from ./templates/insert_template.xml."""

    def __init__(self, insert_template_file: Path):
        # Load templates for inserts
        insert_pattern: re.Pattern = re.compile(
            r'<insert for="(?P<for>.*?)" name="(?P<name>.*?)"(?P<prep> preprocess="true")?>(?P<text>.*?)</insert>',
            re.DOTALL)

        # Load templates for repeating patterns
        template_pattern: re.Pattern = re.compile(r'<template name="(?P<name>.*?)">(?P<text>.*?)</template>',
                                                  re.DOTALL)

        collection_pattern: re.Pattern = re.compile(
            r'<collection for="(?P<for>.*?)" name="(?P<name>.*?)">(?P<text>.*?)</collection>', re.DOTALL)

        full_text: str = insert_template_file.read_text(encoding='utf-8')

        # Get all templates from the file
        self.templates: dict[str, str] = {m.group('name'): m.group('text')
                                          for m in template_pattern.finditer(full_text)}

        # Maps collection_name to (insert_id, text)
        self.collections: dict[str, tuple[str, str]] = {m.group('for'): (m.group('name'), m.group('text'))
                                                        for m in collection_pattern.finditer(full_text)}

        # Maps ICD10-number to (insert_id, text) or (collection_name, text)
        self.inserts: dict[str, dict[str, str]] = {}

        # Saves names of inserts to preprocess
        self.preprocess_names: list[str] = []

        # Add Inserts from matches
        for m in insert_pattern.finditer(full_text):
            for_id: str = m.group('for')
            if for_id not in self.inserts:
                self.inserts[for_id] = {}

            self.inserts[for_id][m.group('name')] = m.group('text')

            # Test if this match should be preprocessed
            if m.group('prep'):
                self.preprocess_names.append(m.group('name'))


    def get_inserts(self, for_ids: list[str]) -> dict[str, str]:
        """Looks for the keys for_ids in inserts and returns them as a dict mapping the template name
        onto the insert string. If an insert is defined but not present in for_ids its name will also be
        keyes in the result, but will be mapped onto an empty string."""

        # Maps insert_key to text
        result: dict[str, str] = {}

        # Do not change object
        buffer: dict[str, dict[str, str]] = self.inserts.copy()

        # Maps insert_text to list of text
        collection_list: dict[str, list[str]] = {}

        # Insert every block with a corresponding id in ids.
        for n in for_ids:
            if n not in buffer:
                continue

            insert: dict[str, str] = buffer.pop(n)
            insert_keys: list[str] = list(insert.keys())

            # Look for collection ids
            for k in insert_keys:
                if k in self.collections:
                    if k not in collection_list:
                        collection_list[k] = []
                    collection_list[k].append(insert.pop(k))

            result.update(insert)

        # For every other key only insert an empty string
        result.update({key: "" for d in buffer.values() for key in d.keys()})

        # Insert texts for collections
        result.update({insert_id: "" if name not in collection_list
                                     else text.format(collection=", ".join(collection_list[name]))
                       for name, (insert_id, text) in self.collections.items()})

        # Preprocess results
        for k in result.keys():
            if k in self.preprocess_names:
                result[k] = result[k].format(**result)

        return result

    def apply_template(self, template_name: str, **kwargs) -> str:
        return self.templates[template_name].format(**kwargs) if template_name in self.templates else ""
