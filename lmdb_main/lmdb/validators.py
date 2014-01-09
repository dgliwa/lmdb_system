from django.core.exceptions import ValidationError

def is_num(value):
    if not value.isdigit():
        raise ValidationError('Please enter a valid phone number.')
    if len(value) != 10:
        raise ValidationError('Please enter a valid phone number.')

