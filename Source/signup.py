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
import tkinter as tk
from tkinter import messagebox as msg
import functions as f

class SignupPage(tk.Frame):
    # Provides an interface for users to:
    # - Enter credentials (full name, email address, username, and password)
    # - Validate input by calling functions from the module
    # - Navigate to the login page upon successful signup

   def __init__(self, controller):
        # Display signup configuration
        # User can input credentials 
        # widger placements

        super().__init__(controller)
        self.controller = controller

        
        # Make column 0 expand to fill space
        self.grid_columnconfigure(0, weight=1) # column 0 expands horizontally
        # self.grid_rowconfigure(0, weight=1)     # row 0 expands vertically

        self.controller.title("Sign up")  # Defining Title for this Frame - Window Form

        # Set defaults configuration BEFORE creating pages
        self.option_add("*Font", "TkDefaultFont 12")  # Default font for frames and entry fields
        self.option_add("*Label.Font", "TkDefaultFont 9")  # Font specifically for labels
        self.option_add("*Foreground", "black") # Default text color for widgets

        
        tk.Label(self, text="Create Account", font=("TkDefaultFont", 12)).grid(row=0, column=0, columnspan=2, padx=120, pady=(10,15), sticky="n")

        tk.Label(self, text="Full Name").grid(row=1, column=0, padx=40, pady=0, sticky="w")
        self.entname = tk.Entry(self, width=35)
        self.entname.grid(row=2, column=0, padx=40, pady=(0,8), sticky="n")

        tk.Label(self, text="Email Address").grid(row=3, column=0, padx=40, pady=0, sticky="w")
        self.entEmail = tk.Entry(self, width=35)
        self.entEmail.grid(row=4, column=0, padx=40, pady=(0,8), sticky="n")

        tk.Label(self, text="Username ").grid(row=5, column=0, padx=40, pady=0, sticky="w")
        self.entUser = tk.Entry(self, width=35)
        self.entUser.grid(row=6, column=0, padx=40, pady=(0,8), sticky="n")

        tk.Label(self, text="Password").grid(row=7, column=0, padx=40, pady=0, sticky="w")
        self.entPass = tk.Entry(self, width=35, show="•")
        self.entPass.grid(row=8, column=0, padx=40, pady=(0,3), sticky="n")


        tk.Button(self, text="Register", command=self.Register).grid(row=9, column=0, pady=5, padx=3, sticky="s")
        tk.Button(self, text="Back", command=lambda: controller.show_frame("LoginPage")).grid(row=10, column=0,  sticky="s")


   def Register(self):
        # Get user input
        # Validate user inputs from module and store the response
        # if response True: show message and return to login form/fram
        # if invalid email address, show error message and delete user input email address
        # if invalid password format, show erroe message and delete user input password

        sName = self.entname.get()
        sEmail = self.entEmail.get().strip()
        sUser = self.entUser.get()
        sPass = self.entPass.get()

        response = f.CreateAccount(sName, sEmail, sUser, sPass) # Validate user inputs and store the response
        if response is True:
            msg.showinfo("Success", "Account created! Please login.") # show message upon sign up successfull
            self.controller.show_frame("LoginPage")

        else:

            msg.showerror("Error", response)
            

       



    
