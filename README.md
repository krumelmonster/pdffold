# pdffold

Say you have a pdf of some book or text and you want to print it, fold it and staple it in order to read it as a book, you can use pdfbook2 or you can use pdffold.

pdffold is in a protype state and under active development.

```
usage: pdffold.py [-h] [--sel SEL] -o OUTPUT pdf_file

Shuffle a pdf for booklet printing

positional arguments:
  pdf_file              Path to the PDF file

options:
  -h, --help            show this help message and exit
  --sel SEL             Page selection e.g., 1,blank,3,5-11,20-
  -o OUTPUT, --output OUTPUT
                        Output PDF file path
```