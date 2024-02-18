from abc import ABC, abstractmethod
from utils import split_text, getStyleSheet, PageMode, get_page_number_as_str
from reportlab.graphics.shapes import Drawing, String, Line, Circle, Rect
from reportlab.platypus import Paragraph, Image
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle


class ContentElement(ABC):
    """
    This is an interface for each content element.
    """

    def __init__(self, data, width=0, mode: PageMode = PageMode.light):
        """
        :param data: dictionary of all attributes
        :param width: width of a content element
        :param mode: page mode
        """
        self.mode = mode
        self.width = width
        self.styles = getStyleSheet(self.mode)
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)

    @abstractmethod
    def get_content(self):
        """
        Each child content element should implement realisation for its content.
        """
        pass


class CategoryElement(ContentElement):
    """
    Page category realisation.
    """

    def __init__(self, data, mode: PageMode,
                 h_padding=6,
                 v_padding=4):
        """
        :param data: category data
        :param mode: page mode
        :param h_padding: horizontal padding for the box
        :param v_padding: vertical padding for the box
        """
        # default value for the name
        self.name = ''
        self.h_padding = h_padding
        self.v_padding = v_padding
        super().__init__(data, 0, mode)

    def get_content(self):
        """
        :return: Drawing for the category.
        """
        # defining color. The color depends on the page mode.
        fill_color = '#EDEDED' if self.mode == PageMode.light else '#ADC3CA'
        #define styles for the category
        style = self.styles['Category']
        text_color = getattr(style, 'textColor', None)
        font_name = getattr(style, 'fontName', None)
        font_size = getattr(style, 'fontSize', None)
        s = String(self.h_padding, self.v_padding, self.name.upper(), fontSize=font_size,
                   fillColor=text_color,
                   fontName=font_name)
        width = s.getEast() + self.h_padding
        height = font_size + self.v_padding * 2 - 2
        d = Drawing(width, height)
        # draw box around category using width of the string
        d.add(Rect(0, 0, width, height, fillColor=fill_color, strokeColor=None))
        d.add(s)
        return d


class HeaderElement(ContentElement):
    """
    The header element draws breadcrumbs, a line and a page number.
    """
    def __init__(self, data, width, page_number, mode: PageMode):
        """
        :param data: a dictionary about the header
        :param width: width of the header
        :param page_number:
        :param mode: page mode
        """
        # default values
        self.breadcrumbs = ()
        self.page_number = get_page_number_as_str(page_number)
        # calling a parent constructor to initialise all attributes
        super().__init__(data, width, mode)

    def get_content(self):
        """
        :return: Drawing for the Header.
        """
        d = Drawing(self.width, 30)
        # styles receiving
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

        # breadcrumbs drawing
        for i, item in enumerate(self.breadcrumbs):
            last_item = i == len(self.breadcrumbs) - 1
            s = String(elements_width, 0, item, fontSize=text_font_size,
                       fillColor=normal_text_color if last_item else breadcrumbs_text_color,
                       fontName=text_font_name)
            d.add(s)
            # calculation of the breadcrumbs' width.
            elements_width = s.getEast() + between_text_space_width

            # delimiter between breadcrumbs
            if not last_item:
                c = Circle(elements_width, middle_y, circle_radius, fillColor=breadcrumbs_text_color,
                           strokeColor=None, fillOverprint=False)
                d.add(c)
                elements_width += between_text_space_width
        # delimiter between breadcrumbs and a page number
        l = Line(elements_width + between_text_space_width, middle_y,
                 self.width - page_number_width - between_text_space_width * 2, middle_y,
                 strokeColor=breadcrumbs_text_color)
        d.add(l)

        # drawing a page number
        s = String(self.width - page_number_width, 0, self.page_number, fontSize=page_number_font_size,
                   fillColor=page_number_text_color,
                   fontName=text_font_name)
        d.add(s)
        return d


class BodyElement(ContentElement):
    """
    Drawing for the regular page body.
    """
    def __init__(self, data, width, page_number, mode: PageMode):
        """
        :param data: a dictionary with all body attributes
        :param width: the body width
        :param page_number:
        :param mode: a page mode
        """
        #default values
        self.text = ''
        self.title = ''
        self.subtitle = ''
        # transforming a page number to a string like 01, 02 etc.
        self.page_number = get_page_number_as_str(page_number)
        # calling a parent constructor to initialise all attributes
        super().__init__(data, width, mode)

    @property
    def __column_width(self):
        return self.width / 3

    def get_content(self):
        """
        :return: drawing for the body
        """
        # splitting a text to two columns
        first_text, second_text = split_text(self.text)

        # Create a new content element to draw a subtitle
        subtitle = SubtitleElement(self.subtitle, self.page_number, self.mode).get_content()

        # data for the table
        content_table_body = [
            [subtitle, ''],
            [Paragraph(first_text, self.styles['BodyText']), Paragraph(second_text, self.styles['BodyText'])]
        ]
        # creating and styling a table for the body
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
    """
     Drawing for the regular page body with a statement.
    """
    def __init__(self, data, width, page_number, mode: PageMode):
        """
        :param data: a dictionary with all body attributes
        :param width: the body width
        :param page_number:
        :param mode: a page mode
        """
        # calling a parent constructor to initialise all attributes
        super().__init__(data, width, page_number, mode)

    def get_content(self):
        """
        drawing a simple table with three rows
        :return: drawing for the body
        """
        column_width = 360
        title = Paragraph(self.title, self.styles['Heading1'])
        # Create a new content element to draw a subtitle
        subtitle = SubtitleElement(self.subtitle, self.page_number, self.mode).get_content()
        content_table_body = [
            [title],
            [subtitle],
            [Paragraph(self.text, self.styles['Statement'])]
        ]
        # creating and styling a table for the body
        content_table = Table(content_table_body, colWidths=(column_width), rowHeights=(130, 30, 180),
                              hAlign='LEFT')
        content_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (0, 2), 'TOP'),
        ]))

        return content_table


class SubtitleElement(ContentElement):
    """
     A drawing for the subtitle on the page's body.
    """
    def __init__(self, text, page_number, mode: PageMode):
        """
        :param text: text for the subtitle
        :param page_number:
        :param mode: page mode
        """
        self.text = text
        self.page_number = page_number
        # calling a parent constructor to initialise all attributes
        super().__init__({}, 0, mode)

    def get_content(self):
        """
        :return: A drawing that consists from two elements a page number and a title
        """
        h_padding = 10
        height = 15
        # receiving of the styles
        page_number_style = self.styles['FooterText']
        page_number_text_color = getattr(page_number_style, 'textColor', None)
        page_number_font_name = getattr(page_number_style, 'fontName', None)
        page_number_font_size = getattr(page_number_style, 'fontSize', None)
        title_style = self.styles['Subtitle']
        title_text_color = getattr(title_style, 'textColor', None)
        title_font_name = getattr(title_style, 'fontName', None)
        title_font_size = getattr(title_style, 'fontSize', None)
        # a drawing for the page number
        s = String(0, title_font_size - page_number_font_size, '{}/'.format(self.page_number),
                   fontSize=page_number_font_size,
                   fillColor=page_number_text_color,
                   fontName=page_number_font_name)
        # calculation of the width to add a title
        width = s.getEast() + h_padding
        # a drawing for the title
        st = String(width, 0, self.text, fontSize=title_font_size,
                    fillColor=title_text_color,
                    fontName=title_font_name)
        d = Drawing(width, height)

        d.add(s)
        d.add(st)
        return d


class FooterElement(ContentElement):
    """
    A drawing for the regular footer.
    """
    def __init__(self, data, width, mode: PageMode):
        """
        :param data: a dictionary with all body attributes
        :param width: footer width
        :param mode: page mode
        """
        # default values
        self.images = []
        self.text = ''
        # calling a parent constructor to initialise all attributes
        super().__init__(data, width, mode)

    def get_content(self):
        """
        :return: a drawing for the footer
        """
        # calculation for the columns width
        column_width = self.width / 3
        text_content = Paragraph(self.text.upper(), self.styles['FooterText'])
        footer_content = [[text_content]]

        # a drawing for the images
        for image in self.images:
            footer_content[0].append(Image(image, width=174, height=171, kind='proportional'))
        footer_table = Table(footer_content, colWidths=[column_width, column_width, column_width])
        return footer_table


class FooterTestsElement(FooterElement):
    """
    A drawing for the footer with the test results.
    """
    def __init__(self, data, width, mode: PageMode):
        """
        :param data: a dictionary with all body attributes
        :param width: footer width
        :param mode: page mode
        """
        # default values
        self.headers = ()
        self.rows = [[]]
        super().__init__(data, width, mode)

    def get_content(self):
        """
        :return: a table with a test results
        """
        # calculation for the columns width
        column_width = self.width / 3
        # a small title undedr the table
        text_content = Paragraph('<b>{}</b>'.format(self.text), self.styles['SmallTitle'])

        # generation of a header and cells for the table
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
