
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
import os

if not __name__ == "__main__":
    from .models import PredefinedPoint
    QRCODE_FILE ='apps/transportation/tasks_pdf_qrcodes/qrcode.png'
    PDF_FILE = 'apps/transportation/tasks_pdf_qrcodes/'

else:
    QRCODE_FILE ='tasks_pdf_qrcodes/qrcode.png'
    PDF_FILE = 'tasks_pdf_qrcodes/'
    data = {'driver_name':'امیر محمد غفاری' , 
        'driver_num':'۱۳۷۶۵۴۳۲۱' , 
        'car_license_plate':'۱۲ش۸۷۶',
        'task_subject':'حمل بار',
        'task_duration':'۲ روز',
        'task_start_end':'تهران-تبریز',
        'url':'http://localhost:8000/transportation/car/1/'}
    
    fields_to_fill = {
    "امیر غفاری": (1450,1250),  # Example text and position
    "12ش234": (1900,1370),
    "پراید 131":(1700,1370),

}



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
    img.save(QRCODE_FILE)

    
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

def create_persian_pdf_task_bill(filename , data):

    filename = PDF_FILE + filename
    
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    title_1 = fix_arabic("بسمتعالی")
    c.setFont("PersianFont", 12)
    c.drawRightString(width - 250, height - 20, title_1)

    title = fix_arabic("برگه ماموریت")
    c.setFont("PersianFont", 18)
    c.drawRightString(width - 220, height - 60, title)   

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
         get_display(arabic_reshaper.reshape("تاریخ ورود\n به واحد اصلی")),
         get_display(arabic_reshaper.reshape("تاریخ خروج از\n محل ماموریت")),
         get_display(arabic_reshaper.reshape("وسیله مراجعت")),
         get_display(arabic_reshaper.reshape("تاریخ ورود به\n محل ماموریت")),
         get_display(arabic_reshaper.reshape("وسیله عزیمت")),
         get_display(arabic_reshaper.reshape("تاریخ عزیمت")),
        ],
        
        [
         get_display('بله'),
         get_display(arabic_reshaper.reshape('1403/12/12')),
         get_display(arabic_reshaper.reshape('1403/12/11')),
         get_display('پراید 131'),
         get_display(arabic_reshaper.reshape('1403/12/10')),
         get_display(arabic_reshaper.reshape(data['car_license_plate'])),
         data['task_start'],
         ]]

    table = Table(table_data)#, colWidths=[100,100, 100, 60,80,60,60])
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
    table.drawOn(c, width - 500, height - 250)

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
    c.drawInlineImage(QRCODE_FILE, width -230, height - 450, width=100, height=100)


    # Save the PDF
    c.showPage()
    c.save()





import fitz  # PyMuPDF
from PIL import Image, ImageDraw, ImageFont

from arabic_reshaper import reshape
from bidi.algorithm import get_display

# Arabic text formatting function
def ar(text):
    return get_display(reshape(text))

def create_persian_pdf_car_bill(output_pdf, fields):
    """Fill specific fields in a table inside a PDF and save it."""
    input_pdf = 'car_blit_input.pdf'
    filename = PDF_FILE + output_pdf
    doc = fitz.open(PDF_FILE + input_pdf)
    images = []

    for page_num in range(len(doc)):
        # Convert PDF page to high-resolution image
        pix = doc[page_num].get_pixmap(dpi=300)  # High resolution
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        # Draw on the image
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("arial.ttf", 40)  # Adjust size accordingly
        except:
            font = ImageFont.load_default()

        # Fill predefined table fields
        for (text, pos) in fields.items():
            text = ar(text)
            draw.text(pos, text, fill="black", font=font)

        # Store modified image
        images.append(img)

    # Save the edited images back as a high-quality PDF
    images[0].save(filename, save_all=True, append_images=images[1:], resolution=300)

# fill_pdf_table("./tasks_pdf_qrcodes/car_blit_input.pdf", "./tasks_pdf_qrcodes/filled_output.pdf", fields_to_fill)


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