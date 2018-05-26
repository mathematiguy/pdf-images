import os
import PyPDF2
from PIL import Image

def scrape_images(pdf_path):
         
    file = PyPDF2.PdfFileReader(open(pdf_path, "rb"))
    page = file.getPage(0)

    try:
        xObject = page['/Resources']['/XObject'].getObject()
    except KeyError:
        print("KeyError at:", xObject[obj]['/Name'], "(page %d)" % page_num)

    for obj in xObject:
        if xObject[obj]['/Subtype'] == '/Image':
            name = xObject[obj]['/Name'].replace("/", "")
            size = (xObject[obj]['/Width'], xObject[obj]['/Height'])

            image_folder = os.path.join("images", pdf_path.replace(".pdf", ""))
            filepath = os.path.join(image_folder, name)

            if not os.path.exists(image_folder):
                os.makedirs(image_folder)

            try:
                data = xObject[obj].getData()
            except NotImplementedError:
                print("NotImplementedError at:", xObject[obj]['/Name'], "for filter type", 
                      xObject[obj]['/Filter'], "(page %d)" % page_num)
                continue
            
            if xObject[obj]['/ColorSpace'] == '/DeviceRGB':
                mode = "RGB"
            else:
                mode = "P"

            if xObject[obj]['/Filter'] == '/FlateDecode':
                img = Image.frombytes(mode, size, data)
                img.save(filepath + ".png")
            elif xObject[obj]['/Filter'] == '/DCTDecode':
                img = open(filepath + ".jpg", "wb")
                img.write(data)
                img.close()
            elif xObject[obj]['/Filter'] == '/JPXDecode':
                img = open(filepath + ".jp2", "wb")
                img.write(data)
                img.close()
            else:
                print("No decoder for image %s" % name)

def Main():

    for pdf in os.listdir("pdfs"):        
        if pdf.endswith("pdf"):
            
            pdf_path = os.path.join("pdfs", pdf)
            scrape_images(pdf_path)

if __name__ == "__main__":
    Main()