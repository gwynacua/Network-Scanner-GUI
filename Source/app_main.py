
# =================================================================================================================================#
# Copyright © 2026, Gwyn Villegas                                                                                                  #
# System Management and Cybersecurity                                                                                              #
#                                                                                                                                  #
# This program was created for OULTON COLLEGE for learning purposes                                                                #
# This program was developed using variety of resources, including python course from SMC program, programming tutorials, example  #
# code from websites such as github, GeeksforGeeks, Stack overlow as well as AI-assisted tools.                                    #                                                                                                                 #
# This code has been adapted, modified to fit the requirements of this application.                                                #
# =================================================================================================================================#



#-------------------------------------------------
# IMPORTS
#-------------------------------------------------
from login import LoginPage
from signup import SignupPage
from updatepassword import UpdatePassword
from dashboard import Dashboard
import tkinter as tk
from tkinter import messagebox as msg
import functions as f


class App(tk.Tk):
    # Main application frame.
    # Manages all application frames and handles navigation between pages using the show_frame() method.

    def __init__(self):
        # Initialize the main application with all available pages.
        # This method sets up a dictionary `self.frames` that maps page names to their corresponding page classes. It allows easy navigation between pages such as Login, Signup, Password Update, and Dashboard.

        super().__init__()
        self.frames = {
            "LoginPage": LoginPage,
            "SignupPage": SignupPage,
            "UpdatePasswordPage": UpdatePassword,
            "DashboardPage": Dashboard
        }

        self.current_frame = None
        self.show_frame("LoginPage")


    def show_frame(self, page_name):
        # switch frames to specificed page and resize the windows 
        # page_name paramenter is the page to displaye (e.g login/signup/update/dashboard)
        # destroy/close current frame if one existed.
        # Adjust the window size based on page 
        #   for login/signup/updatepassword is set to default
        #   if dashboard it set to 570,700

        if self.current_frame:
            self.current_frame.destroy()

        frame_class = self.frames[page_name]
        self.current_frame = frame_class(self)
        self.current_frame.pack(fill="both", expand=True)

        # Change window size per page - frame
        if page_name == "LoginPage" or page_name == "SignupPage" or page_name == "UpdatePasswordPage":
            center_window(self, 400, 380) # width, height

        elif page_name == "DashboardPage":
            center_window(self, 570, 700)


    
    def on_close(self):
        # Stop scheduler if the current frame has one
        if hasattr(self.current_frame, "scheduler"):
            self.current_frame.scheduler.shutdown(wait=False)
        self.destroy()



def center_window(root, width=400, height=380):
    # Center a Tkinter window on the screen.
    # This function set the frame/windows form into center on the screen.
    # Calculate x and y coordinates for the Tk root window
    # root (tk.Tk) The tkinter window to center
    # width width of the window set to default 400
    # height set to default 380

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    
    ix = int((screen_width / 2) - (width / 2))
    iy = int((screen_height / 2) - (height / 2))

    root.geometry(f"{width}x{height}+{ix}+{iy}")


if __name__ == "__main__":
    # Entry point for the application.
    #   - Creates the main Tkinter application window.
    #   - Disables window resizing.
    #   - Binds the window close event to the cleanup method.
    #   - Starts the Tkinter event loop.

    app = App()
    app.resizable(False, False)  # disable resizing, need to disable it so it won't ruin my widget placment

    # Bind the close event to the cleanup
    app.protocol("WM_DELETE_WINDOW", app.on_close)
    
    app.mainloop()








