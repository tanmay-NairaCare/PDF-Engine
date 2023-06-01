import os
from pdf2image import convert_from_path
import PyPDF2
def convert_pdf_to_image(filepath):
    pdfFile = open(filepath, 'rb+')
    pdf_reader = PyPDF2.PdfReader(pdfFile)
    if pdf_reader.is_encrypted:
        password = input('Enter password:')
        pdf_reader.decrypt(password)

    pdf_writer = PyPDF2.PdfWriter()
    
    # Add all pages of the PDF to the writer object
    for page_num in range(len(pdf_reader.pages)):
        pdf_writer.add_page(pdf_reader.pages[page_num])
    
    # Set all permissions to the PDF
    pdf_writer.encrypt('', '', 0, True)
    
    pdfFile.seek(0)
    pdf_writer.write(pdfFile)
    pdfFile.truncate()
    
    # Create a folder with the same name as the PDF file
    folder_name = os.path.splitext(filepath)[0]
    print(folder_name)
    os.makedirs(folder_name, exist_ok=True)

    # Convert PDF pages to images and save them in the folder
    images = convert_from_path(filepath,dpi=400)                                                    
    for i, image in enumerate(images):
        image.save(os.path.join(folder_name, f'page{i}.jpg'), 'JPEG')
    return folder_name

