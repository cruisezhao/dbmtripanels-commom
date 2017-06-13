"""Auto-generated file, do not edit by hand. TO metadata"""
from ..phonemetadata import NumberFormat, PhoneNumberDesc, PhoneMetadata

PHONE_METADATA_TO = PhoneMetadata(id='TO', country_code=676, international_prefix='00',
    general_desc=PhoneNumberDesc(national_number_pattern='[02-8]\\d{4,6}', possible_number_pattern='\\d{5,7}', possible_length=(5, 7)),
    fixed_line=PhoneNumberDesc(national_number_pattern='(?:2\\d|3[1-8]|4[1-4]|[56]0|7[0149]|8[05])\\d{3}', possible_number_pattern='\\d{5}', example_number='20123', possible_length=(5,)),
    mobile=PhoneNumberDesc(national_number_pattern='(?:7[578]|8[47-9])\\d{5}', possible_number_pattern='\\d{7}', example_number='7715123', possible_length=(7,)),
    toll_free=PhoneNumberDesc(national_number_pattern='0800\\d{3}', possible_number_pattern='\\d{7}', example_number='0800222', possible_length=(7,)),
    premium_rate=PhoneNumberDesc(),
    shared_cost=PhoneNumberDesc(),
    personal_number=PhoneNumberDesc(),
    voip=PhoneNumberDesc(),
    pager=PhoneNumberDesc(),
    uan=PhoneNumberDesc(),
    voicemail=PhoneNumberDesc(),
    no_international_dialling=PhoneNumberDesc(),
    number_format=[NumberFormat(pattern='(\\d{2})(\\d{3})', format='\\1-\\2', leading_digits_pattern=['[1-6]|7[0-4]|8[05]']),
        NumberFormat(pattern='(\\d{3})(\\d{4})', format='\\1 \\2', leading_digits_pattern=['7[5-9]|8[47-9]']),
        NumberFormat(pattern='(\\d{4})(\\d{3})', format='\\1 \\2', leading_digits_pattern=['0'])],
    leading_zero_possible=True)
