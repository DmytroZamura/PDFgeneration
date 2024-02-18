from abc import ABC, abstractmethod
from utils import split_text, getStyleSheet, PageMode, get_page_number_as_str
from reportlab.graphics.shapes import Drawing, String, Line, Circle, Rect
from reportlab.platypus import Paragraph, Image
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle

class ContentElement(ABC):
    def __init__(self, data, width=0, mode: PageMode = PageMode.light):
        self.mode = mode
        self.width = width
        self.styles = getStyleSheet(self.mode)
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)

    @abstractmethod
    def get_content(self):
        pass


class CategoryElement(ContentElement):
    def __init__(self, data, mode: PageMode,
                 h_padding=6,
                 v_padding=4):
        self.name = ''
        self.h_padding = h_padding
        self.v_padding = v_padding
        super().__init__(data, 0, mode)

    def get_content(self):
        fill_color = '#EDEDED' if self.mode == PageMode.light else '#ADC3CA'
        style = self.styles['Catetgory']
        text_color = getattr(style, 'textColor', None)
        font_name = getattr(style, 'fontName', None)
        font_size = getattr(style, 'fontSize', None)
        s = String(self.h_padding, self.v_padding, self.name.upper(), fontSize=font_size,
                   fillColor=text_color,
                   fontName=font_name)
        width = s.getEast() + self.h_padding
        height = font_size + self.v_padding * 2 - 2
        d = Drawing(width, height)
        d.add(Rect(0, 0, width, height, fillColor=fill_color, strokeColor=None))
        d.add(s)
        return d


class HeaderElement(ContentElement):
    def __init__(self, data, width, page_number, mode: PageMode):
        self.breadcrumbs = ()
        self.page_number = get_page_number_as_str(page_number)
        super().__init__(data, width, mode)

    def get_content(self):
        d = Drawing(self.width, 30)
        breadcrumbs_style = self.styles['Breadcrumbs']
        normal_style = self.styles['Normal']
        page_number_style = self.styles['PageNumber']
        elements_width = 0
        between_text_space_width = 10
        text_font_size = getattr(breadcrumbs_style, 'fontSize', None)
        text_font_name = 'NeueMontreal'
        breadcrumbs_text_color = getattr(breadcrumbs_style, 'textColor', None)
        normal_text_color = getattr(normal_style, 'textColor', None)
        page_number_text_color = getattr(page_number_style, 'textColor', None)
        page_number_font_size = getattr(page_number_style, 'fontSize', None)
        circle_radius = 1  # Adjust the radius of the circles
        middle_y = 4  # Adjust the y-coordinate for the circles
        page_number_width = 40
        for i, item in enumerate(self.breadcrumbs):
            last_item = i == len(self.breadcrumbs) - 1
            s = String(elements_width, 0, item, fontSize=text_font_size,
                       fillColor=normal_text_color if last_item else breadcrumbs_text_color,
                       fontName=text_font_name)
            d.add(s)
            elements_width = s.getEast() + between_text_space_width
            if not last_item:
                c = Circle(elements_width, middle_y, circle_radius, fillColor=breadcrumbs_text_color,
                           strokeColor=None, fillOverprint=False)
                d.add(c)
                elements_width += between_text_space_width

        l = Line(elements_width + between_text_space_width, middle_y,
                 self.width - page_number_width - between_text_space_width * 2, middle_y,
                 strokeColor=breadcrumbs_text_color)
        d.add(l)
        s = String(self.width - page_number_width, 0, self.page_number, fontSize=page_number_font_size,
                   fillColor=page_number_text_color,
                   fontName=text_font_name)
        d.add(s)
        return d


class BodyElement(ContentElement):
    def __init__(self, data, width, page_number, mode: PageMode):
        self.text = ''
        self.title = ''
        self.subtitle = ''
        self.page_number = get_page_number_as_str(page_number)
        super().__init__(data, width, mode)

    @property
    def __column_width(self):
        return self.width / 3

    def get_content(self):
        first_text, second_text = split_text(self.text)
        subtitle = SubtitleElement(self.subtitle, self.page_number, self.mode).get_content()
        content_table_body = [
            [subtitle, ''],
            [Paragraph(first_text, self.styles['BodyText']), Paragraph(second_text, self.styles['BodyText'])]
        ]
        content_table = Table(content_table_body, colWidths=[self.__column_width - 10, self.__column_width - 10],
                              rowHeights=(30, 300))
        content_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP')]))
        # Define body content
        body_content = [[Paragraph(self.title, self.styles['Heading1']),
                         content_table]]
        body_table = Table(body_content, colWidths=[self.__column_width, self.__column_width * 2])
        body_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (0, -1), 'TOP')]))
        return body_table


class BodyStatementElement(BodyElement):
    def __init__(self, data, width, page_number, mode: PageMode):
        super().__init__(data, width, page_number, mode)

    def get_content(self):
        column_width = 360
        title = Paragraph(self.title, self.styles['Heading1'])
        subtitle = SubtitleElement(self.subtitle, self.page_number, self.mode).get_content()
        content_table_body = [
            [title],
            [subtitle],
            [Paragraph(self.text, self.styles['Statement'])]
        ]
        content_table = Table(content_table_body, colWidths=(column_width), rowHeights=(130,30, 180),
                              hAlign='LEFT')
        content_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (0, 2), 'TOP'),
        ]))

        return content_table


class SubtitleElement(ContentElement):
    def __init__(self, text, page_number, mode: PageMode):
        self.text = text
        self.page_number = page_number
        super().__init__({}, 0, mode)

    def get_content(self):
        h_padding = 10
        height = 15
        page_number_style = self.styles['FooterText']
        page_number_text_color = getattr(page_number_style, 'textColor', None)
        page_number_font_name = getattr(page_number_style, 'fontName', None)
        page_number_font_size = getattr(page_number_style, 'fontSize', None)
        title_style = self.styles['Subtitle']
        title_text_color = getattr(title_style, 'textColor', None)
        title_font_name = getattr(title_style, 'fontName', None)
        title_font_size = getattr(title_style, 'fontSize', None)
        s = String(0, title_font_size - page_number_font_size, '{}/'.format(self.page_number), fontSize=page_number_font_size,
                   fillColor=page_number_text_color,
                   fontName=page_number_font_name)
        width = s.getEast() + h_padding
        st = String(width, 0, self.text, fontSize=title_font_size,
                   fillColor=title_text_color,
                   fontName=title_font_name)
        d = Drawing(width, height)

        d.add(s)
        d.add(st)
        return d


class FooterElement(ContentElement):
    def __init__(self, data, width, mode: PageMode):
        self.images = []
        self.text = ''
        super().__init__(data, width, mode)

    def get_content(self):
        # Define footer content
        column_width = self.width / 3
        text_content = Paragraph(self.text.upper(), self.styles['FooterText'])
        footer_content = [[text_content]]
        for image in self.images:
            footer_content[0].append(Image(image, width=174, height=171, kind='proportional'))
        footer_table = Table(footer_content, colWidths=[column_width, column_width, column_width])
        return footer_table


class FooterTestsElement(FooterElement):
    def __init__(self, data, width, mode: PageMode):
        self.headers = ()
        self.rows = [[]]
        super().__init__(data, width, mode)

    def get_content(self):
        column_width = self.width / 3
        text_content = Paragraph('<b>{}</b>'.format(self.text), self.styles['SmallTitle'])
        headers_content = [Paragraph(item.upper(), self.styles['FooterText']) for item in self.headers]
        rows_content = [[Paragraph(cell, self.styles['SmallText']) for cell in item] for item in self.rows]
        footer_content = [[text_content, '', ''],
                          [*headers_content],
                          *rows_content
                          ]
        footer_table = Table(footer_content, colWidths=[column_width, column_width, column_width])
        white_with_opacity = colors.Color(1, 1, 1, alpha=0.1)
        footer_table.setStyle(TableStyle([
            ('LINEBELOW', (0, 1), (-1, -1), 1, white_with_opacity),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        return footer_table