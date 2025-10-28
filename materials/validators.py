import re
from rest_framework.serializers import ValidationError

def validate_forbidden_words(value):
    reg = re.compile('^(https?://)?(www\.)?youtube\.com/?$')
    tmp_val = value
    if not bool(reg.match(tmp_val)):
        raise ValidationError('Запрещенная ссылка. Разрешены только ссылки на youtube.com.')

