import qrcode
from fpdf import FPDF
import csv
import arabic_reshaper
import bidi.algorithm as ba
import shutil


def ar_display(string):
    return ba.get_display(arabic_reshaper.reshape(string))

my_novles = []
with open("workenv/webscrap_task/novels.csv", "r") as my_file:
    my_file = csv.reader(my_file)
    for row in my_file:
        my_novles.append(row)
        
my_novles = my_novles[1:]

def save_to_pdf():
    for novel in my_novles:
        pdf = FPDF(orientation="P", unit="mm", format="A4")
        pdf.add_page()
        img = qrcode.make(novel[2])
        pdf.image(img.get_image(), x=50, y=0, w=120, h=120, link=novel[2])
        pdf.add_font('ArialUnicode',fname='workenv/qr_task/fonts/arial-unicode-ms/arial-unicode-ms.ttf',uni=True)
        pdf.set_font('ArialUnicode', '', 24)
        pdf.set_xy(0, 110)
        text = novel[1] + "\n" + novel[3]
        pdf.multi_cell(225, 35, txt=ar_display(text), align="C")
        pdf.output("workenv/qr_task/covers/" + novel[1] + ".pdf")
        

def compress_directory(directory_name, output_name):
    shutil.make_archive(output_name, 'zip', directory_name)

# ===== run =====

save_to_pdf()
compress_directory("workenv/qr_task/covers/", "workenv/qr_task/books_covers")