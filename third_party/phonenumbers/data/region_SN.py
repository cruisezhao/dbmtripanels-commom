"""Auto-generated file, do not edit by hand. SN metadata"""
from ..phonemetadata import NumberFormat, PhoneNumberDesc, PhoneMetadata

PHONE_METADATA_SN = PhoneMetadata(id='SN', country_code=221, international_prefix='00',
    general_desc=PhoneNumberDesc(national_number_pattern='[3789]\\d{8}', possible_number_pattern='\\d{9}', possible_length=(9,)),
    fixed_line=PhoneNumberDesc(national_number_pattern='3(?:0(?:1[0-2]|80)|282|3(?:8[1-9]|9[3-9])|611)\\d{5}', example_number='301012345', possible_length=(9,)),
    mobile=PhoneNumberDesc(national_number_pattern='7(?:[06-8]\\d|21|90)\\d{6}', example_number='701234567', possible_length=(9,)),
    toll_free=PhoneNumberDesc(national_number_pattern='800\\d{6}', possible_number_pattern='\\d{9}', example_number='800123456', possible_length=(9,)),
    premium_rate=PhoneNumberDesc(national_number_pattern='88[4689]\\d{6}', possible_number_pattern='\\d{9}', example_number='884123456', possible_length=(9,)),
    shared_cost=PhoneNumberDesc(national_number_pattern='81[02468]\\d{6}', possible_number_pattern='\\d{9}', example_number='810123456', possible_length=(9,)),
    personal_number=PhoneNumberDesc(),
    voip=PhoneNumberDesc(national_number_pattern='39[01]\\d{6}|3392\\d{5}|93330\\d{4}', possible_number_pattern='\\d{9}', example_number='933301234', possible_length=(9,)),
    pager=PhoneNumberDesc(),
    uan=PhoneNumberDesc(),
    voicemail=PhoneNumberDesc(),
    no_international_dialling=PhoneNumberDesc(),
    number_format=[NumberFormat(pattern='(\\d{2})(\\d{3})(\\d{2})(\\d{2})', format='\\1 \\2 \\3 \\4', leading_digits_pattern=['[379]']),
        NumberFormat(pattern='(\\d{3})(\\d{2})(\\d{2})(\\d{2})', format='\\1 \\2 \\3 \\4', leading_digits_pattern=['8'])])
