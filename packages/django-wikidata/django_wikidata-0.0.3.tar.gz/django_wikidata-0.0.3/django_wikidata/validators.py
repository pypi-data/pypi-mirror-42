from django import forms

from wikidata.entity import Entity


def validate_wikidata_item(value):
    if isinstance(value, Entity):
        return
    if not value.startswith('Q'):
        raise forms.ValidationError('"{}" is not a Wikidata Item ID'.format(value))
    try:
        int(value[1:])
    except ValueError:
        raise forms.ValidationError('"{}" is not a Wikidata Item ID'.format(value))
