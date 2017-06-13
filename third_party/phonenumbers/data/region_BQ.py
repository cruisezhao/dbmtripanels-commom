"""Auto-generated file, do not edit by hand. BQ metadata"""
from ..phonemetadata import NumberFormat, PhoneNumberDesc, PhoneMetadata

PHONE_METADATA_BQ = PhoneMetadata(id='BQ', country_code=599, international_prefix='00',
    general_desc=PhoneNumberDesc(national_number_pattern='[347]\\d{6}', possible_number_pattern='\\d{7}', possible_length=(7,)),
    fixed_line=PhoneNumberDesc(national_number_pattern='(?:318[023]|41(?:6[023]|70)|7(?:1[578]|50)\\d)\\d{3}', example_number='7151234', possible_length=(7,)),
    mobile=PhoneNumberDesc(national_number_pattern='(?:31(?:8[14-8]|9[14578])|416[145-9]|7(?:0[01]|7[07]|8\\d|9[056])\\d)\\d{3}', example_number='3181234', possible_length=(7,)),
    toll_free=PhoneNumberDesc(),
    premium_rate=PhoneNumberDesc(),
    shared_cost=PhoneNumberDesc(),
    personal_number=PhoneNumberDesc(),
    voip=PhoneNumberDesc(),
    pager=PhoneNumberDesc(),
    uan=PhoneNumberDesc(),
    voicemail=PhoneNumberDesc(),
    no_international_dialling=PhoneNumberDesc())
