import os
import customtkinter as ctk
from PIL import Image

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sudoku Sense")
        self.geometry("700x550")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image
        image_path  = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        
        # Icon in the right frame
        self.logo_image = ctk.CTkImage(Image.open(os.path.join(image_path, "icon.png")), size=(35, 35))
        # Icon for the main frame
        self.sudoku_image = ctk.CTkImage(Image.open(os.path.join(image_path, "logo.png")), size=(500, 425))
        # Icon to import
        self.import_icon = ctk.CTkImage(Image.open(os.path.join(image_path, "import.png")), size=(20, 20))
        # Icon to pause
        self.pause_icon = ctk.CTkImage(Image.open(os.path.join(image_path, "pause.png")), size=(20, 20))
        # Icon to play
        self.play_icon = ctk.CTkImage(Image.open(os.path.join(image_path, "play.png")), size=(20, 20))
        # Icon to restart
        self.restart_icon = ctk.CTkImage(Image.open(os.path.join(image_path, "restart.png")), size=(20, 20))
        # Icon to get the result
        self.result_icon = ctk.CTkImage(Image.open(os.path.join(image_path, "result.png")), size=(20, 20))

        # create options frame
        self.option_frame = ctk.CTkFrame(self, corner_radius=0)
        self.option_frame.grid(row=0, column=0, sticky="nsew")
        self.option_frame.grid_rowconfigure(6, weight=1)
        
        self.navigation_frame_label = ctk.CTkLabel(self.option_frame, text=" Sudoku Sense", image=self.logo_image,
                                                             compound="left", font=ctk.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        # Import
        self.button_import = ctk.CTkButton(self.option_frame, text="Import", image=self.import_icon, compound="left", fg_color="#23272d", command=self.importImage)
        self.button_import.grid(row=1, column=0, padx=2, pady=20)

        # Get result
        self.button_import = ctk.CTkButton(self.option_frame, text="Result", image=self.result_icon, compound="left", fg_color="#23272d", command=self.getResult)
        self.button_import.grid(row=2, column=0, padx=2, pady=20)

        # Play
        self.button_play = ctk.CTkButton(self.option_frame, text="Play   ", image=self.play_icon, compound="left", fg_color="#23272d", command=self.startApp)
        self.button_play.grid(row=3, column=0, padx=2, pady=20)

        # Pause
        self.button_restart = ctk.CTkButton(self.option_frame, text="Pause", image=self.restart_icon, compound="left", fg_color="#23272d", command=self.pauseApp)
        self.button_restart.grid(row=4, column=0, padx=2, pady=20)

        # Restart
        self.button_pause = ctk.CTkButton(self.option_frame, text="Restart", image=self.pause_icon, compound="left", fg_color="#23272d", command=self.restartApp)
        self.button_pause.grid(row=5, column=0, padx=2, pady=20)

        # create home frame
        self.home_frame = ctk.CTkFrame(self, corner_radius=0)
        self.home_frame.grid_columnconfigure(0, weight=1)
        self.home_frame.grid(row=0, column=1, padx=(0, 10), pady=(10, 0), sticky="nsew")

        self.home_frame_large_image_label = ctk.CTkLabel(self.home_frame, image=self.sudoku_image)
        self.home_frame_large_image_label.grid(row=0, column=0, padx=20, pady=10)

        # Description of the process
        self.description = ctk.CTkTextbox(master=self, width=225, height=65, corner_radius=0)
        self.description.insert("0.0", " Select an image and press the start button to process.")
        self.description.grid(row=7, column=0, padx=10, pady=10, sticky="ew", columnspan=2)
    
    # Function to handle the "Import" button press
    # For the image of the Sudoku in the right frame
    def importImage(self):
        pass

    # Function to get the solved grid
    def getResult(self):
        pass

    # Function that launches App
    def startApp(self):
        pass
    
    # Function to pause App
    def pauseApp(self):
        pass

    # Function to restart App
    def restartApp(self):
        pass

# Main function for the Tkinter UI interface
def mainInterface():
    # Initialize a root windows for the interface
    app = App()
    app.mainloop()

# Test the main function
mainInterface()