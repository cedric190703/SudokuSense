import os
import customtkinter as ctk
from PIL import Image
import sys
import cv2
import numpy as np
import time
import threading

sys.path.append('./ImageProcess')
sys.path.append('./Results')

from processing import *
from drawGrid import *

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sudoku Sense")
        self.geometry("700x550")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image
        image_path  = os.path.join(os.path.dirname(os.path.realpath(__file__)),
        "images")
        
        # Icon in the option frame
        self.logo_image = ctk.CTkImage(Image.open(os.path.join(image_path,
        "icon.png")), size=(35, 35))

        # Icon for the main frame
        self.sudoku_image = ctk.CTkImage(Image.open(os.path.join(image_path,
        "logo.png")), size=(500, 425))

        # Icon to import
        self.import_icon = ctk.CTkImage(Image.open(os.path.join(image_path,
        "import.png")), size=(20, 20))

        # Icon to pause
        self.pause_icon = ctk.CTkImage(Image.open(os.path.join(image_path,
        "stop.png")), size=(20, 20))

        # Icon to play
        self.play_icon = ctk.CTkImage(Image.open(os.path.join(image_path,
        "play.png")), size=(20, 20))

        # Icon to resume
        self.resume_icon = ctk.CTkImage(Image.open(os.path.join(image_path,
        "resume.png")), size=(20, 20))

        # Icon to restart
        self.restart_icon = ctk.CTkImage(Image.open(os.path.join(image_path,
        "restart.png")), size=(20, 20))

        # Icon to get the result
        self.result_icon = ctk.CTkImage(Image.open(os.path.join(image_path,
        "result.png")), size=(20, 20))

        # create options frame
        self.option_frame = ctk.CTkFrame(self, corner_radius=0)
        self.option_frame.grid(row=0, column=0, sticky="nsew")
        self.option_frame.grid_rowconfigure(7, weight=1)
        
        # Set the label of the option frame
        self.option_frame_label = ctk.CTkLabel(self.option_frame, 
        text=" Sudoku Sense", image=self.logo_image,
        compound="left", font=ctk.CTkFont(size=15, weight="bold"))

        self.option_frame_label.grid(row=0, column=0, padx=20, pady=20)

        # Import
        self.button_import = ctk.CTkButton(self.option_frame, text="Import ",
        image=self.import_icon, compound="left", fg_color="#23272d",
        command=self.importImage)
        self.button_import.grid(row=1, column=0, padx=2, pady=15)

        # Get result
        self.button_import = ctk.CTkButton(self.option_frame, text="Result  ",
        image=self.result_icon, compound="left", fg_color="#23272d",
        command=self.getResult)
        self.button_import.grid(row=2, column=0, padx=2, pady=15)

        # Play
        self.button_play = ctk.CTkButton(self.option_frame, text="Play     ",
        image=self.play_icon, compound="left", fg_color="#23272d", command=self.startApp)
        self.button_play.grid(row=3, column=0, padx=2, pady=15)

        # Pause
        self.button_restart = ctk.CTkButton(self.option_frame, text="Pause   ",
        image=self.pause_icon, compound="left", fg_color="#23272d", command=self.pauseApp)
        self.button_restart.grid(row=4, column=0, padx=2, pady=15)

        # Resume
        self.button_restart = ctk.CTkButton(self.option_frame, text="Resume",
        image=self.resume_icon, compound="left", fg_color="#23272d", command=self.resumeApp)
        self.button_restart.grid(row=5, column=0, padx=2, pady=15)

        # Restart
        self.button_pause = ctk.CTkButton(self.option_frame, text="Restart   ",
        image=self.restart_icon, compound="left", fg_color="#23272d", command=self.restartApp)
        self.button_pause.grid(row=6, column=0, padx=2, pady=15)

        # create home frame
        self.home_frame = ctk.CTkFrame(self, corner_radius=0)
        self.home_frame.grid_columnconfigure(0, weight=1)
        self.home_frame.grid(row=0, column=1, padx=(0, 10), pady=(10, 0), sticky="nsew")

        # Set the label of the main frame
        self.home_frame_large_image_label = ctk.CTkLabel(self.home_frame,
        text="", image=self.sudoku_image)
        self.home_frame_large_image_label.grid(row=0, column=0, padx=20, pady=10)

        # Description of the process
        self.description = ctk.CTkTextbox(master=self, width=225, height=65, corner_radius=0)
        
        # Set the text font and size
        self.description.configure(font=("Optima", 18))

        # Sentence that describes the process
        self.description.insert("0.0", "Import an image and then press the start button to process the selected image.💻")
        self.description.grid(row=7, column=0, padx=10, pady=10, sticky="ew", columnspan=2)
        
        # Step to be situated in the process
        self.step = 0
        
        # Main grid to complete at the end of the process
        self.grid = []

        # Boolean that handle the process when the user clicks on the paused button
        self.paused = 0
    
    # Function to get the binary image
    # First step of this entire part give a clean image (binary)
    def processing(self, image):

        # Convert the image in a Grayscale image
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        self.update_text("step1.1: Convert the image in a Grayscale image.🎥")
        self.update_image(self.convert_cv_PIL(gray))
        time.sleep(2)

        # Apply gaussian blur on the Grayscale image
        blur = cv2.GaussianBlur(gray, (5,5), 0)

        self.update_text("step1.2: Apply gaussian blur on the Grayscale image.🛠")
        self.update_image(self.convert_cv_PIL(blur))
        time.sleep(2)

        # Apply the threshold on the blur image
        binary = cv2.adaptiveThreshold(blur, 255,
        cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 4)
        
        self.update_text("step1.3: Apply the threshold on the blur image.⚙")
        self.update_image(self.convert_cv_PIL(binary))
        time.sleep(2)

        return binary

    # Function to update the image instantly
    def update_image(self, image):
        # Create a new CTkImage object with the updated image
        updated_sudoku_image = ctk.CTkImage(image, size=(500, 425))

        # Update the image on the main frame
        self.home_frame_large_image_label.configure(image=updated_sudoku_image)
        self.home_frame_large_image_label.update()

    # Convert the openCV image into a PIL image
    def convert_cv_PIL(self, image):
        # Convert image from BGR to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Create PIL image object
        image_pil = Image.fromarray(image_rgb)

        return image_pil

    # Function to update the text instantly
    def update_text(self, text):
        self.description.delete("0.0", "25.25")
        self.description.insert("0.0", text)
    
    # Function to handle the "Import" button press
    # For the image of the Sudoku in the right frame
    def importImage(self):
        # correct format of the Sudoku image
        f_types = [('Jpg Files', '*.jpg'), ('Png Files', '*.png')]

        # Select a file from files
        filename = ctk.filedialog.askopenfilename(filetypes=f_types)

        # Get the image from the path
        image = Image.open(filename).convert('RGB')
        
        # Reset the image to update the image on the frame
        self.sudoku_image._light_image = image
        self.sudoku_image._dark_image = image

        # Update the image label
        self.update_image(image)
    
    # Function to get the solved grid
    def getResult(self):
        # Check step code to see if the result is finished
        if(self.step == 9):
            # Create the final Sudoku image
            image_path = "sudoku_completed.jpg"

            # Call the main function to get the image result
            mainDraw(self.grid)

            # Open the final image
            final_image = Image.open(image_path)

            self.update(final_image)
    
    # Function that launches App
    def startApp(self):

        # Convert PIL image into openCV IMAGE
        image = cv2.cvtColor(np.array(self.sudoku_image._light_image.convert('RGB')),
        cv2.COLOR_RGB2BGR)

        self.step += 1
        # First step of the application
        binary = self.processing(image)
        
        if(self.paused):
            return
        
        # Step 2 : Finding the grid
        self.step += 1

        # Step 2, 3 : Finding, cutting the Sudoku grid
        # Step 4 : Apply the perspective transform on the image
        # Start the image preprocessing before
        (status, image) = mainProcessing(binary)

        # Check status
        if(status):
            # Show the perspective 
            self.update_text("step3: Show result.🎇")
            self.update_image(self.convert_cv_PIL(image))
            time.sleep(2)

            if(self.paused):
                return
        
            # Step 5 : Recognize digits in the grid
            self.step = 5
            # TODO

            
            if(self.paused):
                return
        
            # Step 6 : Solve grid
            self.step += 1
            # TODO
            
            if(self.paused):
                return
        
            # Step 7 : Show the result
            # The user need to click on the button to show this step
            self.step += 1
            # TODO
        else:
            # Error in the processing of the image
            self.update_text("An error occurs on the step: "+self.step)

    # Function to pause App
    def pauseApp(self):
        self.paused = 1

    # Function to resume App
    def resumeApp(self):
        self.paused = 0
        threading.Thread(target=self.startApp).start()

    # Function to restart App
    def restartApp(self):
        self.paused = 1
        self.startApp()

# Main function for the Tkinter UI interface
def mainInterface():
    # Initialize a root windows for the interface
    app = App()
    app.mainloop()

# Test the main function
mainInterface()