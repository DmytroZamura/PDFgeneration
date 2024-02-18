from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from data import data_pages
from document import DocumentGenerator

# Register fonts
pdfmetrics.registerFont(TTFont('NeueMontreal', 'static/fonts/NeueMontreal-Regular.ttf'))
pdfmetrics.registerFont(TTFont('NeueMontrealLight', 'static/fonts/NeueMontreal-Light.ttf'))
pdfmetrics.registerFont(TTFont('NeueMontrealMedium', 'static/fonts/NeueMontreal-Medium.ttf'))
pdfmetrics.registerFont(TTFont('NeueMontrealBold', 'static/fonts/NeueMontreal-Bold.ttf'))
pdfmetrics.registerFont(TTFont('ZagmaMonoTrial', 'static/fonts/F37ZagmaMonoTrial-Regular.ttf'))

if __name__ == '__main__':
    # Create a PDF document
    generator = DocumentGenerator('customer_report.pdf', data_pages)
    # Build the PDF document
    generator.build()

