from django.core.exceptions import ValidationError

def validate_file_size(file):
    limit= 2*1024*1024  # 2 MB
    if file.size > limit:
        raise ValidationError('File too large. Size should not exceed 2 MiB.')