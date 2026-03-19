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

class UpdatePassword(tk.Frame):
        # Frame for updating user's password
        # This screen:
        # - Displays the current username (disabled field) 
        # - Allows the user to enter a new password
        # - Confirms the new password
        # - Calls the updatePassword function to validate user inputs
  

  def __init__(self, controller):
        # Display update password configuration - layout
        # widger placements
    
        super().__init__(controller)
        self.controller = controller

        
        # Make column 0 expand to fill space
        self.grid_columnconfigure(0, weight=1) # column 0 expands horizontally
        # self.grid_rowconfigure(0, weight=1)     # row 0 expands vertically

        self.controller.title("Update Password")  # Defining Title for this Frame - Window Form

        # Set defaults configuration BEFORE creating pages
        self.option_add("*Font", "TkDefaultFont 12")  # Default font for frames and entry fields
        self.option_add("*Label.Font", "TkDefaultFont 9")  # Font specifically for labels
        self.option_add("*Foreground", "black") # Default text color for widgets

        
        tk.Label(self, text="Update Password", font=("TkDefaultFont", 14)).grid(row=0, column=0, columnspan=2, padx=110, pady=20, sticky="n")

         
        tk.Label(self, text="Username").grid(row=1, column=0, padx=40, pady=0, sticky="w")
        self.entUser = tk.Entry(self, width=35)
        self.entUser.grid(row=2, column=0, padx=40, pady=(0,15), sticky="n")
         
        response = f.GetAccountReadJson() # Get username 
        self.entUser.insert(0, response)
        self.entUser.config(state="disabled") # Disabled the entry field 

        tk.Label(self, text="Update Password").grid(row=3, column=0, padx=40, pady=0, sticky="w")
        self.entPass = tk.Entry(self, width=35, show="•")
        self.entPass.grid(row=4, column=0, padx=40, pady=(0,15), sticky="n")

        tk.Label(self, text="Confirm Password ").grid(row=5, column=0, padx=40, pady=0, sticky="w")
        self.entCpass = tk.Entry(self, width=35, show="•")
        self.entCpass.grid(row=6, column=0, padx=40, pady=(0,15), sticky="n")


        tk.Button(self, text="Update Password", command=self.UpdatePassword).grid(row=7, column=0, pady=5, sticky="s")

        tk.Button(self, text="Back", command=lambda: controller.show_frame("LoginPage")).grid(row=8, column=0,  sticky="s")

     
     
  def UpdatePassword(self):
      # Updates the user password by calling the password update function.
      # Retrieve user input from password and confirm password fields
      # Call the updatePassword function
      # - if the response is true: Display success message and navigate to login page
      # - if the response is not true: Display error message, clear both field and set focus bac to password field.

      sPassword = self.entPass.get()
      sConfirmpass = self.entCpass.get()

      response = f.updatePassword(sPassword, sConfirmpass)
      if response is True:
          msg.showinfo("Success", "Password has been updated")
          self.controller.show_frame("LoginPage")
      else:
          msg.showerror("Error", response)
          self.entPass.delete(0, tk.END)
          self.entCpass.delete(0, tk.END)
          self.entPass.focus() # set focus to the confirm password field
        #   self.controller.show_frame("LoginPage")
       