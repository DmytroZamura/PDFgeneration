from utils import PageMode

data_pages = [
    {'page_number': 1,
     'mode': PageMode.light,
     'header': {
         'class_name': 'HeaderElement',
         'breadcrumbs': ('Preliminary', 'Dimorphism', 'Theory')
     },
     'category': {
         'class_name': 'CategoryElement',
         'name': 'Sexual Dimorphism'},
     'body': {
         'class_name': 'BodyElement',
         'title': 'Theory',
         'subtitle': 'What Is It?',
         'text': """
                   <b> Humans</b> have long been fascinated by facial proportions as ultimately these proportions make up the geometry of one’s face. In short, you are your proportions, measurements and ratios.

        Following this, it is easy to understand why proportions are so closely linked to beauty. An attractive face by definition would have to have different proportions to an unattractive one as they inherently look different and have different forms. While this idea has held true for millennia, our application of facial proportions has changed.

        In the early BC years, Ancient Greeks believed in divine proportions and canons of beauty. Think of the ‘Golden Ratio’, ‘Perfect Thirds,’ or similar and we can link them back to the works of early Hellenistic philosophers. In fact, most famous renaissance works such as Michalengo’s ‘David’ statue followed these proportions of beauty..
        However, modern science shows us these proportions of beauty are misguided. They are simply too idealistic to be realistic. Schmid Et al’s research found only a weak link between these Golden Ratios and Neoclassical canons, meaning they are not as closely linked to beauty as humans once thought.

        Instead, in contemporary science, plastic surgeons and orthodontists use ‘Modern Anthropometry,’ where instead of relying on arbitrary proportions and one-size-fits-all shapes, we use demographic data of populations to establish the actual proportions that contribute to attractiveness for that group.

        For example, the features that makes a <u><font face='NeueMontrealMedium'>White Male</font></u> of <u><font face='NeueMontrealMedium'>30 years</font></u> age attractive, may not necessarily be the same proportions that make a <font face='NeueMontrealMedium'><u>Black Womans</u></font> of <font face='NeueMontrealMedium'><u>20 years</u></font> age attractive, which is why Modern Anthropometry is needed. Clincians must compare apples to apples to be precise.

        """
     },
     'footer': {
         'class_name': 'FooterElement',
         'text': """
         FIG 2 : Ratios greater than 1.10  (i.e. there is a 110% difference between you and the most extreme comparisons) are shown here as they are dimorphic traits.
         """,
         'images': ('static/images/face.jpg', 'static/images/face.jpg')
     }
     },
    {'page_number': 2,
     'mode': PageMode.dark,
     'header': {
         'class_name': 'HeaderElement',
         'breadcrumbs': ('Preliminary', 'Dimorphism', 'Assessment')
     },
     'category': {
         'class_name': 'CategoryElement',
         'name': 'Sexual Dimorphism'},
     'body': {
         'class_name': 'BodyStatementElement',
         'title': 'Assessment Overview',
         'subtitle': 'Next Few Pages',
         'text': """
        Our main goal with Facial Proportions is to take an overall look at your facial configuration and dimensions. Later in chapter 2 we  look into individual proportions, feature-by-feature.
        """
     },
     'footer': {
         'class_name': 'FooterTestsElement',
         'text': 'Summary of Tests',
         'headers': ('Table iii', 'Raw Result', 'Explanation'),
         'rows': [
             [
                 'Euclidean Matrix Analysis', 'Saller and colleagues [22]',
                 'The subject has a moderately juvenile face.'
             ],
             [
                 'Dimorphism Analysis', 'Edmondson and colleagues [23]',
                 'Measuring changes of the face as as masculinity is artificially increased or decreased'
             ]
         ]
     }
     }

]
