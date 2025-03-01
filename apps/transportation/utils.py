from persiantools.jdatetime import JalaliDate
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from bidi.algorithm import get_display
import arabic_reshaper

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
    

FONT_PATH = "Vazirmatn-VariableFont_wght.ttf"  # Change to your Persian font file

# Register the font in ReportLab
pdfmetrics.registerFont(TTFont('PersianFont', FONT_PATH))

def create_persian_pdf(filename , data):
    
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    # Set the Persian font
    c.setFont("PersianFont", 14)

    # Persian title (shaped and bidi-corrected)
    title = "برگه ماموریت"
    title_shaped = get_display(arabic_reshaper.reshape(title))
    c.drawString(width - 100, height - 50, title_shaped)

    # Add some Persian text
    text = "مثال"
    text_shaped = get_display(arabic_reshaper.reshape(text))
    c.drawString(width - 400, height - 140, text_shaped)

    # Draw a rectangle around text
    c.rect(width - 420, height - 160, 300, 40, stroke=1, fill=0)

    # Add a Persian table
    from reportlab.platypus import Table, TableStyle
    from reportlab.lib import colors

    data = [
        [get_display(arabic_reshaper.reshape("نام")), get_display(arabic_reshaper.reshape("سن")), get_display(arabic_reshaper.reshape("کشور"))],
        [get_display(arabic_reshaper.reshape("علی")), "۳۰", get_display(arabic_reshaper.reshape("ایران"))],
        [get_display(arabic_reshaper.reshape("زهرا")), "۲۵", get_display(arabic_reshaper.reshape("افغانستان"))],
        [get_display(arabic_reshaper.reshape("محمد")), "۳۵", get_display(arabic_reshaper.reshape("ترکیه"))],
    ]

    table = Table(data, colWidths=[100, 50, 100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'PersianFont'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    table.wrapOn(c, width, height)
    table.drawOn(c, width - 400, height - 300)

    # Save the PDF
    c.showPage()
    c.save()


# from reportlab.pdfgen import canvas
# from reportlab.lib.pagesizes import A4
# from reportlab.pdfbase.ttfonts import TTFont
# from reportlab.pdfbase import pdfmetrics
# from reportlab.platypus import Table, TableStyle
# from reportlab.lib import colors


# pdfmetrics.registerFont(TTFont('Persian', FONT_PATH))  # Ensure you have this TTF file

# def create_persian_pdf(driver_name, personal_number, license_plate, task_subject, output_filename):
#     c = canvas.Canvas(output_filename, pagesize=A4)
#     c.setFont("Persian", 12)
    
#     # Set document title with border
#     c.rect(100, 780, 400, 40)
#     c.drawCentredString(300, 800, "صورت‌حساب مأموریت")
    
#     # Add details with borders
#     details = [
#         ["نام راننده:", driver_name],
#         ["شماره پرسنلی:", personal_number],
#         ["پلاک خودرو:", license_plate],
#         ["موضوع مأموریت:", task_subject]
#     ]
    
#     table = Table(details, colWidths=[150, 250], rowHeights=30, hAlign='RIGHT')
#     table.setStyle(TableStyle([
#         ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#         ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#         ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
#         ('FONTNAME', (0, 0), (-1, -1), 'Persian'),
#         ('FONTSIZE', (0, 0), (-1, -1), 12),
#         ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
#         ('GRID', (0, 0), (-1, -1), 1, colors.black)
#     ]))
    
#     table.wrapOn(c, 50, 600)
#     table.drawOn(c, 100, 600)
    
#     # Footer with border
#     c.rect(100, 80, 400, 40)
#     c.drawCentredString(300, 100, "این سند رسمی و محرمانه است")
    
#     # Save PDF
#     c.save()

# # Example Usage
# create_persian_pdf("علی رضایی", "123456", "۱۲۳-۴۵۶ ایران ۵۱", "حمل و نقل بار به مقصد تهران", "task_bill.pdf")
