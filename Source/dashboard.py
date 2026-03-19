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
from tkinter import ttk
from tkinter import *
from tkinter import scrolledtext as scroll
import functions as f
import threading
import ipaddress


class Dashboard(tk.Frame):
    # Dashboard frame for the network scanning application.
    # This frame is the main screen where users can start network scans, 
    # set up scheduled scans, and see the scan results. It handles user input, runs scans without freezing the app, and safely updates the display.
    

    def __init__(self, controller):
       # This initiliaze the Dashboard page.
       # - GUI elements (labels, buttons, entry fields, progress bars, scroll text and etc.)
       # - Network interface information (IP, subnet mask, CIDR)
       # - Display current OS of machine
       # - Background scheduler for scan tasks

        super().__init__(controller)
        self.controller = controller

        self.stop_scan = threading.Event()
        self.controller.title("Dashboard")  # Defining Title for this Frame - Window Form


        # Make column 0 expand to fill space
        self.grid_columnconfigure(0, weight=1) # column 0 expands horizontally
        self.grid_rowconfigure(4, weight=1) 


        # Set defaults configuration (font, size and color ) BEFORE creating pages
        self.option_add("*Font", "TkDefaultFont 11")
        self.option_add("*Foreground", "black") 

         # Logout button
        tk.Button(self, text="Logout", command=lambda: controller.show_frame("LoginPage")).grid(row=0, column=0, sticky="ne", padx=30, pady=(40,10))

        # Open File
        self.btnOpenFile = tk.Button(self, text="Open Logs", fg="blue", command=self.OpenFileLog) 
        self.btnOpenFile.grid(row=1, column=0, sticky="ne", padx=30)


        # Get IP address and Subnet mask by calling function module and assigning it by local variables
        self.sIpAddress = f.find_local_ip() 

        self.sMask = f.getSubnetMask() 
        sIpAddress = f"Your Active Interface: {self.sMask[0]}" # Index 0 - display active interface
        tk.Label(self, text=sIpAddress).grid(row=0, column=0, sticky="nw", padx=30, pady=(45,5))

       
        self.sCidr = f.getCIDR(self.sIpAddress, self.sMask[1])# Get CIDR
        tk.Label(self, text=f"IP Address: {self.sIpAddress}").grid(row=1, column=0, sticky="nw", padx=30, pady=(0,5)) #label IP addresss
        tk.Label(self, text=f"Network: {self.sCidr}").grid(row=2, column=0, sticky="nw", padx=30, pady=(0,5)) #label IP addresss

        tk.Label(self, text="TARGET IP ADDRESS: ").grid(row=2, column=0, sticky="nw", padx=30, pady=(50,5)) # Index 1 to display 
        self.EntTargetIP =  tk.Entry(self, width=50)
        self.EntTargetIP.grid(row=2, column=0, sticky="nw", padx=200, pady=(50,5))


        # Normal Scan
        self.BtnScan = tk.Button(self, text="Scan", command=self.NormalScan_Thread) # Scan Button
        self.BtnScan.config(font=("TkDefaultFont", 9, "bold"))
        self.BtnScan.grid(row=2, column=0, sticky="ne", padx=90, pady=(46,5))

        # Cancel Scan button
        self.BtncancelScan = tk.Button(self, text="Cancel",command=self.CancelScan)
        self.BtncancelScan.config(font=("TkDefaultFont", 9, "bold"))
        self.BtncancelScan.grid(row=2, column=0, sticky="ne", padx=30, pady=(46,5))
        self.BtncancelScan.config(state="disabled") 

       
        # Schedule Scan - Menu
        self.dictIntervalOption = {
                "Every 6 Hours": {"hours": 6},
                "Every 12 Hours": {"hours": 12},
                "Daily": {"hours": 24},
                "Every 3 Days": {"days": 3},
                "Weekly": {"weeks": 1},
                "Every 1 minutes": {"minutes": 1} }
       
        tk.Label(self, text="SCHEDULE SCAN:").grid(row=3, column=0, sticky="nw", padx=30, pady=(12,5)) #Label Schedule

        # Dropdown menu
        self.sSelectedOpt = StringVar(value="Every 1 minutes")  # Select/Display index 0 in list
        self.DrpMenuOption = OptionMenu(self, self.sSelectedOpt, *self.dictIntervalOption) 
        self.DrpMenuOption.grid(row=3, column=0, sticky="nw", padx=170, pady=(6,5))
        self.DrpMenuOption.config(font=("TkDefaultFont", 9))
       

        # Start/Schedule Button
        self.BtnSchedScan = tk.Button(self, text="Schedule", command=self.Schedule_Thread) 
        self.BtnSchedScan.grid(row=3, column=0, sticky="e", padx=180, pady=(6,5))
        self.BtnSchedScan.config(font=("TkDefaultFont", 9))
       

        # Stop Schedule Button
        self.BtnStopSched = tk.Button(self, text="Stop", font=("TkDefaultFont", 9, "bold"), command=self.StopScheduleScan) 
        self.BtnStopSched.grid(row=3, column=0, sticky="e", padx=130, pady=(6,5))
        self.BtnStopSched.config(state="disabled")
       

        # Checkbox
        self.isEnableNotification = IntVar()
        self.chkboxNotification = Checkbutton(self, text = "Notification", 
                    variable = self.isEnableNotification, 
                    onvalue = 1, 
                    offvalue = 0, 
                    height = 2, 
                    width = 10,
                    command=self.isNotify) 
        self.chkboxNotification.config(font=("TkDefaultFont", 9))
        self.chkboxNotification.grid(row=3, column=0, sticky="e", padx=25, pady=(2,5))
       


       # List view - ScrolledText
        self.ScrollTextArea = scroll.ScrolledText(self,
                                      wrap = tk.WORD, 
                                      width = 70, 
                                      height = 23, 
                                      font = ("TkDefaultFont",
                                              10))
        self.ScrollTextArea.grid(row=4, column=0, sticky="nsew", padx=25, pady=(2,5))

        # Progress bar widget
        self.progressBar = ttk.Progressbar(self, orient="horizontal", length=506, mode="indeterminate") 
        self.progressBar.grid(row=5, column=0, sticky="ew", padx=28, pady=(2,5))
       
        # Scanning indicator
        self.lblProgress = tk.Label(self, text="", font=("TkDefaultFont", 8)) #label if scanning start
        self.lblProgress.grid(row=6, column=0, sticky="w", padx=28, pady=(1,5))


        # OS running
        self.sCurrentOS = f.GetOs()
        self.lblOS = tk.Label(self, text=f"Current OS: {self.sCurrentOS}", font=("TkDefaultFont", 8), fg="blue")
        self.lblOS.grid(row=7, column=0, sticky="s", pady=(15,5))


#---------------------------------------------------------------------------------------------------------------------------------------
    def isNotify(self):
    # Enable or disable desktop notifications based on user preference and if plyer is installed using pip
    # Check if the user has enabled notification checkbox and call 'checkPlyerModule' to verify if plyer library is installed.
    #       if not message display explaning which this feature is unavailable
    # If plyer is installed, notification appear after scan result successful

         if self.isEnableNotification.get():
              bisPlayerInstall = f.checkPlyerModule()
              if bisPlayerInstall is False:
                   self.isEnableNotification.set(0) # if not installed uncheck box

              else:
                   self.isEnableNotification.set(1) # if installed check box
            

#---------------------------------------------------------------------------------------------------------------------------------------
    def OpenFileLog(self):
    # Open the scan log file using the system's default application.
    # Call 'Open log' function with parameter current OS detected
    # if Open log fail, display error message using tkinter message box
    
        OpenFile = f.OpenLog(self.sCurrentOS)
        if OpenFile is False:
             msg.showinfo("Unavailable", "No Logs Available. Run a scan and then try again.")

        elif OpenFile is True:
             pass
        else:
             msg.showerror("Error", OpenFile)
    


#---------------------------------------------------------------------------------------------------------------------------------------
    def validateTargetIP(self):
        # Validate the target IP address entered by the user.
        # Retrieves the IP address from the entry field.
        # Checks if the entry is empty - Shows an error message if empty and returns False.
        # Checks if the IP address is within the local network range:
        #   - Converts both the target and local network addresses to `ipaddress.ip_network` objects.
        #   - If the target IP is not within the local network, shows an error message and returns False.
        # Returns True if the IP address is valid and within the local network.
        # Handles invalid IP input (ValueError) by showing an error message and returning False.

        # Returns:
        #     bool: True if the target IP is valid and within the local network, False otherwise.
          
        try:
              ipAdd = self.EntTargetIP.get()

              if ipAdd == '':
                   msg.showerror("Error", "Target IP Address field is required.")
                   return False
              
              else:
                   network = ipaddress.ip_network(ipAdd, strict=False)
                   localNetwork = ipaddress.ip_network(self.sCidr, strict=False)
                   if not network.subnet_of(localNetwork):
                       
                       msg.showerror("Invalid IP", "Target IP address entered not within the local network.\nPlease try again.")
                       return False
                   
                   else:
                       
                       return True
                    
        except ValueError:
              msg.showerror("Invalid", "Please input valid IP address.\nPlease try again.")
              return False
        


#---------------------------------------------------------------------------------------------------------------------------------------
    def Schedule_Thread(self):
        # Starts a scheduled scan by launching the ScheduleScan method in a separate daemon thread to keep the GUI responsive during the scan
        # Tkinter is single-threaded,so having this prevent GUI from freezing or become unresponsive if run long taks like network scan
        # Uses APScheduler's BackgroundScheduler to manage scheduled scans.
        # Launches `self.RunSchedule` in a daemon thread to keep the Tkinter GUI responsive.
        # Handles missing APScheduler module by showing an error message and feature won't run

        try:

            from apscheduler.schedulers.background import BackgroundScheduler 
            
            self.scheduler = BackgroundScheduler()
            self.scheduler.start()
           
            
            threading.Thread(target=self.RunSchedule, daemon=True).start()

        except (ModuleNotFoundError, ImportError):

            msg.showerror(
                "Scheduler Not Found or Import Error",
                "The program cannot continue.\n"
                "Please install or fix the APScheduler package using pip."
            )
            self.EntTargetIP.delete(0, tk.END)

       

#---------------------------------------------------------------------------------------------------------------------------------------
    def RunSchedule(self):
    # Validate the target IP and start a scheduled network scan using APScheduler.
    # Removes any previously scheduled jobs to prevent duplicates.
    # Validates the target IP before scheduling.
    # Prompts the user with an informational message about scheduled scans and notifications.
    # If user confirms, schedules the scan at the selected interval and disables GUI controls to prevent changes during the scan.
    # If user cancels or validation fails, clears the target IP entry.

    # Scheduled scan run in background using APSCHEDULER
    # Desktop notification is optional


        if self.scheduler.get_jobs():  # This remove previous jobs - scan
            self.scheduler.remove_all_jobs()
         
        bResponse = self.validateTargetIP() 
        if bResponse:  
            userResponse = msg.askyesnocancel(
                "Information",
                "Starting a scheduled scan requires the program to remain running.\n\n"
                "The selected schedule will determine how often the network scan runs "
                "and how frequently notifications are sent in enabled.\n\n"
                "If you would like to receive desktop notifications, it is recommended to enable or check the notification box.\n\n"
                "Please note that when the device enters sleep mode, the scan will pause and will automatically continue once the device wakes up.\n\n"
                "Do you want to continue?")

            
            if userResponse:  

                selected_option = self.sSelectedOpt.get()
                self.ScrollTextArea.delete(1.0, tk.END)
                intSelected = self.dictIntervalOption.get(selected_option)
                

                self.scheduler.add_job(
                    self.Scan,
                    'interval',
                    **intSelected,
                    max_instances=1,  # prevent overlapping scans
                    coalesce=True   # merge missed runs
                )


                self.DrpMenuOption.config(state="disabled")
                self.BtnScan.config(state="disabled")
                self.BtnSchedScan.config(state="disabled")
                self.EntTargetIP.config(state="disabled")
                self.BtnStopSched.config(state="normal")
                self.chkboxNotification.config(state="disabled")


            else:
                
                self.EntTargetIP.delete(0, tk.END)


        else:
             
                self.EntTargetIP.delete(0, tk.END)




             


#---------------------------------------------------------------------------------------------------------------------------------------
    def NormalScan_Thread(self):
        # Starts a normal scan by launching the NormalScan method in a separate daemon thread to keep the GUI responsive during the scan
        # Tkinter is single-threaded,so having this prevent GUI from freezing or become unresponsive if run long taks like network scan
        
        threading.Thread(target=self.RunNormalScan, daemon=True).start()



#---------------------------------------------------------------------------------------------------------------------------------------
    def RunNormalScan(self):
        # Perform a normal network scan on the target IP address entered by the user.
        # - Clears the previous scan output in the scrolled text area.
        # - Disables the target IP entry and scan button to prevent user interference.
        # - Validates the target IP to ensure it is within the local network.
        # - If valid:
        #     - Enables the cancel button and updates its appearance.
        #     - Starts the progress bar and shows scanning status.
        #     - Disables scheduling options during the scan.
        #     - Calls the Scan() method to perform the network scan.
        #     - Updates the GUI with scan results and resets buttons and progress indicators after completion.
        # - If invalid or cancelled:
        #     - Stops the progress bar.
        #     - Resets all buttons and entry fields to their default state.

        # Threading Note:
        # This method runs in a separate thread (via StartNormalScan) to keep the Tkinter GUI responsive during long scans.
          
            self.ScrollTextArea.delete(1.0, tk.END)   
            self.EntTargetIP.config(state="disabled")
            self.BtnScan.config(state="disabled")

            bResponse = self.validateTargetIP()
            if bResponse:
                self.BtncancelScan.config(state="normal")
                # self.BtncancelScan.config(bg="red", fg="white")
                self.progressBar.start(20)
                self.lblProgress.config(text="Scanning... Please wait..")
                self.DrpMenuOption.config(state="disabled")
                self.BtnSchedScan.config(state="disabled")
                self.BtncancelScan.config(state="normal")
                self.chkboxNotification.config(state="disabled")

                bReturn = self.Scan()
                if bReturn:
                     
                    self.lblProgress.config(text="Scan Completed")  # stop progress indicator

                    self.after(5000, lambda: self.lblProgress.config(text="")) #The label will dissapear
                    self.progressBar.stop()
                    self.BtnScan.config(state="normal")
                    self.EntTargetIP.config(state="normal")
                    self.EntTargetIP.delete(0, tk.END)
                    self.BtnSchedScan.config(state="normal")
                    self.DrpMenuOption.config(state="normal")
                    self.BtncancelScan.config(state="disabled")
                    self.chkboxNotification.config(state="normal")
                    # self.BtncancelScan.config(bg="SystemButtonFace", fg="black")

                
                else:
                    self.progressBar.stop()
                    self.BtnSchedScan.config(state="normal")
                    self.BtnScan.config(state="normal")
                    self.EntTargetIP.config(state="normal")
                    self.EntTargetIP.delete(0, tk.END)
                    self.chkboxNotification.config(state="normal")
                    # self.BtncancelScan.config(bg="SystemButtonFace", fg="black")

                    
            else:
                self.progressBar.stop()
                self.BtnSchedScan.config(state="normal")
                self.BtnScan.config(state="normal")
                self.EntTargetIP.config(state="normal")
                self.EntTargetIP.delete(0, tk.END)
                # self.BtncancelScan.config(bg="SystemButtonFace", fg="black")


    
#---------------------------------------------------------------------------------------------------------------------------------------
    def Scan(self):
        # Perform a network port scan for the IP address or network provided in the GUI
        # The method clears previous results, starts the progress bar, and calls the Scan function to discover active hosts and their open ports.
        # Results are displayed in the scrollable text area and saved to a log file. The scan can be cancelled using the stop event.
        # Saved scan result to a log file
        # If APScheduler is available and scheduled jobs exist, a desktop notification is triggered after the scan completes.
        # Returns: True if the scan is successful otherwise False.

        # if Scan is cancelled using 'stop_scan' event display scan is cancelled.
        # check if desktop notification check is enable and trigger them after by calling function DesktopNotification with parameter of dictionary (dctRiskPort)


        self.stop_scan.clear()

        self.dctHostOpenPorts = {}

        self.dctRiskPort = {}

        sIpAdd = self.EntTargetIP.get()

        # Convert input to a network
        sInputeNetwork = ipaddress.ip_network(sIpAdd, strict=False)

        # Clear previous results and start progress bar
        self.ScrollTextArea.delete(1.0, tk.END)
        self.progressBar.start()

             
        bStatus, result = f.ScanPorts(sInputeNetwork)

        if bStatus:
                if len(result['hosts']) == 0:
                        if self.stop_scan.is_set():
                                # This check if the scan has been cancelled by user
                                # If the stop_scan is set 
                                # - Stop progressBar widget
                                # - Exit the scanning loop
                                # - Prevent further GUI update or processing 
                                self.progressBar.stop()
                                return False
                        
                        self.ScrollTextArea.insert(tk.END, f"No Active host(s) with IP/Network {sIpAdd}")
                        self.after(10000, lambda: self.ScrollTextArea.delete(1.0, tk.END)) #The above label will disappear by 10seconds

                else:
                        if self.stop_scan.is_set():
                            self.progressBar.stop()
                            return False
                        
                        self.ScrollTextArea.tag_configure("bold", font=("Courier", 10, "bold"))
                        self.ScrollTextArea.insert(tk.END, "="*60 + "\n", "bold")
                        self.ScrollTextArea.insert(tk.END, f"Scan Time: {result['scan_time']}\n", "bold")
                        self.ScrollTextArea.insert(tk.END, f"Network: {result['network']}\n", "bold")

                        # Process each host sequentially
                        for host in result["hosts"]:

                            if self.stop_scan.is_set():
                                self.progressBar.stop()
                                return False
                            
                            self.DisplayHostResults(host)
                        

                
                sContent = self.ScrollTextArea.get("1.0", "end-1c") # Retrieve all text currently displayed in scrolledText widget

                # Check if there is content and save it. 
                if sContent.strip(): # this ensures even spaces/newlines don't count
                        sContentInlines = sContent.splitlines()  # Split text into individual lines
                        f.SaveScanLog(sContentInlines) # Save file in .txt by calling function 
                
                else:
                     msg.showerror("Error", sContent)


                self.progressBar.stop() # Stop progress bar after scan done - w/out content
                

                
                if self.isEnableNotification.get():
                     f.DesktopNotification(self.dctRiskPort)
                     

                return True
             
     
        else:
            if self.stop_scan.is_set():
                    self.progressBar.stop()    
                        
            else:
                 
                msg.showerror("Error", result)

            
            return False 

             
              
        

#---------------------------------------------------------------------------------------------------------------------------------------
    def DisplayHostResults(self, host):
    # Display scan results for a single host in the scrollable text area and identify potential high-risk ports
    # Paramters pass from function 'Scan' - dictionary consists of the following: IP Address, Mac Address, OS and Ports 
    # Displays host information and a formatted table of ports.
    # Appends open ports to the host's entry in self.dctHostOpenPorts.   
    # Checks for high-risk ports using the PotentialRiskPorts function.
    # Highlights high-risk ports in red and bold.
    # Updates self.dctRiskPort with risky ports keyed by host IP.                                                        

        sIPadd = host['IP Address']
        
        # Only add new IPs; don't overwrite previous ones
        if sIPadd not in self.dctHostOpenPorts:
            self.dctHostOpenPorts[sIPadd] = {"Ports": []}


        # Display host info in ScrollTextArea
        self.ScrollTextArea.insert(tk.END, "-"*60 + "\n", "bold")
        self.ScrollTextArea.insert(tk.END, f"\nIP Address: {sIPadd}\n", "bold")
        self.ScrollTextArea.insert(tk.END, f"Mac Address: {host['Mac Address']}\n", "bold")
        self.ScrollTextArea.insert(tk.END, f"OS: {host['OS']}\n\n", "bold")

        # Display ports table
        self.ScrollTextArea.insert(tk.END, f"{'PORT':<8}{'STATE':<15}{'SERVICE':<18}{'PROTOCOL'}\n", "bold")
        for port in host["Ports"]:
            self.ScrollTextArea.insert(tk.END, f"{port['Port']:<8}{port['State']:<15}{port['Service']:<18}{port['Protocol']}\n", "bold")
            
            # Append open ports to dictionary
            if port['State'] == 'open':
                iPortNum = port['Port']
                self.dctHostOpenPorts[sIPadd]['Ports'].append(iPortNum)


        # Check for high-risk ports               
        self.dctPotentialRiskPorts = f.PotentialRiskPorts(self.dctHostOpenPorts[sIPadd])

        if self.dctPotentialRiskPorts:
            self.ScrollTextArea.tag_configure("RedFont", foreground="red", font=("arial", 9, "bold"))
            self.ScrollTextArea.insert(tk.END, f"\n\nOPEN PORTS DETECTED _ POTENTIAL SECURITY RISK\n\n", "RedFont")
            for port, info in self.dctPotentialRiskPorts.items():
                self.ScrollTextArea.insert(tk.END, f"Port: {port}\n", "RedFont")
                self.ScrollTextArea.insert(tk.END, f"Service: {info['service']}\n", "RedFont")
                self.ScrollTextArea.insert(tk.END, f"Risk: {info['risk']}\n", "RedFont")
                self.ScrollTextArea.insert(tk.END, f"Explanation: {info['explanation']}\n", "RedFont")
                self.ScrollTextArea.insert(tk.END, f"Advice: {info['advice']}\n", "RedFont")
                self.ScrollTextArea.insert(tk.END, f"Risk Level: {info['level']}\n\n", "RedFont")

                # store risky port by IP
                if sIPadd not in self.dctRiskPort:
                    self.dctRiskPort[sIPadd] = []

                self.dctRiskPort[sIPadd].append(port)

        


#---------------------------------------------------------------------------------------------------------------------------------------
    def CancelScan(self):
        # Cancel an ongoing network scan.
        # Stops the scan thread, halts the progress bar, clears or updates the GUI, resets tkinter widget (button, entry field).
        #   Enabled Buttons: Scan, Schedule Scan, Field for target IP, Notification checkbox
        #   Disabled Buttons: Schedule Stop, Cancel for normal scan
        
        # Shows a temporary message indicating that the scan was cancelled.


        self.progressBar.stop()
        self.lblProgress.config(text="")
        self.ScrollTextArea.insert(tk.END," ========= Scan Cancelled =========")
        self.after(5000, lambda: self.ScrollTextArea.delete(1.0, tk.END)) #The label will dissapear
        self.BtnScan.config(state="normal")
        self.BtnSchedScan.config(state="normal")
        self.EntTargetIP.config(state="normal")
        self.DrpMenuOption.config(state="normal")
        self.BtnStopSched.config(state="disabled")
        self.BtncancelScan.config(state="disabled")
        self.chkboxNotification.config(state="normal")
        self.EntTargetIP.delete(0, tk.END)
        self.stop_scan.set()




#---------------------------------------------------------------------------------------------------------------------------------------
    def StopScheduleScan(self):
    # Stop a currently scheduled network scan.
    # Prompts the user to confirm stopping the scheduled scan.
    # if user click yes:
    #   - Clears the scrollable text area.
    #   - Stops the progress bar.
    #   - Removes all scheduled jobs from the APScheduler scheduler.
    #   - Sets the stop event to cancel any running scan.
    #   - Re-enables GUI controls for scanning.
    #   - Unchecks the notification checkbox.
    #   - Displays a temporary message indicating the scheduled scan has been stopped.
    # Do nothing if user click cancel or no button

        result = msg.askyesnocancel("Stop Scheduled Scan", "Are you sure you want to stop the scheduled scan?")
        if result is True:
            self.ScrollTextArea.delete(1.0, tk.END)
            self.scheduler.remove_all_jobs()
            self.progressBar.stop()
            self.stop_scan.set()
            self.BtnScan.config(state="normal")
            self.BtnSchedScan.config(state="normal")
            self.EntTargetIP.config(state="normal")
            self.DrpMenuOption.config(state="normal")
            self.EntTargetIP.delete(0, tk.END)
            self.chkboxNotification.config(state="normal")
            self.BtnStopSched.config(state="disabled")
            self.ScrollTextArea.get(1.0, tk.END)
            self.isEnableNotification.set(0) # This set uncheck the checkbox if check 
            self.ScrollTextArea.insert(tk.END, "Schedule scan has been stop...")
            self.after(5000, lambda: self.ScrollTextArea.delete(1.0, tk.END)) #The label will dissapear


        else:
             pass
