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
import functions as f
from tkinter import messagebox as msg

class LoginPage(tk.Frame):
    # Login page frame
    # Provides an interface for users to:
    # - Enter username and password
    # - Authenticate credentials via the functions module
    # - Navigate to the signup page, update password if credential existed
    # - Access the dashboard upon successful login


    def __init__(self, controller):
        super().__init__(controller)
        self.controller = controller

        # Set defaults configuration BEFORE creating pages
        self.option_add("*Font", "TkDefaultFont 12") # Default font for frames and entry fields
        self.option_add("*Label.Font", "TkDefaultFont 9")  # Font specifically for labels
        self.option_add("*Foreground", "black") # Default text color for widgets
        

        # Defining Title for this Frame - Window Form
        self.controller.title("Login")

        


        # label and set font size, text color - placement of label
        tk.Label(self, text="Network Scanner Automation", font=("TkDefaultFont", 14), fg="black").grid(row=0, column=0, columnspan=2, padx=51, pady=40)

        # Username label and entry with placement
        tk.Label(self, text="Username").grid(row=1, column=0, padx=40, pady=0, sticky="w")
        self.entUser = tk.Entry(self, width=35)
        self.entUser.grid(row=2, column=0, padx=40, pady=0, sticky="n")

        # Password label and entry with placement
        tk.Label(self, text="Password").grid(row=3, column=0, padx=40, pady=(20,0), sticky="w")
        self.entPass = tk.Entry(self, width=35, show="•") # if user input show '*" instead the letters,number and special charaters"
        self.entPass.grid(row=4, column=0, padx=40, pady=0, sticky="n")

        # Button for login 
        self.btnLogin = tk.Button(self, text="Login", command=self.Login)
        self.btnLogin.grid(row=6, column=0, padx=90, pady=(15,10), sticky="n") #place(relx=0.47, rely=0.68, anchor='center')


        response = f.GetAccountReadJson() # Call module functions to check if credential exist - json file exist
        #   if existed - display update password button
        #   if not - display signup

        if response:
            self.entUser.insert(0, response) # insert value from response to username entry
            self.entUser.config(state="disabled") # Disabled the entry field 
            self.entPass.config(state="normal")
            self.btnLogin.config(state="normal")
            tk.Button(self, text="Update Password", command=lambda: controller.show_frame("UpdatePasswordPage")).grid(row=7, column=0, padx=90, pady=(0,5), sticky="n") 

        else:
            self.entUser.config(state="disabled")
            self.entPass.config(state="disabled")
            self.btnLogin.config(state="disabled")
            tk.Label(self, text="No Account. Please Create an account. ", font=("TkDefaultFont", 9), fg="red").grid(row=8, column=0, pady=10) 
            tk.Button(self, text="Sign up", command=lambda: controller.show_frame("SignupPage")).grid(row=7, column=0, padx=90, pady=(0,5), sticky="n") 
                                                  # Use lambda to delay function execution until user click.
                                                  # withou lambda -  it will run immediately the button created and it cause overlapping design
                                                  # https://www.w3schools.com/python/python_lambda.asp
                                                  # https://support.microsoft.com/en-us/office/lambda-function-bd212d27-1cd1-4321-a34a-ccbf254b8b67

            

                                                  
    def Login(self):
        # Authenticate user login.
        # Retrieves username and password from the entry fields,
        # verifies the credentials using module functions
        #   - if json file exist "update password button displyed" otherwise "signup" will display
        # Navigates to the dashboard if successful login. 
        # Displays an error message if authentication fails.

        username = self.entUser.get()
        password = self.entPass.get()
        
        response = f.checkCredentials(password)
        if response is True:     
             self.controller.show_frame("DashboardPage")
        else:
             msg.showerror(f"Login Error", response)
             self.entPass.delete(0, tk.END) # clear the user input - username & password fields
             self.entUser.focus() # set focus to the username field
             self.controller.show_frame("LoginPage")
      