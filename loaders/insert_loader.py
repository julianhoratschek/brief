import re
from pathlib import Path


def glob_str(pattern: str, text: str) -> bool:
    """
    Simulates glob pattern matching using regex.
    :param pattern: The pattern to match.
    :param text: The text to match.
    :return: True if the pattern matches, False otherwise.
    """

    return re.search(pattern.replace('.', '\\.')
                            .replace('?', '.?')
                            .replace('*', '.*?'),
                     text) is not None


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

        # Save glob keys for later
        self.pattern_keys: list[str] = []

        # Add Inserts from matches
        for m in insert_pattern.finditer(full_text):
            for_id: str = m.group('for')
            if for_id not in self.inserts:
                self.inserts[for_id] = {}

            self.inserts[for_id][m.group('name')] = m.group('text')

            # Test if this match should be preprocessed
            if m.group('prep'):
                self.preprocess_names.append(m.group('name'))

            # Test if key is a glob pattern
            if '*' in for_id or '?' in for_id:
                self.pattern_keys.append(for_id)

    def get_inserts(self, for_ids: list[str]) -> dict[str, str]:
        """Looks for the keys for_ids in inserts and returns them as a dict mapping the template name
        onto the insert string. If an insert is defined but not present in for_ids its name will also be
        keyes in the result, but will be mapped onto an empty string."""

        # Maps insert_key to text
        result: dict[str, str] = {}

        # Do not change object
        buffer: dict[str, dict[str, str]] = self.inserts.copy()
        pattern_buffer: list[str] = self.pattern_keys.copy()

        # Maps insert_text to list of text
        collection_list: dict[str, list[str]] = {}

        # Insert every block with a corresponding id in ids.
        for n in for_ids:

            # If we don't find the id in our buffer
            if n not in buffer:

                # Test, if id matches a glob pattern
                for id_i, insert_id in enumerate(pattern_buffer):

                    # If id matches a pattern, add key id to buffer and remove pattern
                    if glob_str(insert_id, n):
                        buffer[n] = buffer.pop(insert_id)
                        break

                # If id didn't match a glob pattern, continue
                else:
                    continue

                # Remove glob pattern as we filled it in
                pattern_buffer.pop(id_i)

            insert: dict[str, str] = buffer.pop(n)
            insert_keys: list[str] = list(insert.keys())

            # Look for collection ids
            for k in insert_keys:
                if k in self.collections:
                    if k not in collection_list:
                        collection_list[k] = []
                    collection_list[k].append(insert.pop(k))

            result.update(insert)

        # For every other key only insert a comment for later patching
        result.update({key: f"<!-- insert_id: [{key}] !-->" for d in buffer.values() for key in d.keys()})

        # Insert texts for collections
        result.update({insert_id: f"<!-- insert_id: [{insert_id}] !-->" if name not in collection_list else
                                  text.format(collection=", ".join(collection_list[name]))
                       for name, (insert_id, text) in self.collections.items()})

        # Preprocess results
        for k in result.keys():
            if k in self.preprocess_names:
                result[k] = result[k].format(**result)

        return result

    def apply_template(self, template_name: str, **kwargs) -> str:
        return self.templates[template_name].format(**kwargs) if template_name in self.templates else ""
