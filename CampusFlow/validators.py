from django.core.validators import RegexValidator



PHONE_NUMBER_VALIDATOR = RegexValidator(r'^\d{10}$', message="Enter a Valid Number")


USN_VALIDATOR = RegexValidator(
    regex=r'^[0-9]{1}[A-Z]{2}[0-9]{2}[A-Z]{2}[0-9]{3}$',
    message="USN must be in the format: 2sd23XXYYY"
)