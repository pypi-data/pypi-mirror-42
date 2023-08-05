'''
Created on 23/01/2019

@author: a16daviddss
'''

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import BDres
import locale
from reportlab.lib.units import inch


def genfact(id=6):
    """
        Genera la factura del id especificado, si no se especifica la genera del 6 por pruebas
    """
    pdfmetrics.registerFont(TTFont('AnthoniSignature', 'AnthoniSignature.ttf'))
    # pdfmetrics.registerFont(TTFont('LongLiner', 'LongLiner.ttf'))

    infofact = BDres.getfact(id)
    c = canvas.Canvas("factura_" + str(id) + ".pdf", pagesize=A4)
    # c.setFont("Helvetica", 10)
    c.setFont("AnthoniSignature", 10)
    c.setLineWidth(0.25)
    c.line(30, 780, 565, 780)
    c.line(50, 775, 545, 775)
    c.line(30, 780, 50, 775)
    c.line(565, 780, 545, 775)
    ''''c.line(30,815,565,815)
    c.line(50,820,545,820)
    c.line(30,815,50,820)
    c.line(565,815,545,820)'''
    # c.drawString(30, 765, "Factura")
    centrox,centroy = A4[0]/2,A4[1]/2
    camarero = BDres.getcamarero(id)
    #aqui añado la imagen para que el texto quede por encima
    c.drawImage("./hkwm2.png", 120.75, centroy-200, 5*inch, 5*inch)
    c.drawCentredString(297.5, 795, "Restaurante David")
    c.setFont("Helvetica", 10)
    c.drawString(30, 710, "Camarero: " + camarero)
    c.drawString(30, 730, "Nº de factura: " + str(id))
    c.drawRightString(560, 730, "Fecha de factura: " + infofact[4])
    c.drawString(30, 635, "Descripcion")
    c.drawRightString(297.5, 635, "Unidades")
    c.drawRightString(431.25, 635, "Precio")
    c.drawRightString(565, 635, "Total")
    c.setDash(6, 3)
    c.setLineWidth(1)
    c.line(30, 628, 565, 628)
    c.line(30, 625, 565, 625)
    total = 0
    ciclo = 2
    locale.setlocale(locale.LC_ALL, '')
    lineas = BDres.getlineas(id)
    for linea in lineas:
        producto = linea[2]
        cantidad = linea[3]
        info = BDres.getnompre(producto)
        subtotal = cantidad * info[1]
        total = total + subtotal
        c.drawString(30, 640 - (ciclo * 20), info[0].title())
        c.drawRightString(297.5, 640 - (ciclo * 20), str(cantidad))
        c.drawRightString(431.25, 640 - (ciclo * 20), locale.currency(info[1]))
        c.drawRightString(565, 640 - (ciclo * 20), locale.currency(subtotal))
        ciclo = ciclo + 1
    c.line(30, 645 - (ciclo * 20), 565, 645 - (ciclo * 20))
    c.drawRightString(565, 640 - ((ciclo + 1) * 20), "TOTAL:   " + locale.currency(total))
    c.setDash(1, 0)
    c.setFont("AnthoniSignature", 10)
    c.setLineWidth(0.25)
    ''''c.line(30, 20, 565, 20)
    c.line(50, 15, 545, 15)
    c.line(30, 20,50, 15)
    c.line(565, 20,545, 15)'''
    c.line(30, 55, 565, 55)
    c.line(50, 60, 545, 60)
    c.line(30, 55, 50, 60)
    c.line(565, 55, 545, 60)
    c.drawCentredString(297.5, 35, "Gracias Por Su Visita")
    
    c.showPage()
    c.save()

