# =================================================================================================================================#
# Copyright © 2026, Gwyn Villegas                                                                                                  #
# System Management and Cybersecurity                                                                                              #                     #
# This program was created learning and educational purposes only.                                                                 #
# This program was developed using variety of resources, including python course from SMC program, programming tutorials, example  #
# code from websites such as github, GeeksforGeeks, Stack overlow as well as AI-assisted tools.                                    #                                                                                                                 #
# This code has been adapted, modified to fit the requirements of this application.                                                #
# ================================================================================================================================


#-------------------------------------------------
# IMPORTS
#-------------------------------------------------
import tkinter as tk
from tkinter import ttk
import functions as f
from tkinter import messagebox as msg
from tkinter import *
from tkinter import scrolledtext as scroll
import ipaddress
import threading
from apscheduler.schedulers.background import BackgroundScheduler 
            

root = tk.Tk()
root.resizable(False, False)

dctHostOpenPorts = {}
dctRiskPort = {}


            
scheduler = BackgroundScheduler()
scheduler.start()


def center_window(width=570, height=700):
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


center_window()
root.title("Network Scanner")

stop_scan = threading.Event()

# Make column 0 expand to fill space
root.grid_columnconfigure(0, weight=1) # column 0 expands horizontally
root.grid_rowconfigure(4, weight=1) 

# Set defaults configuration (font, size and color ) BEFORE creating pages
root.option_add("*Font", "TkDefaultFont 11")
root.option_add("*Foreground", "black") 

# Open File
btnOpenFile = tk.Button(root, text="Open Logs", fg="blue", command=lambda:OpenFileLog()) 
btnOpenFile.grid(row=0, column=0, sticky="ne", padx=30, pady=(30,5))


# Get IP address and Subnet mask by calling function module and assigning it by local variables
sIpAddress = f.find_local_ip() 

sMask = f.getSubnetMask() 
sInterface = f"Your Active Interface: {sMask[0]}" # Index 0 - display active interface
tk.Label(root, text=sInterface).grid(row=0, column=0, sticky="nw", padx=30, pady=(25,5))

       
sCidr = f.getCIDR(sIpAddress, sMask[1])# Get CIDR
tk.Label(root, text=f"IP Address: {sIpAddress}").grid(row=0, column=0, sticky="nw", padx=30, pady=(55,0)) #label IP addresss
tk.Label(root, text=f"Network: {sCidr}").grid(row=0, column=0, sticky="nw", padx=30, pady=(83,0)) #label IP addresss

tk.Label(root, text="TARGET IP ADDRESS: ").grid(row=2, column=0, sticky="nw", padx=30, pady=(50,5)) # Index 1 to display 
EntTargetIP =  tk.Entry(root, width=50)
EntTargetIP.grid(row=2, column=0, sticky="nw", padx=200, pady=(50,5))

# Normal Scan
BtnScan = tk.Button(root, text="Scan", command=lambda:NormalScan_Thread()) # Scan Button
BtnScan.config(font=("TkDefaultFont", 9, "bold"))
BtnScan.grid(row=2, column=0, sticky="ne", padx=90, pady=(46,5))

# Cancel Scan button
BtncancelScan = tk.Button(root, text="Cancel",command=lambda:CancelScan())
BtncancelScan.config(font=("TkDefaultFont", 9, "bold"))
BtncancelScan.grid(row=2, column=0, sticky="ne", padx=30, pady=(46,5))
BtncancelScan.config(state="disabled") 


# Schedule Scan - Menu
dictIntervalOption = {
                "Every 2 Hours": {"hours": 2},
                "Every 6 Hours": {"hours": 6},
                "Every 12 Hours": {"hours": 12},
                "Daily": {"hours": 24},
                "Every 3 Days": {"days": 3},
                "Weekly": {"weeks": 1},
                 }
       
tk.Label(root, text="SCHEDULE SCAN:").grid(row=3, column=0, sticky="nw", padx=30, pady=(12,5)) #Label Schedule

# Dropdown menu
sSelectedOpt = StringVar(value="Every 2 Hours")  # Select/Display index 0 in list
DrpMenuOption = OptionMenu(root, sSelectedOpt, *dictIntervalOption) 
DrpMenuOption.grid(row=3, column=0, sticky="nw", padx=170, pady=(6,5))
DrpMenuOption.config(font=("TkDefaultFont", 9))
       
# Start/Schedule Button
BtnSchedScan = tk.Button(root, text="Schedule", command=lambda:Schedule_Thread()) 
BtnSchedScan.grid(row=3, column=0, sticky="e", padx=180, pady=(6,5))
BtnSchedScan.config(font=("TkDefaultFont", 9))
       

# Stop Schedule Button
BtnStopSched = tk.Button(root, text="Stop", font=("TkDefaultFont", 9, "bold"), command=lambda:StopScheduleScan()) 
BtnStopSched.grid(row=3, column=0, sticky="e", padx=130, pady=(6,5))
BtnStopSched.config(state="disabled")
       


# List view - ScrolledText
ScrollTextArea = scroll.ScrolledText(root,
                                      wrap = tk.WORD, 
                                      width = 70, 
                                      height = 23, 
                                      font = ("TkDefaultFont",
                                              10))
ScrollTextArea.grid(row=4, column=0, sticky="nsew", padx=25, pady=(2,5))

# Progress bar widget
progressBar = ttk.Progressbar(root, orient="horizontal", length=506, mode="indeterminate") 
progressBar.grid(row=5, column=0, sticky="ew", padx=28, pady=(2,5))
       
# Scanning indicator
lblProgress = tk.Label(root, text="", font=("TkDefaultFont", 8)) #label if scanning start
lblProgress.grid(row=6, column=0, sticky="w", padx=28, pady=(1,5))

# OS running
sCurrentOS = f.GetOs()
lblOS = tk.Label(root, text=f"Current OS: {sCurrentOS}", font=("TkDefaultFont", 8), fg="blue")
lblOS.grid(row=7, column=0, sticky="s", pady=(15,5))




#---------------------------------------------------------------------------------------------------------------------------------------
def OpenFileLog():
    # Open the scan log file using the system's default application.
    # Call 'Open log' function with parameter current OS detected
    # if Open log fail, display error message using tkinter message box
    
        OpenFile = f.OpenLog(sCurrentOS)
        if OpenFile is False:
             msg.showinfo("Unavailable", "No Logs Available. Run a scan and then try again.")

        elif OpenFile is True:
             pass
        else:
             msg.showerror("Error", OpenFile)
    


#---------------------------------------------------------------------------------------------------------------------------------------
def validateTargetIP():
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
              ipAdd = EntTargetIP.get()

              if ipAdd == '':
                   msg.showerror("Error", "Target IP Address field is required.")
                   return False
              
              else:
                   network = ipaddress.ip_network(ipAdd, strict=False)
                   localNetwork = ipaddress.ip_network(sCidr, strict=False)
                   if not network.subnet_of(localNetwork):
                       
                       msg.showerror("Invalid IP", "Target IP address entered not within the local network.\nPlease try again.")
                       return False
                   
                   else:
                       
                       return True
                    
        except ValueError:
              msg.showerror("Invalid", "Please input valid IP address.\nPlease try again.")
              return False
        


#---------------------------------------------------------------------------------------------------------------------------------------
def Schedule_Thread():
        # Starts a scheduled scan by launching the ScheduleScan method in a separate daemon thread to keep the GUI responsive during the scan
        # Tkinter is single-threaded,so having this prevent GUI from freezing or become unresponsive if run long taks like network scan
        # Uses APScheduler's BackgroundScheduler to manage scheduled scans.
        # Launches `RunSchedule` in a daemon thread to keep the Tkinter GUI responsive.
        # Handles missing APScheduler module by showing an error message and feature won't run

        threading.Thread(target=RunSchedule, daemon=True).start()

       

#---------------------------------------------------------------------------------------------------------------------------------------
def RunSchedule():
    # Validate the target IP and start a scheduled network scan using APScheduler.
    # Removes any previously scheduled jobs to prevent duplicates.
    # Validates the target IP before scheduling.
    # Prompts the user with an informational message about scheduled scans and notifications.
    # If user confirms, schedules the scan at the selected interval and disables GUI controls to prevent changes during the scan.
    # If user cancels or validation fails, clears the target IP entry.

    # Scheduled scan run in background using APSCHEDULER
    # Desktop notification is optional


        if scheduler.get_jobs():  # This remove previous jobs - scan
            scheduler.remove_all_jobs()
         
        bResponse = validateTargetIP() 
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

                selected_option = sSelectedOpt.get()
                ScrollTextArea.delete(1.0, tk.END)
                intSelected = dictIntervalOption.get(selected_option)
                

                scheduler.add_job(
                    Scan,
                    'interval',
                    **intSelected,
                    max_instances=1,  # prevent overlapping scans
                    coalesce=True   # merge missed runs
                )


                DrpMenuOption.config(state="disabled")
                BtnScan.config(state="disabled")
                BtnSchedScan.config(state="disabled")
                EntTargetIP.config(state="disabled")
                BtnStopSched.config(state="normal")


            else:
                
                EntTargetIP.delete(0, tk.END)


        else:
             
                EntTargetIP.delete(0, tk.END)




             


#---------------------------------------------------------------------------------------------------------------------------------------
def NormalScan_Thread():
        # Starts a normal scan by launching the NormalScan method in a separate daemon thread to keep the GUI responsive during the scan
        # Tkinter is single-threaded,so having this prevent GUI from freezing or become unresponsive if run long taks like network scan
        
        threading.Thread(target=RunNormalScan, daemon=True).start()



#---------------------------------------------------------------------------------------------------------------------------------------
def RunNormalScan():
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
          
            ScrollTextArea.delete(1.0, tk.END)   
            EntTargetIP.config(state="disabled")
            BtnScan.config(state="disabled")

            bResponse = validateTargetIP()
            if bResponse:
                BtncancelScan.config(state="normal")
                # BtncancelScan.config(bg="red", fg="white")
                progressBar.start(20)
                lblProgress.config(text="Scanning... Please wait..")
                DrpMenuOption.config(state="disabled")
                BtnSchedScan.config(state="disabled")
                BtncancelScan.config(state="normal")


                bReturn = Scan()
                if bReturn:
                     
                    lblProgress.config(text="Scan Completed")  # stop progress indicator

                    root.after(5000, lambda: lblProgress.config(text="")) #The label will dissapear
                    progressBar.stop()
                    BtnScan.config(state="normal")
                    EntTargetIP.config(state="normal")
                    EntTargetIP.delete(0, tk.END)
                    BtnSchedScan.config(state="normal")
                    DrpMenuOption.config(state="normal")
                    BtncancelScan.config(state="disabled")

                
                else:
                    progressBar.stop()
                    BtnSchedScan.config(state="normal")
                    BtnScan.config(state="normal")
                    EntTargetIP.config(state="normal")
                    EntTargetIP.delete(0, tk.END)


                    
            else:
                progressBar.stop()
                BtnSchedScan.config(state="normal")
                BtnScan.config(state="normal")
                EntTargetIP.config(state="normal")
                EntTargetIP.delete(0, tk.END)
                # BtncancelScan.config(bg="SystemButtonFace", fg="black")


    
#---------------------------------------------------------------------------------------------------------------------------------------
def Scan():
        # Perform a network port scan for the IP address or network provided in the GUI
        # The method clears previous results, starts the progress bar, and calls the Scan function to discover active hosts and their open ports.
        # Results are displayed in the scrollable text area and saved to a log file. The scan can be cancelled using the stop event.
        # Saved scan result to a log file
        # If APScheduler is available and scheduled jobs exist, a desktop notification is triggered after the scan completes.
        # Returns: True if the scan is successful otherwise False.

        # if Scan is cancelled using 'stop_scan' event display scan is cancelled.
        # check if desktop notification check is enable and trigger them after by calling function DesktopNotification with parameter of dictionary (dctRiskPort)


        stop_scan.clear()

        

       

        sIpAdd = EntTargetIP.get()

        # Convert input to a network
        sInputeNetwork = ipaddress.ip_network(sIpAdd, strict=False)

        # Clear previous results and start progress bar
        ScrollTextArea.delete(1.0, tk.END)
        progressBar.start()

             
        bStatus, result = f.ScanPorts(sInputeNetwork)

        if bStatus:
                if len(result['hosts']) == 0:
                        if stop_scan.is_set():
                                # This check if the scan has been cancelled by user
                                # If the stop_scan is set 
                                # - Stop progressBar widget
                                # - Exit the scanning loop
                                # - Prevent further GUI update or processing 
                                progressBar.stop()
                                return False
                        
                        ScrollTextArea.insert(tk.END, f"No Active host(s) with IP/Network {sIpAdd}")
                        root.after(10000, lambda: ScrollTextArea.delete(1.0, tk.END)) #The above label will disappear by 10seconds

                else:
                        if stop_scan.is_set():
                            progressBar.stop()
                            return False
                        
                        ScrollTextArea.tag_configure("bold", font=("Courier", 10, "bold"))
                        ScrollTextArea.insert(tk.END, "="*60 + "\n", "bold")
                        ScrollTextArea.insert(tk.END, f"Scan Time: {result['scan_time']}\n", "bold")
                        ScrollTextArea.insert(tk.END, f"Network: {result['network']}\n", "bold")

                        # Process each host sequentially
                        for host in result["hosts"]:

                            if stop_scan.is_set():
                                progressBar.stop()
                                return False
                            
                            DisplayHostResults(host)
                        

                
                sContent = ScrollTextArea.get("1.0", "end-1c") # Retrieve all text currently displayed in scrolledText widget

                # Check if there is content and save it. 
                if sContent.strip(): # this ensures even spaces/newlines don't count
                        sContentInlines = sContent.splitlines()  # Split text into individual lines
                        f.SaveScanLog(sContentInlines) # Save file in .txt by calling function 
                
                else:
                     msg.showerror("Error", sContent)


                progressBar.stop() # Stop progress bar after scan done - w/out content
                


                return True
             
     
        else:
            if stop_scan.is_set():
                    progressBar.stop()    
                        
            else:
                 
                msg.showerror("Error", result)

            
            return False 

             
              
        

#---------------------------------------------------------------------------------------------------------------------------------------
def DisplayHostResults(host):
    # Display scan results for a single host in the scrollable text area and identify potential high-risk ports
    # Paramters pass from function 'Scan' - dictionary consists of the following: IP Address, Mac Address, OS and Ports 
    # Displays host information and a formatted table of ports.
    # Appends open ports to the host's entry in dctHostOpenPorts.   
    # Checks for high-risk ports using the PotentialRiskPorts function.
    # Highlights high-risk ports in red and bold.
    # Updates dctRiskPort with risky ports keyed by host IP.                                                        

        sIPadd = host['IP Address']
        
        # Only add new IPs; don't overwrite previous ones
        if sIPadd not in dctHostOpenPorts:
            dctHostOpenPorts[sIPadd] = {"Ports": []}


        # Display host info in ScrollTextArea
        ScrollTextArea.insert(tk.END, "-"*60 + "\n", "bold")
        ScrollTextArea.insert(tk.END, f"\nIP Address: {sIPadd}\n", "bold")
        ScrollTextArea.insert(tk.END, f"Mac Address: {host['Mac Address']}\n", "bold")
        ScrollTextArea.insert(tk.END, f"OS: {host['OS']}\n\n", "bold")

        # Display ports table
        ScrollTextArea.insert(tk.END, f"{'PORT':<8}{'STATE':<15}{'SERVICE':<18}{'PROTOCOL'}\n", "bold")
        for port in host["Ports"]:
            ScrollTextArea.insert(tk.END, f"{port['Port']:<8}{port['State']:<15}{port['Service']:<18}{port['Protocol']}\n", "bold")
            
            # Append open ports to dictionary
            if port['State'] == 'open':
                iPortNum = port['Port']
                dctHostOpenPorts[sIPadd]['Ports'].append(iPortNum)


        # Check for high-risk ports               
        dctPotentialRiskPorts = f.PotentialRiskPorts(dctHostOpenPorts[sIPadd])

        if dctPotentialRiskPorts:
            ScrollTextArea.tag_configure("RedFont", foreground="red", font=("arial", 9, "bold"))
            ScrollTextArea.insert(tk.END, f"\n\nOPEN PORTS DETECTED _ POTENTIAL SECURITY RISK\n\n", "RedFont")
            for port, info in dctPotentialRiskPorts.items():
                ScrollTextArea.insert(tk.END, f"Port: {port}\n", "RedFont")
                ScrollTextArea.insert(tk.END, f"Service: {info['service']}\n", "RedFont")
                ScrollTextArea.insert(tk.END, f"Risk: {info['risk']}\n", "RedFont")
                ScrollTextArea.insert(tk.END, f"Explanation: {info['explanation']}\n", "RedFont")
                ScrollTextArea.insert(tk.END, f"Advice: {info['advice']}\n", "RedFont")
                ScrollTextArea.insert(tk.END, f"Risk Level: {info['level']}\n\n", "RedFont")

                # store risky port by IP
                if sIPadd not in dctRiskPort:
                    dctRiskPort[sIPadd] = []

                dctRiskPort[sIPadd].append(port)

        


#---------------------------------------------------------------------------------------------------------------------------------------
def CancelScan():
        # Cancel an ongoing network scan.
        # Stops the scan thread, halts the progress bar, clears or updates the GUI, resets tkinter widget (button, entry field).
        #   Enabled Buttons: Scan, Schedule Scan, Field for target IP, Notification checkbox
        #   Disabled Buttons: Schedule Stop, Cancel for normal scan
        
        # Shows a temporary message indicating that the scan was cancelled.


        progressBar.stop()
        lblProgress.config(text="")
        ScrollTextArea.insert(tk.END," ========= Scan Cancelled =========")
        root.after(5000, lambda: ScrollTextArea.delete(1.0, tk.END)) #The label will dissapear
        BtnScan.config(state="normal")
        BtnSchedScan.config(state="normal")
        EntTargetIP.config(state="normal")
        DrpMenuOption.config(state="normal")
        BtnStopSched.config(state="disabled")
        BtncancelScan.config(state="disabled")
        EntTargetIP.delete(0, tk.END)
        stop_scan.set()




#---------------------------------------------------------------------------------------------------------------------------------------
def StopScheduleScan():
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
            ScrollTextArea.delete(1.0, tk.END)
            scheduler.remove_all_jobs()
            progressBar.stop()
            stop_scan.set()
            BtnScan.config(state="normal")
            BtnSchedScan.config(state="normal")
            EntTargetIP.config(state="normal")
            DrpMenuOption.config(state="normal")
            EntTargetIP.delete(0, tk.END)
            BtnStopSched.config(state="disabled")
            ScrollTextArea.get(1.0, tk.END)
            ScrollTextArea.insert(tk.END, "Schedule scan has been stop...")
            root.after(5000, lambda: ScrollTextArea.delete(1.0, tk.END)) #The label will dissapear


        else:
             pass



mainloop()

