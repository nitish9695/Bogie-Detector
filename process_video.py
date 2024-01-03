import cv2 as cv
import os
import numpy as np
from ultralytics import YOLO
from utility import resized
from PIL import Image, ImageTk
import tkinter as tk


# Function to display an image on the canvas
def display_images(canvas, image_array):
    # Convert the NumPy array to a PIL Image
    image = Image.fromarray(np.uint8(image_array))

    # Convert the PIL Image to a PhotoImage
    photo = ImageTk.PhotoImage(image)

    # Update the canvas with the new image
    canvas.create_image(0, 0, anchor=tk.NW, image=photo)
    canvas.image = photo  # Keep a reference to the image to prevent garbage collection

def classify_and_save(image, cls_model_path, save_path, a, side):

    cls_model =YOLO(cls_model_path)

    # Perform classification on the cropped image   
    results = cls_model(image)  # predict on an image
    names_dict = results[0].names
    probs = results[0].probs.data.tolist()
    class_label = names_dict[np.argmax(probs)]  # Modify this line according to your classification function
    
    # Determine the output folder based on the class label
    output_folder = os.path.join(save_path, class_label)
    os.makedirs(output_folder, exist_ok=True)

    # Save the cropped image with a unique filename
    filename = f"{class_label}-{a}_{side}.jpg"
    filepath = os.path.join(output_folder, filename)
    cv.imwrite(filepath, image)     
    
def process_frame(video_path, reco_model, cls_model, save_path, side, canvas, progress_bar):
    # Create a YOLO model
    model = YOLO(reco_model)
    
    # Open the video capture
    cap = cv.VideoCapture(video_path)

    total_frames = int(cap.get(cv.CAP_PROP_FRAME_COUNT))   

    a = 1
    skip_frames = 30
    frame_counter = 0
    start_frame = 0
    object_detected = True

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        frame_counter += 1    
        start_frame += 1   

        # Calculate progress value
        progress_value = (start_frame / total_frames) * 100
        progress_bar["value"] = progress_value
        canvas.update_idletasks()

        # Skip frames
        if frame_counter < skip_frames:
            continue

        # Resize the frame
        #frame = cv.resize(frame, (480, 270))  
        frame = cv.resize(frame, (960, 540))
        # frame = cv.resize( frame, (1920, 1080))            

        results = model(frame, verbose=False, conf=0.5, classes=2)

        for result in results:
            boxes = result.boxes.cpu().numpy()
            for _, box in enumerate(boxes):
                r = box.xyxy[0].astype(int)
                Class = int(box.cls[0])
                name = result.names[Class] + "_" + str(a) + side
                print(r, Class, skip_frames, frame_counter)

                # Draw boxes on the image
                Box_img = cv.rectangle(frame, (r[0] - 10, r[1] - 10), (r[2] + 10, r[3] + 10), (255, 255, 255), 3)
                #cv.imshow("Image", Box_img)                
                #if ((100 < r[0] < 150) and (r[2] - r[0]) > 200):
                if ((200 < r[0] < 300) and (r[2] - r[0]) > 300):
                #if ((400 < r[0] < 600) and (r[2] - r[0]) > 400):
                    if object_detected:                    
                        object_detected = False
                        frame_counter = 0                        
                        crop = Box_img[r[1] - 10: r[3] + 10, r[0] - 10: r[2] + 10]
                        text_image = cv.putText(crop, name,(10, 30),cv.FONT_HERSHEY_SIMPLEX,1,(255, 255, 255),1,cv.LINE_AA)

                        # Resize the frame
                        #text_image = cv.resize(text_image, (640, 320)) 
                        text_image = cv.resize(text_image, (635, 270 ))
                        print(text_image.shape)
                            
                        # Update the canvas with the cropped image
                        display_images(canvas, text_image) 
                        classify_and_save(text_image, cls_model, save_path, a=a, side=side)                  
                        a += 1                   


                if frame_counter >= skip_frames:
                    object_detected = True

        # Check for the "Q" key press
        key = cv.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    # Release the video capture and close all windows
    cap.release()
    cv.destroyAllWindows()


