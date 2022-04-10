import barcode
from barcode.writer import ImageWriter
from PIL import Image, ImageDraw, ImageFilter
import os
from PyPDF2 import PdfFileMerger

# Make sure to close the PDF before rerunning!

# Tracks the code and iterates everytime the program runs (to ensure unique codes)
f = open("./code.txt", 'r')
start_code = int(f.read())
f.close()

# Generate barcodes
num_codes = int(input("How many codes would you like? "))

for i in range(num_codes):
    code128 = barcode.get('code128', str(10000000000 + i + start_code)[1:], writer=ImageWriter())
    filename = code128.save('./barcodes/'+str(10000000000 + i + start_code)[1:])

f = open("./code.txt", 'w')
f.write(str(start_code + num_codes))
f.close()

# Format into pages
barcodesFolder = './barcodes'
barcodes = os.listdir(barcodesFolder)
barcode_size = (800, 450)

i = 0
while len(barcodes) != 0:
    img = Image.new("RGB", (2550, 3300), (255, 255, 255))

    j = i
    while j<(i+6) and len(barcodes) != 0:
        height_pos = (j-i)
        barcode_img = Image.open("./barcodes/"+barcodes[0])
        barcode_img = barcode_img.resize(barcode_size)
        img.paste(barcode_img, (200, 100+(500*height_pos)))

        os.remove("./barcodes/"+barcodes[0])
        barcodes.pop(0)

        j += 1

    if len(barcodes) != 0:
        j = i+6
        while j<(i+12) and len(barcodes) != 0:
            height_pos = (j-(i+6))
            barcode_img = Image.open("./barcodes/"+barcodes[0])
            barcode_img = barcode_img.resize(barcode_size)
            img.paste(barcode_img, (1425, 100+(500*height_pos)))

            os.remove("./barcodes/"+barcodes[0])
            barcodes.pop(0)

            j += 1

    img.save("./barcode_pages/"+str(i)+"_to_"+str(j)+".pdf")

    i += 12


# Combine pages into pdf
barcodePagesFolder = './barcode_pages/'

pages = os.listdir(barcodePagesFolder)

merger = PdfFileMerger()
for i in range(len(pages)): 
    merger.append(barcodePagesFolder+pages[i])

merger.write("./barcode_pdfs/list_of_barcodes.pdf")
merger.close()

for i in range(len(pages)): 
    os.remove(barcodePagesFolder+pages[i])
