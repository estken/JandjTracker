import re

def has_country_code(phone_number):
    # Regular expression pattern for matching a country code (leading + followed by digits)
    country_code_pattern = r'^\+\d+'

    # Use re.search to find the first occurrence of the country code pattern in the phone number
    match = re.search(country_code_pattern, phone_number)

    # Return True if a country code is found, False otherwise
    return match is not None