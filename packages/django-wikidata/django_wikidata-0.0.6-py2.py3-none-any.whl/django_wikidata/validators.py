import re

from django import forms

from wikidata.entity import Entity


WIKIDATA_ENTITY_RE = re.compile(r'^[PQLS]\d+$')


def validate_wikidata_item(value):
    if isinstance(value, Entity):
        return
    match = WIKIDATA_ENTITY_RE.match(value)
    if match is None:
        raise forms.ValidationError('"{}" is not a Wikidata Item ID'.format(value))
