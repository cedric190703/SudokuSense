import customtkinter as ctk
from PIL import Image

# Right frame for the image
class RightFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        # TODO: Add image widget

# Left frame of the interface for :
# Options and the main button to import the image of the Sudoku
class LeftFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        # Button to import the image of the Sudoku
        self.btn1 = ctk.CTkButton(self, text="Import", command=self.importImage)
        self.btn1.grid(row=0, column=0, padx=10, pady=(20, 0), sticky="w")

        # Button to get the final Sudoku grid with the result
        self.btn2 = ctk.CTkButton(self, text="Get result", command=self.getResult)
        self.btn2.grid(row=1, column=0, padx=10, pady=(125, 0), sticky="w")

        # Button to start the main process of the application
        self.btn3 = ctk.CTkButton(self, text="Start", command=self.startApp)
        self.btn3.grid(row=2, column=0, padx=10, pady=(100, 0), sticky="w")

        # Button to pause the process of the application
        self.btn4 = ctk.CTkButton(self, text="Pause", command=self.startApp)
        self.btn4.grid(row=3, column=0, padx=10, pady=(20, 0), sticky="w")

        # Button to restart the process of the application
        self.btn5 = ctk.CTkButton(self, text="Restart", command=self.startApp)
        self.btn5.grid(row=4, column=0, padx=10, pady=(20, 0), sticky="w")

    # Function to handle the "Import" button press
    # For the image of the Sudoku in the right frame
    def importImage():
        pass

    # Function to get the solved grid
    def getResult():
        pass

    # Function that launches App
    def startApp():
        pass
    
    # Function to pause App
    def pauseApp():
        pass

    # Function to restart App
    def restartApp():
        pass

# Class that define the main part of the interface
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sudoku Sense")
        self.geometry("550x550")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Left Frame for all options
        self.leftFrame = LeftFrame(self)
        self.leftFrame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsew")

        # Right Frame for the image process
        self.rightFrame = RightFrame(self)
        self.rightFrame.grid(row=0, column=1, padx=(0, 10), pady=(10, 0), sticky="nsew")

        # Description of the current process of the application
        self.description = ctk.CTkTextbox(master=self, width=350, height=75,corner_radius=0)
        self.description.grid(row=3, column=0, padx=10, pady=10, sticky="ew", columnspan=2)
        self.description.insert("0.0", " Apply the greyscale filter on the image🤖.")

# Main function for the Tkinter UI interface
def mainInterface():
    # Initialize a root windows for the interface
    app = App()
    app.mainloop()

# Test the main function
mainInterface()