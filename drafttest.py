'''Tests for pdf_toc_builder.py'''

import pdf_toc_builder as PTB
import config as CF

content_of_pdf = PTB.get_content_from_PDF("./dummydata/DummyPDF.pdf")
print(content_of_pdf )