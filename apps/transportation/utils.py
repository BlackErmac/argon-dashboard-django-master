from persiantools.jdatetime import JalaliDate

def persian_to_latin(s):
    persian_digits = '۰۱۲۳۴۵۶۷۸۹'
    latin_digits = '0123456789'
    date = s.translate(str.maketrans(persian_digits, latin_digits))
    date = JalaliDate(*map(int , date.split('-'))).to_gregorian()

    return date

def latin_to_persian(s):
    latin_digits = '0123456789'
    persian_digits = '۰۱۲۳۴۵۶۷۸۹'
    return s.translate(str.maketrans(latin_digits, persian_digits))

def car_forms_date_persian_to_latin(data):
    data['production_date'] = persian_to_latin(data['production_date'])
    data['car_insurance_start_date'] = persian_to_latin(data['car_insurance_start_date'])
    data['car_insurance_end_date'] = persian_to_latin(data['car_insurance_end_date'])

    return data

def driver_forms_data_persian_to_latin(data):
    data['sertificate_expiration_date'] = persian_to_latin(data['sertificate_expiration_date'])
    data['birthday'] = persian_to_latin(data['birthday'])
    
