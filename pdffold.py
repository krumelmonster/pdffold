import argparse
import fitz
import math

def get_page_dimensions(doc, page_numbers):
    dimensions = None
    
    for num in page_numbers:
        page = doc.load_page(num - 1)
        pagedimensions=(page.rect.width, page.rect.height)
        if dimensions==None:
            dimensions=pagedimensions
        elif dimensions!=pagedimensions:
            return None
    return dimensions

def main():
    parser = argparse.ArgumentParser(description="Shuffle a pdf for booklet printing")
    parser.add_argument("pdf_file", help="Path to the PDF file")
    parser.add_argument("--sel", metavar="SEL", help="Page selection e.g., 1,blank,3,5-11,20-")
    parser.add_argument("-o", "--output", required=True, help="Output PDF file path")
    args = parser.parse_args()

    indoc = fitz.open(args.pdf_file)
    
    page_numbers = []
    if args.sel:
        for part in args.sel.split(","):
            if "-" in part:
                start, end = part.split("-")
                if not start:
                    start=1
                else:
                    start=int(start)
                if not end:
                    end=indoc.page_count
                else:
                    end=int(end)
                if start>end:
                    raise ValueError('Range start>end')
                page_numbers.extend(range(start, end + 1))
            elif part=="blank":
                page_numbers.append(-1)
            else:
                page_numbers.append(int(part))
    else:
        page_numbers = list(range(1, indoc.page_count + 1))

    print(page_numbers)
    dimensions = get_page_dimensions(indoc, page_numbers)
    if dimensions is None:
        print("Not all pages have the same dimensions!")
        exit(1)
    sheetcount=math.ceil(len(page_numbers)/4)

    while len(page_numbers) < 4*sheetcount:
        page_numbers.append(-1)
    pagecount=4*sheetcount

    outdimensions=(dimensions[0]*2, dimensions[1])

    outdoc = fitz.open()

    for sheet in range(sheetcount):
        sheetpages=[
            page_numbers[pagecount-sheet*2-1],
            page_numbers[sheet*2],
            page_numbers[sheet*2+1],
            page_numbers[pagecount-sheet*2-2]
        ]
        uppage=outdoc.new_page(width=outdimensions[0], height=outdimensions[1])
        if sheetpages[0]>0:
            uppage.show_pdf_page(fitz.Rect(0, 0, dimensions[0], dimensions[1]), indoc, pno=sheetpages[0]-1)
        if sheetpages[1]>0:
            uppage.show_pdf_page(fitz.Rect(outdimensions[0]/2, 0, outdimensions[0]/2+dimensions[0], dimensions[1]), indoc, pno=sheetpages[1]-1)
        downpage=outdoc.new_page(width=outdimensions[0], height=outdimensions[1])
        if sheetpages[2]>0:
            downpage.show_pdf_page(fitz.Rect(0, 0, dimensions[0], dimensions[1]), indoc, pno=sheetpages[2]-1)
        if sheetpages[3]>0:
            downpage.show_pdf_page(fitz.Rect(outdimensions[0]/2, 0, outdimensions[0]/2+dimensions[0], dimensions[1]), indoc, pno=sheetpages[3]-1)


    outdoc.save(args.output)

if __name__ == "__main__":
    main()
