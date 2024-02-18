from enum import Enum

from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.styles import StyleSheet1, ParagraphStyle


class PageMode(Enum):
    light = '#FFFFFF'
    dark = '#233137'


def get_page_number_as_str(number):
    if number < 10:
        return '0' + str(number)
    else:
        str(number)

def split_text(str):
    middle = round(len(str) / 2)
    if (middle != '.'):
        middle = str.find('.', middle)

    first_text = str[:middle+1]
    second_text = str[middle+1:]
    return (first_text, second_text)


def getStyleSheet(mode: PageMode = PageMode.light):
    stylesheet = StyleSheet1()

    main_text_color = '#121212' if mode == PageMode.light else '#FFFFFF'
    transparent_color = colors.Color(red=0, green=0, blue=0, alpha=0.5) if mode == PageMode.light else colors.Color(0.5,
                                                                                                                    0.5,
                                                                                                                    0.5)
    stylesheet.add(ParagraphStyle(name='Normal',
                                  fontName=('NeueMontreal'),
                                  fontSize=10,
                                  leading=12,
                                  textColor=main_text_color)
                   )
    stylesheet.add(ParagraphStyle(name='Subtitle',
                                  parent=stylesheet['Normal'],
                                  fontName='NeueMontrealMedium')
                   )
    stylesheet.add(ParagraphStyle(name='BodyText',
                                  parent=stylesheet['Normal'],
                                  spaceBefore=6,
                                  alignment=TA_JUSTIFY)
                   )
    stylesheet.add(ParagraphStyle(name='SmallText',
                                  parent=stylesheet['Normal'],
                                  fontSize=8)
                   )
    stylesheet.add(ParagraphStyle(name='SmallTitle',
                                  parent=stylesheet['SmallText'],
                                  fontName='NeueMontrealMedium')
                   )
    stylesheet.add(ParagraphStyle(name='Heading1',
                                  parent=stylesheet['Normal'],
                                  fontName='NeueMontrealMedium',
                                  fontSize=40,
                                  leading=40,
                                  spaceAfter=6,
                                  alignment=TA_LEFT),
                   alias='h1')
    stylesheet.add(ParagraphStyle(name='Statement',
                                  parent=stylesheet['Normal'],
                                  fontSize=20,
                                  leading=20,
                                  firstLineIndent = 60)
                   )
    stylesheet.add(ParagraphStyle(name='Breadcrumbs',
                                  parent=stylesheet['Normal'],
                                  textColor=transparent_color,
                                  alignment=TA_LEFT)
                   )
    stylesheet.add(ParagraphStyle(name='PageNumber',
                                  parent=stylesheet['Normal'],
                                  fontName='NeueMontreal',
                                  leading=12,
                                  alignment=TA_RIGHT,
                                  fontSize=15)
                   )
    stylesheet.add(ParagraphStyle(name='Catetgory',
                                  parent=stylesheet['Normal'],
                                  fontName='ZagmaMonoTrial',
                                  leading=12,
                                  alignment=TA_RIGHT,
                                  textColor = '#233137',
                                  fontSize=8)
                   )

    stylesheet.add(ParagraphStyle(name='FooterText',
                                  parent=stylesheet['Normal'],
                                  fontName='ZagmaMonoTrial',
                                  leading=12,
                                  alignment=TA_LEFT,
                                  fontSize=8,
                                  textColor=transparent_color)
                   )
    return stylesheet
