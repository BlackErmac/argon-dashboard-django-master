
from __future__ import annotations
from persiantools.jdatetime import JalaliDate
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from bidi.algorithm import get_display
import arabic_reshaper
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
import qrcode
from .models import PredefinedPoint

def create_qrcode(url):
    qr = qrcode.QRCode(
    version=1,  # QR code size (1 is smallest, higher = bigger)
    error_correction=qrcode.constants.ERROR_CORRECT_L,  # Error correction level
    box_size=10,  # Size of each box in the QR grid
    border=4,  # Border size
    )

    qr.add_data(url)
    qr.make(fit=True)

    # Create an image from the QR Code
    img = qr.make_image(fill="black", back_color="white")

    # Save the QR code image
    img.save("./apps/transportation/tasks_pdf_qrcodes/qrcode.png")
    


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
    data['birthday_date'] = persian_to_latin(data['birthday_date'])
    
    return data
    
def fix_arabic(text):
    return get_display(arabic_reshaper.reshape(text))


FONT_PATH = "arial.ttf"  # Change to your Persian font file

# Register the font in ReportLab
pdfmetrics.registerFont(TTFont('PersianFont', FONT_PATH))

def create_persian_pdf(filename , data):

    filename = './apps/transportation/tasks_pdf_qrcodes/' + filename
    
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    title_1 = fix_arabic("بسم الله الرحمن الرحیم")
    c.setFont("PersianFont", 12)
    c.drawRightString(width - 250, height - 20, title_1)

    title = fix_arabic("برگه ماموریت")
    c.setFont("PersianFont", 18)
    c.drawRightString(width - 250, height - 60, title)   

    # c.rect(100, 780, 400, 40)
    # c.setFont("PersianFont", 10)
    # c.drawCentredString(500 , 400, fix_arabic("صورت‌حساب مأموریت"))
    
    title = fix_arabic("برابر امریه شماره ............ به .................... ماموریت") 
    c.setFont("PersianFont", 10)
    c.drawRightString(width - 30, height - 90, title)
    title = fix_arabic("داده میشود که از تاریخ ............ به .................... عزیمت") 
    c.setFont("PersianFont", 10)
    c.drawRightString(width - 30, height - 105, title)
    title = fix_arabic("و پس از انجام ماموریت خود را به واحد اصلی معرفی نماید.") 
    c.setFont("PersianFont", 10)
    c.drawRightString(width - 30, height - 120, title)


    title = fix_arabic("۱- فرمانده یگان:....................") 
    c.setFont("PersianFont", 10)
    c.drawRightString(width -300, height - 125, title)
    title = fix_arabic("۲- رییس پرسنلی یگان:....................") 
    c.setFont("PersianFont", 10)
    c.drawRightString(width - 300, height - 140, title)
    title = fix_arabic("۳- فرمانده یا رپیس مستقیم:....................") 
    c.setFont("PersianFont", 10)
    c.drawRightString(width - 300, height - 155, title)
   
    
    table_data = [
        [
         get_display(arabic_reshaper.reshape("استفاده یا عدم استفاده \nاز تسهیلات زیست و غذا")),
         get_display(arabic_reshaper.reshape("تاریخ ورود به واحد اصلی")),
         get_display(arabic_reshaper.reshape("تاریخ خروج از محل ماموریت")),
         get_display(arabic_reshaper.reshape("وسیله مراجعت")),
         get_display(arabic_reshaper.reshape("تاریخ ورود به محل ماموریت")),
         get_display(arabic_reshaper.reshape("وسیله عزیمت")),
         get_display(arabic_reshaper.reshape("تاریخ عزیمت")),
        ],
        
        [
         get_display(arabic_reshaper.reshape(data['task_duration'])),
         get_display(arabic_reshaper.reshape(data['task_subject'])),
         get_display(arabic_reshaper.reshape(data['car_license_plate'])),
         get_display(arabic_reshaper.reshape(data['driver_num'])),
         get_display(arabic_reshaper.reshape(data['driver_name'])),
         ]]

    table = Table(table_data, colWidths=[80, 80, 80,80,80,80])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, -1), 'PersianFont'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    table.wrapOn(c, width, height)
    table.drawOn(c, width - 530, height - 250)

    title = fix_arabic("محل امضای رییس:") 
    c.setFont("PersianFont", 10)
    c.drawRightString(width -50, height - 300, title)
    title = fix_arabic("محل امضای راننده:") 
    c.setFont("PersianFont", 10)
    c.drawRightString(width -200, height - 300, title)
    title = fix_arabic("محل امضای ناظر:") 
    c.setFont("PersianFont", 10)
    c.drawRightString(width -350, height - 300, title)
    

    title = fix_arabic("امضای دیجیتال:") 
    c.setFont("PersianFont", 10)
    c.drawRightString(width -50, height - 400, title)
    create_qrcode(data['url'])
    c.drawInlineImage("./apps/transportation/tasks_pdf_qrcodes/qrcode.png", width -230, height - 450, width=100, height=100)


    # Save the PDF
    c.showPage()
    c.save()

data = {'driver_name':'امیر محمد غفاری' , 
        'driver_num':'۱۳۷۶۵۴۳۲۱' , 
        'car_license_plate':'۱۲ش۸۷۶',
        'task_subject':'حمل بار',
        'task_duration':'۲ روز',
        'task_start_end':'تهران-تبریز',
        'url':'http://localhost:8000/transportation/car/1/'}

# create_persian_pdf('test.pdf', data)


def load_predefined_points():
    points = [
        {"name": "Tehran", "latitude": 35.6892, "longitude": 51.3890},
        {"name": "Tabriz", "latitude": 38.0800, "longitude": 46.2919},
        {"name": "Mashhad", "latitude": 36.2605, "longitude": 59.6168},
        {"name": "Isfahan", "latitude": 32.4279, "longitude": 51.6894},
        {"name": "Shiraz", "latitude": 29.5926, "longitude": 52.5836},
        {"name": "Karaj", "latitude": 35.8353, "longitude": 50.9928},
        {"name": "Qom", "latitude": 34.6401, "longitude": 50.8764},
        {"name": "Ahvaz", "latitude": 31.3183, "longitude": 48.6693},
        {"name": "Kermanshah", "latitude": 34.3142, "longitude": 47.0650},
        {"name": "Urmia", "latitude": 37.5527, "longitude": 45.0761},
        {"name": "Rasht", "latitude": 37.2800, "longitude": 49.5830},
        {"name": "Zahedan", "latitude": 29.4963, "longitude": 60.8629},
        {"name": "Kerman", "latitude": 30.2839, "longitude": 57.0834},
    ]
    for point in points:
        PredefinedPoint.objects.get_or_create(**point)