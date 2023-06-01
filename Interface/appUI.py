import os
import customtkinter as ctk
from PIL import Image
import sys
import cv2
import numpy as np
import time
import threading
import tensorflow as tf
import threading

sys.path.append('./ImageProcess')
sys.path.append('./Results')
sys.path.append('./Solver')

from processing import main_processing
from drawGrid import mainDraw
from solver import mainSolver

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
        command=self.import_image)
        self.button_import.grid(row=1, column=0, padx=2, pady=15)

        # Get result
        self.button_import = ctk.CTkButton(self.option_frame, text="Result  ",
        image=self.result_icon, compound="left", fg_color="#23272d",
        command=self.get_result)
        self.button_import.grid(row=2, column=0, padx=2, pady=15)

        # Play
        self.button_play = ctk.CTkButton(self.option_frame, text="Play     ",
        image=self.play_icon, compound="left", fg_color="#23272d", command=self.start_app)
        self.button_play.grid(row=3, column=0, padx=2, pady=15)

        # Pause
        self.button_restart = ctk.CTkButton(self.option_frame, text="Pause   ",
        image=self.pause_icon, compound="left", fg_color="#23272d", command=self.pause_app)
        self.button_restart.grid(row=4, column=0, padx=2, pady=15)

        # Resume
        self.button_restart = ctk.CTkButton(self.option_frame, text="Resume",
        image=self.resume_icon, compound="left", fg_color="#23272d", command=self.resume_app)
        self.button_restart.grid(row=5, column=0, padx=2, pady=15)

        # Restart
        self.button_pause = ctk.CTkButton(self.option_frame, text="Restart   ",
        image=self.restart_icon, compound="left", fg_color="#23272d", command=self.restart_app)
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
        self.description = ctk.CTkTextbox(master=self, width=225, height=65,
        corner_radius=0)
        
        # Set the text font and size
        self.description.configure(font=("Optima", 18))

        # Sentence that describes the process
        self.description.insert("0.0",
        "Import an image and then press the start button to process the selected image.💻")
        self.description.grid(row=7, column=0, padx=10,
        pady=10, sticky="ew", columnspan=2)
        
        # Step to be situated in the process
        self.step = 0

        #Check if the Sudoku image have been imported
        self.imported = 0

        # Main grid to complete at the end of the process
        self.grid = []

        # Boolean that handle the process when the user clicks on the paused button
        self.paused = 0
    
    # Function to get the binary image
    # First step of this entire part give a clean image (binary)
    def processing(self, image):
        time.sleep(2)
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
    
    def find_grid(self, binary):
        # Find the contours on the binary image
        contours, _ = cv2.findContours(binary, 
                                    cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Filter the contours based on their area
        contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 1000]

        # Sort the contours by area in descending order
        contours = sorted(contours, key=cv2.contourArea, reverse=True)

        # Find the largest contour with 4 sides
        for cnt in contours:
            perimeter = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * perimeter, True)
            if len(approx) == 4:
                return approx.reshape(4, 2)

        # If no suitable contour is found, return None
        return None
    
    # Function to update the image instantly
    def update_image(self, image):
        # Create a new CTkImage object with the updated image
        updated_sudoku_image = ctk.CTkImage(image, size=(465, 415))

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
    def import_image(self):
        self.imported = 1

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
    def get_result(self):
        # Create the final Sudoku image
        image_path = "sudoku_completed.jpg"

        self.update_text("The process is finished.")

        # Open the final image
        final_image = Image.open(image_path)

        self.update_image(final_image)
    
    # Define a timeout handler
    def timeout_handler(self, timer):
        self.update_text("Step6.0: Sudoku could not be solved.")

    # Function that take images and create the Sudoku grid
    def recognize_digits(self, images):
        grid = [[0 for _ in range(9)] for _ in range(9)]
        L = len(images)
        
        # Load the saved model
        model = tf.keras.models.load_model('model.h5')

        for i in range(L):
            x = images[i][1]
            y = images[i][2]
            if images[i][3]:
                # Resize and reshape the image
                image = images[i][0]
                image = cv2.resize(image, (28, 28))
                image = np.array(image)
                image_digit = image.reshape(1, 28, 28, 1)  # Adjust the reshape dimensions

                # Perform prediction using the loaded model
                prediction = np.argmax(model.predict(image_digit)[0])

                # Assign the predicted digit to the corresponding grid cell
                cv2.imshow('digit', image)
                grid[y][x] = prediction
                print(prediction)
        
        return grid
    
    # Function that launches App
    def start_app(self):
        if(not self.imported):
            return
        
        # Convert PIL image into openCV IMAGE
        image = cv2.cvtColor(np.array(self.sudoku_image._light_image.convert('RGB')),
        cv2.COLOR_RGB2BGR)

        # First step of the application
        binary = self.processing(image)
        
        if(self.paused):
            return

        # Step 2 : finding the Sudoku grid
        self.step = 5
        
        grid = []

        try:
            # Try to find the Sudoku grid
            grid = self.find_grid(binary)
        except:
            self.update_text("An error occurs on the step: "+self.step)
            return
        
        # Draw contours in the image
        cv2.drawContours(image, [grid], -1, (0, 255, 0), 2)
        self.update_text("Step2.0: Find the Sudoku grid.🔎")
        self.update_image(self.convert_cv_PIL(image))
        time.sleep(2)

        if(self.paused):
            return

        # Step 3 : cut the Sudoku grid
        (status, images, cut) = main_processing(grid, binary)

        # Check status
        if(status):
            self.update_text("Step3.0: Cut the Sudoku grid.🔪")
            self.update_image(self.convert_cv_PIL(cut))
            time.sleep(2)

            if(self.paused):
                return

            # Step 4 : Recognize digits
            self.update_text("Step4.0: Recognize digits.🤖")
            grid = self.recognize_digits(images)
            print(grid)
            time.sleep(2)
            
            if(self.paused):
                return

            # Set the timeout value (in seconds)
            timeout = 8

            # Create a Timer thread
            timer = threading.Timer(timeout, self.timeout_handler)

            # Step 5: Solve the Sudoku grid
            self.update_text("Step5.0: Solve the Sudoku grid.👌")
            try:
                # Start the timer
                timer.start()

                # Call the mainSolver function
                result = mainSolver(grid)

                # Cancel the timer if the function completes before the timeout
                timer.cancel()

            except TimeoutError:
                # Handle the timeout error
                self.update_text("Step6.0: Sudoku could not be solved.\n"
                +"Click on the 'Result' button to see the grid recognized by the OCR.")
                mainDraw(grid)
                return
            
            if(self.paused):
                return

            # Step 6 : Show Result
            # In this step the user need to press the button
            if(result == -1):
                self.update_text("Step6.0: Sudoku could not be solved.\n"
                +"Click on the 'Result' button to see the grid recognized by the OCR.")
                mainDraw(grid)
            else :
                self.update_text("Step6.0: Click on the 'Result' button to see the grid solved.💯")
                mainDraw(result)

        else:
            self.update_text("An error occurs in the process")

    # Function to pause App
    def pause_app(self):
        self.paused = 1

    # Function to resume App
    def resume_app(self):
        self.paused = 0
        threading.Thread(target=self.startApp).start()

    # Function to restart App
    def restart_app(self):
        self.paused = 1
        self.startApp()

# Main function for the Tkinter UI interface
def main_interface():
    # Initialize a root windows for the interface
    app = App()
    app.mainloop()