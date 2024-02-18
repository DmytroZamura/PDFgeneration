from utils import PageMode
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Spacer, TopPadder, PageBreak
from typing import List


class Page():
    def __init__(self, data, width):
        self.mode = data['mode']
        self.page_number = data['page_number']
        self.header = globals()[data['header']['class_name']](data['header'], width, self.page_number, self.mode)
        self.category = globals()[data['category']['class_name']](data['category'], self.mode)
        self.body = globals()[data['body']['class_name']](data['body'], width, self.page_number, self.mode)
        self.footer = globals()[data['footer']['class_name']](data['footer'], width, self.mode)

    def get_story(self):
        return [
            self.header.get_content(),
            Spacer(0, 50),
            self.category.get_content(),
            Spacer(0, 4),
            self.body.get_content(),
            TopPadder(self.footer.get_content()),
        ]


class DocumentGenerator():
    def __init__(self, output_filename, pages):
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
        story = []
        for i, page in enumerate(self.pages):
            if i > 0:
                story.append(PageBreak())
            story.extend(page.get_story())
        return story

    def __onSetPageColor(self, canvas, document):
        if (self.currentMode == PageMode.light):
            self.currentMode = PageMode.dark
        else:
            self.currentMode = PageMode.light
        canvas.setFillColor(self.currentMode.value)
        canvas.rect(0, 0, document.width + document.leftMargin + document.rightMargin, document.height
                    + document.topMargin + document.bottomMargin,
                    fill=True, stroke=False)

    def build(self):
        self.doc.build(self.__get_story(), onLaterPages=self.__onSetPageColor)
