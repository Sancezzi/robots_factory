import re

from django.core.exceptions import ValidationError


def validate_data_format(value: str) -> None:
    """
    Функция для валидации данных.
    Данные должны соответствовать 
    одному из следующих условий: ('AA', 'A1', '1A', '11').
    """
    
    pattern = r'^(?:[A-Z0-9][A-Z0-9])$'
    if not re.match(pattern, value):
        raise ValidationError('The data about the model or version should comply with the established standards.')
    
    