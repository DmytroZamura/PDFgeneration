from utils import PageMode
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Spacer, TopPadder, PageBreak
from typing import List
from elements import HeaderElement, CategoryElement, SubtitleElement, BodyElement, \
    BodyStatementElement, FooterElement, FooterTestsElement


class Page():
    """
    This class keeps data about the page, creates all page structure and nested content elements.
    """
    def __init__(self, data, width):
        """
        :param data: dictionary with data about page
        :param width: width of the page. The page use width for drawing elements.
        """
        # Mode of the page (dark or light)
        self.mode = data['mode']
        self.page_number = data['page_number']

        # Dynamic classes assignment using data about the page.
        # Each content element can have different classes for the particular design layout realisation.
        self.header = globals()[data['header']['class_name']](data['header'], width, self.page_number, self.mode)
        self.category = globals()[data['category']['class_name']](data['category'], self.mode)
        self.body = globals()[data['body']['class_name']](data['body'], width, self.page_number, self.mode)
        self.footer = globals()[data['footer']['class_name']](data['footer'], width, self.mode)

    def get_story(self):
        """
        The page generates own story for all content elements.
        :return:
        """
        return [
            self.header.get_content(),
            Spacer(0, 50),
            self.category.get_content(),
            Spacer(0, 4),
            self.body.get_content(),
            TopPadder(self.footer.get_content()),
        ]


class DocumentGenerator():
    """
    This is a class generator of pdf documents.
    This class collects information about pages, generates stories for pages, and builds and saves pdf.
    """

    def __init__(self, output_filename, pages):
        """
        :param output_filename: this file name for a new report
        :param pages: data about pages to prepare report
        """
        self.doc = SimpleDocTemplate(output_filename, pagesize=letter,
                                     showBoundary=0,
                                     leftMargin=inch * 0.2708333333,
                                     rightMargin=inch * 0.2708333333,
                                     topMargin=inch * 0.1666666667,
                                     bottomMargin=inch * 0.5
                                     )
        self.pages: List[Page] = [Page(page, self.doc.width) for page in pages]
        self.currentMode = PageMode.light

    def __get_story(self):
        """
        :return: story content elements for all pages of the document
        """
        story = []
        for i, page in enumerate(self.pages):
            if i > 0:
                story.append(PageBreak())
            story.extend(page.get_story())
        return story

    def __onSetPageColor(self, canvas, document):
        """
        This is a call-back function for starting a new page of the document.
        """
        # Change background color for the page
        if (self.currentMode == PageMode.light):
            self.currentMode = PageMode.dark
        else:
            self.currentMode = PageMode.light
        canvas.setFillColor(self.currentMode.value)
        canvas.rect(0, 0, document.width + document.leftMargin + document.rightMargin, document.height
                    + document.topMargin + document.bottomMargin,
                    fill=True, stroke=False)

    def build(self):
        """
        build document and save document
        """
        self.doc.build(self.__get_story(), onLaterPages=self.__onSetPageColor)
