from utility import get_date_time, create_folder, pdf_from_images
from process_video import process_frame
import tkinter as tk
from tkinter import filedialog
import ttkbootstrap as ttk
from PIL import Image, ImageTk
import threading, os, time
import numpy as np

def main_window():
    
    print("Program Initiated")

    # Function to open a file dialog and set the selected path in an Entry widget
    def browse_file(entry_widget):
        file_path = filedialog.askopenfilename()
        entry_widget.delete(0, tk.END)  # Clear the current text in the entry widget
        entry_widget.insert(0, file_path)  # Insert the selected file path

    # Function to open a directory dialog and set the selected path in an Entry widget
    def browse_directory(entry_widget):
        dir_path = filedialog.askdirectory()
        entry_widget.delete(0, tk.END)  # Clear the current text in the entry widget
        entry_widget.insert(0, dir_path)  # Insert the selected directory path

    # Function to run the video processing tasks using multithreading
    def run_video_processing_thread():
        try:
            start_time = time.perf_counter()
            dir = directory_entry.get()
            path_L = video_L_entry.get()
            path_R = video_R_entry.get()
            dirname = os.path.dirname(__file__)
            reco_model_path = os.path.join(dirname, 'resource', 'bogie.pt')
            cls_model_path = os.path.join(dirname, 'resource', 'Yolo_cls.pt')

            if not dir or not path_L or not path_R:
                result_label_left.config(text="Please provide all the required paths.")
                result_label_left.config(text="Please provide all the required paths.")
                return

            date_time = get_date_time()
            folder_name = f"Folder_{date_time}"
            save_path = create_folder(folder_name, dir)

            def process_and_display(side, video_path, canvas):
                process_frame(video_path, reco_model_path, cls_model_path, save_path, side=side, canvas=canvas, progress_bar=progress_bar)

            # Create threads for left and right video processing
            left_thread = threading.Thread(target=process_and_display, args=["(L)", path_L, canvas_left])
            right_thread = threading.Thread(target=process_and_display, args=["(R)", path_R, canvas_right])

            # Start the threads
            left_thread.start()
            right_thread.start()

            # Wait for both threads to finish
            left_thread.join()
            right_thread.join()        

            output1_pdf = os.path.join(save_path, f'Non- Defective Bogie {date_time}.pdf')
            output2_pdf = os.path.join(save_path, f'Defective Bogie {date_time}.pdf')

            if os.path.exists(os.path.join(save_path, 'Non- Defective Bogie')):
                pdf_from_images(os.path.join(save_path,'Non- Defective Bogie'), output1_pdf)
            if os.path.exists(os.path.join(save_path, 'Defective Bogie')):
                pdf_from_images(os.path.join(save_path,'Defective Bogie'), output2_pdf)

            progress_bar["value"] = 100
            canvas_left.update_idletasks()
            canvas_right.update_idletasks()

            # Display PDF path
            result_label_left.config(text=f"PDF created at: {save_path}")
            result_label_right.config(text=f"PDF created at: {save_path}")

            end_time = time.perf_counter()

            processing_time = end_time - start_time
            print(f"Time taken to process video: {processing_time}")

            # Enable the Run Program button after processing
            run_button.config(state=tk.NORMAL)

        except Exception as e:
            result_label_left.config(text=f"An error occurred: {str(e)}")
            result_label_right.config(text=f"An error occurred: {str(e)}")

    # Modify the run_program_thread function to call run_video_processing_thread
    def run_program_thread():
        run_button.config(state=tk.DISABLED)
        result_label_left.config(text="Processing videos...")
        result_label_right.config(text="Processing videos...")
        # Run video processing using multithreading
        processing_thread = threading.Thread(target=run_video_processing_thread)
        processing_thread.start()


    # Create the main GUI window
    window = ttk.Window(themename="superhero")  # darkly, superhero, flatly, sandstone

    # Get the screen width and height
    window_width = window.winfo_screenwidth()
    window_height = window.winfo_screenheight()

    window.geometry(f"{window_width}x{window_height}") # 1366x768
    window.title("Bogie Detector System")

    dirname = os.path.dirname(__file__)
    logo_path = os.path.join(dirname, 'resource', 'logo.ico')
    window.iconbitmap(logo_path)

    frame_bootstyle = "default"
    button_bootstyle = "primary"
    entry_bootstyle = "primary"
    label_bootstyle = "inverse-primary"

    # Create frames on the main Window
    image_frame = ttk.Frame(master=window, bootstyle=frame_bootstyle, height=310, width=window_width // 2 - 35, borderwidth=4, relief="solid")
    image_frame.grid(row=0, column=0, pady=(30, 2), padx=(30,2))
    image_frame.grid_propagate(False)  # Disable geometry propagation

    input_frame = ttk.Frame(master=window, bootstyle=frame_bootstyle, height=310, width=window_width // 2 - 35, borderwidth=4, relief="solid")
    input_frame.grid(row=0, column=1, pady=(30, 2), padx=(2, 30))
    input_frame.grid_propagate(False)  # Disable geometry propagation

    lower_left_frame = ttk.Frame(master=window, bootstyle=frame_bootstyle, height=320, width=window_width // 2 - 35, borderwidth=4, relief="solid")
    lower_left_frame.grid(row=1, column=0, pady=(2, 30), padx=(30,2))
    lower_left_frame.grid_propagate(False)  # Disable geometry propagation

    lower_right_frame = ttk.Frame(master=window, bootstyle=frame_bootstyle, height=320, width=window_width // 2 - 35, borderwidth=4, relief="solid")
    lower_right_frame.grid(row=1, column=1, pady=(2, 30), padx=(2, 30))
    lower_right_frame.grid_propagate(False)  # Disable geometry propagation

    # Place button on input frame
    browse_directory_button = ttk.Button(input_frame, text="Browse", bootstyle=button_bootstyle, width=15, command=lambda: browse_directory(directory_entry))
    browse_directory_button.grid(row=1, column=3, padx=5, pady=10)

    browse_left_video = ttk.Button(input_frame, text="Browse", bootstyle=button_bootstyle, width=15, command=lambda: browse_file(video_L_entry))
    browse_left_video.grid(row=2, column=3, padx=5, pady=10)

    browse_right_video = ttk.Button(input_frame, text="Browse", bootstyle=button_bootstyle, width=15, command=lambda: browse_file(video_R_entry))
    browse_right_video.grid(row=3, column=3, padx=5, pady=10)

    run_button = ttk.Button(input_frame, text="RUN",  bootstyle=button_bootstyle, width= 15, command=run_program_thread)
    run_button.grid(row=4, column=2, padx=5, ipadx=15, pady=10)

    # Place Entry on input frame
    directory_entry = ttk.Entry(input_frame, width=60, bootstyle=entry_bootstyle)
    directory_entry.insert(0, 'C:/Users/Acer/Desktop/BogieDetector/run')
    directory_entry.grid(row=1, column=2, pady=10)

    video_L_entry = ttk.Entry(input_frame, width=60, bootstyle=entry_bootstyle)
    video_L_entry.insert(0, 'C:/Users/Acer/Desktop/BogieDetector/Test_Video/test_lhb.mp4')
    video_L_entry.grid(row=2, column=2, pady=10)

    video_R_entry = ttk.Entry(input_frame, width=60, bootstyle=entry_bootstyle)
    video_R_entry.insert(0, 'C:/Users/Acer/Desktop/BogieDetector/Test_Video/test_lhb.mp4')
    video_R_entry.grid(row=3, column=2, pady=10)

    # Place label on input frame
    title_label = ttk.Label(input_frame, text="BOGIE DETECTOR SYSTEM", font="roboto 21 bold", bootstyle=label_bootstyle )
    title_label.grid(row=0, columnspan=4, padx=5, ipady=4, pady=10)

    browse_directory_label = ttk.Label(input_frame, text="Directory Path:", font= "roboto 10", bootstyle=label_bootstyle)
    browse_directory_label.grid(row=1, column=1, padx=10, pady=10, ipadx=12, ipady=4)

    browse_left_video_label = ttk.Label(input_frame, text="Left Video Path:", font= "roboto 10",bootstyle=label_bootstyle)
    browse_left_video_label.grid(row=2, column=1, padx=10, pady=10, ipadx=9, ipady=4)

    browse_right_video_label = ttk.Label(input_frame, text="Right Video Path:", font= "roboto 10",bootstyle=label_bootstyle)
    browse_right_video_label.grid(row=3, column=1, padx=10, pady=10, ipadx=5, ipady=4)

    # Place the image_label in the top-left frame
    dirname = os.path.dirname(__file__)
    image_path = os.path.join(dirname, 'resource', 'vande_bharat.png')
    image = Image.open(image_path)
    my_image = ImageTk.PhotoImage(image)
    image_label = tk.Label(image_frame, image=my_image, justify="center")
    image_label.grid(row=0, column=0, padx=2, pady=2)

    # Create progress bar
    progress_bar = ttk.Progressbar(input_frame, mode='determinate', bootstyle= 'default-striped', length=600, maximum=100)
    progress_bar.grid(row=5, columnspan=4, pady=10)

    # Create a canvas for displaying left side images
    canvas_left = tk.Canvas(lower_left_frame, width=635, height=270)
    canvas_left.grid(row=1, pady=10, padx=2, sticky="nsew")

    # Create a canvas for displaying right side images
    canvas_right = tk.Canvas(lower_right_frame, width=635, height=270)
    canvas_right.grid(row=1, pady=10, padx=2, sticky="nsew")

    # Initialize canvas_image as None
    canvas_image = None

    # Place result label on top of botton frame
    result_label_left = ttk.Label(lower_left_frame, font= "roboto 12 bold", bootstyle=label_bootstyle, text="")
    result_label_left.grid(row=0, padx=5, pady=5)
    result_label_left.config(text="Left Side Bogie")

    # Place result label on top of botton frame
    result_label_right = ttk.Label(lower_right_frame, font= "roboto 12 bold", bootstyle=label_bootstyle, text="")
    result_label_right.grid(row=0, padx=5, pady=5)
    result_label_right.config(text="Right Side Bogie")


    window.mainloop()

main_window()


   