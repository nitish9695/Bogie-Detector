import os
from datetime import datetime
import cv2 as cv
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib import utils
from reportlab.pdfgen import canvas
import os
import re

# function to get current date and time
def get_date_time():
    now = datetime.now()
    return now.strftime("%d-%m-%y_%H-%M")

# function to create folder
def create_folder(folder_name, directory):
    os.chdir(directory)
    os.makedirs(folder_name)
    return os.path.join(directory, folder_name)

# function to resize the frame
def resized(frame, scale_percentage):
    width = int(frame.shape[1] * scale_percentage / 100)
    height = int(frame.shape[0] * scale_percentage / 100)
    dim = (width, height)
    return cv.resize(frame, dim, interpolation=cv.INTER_AREA)


def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)]

def pdf_from_images(folder_path, output_pdf_path):
    c = canvas.Canvas(output_pdf_path, pagesize=landscape(A4))
    width, height = landscape(A4)

    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]
    image_files.sort(key=natural_sort_key)  # Sort images using natural sort

    images_per_page = 8
    images_count = len(image_files)
    current_image_index = 0

    while current_image_index < images_count:
        c.saveState()

        y_offset = height - 10  # Start from the top of the page
        max_img_height = (y_offset - 20) / 4  # Divide available height by number of rows

        for _ in range(4):  # Four rows of images (two parts)
            x_offset = 10  # Start from the left of the page
            max_img_width = (width - 50) / 2  # Adjusted width with space

            for _ in range(2):  # Two columns of images
                if current_image_index >= images_count:
                    break

                image_path = os.path.join(folder_path, image_files[current_image_index])
                img = utils.ImageReader(image_path)
                img_width, img_height = img.getSize()

                aspect_ratio = img_width / img_height

                if aspect_ratio >= 1:  # Landscape image
                    img_width = max_img_width
                    img_height = max_img_width / aspect_ratio
                else:  # Portrait image
                    img_height = max_img_height
                    img_width = max_img_height * aspect_ratio

                c.drawImage(image_path, x_offset, y_offset - img_height, width=img_width, height=img_height)

                x_offset += img_width + 20  # Space between images

                current_image_index += 1

            y_offset -= max_img_height + 5  # Space between rows

        c.restoreState()
        c.showPage()

    c.save()