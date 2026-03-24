# =================================================================================================================================#
# Copyright © 2026, Gwyn Villegas                                                                                                  #
# System Management and Cybersecurity                                                                                              #                     #
# This program was created learning and educational purposes only.                                                                 #
# This program was developed using variety of resources, including python course from SMC program, programming tutorials, example  #
# code from websites such as github, GeeksforGeeks, Stack overlow as well as AI-assisted tools.                                    #                                                                                                                 #
# This code has been adapted, modified to fit the requirements of this application.                                                #
# =================================================================================================================================#


#-------------------------------------------------
# IMPORTS
#-------------------------------------------------
import os # Import os module to interact with it
import sys # To access command-line arguments
from pathlib import Path as p
import re as r # regex
import json as j 
import socket as s # Access to low-level networkking int
import ipaddress # create, manipulate and validate IPv4/6 address and network
import shutil #library module for high-level file operations.
import platform # Use to detect operating system info
from tkinter import messagebox as msg
import datetime 
from pathlib import Path as p
import hashlib as hash #Provide hash function and this function I used SHA256 for password
import subprocess #Commandline - run external program 



# ---------------------------------------------------------------------------------------------------------------------------------
# This condition check if the current machine is Linus/MacOs (not Windows) and this script (.py) whether running as root.
# This ensure that the script run as administrative (root) privileges which is require for certain action like running port scanning (-sS -T4 -F -O)
# If true run as root.

if os.name != "nt" and os.geteuid() != 0:
    os.execvp("sudo", ["sudo", "python3"] + sys.argv)
# ---------------------------------------------------------------------------------------------------------------------------------



############### Check whether the Python module for Nmap is installed.
# This attempt to import the nmap and psutil and also check if nmap is installed in machine

#     Check required dependencies for the app:
#         1. nmap installed on the system
#         2. python-nmap installed
#         3. psutil installed
#         4. unexpected error.
#     Displays an error and exits if any are missing.

try:

     import nmap, psutil

     if not shutil.which("nmap"):
          msg.showerror("Error", "Nmap is not installed.\nPlease install nmap from https://nmap.org")
          sys.exit()


          
except ModuleNotFoundError:

          msg.showerror(
               "Missing Dependency",
               "The program cannot continue.\n\n"
               "Please install the following:\n\n"
               "1. Install the Nmap program from:\n"
               "   https://nmap.org\n\n"
               
               "2. Install the Python library by running:\n"
               "   pip install python-nmap\n\n"
               "3. Install the psutil library by running:\n"
               "   pip install psutil\n\n"
               "   (You may need to run Command Prompt as Administrator and above instruction may be different with different OS)\n\n"
               "After installation, restart the program."
          )
     
          sys.exit()

except Exception as e: # Base class for most error such as ValueError, TypeError, FilenotFoundError and etc. 
                       # with 'e' it will display what specific error occur
     
          msg.showerror("Error", "An unexpected error occured while sending notification: {e}")
          sys.exit()
###############################################################################################





def checkPlyerModule():
# This attempt to import the plyer module for desktop notification.
# It handles erros
#    - ModuleNotFoundError - if 'plyer not installed.
#    - Base Error (Python) - handle unexpected error occur and display specific error

     try:

          import plyer

          return True

     except ModuleNotFoundError:

          msg.showerror(
          "Desktop Notification Unavailable",
          "Desktop notifications cannot be used because the 'plyer' module is not installed.\n\n"
          "If you want to use this feature, install it with:\n\n"
          "pip install plyer")

          return False

     except Exception as e: # Base class for most error such as ValueError, TypeError, FilenotFoundError and etc. 
                         # with 'e' it will display what specific error occur
          
          msg.showerror(
                    "Error",
                    f"An unexpected error occurred while loading notifications:\n{e}")
          
          return False
     
###############################################################################################



# GLOBAL VARIABLE - File Path Configuration -
dataPath = p('data/data.json') # User credential json path file
ScanLogPath = p('data/Scanlog.txt') # Save the scans
#################################################################################################


def OpenLog(currentOs):
# Open the scan log file using the default application based on the operating system.
# Check what OS currently running 
# Open File
#    Return True:
#         if windows used os.startfile
#         if linux used subprocessrun(["xdg-open")
#         if MacOs used  subprocess.run(["open")

#    Return False if:
#         if unsupported OS
#         if the file to open is not found
     try: 

          if currentOs == 'Windows':
               os.startfile(ScanLogPath)
               return True
          elif currentOs == "Linux":
               subprocess.run(["xdg-open", ScanLogPath])
               return True
          elif currentOs == "Darwin":  # macOS
               subprocess.run(["open", ScanLogPath])
               return True
          else:
               return "Unsupported OS"

     
     except FileNotFoundError:
          return False
     
     except Exception as e:
          return e


def GetOs():
     # Identify the operating system currently running the program
     # Returns - string that respresent the OS
     #      w - windows
     #      l - linux
     #      d - MacOs
     #      unknown - unknow OS
     
     sReturn = ""
     if platform.system() == "Windows":
        sReturn = "Windows"
     
     elif platform.system() == "Linux":
        sReturn = "Linux"
     
     elif platform.system() == "Darwin":
        sReturn = "MacOs"
     
     else:
          sReturn = "Unknown OS"

     return sReturn



def SaveScanLog(scan):
# Save the scan results to the scan log file.
# Parameter from dashboard - content from scrollareaview
# Returns: True is save successful, if not return error message 
#    - Ensures the parent 'data' folder exists (creates it if missing).
#    - Appends the scan results to `ScanLogPath`, separating entries with blank lines.

     try: 
            
          ScanLogPath.parent.mkdir(parents=True, exist_ok=True) # Ensure the 'data' folder exists (creates automatically if missing)
          with open(ScanLogPath, "a") as savedFile:
               savedFile.write("\n\n")
               for line in scan:
                    savedFile.write(f"{line}\n")

          return True
          
     except Exception as e:
            
          return f"Error saving scan result logs: {e}"




def find_local_ip():
    # Retrieve the IPv4 address of the current machine/device.
    # This function creates a temporary UDP socket connection to an external address (8.8.8.8, Google DNS) to determine which network interface is currently being used. No actual data is sent to the external server.
    # Retunns:
    #   - Ip address if dectected
    #   - Error if not detected

    # No actual packets are sent to 8.8.8.8; the connection is used only to determine the active network interface.
    # Credit:
    ####################### Code concept from Aleem20 (https://github.com/Aleem20) #############################
    
    try: 

        temp_socket = s.socket(s.AF_INET, s.SOCK_DGRAM)
        temp_socket.connect(("8.8.8.8", 80))
        local_ip = temp_socket.getsockname()[0]
        temp_socket.close()
              
        return local_ip
    
    except Exception as error:
         
        return f"Error retrieving local IP: {error}.\nPlease try again.\nClosing the application"


def getSubnetMask():
    # This function retrieve the subnet mask of the current machine active IPv4 address
    # This function iterates over all network interfacees and their addresses using 'psutil'
    # It compare each interfaces IPv4 Address with the IP address returned by 'find_local_ip()' function 
    # Once a match is found, it return the subnet mask
    # Return string subnet mask correspond with active interface network, if no match return none.

    for int, address in psutil.net_if_addrs().items(): #net_if_addrs return network address in network interface such as IP and netmask
        for ipadd in address: 
              
              ipv4 = ipadd[1] # index 1 to get the ipv4
                              # Sample list: snicaddr(family=<AddressFamily.AF_LINK: -1>, address='F8-ED-FC-35-AC-94', netmask=None, broadcast=None, ptp=None)

              if ipv4 == find_local_ip(): # comparing the address by calling find_local_ip() function - active interface
                     netmask = ipadd[2] # if match: get the netmask with index 2
                     return int, netmask # return: interface active and its netmask



def getCIDR(ipAddress, subnetMask):
    # Convert an IP address and subnet mask into a CIDR network.
    # Parameters: ipAddress (str) and subnetMask (str)

    # Return: the network in CIDR (eg. 10.0.0.0/24)

    network = ipaddress.IPv4Network(f"{ipAddress}/{subnetMask}", strict=False)
    return network



def ScanPorts(network):
# Perform a network scan using Nmap and return structured scan results.
# Parameter: User input : single IP address of network
# Returns:
#         True -> with scan result details
#         False  -> If an error occurs, returns False and an error message.

# Initializes Nmap with common installation paths for Windows, Linux, and macOS.
# Runs a scan using SYN scan (-sS), faster timing (-T4), fast mode (-F), and OS detection (-O) - preconfigured argument 
# Collect detail from scan result: IP, MAC Address, OS and open ports
# Error such missing Nmap component or unexpected error

          try:
               # Initialize Nmap scanner with common installation paths
               from nmap import PortScannerError  # Used to catch Nmap scan errors

               scanner = nmap.PortScanner(nmap_search_path=(
               r"C:\Program Files (x86)\Nmap\nmap.exe",  # Windows
               r"C:\Program Files\Nmap\nmap.exe",        # Windows
               "/usr/bin/nmap",                          # Linux
               "/usr/local/bin/nmap",                    # Linux/macOS
               "/opt/homebrew/bin/nmap"                  # macOS (Apple Silicon via Homebrew)
               ))

            
               
               scanner.scan( hosts=str(network),arguments='-sS -T4 -F -O') # Perform a scan
          
          except PortScannerError:

               return False, "Nmap scan failed. Nmap component are missing.\n\nYou may need to upgrade to the latest version from https://npcap.com."
          
          except Exception as err:

               return False, "Unexpected Error.\n{err}"



          # Get Current Scan time
          sScan_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M") #Get the time

          dctDevice = {
               "network": str(network),
               "scan_time": sScan_time,
               "hosts": []
               }

          try:
             
             for ip in scanner.all_hosts():
                    
                    mac = scanner[ip].get('addresses', {}).get('mac', 'N/A')
                    osmatch = scanner[ip].get('osmatch', [])
                    os_name = osmatch[0]['name'] if osmatch else "Unknown"

                    host_info = {
                         "IP Address": ip,
                         "Mac Address": mac,
                         "OS": os_name,
                         "Ports": []
                    }
                    

                    for protocol in scanner[ip].all_protocols():
                         ports = scanner[ip].get(protocol, {})

                         for port, portData in ports.items():
                              if not isinstance(portData, dict):
                                   continue
                              
                              host_info["Ports"].append({
                                   "Port": port,
                                   "State": portData.get('state', 'Unknown'),
                                   "Service": portData.get('name', 'Unknown'),
                                   "Protocol": protocol
                              })

                    dctDevice["hosts"].append(host_info)

          except ValueError:
               return False, "Host processing error. Please try again"
          

          return True, dctDevice # return true and with scan resutls

         
     

def PotentialRiskPorts(OpenPorts):
# This are preconfigure potential high-risk with details
# Parameter - pass from dashboard: list of open ports
# Returns: A dictionary mapping port numbers to their risk information for all detected risk ports.
# Check all open ports against a preconfigured dictionary of potential high-risk ports.
#         If an open port is considered risky, add it to a dictionary with its risk details.
#         if not in DCTPOTENTIALRISKPORT return none.

     dctPotentialHighRiskPorts = {

          # General Home Devices
          21: {
               "service": "FTP - File Transfer",
               "risk": "Transfers files between computers or storage.",
               "explanation": "Passwords and files are not encrypted, so someone could see them.",
               "advice": "Turn off FTP if not needed or use a secure alternative.",
               "level": "Medium"
          },

          22: {
               "service": "SSH - Remote Access",
               "risk": "Lets someone control your device remotely.",
               "explanation": "Hackers may try to guess your password and get in.",
               "advice": "Use strong passwords and only allow trusted devices.",
               "level": "Medium"
          },

          23: {
               "service": "Telnet - Remote Access",
               "risk": "Old way to log in to devices remotely.",
               "explanation": "Passwords are visible to attackers.",
               "advice": "Turn off Telnet and use SSH if needed.",
               "level": "High"
          },

          80: {
               "service": "HTTP - Device Web Pages",
               "risk": "Used by routers, cameras, or smart devices for control.",
               "explanation": "Data is not encrypted and could be seen by attackers.",
               "advice": "Use HTTPS if possible and change default passwords.",
               "level": "Medium"
          },

          443: {
               "service": "HTTPS - Secure Device Pages",
               "risk": "Encrypted access to routers or smart devices.",
               "explanation": "Weak passwords or outdated devices can still be attacked.",
               "advice": "Keep devices updated and use strong passwords.",
               "level": "Low"
          },

          3389: {
               "service": "Remote Desktop",
               "risk": "Lets someone control your computer remotely.",
               "explanation": "Hackers often scan for this port to try passwords.",
               "advice": "Turn off Remote Desktop if not needed or only allow trusted devices.",
               "level": "High"
          },

          445: {
               "service": "SMB - File Sharing",
               "risk": "Shares files on your home network.",
               "explanation": "Exposed to the internet, attackers could access files or spread malware.",
               "advice": "Only share files with trusted devices; don't open it online.",
               "level": "High"
          },

          5900: {
               "service": "VNC - Remote Screen Access",
               "risk": "Lets someone view or control your computer screen.",
               "explanation": "Weak passwords allow attackers to take control.",
               "advice": "Turn off VNC if not needed or use a strong password.",
               "level": "High"
          },

          1900: {
               "service": "UPnP - Auto Port Opening",
               "risk": "Lets devices automatically open ports on your router.",
               "explanation": "Malware could exploit this to enter your network.",
               "advice": "Turn off UPnP if you don't need it.",
               "level": "Medium"
          },

          # some of IoT Devices ports
          554: {
               "service": "RTSP - Camera Video",
               "risk": "Streams video from security cameras.",
               "explanation": "Someone could watch your cameras if the port is open.",
               "advice": "Set strong passwords and keep cameras inside your network.",
               "level": "High"
          },

          5000: {
               "service": "NAS Admin Panel",
               "risk": "Controls storage devices like Synology/QNAP.",
               "explanation": "Attackers could try to log in and see your files.",
               "advice": "Use strong passwords and only allow access from your home network.",
               "level": "High"
          },

          5001: {
               "service": "Secure NAS Admin Panel",
               "risk": "Encrypted version of NAS management.",
               "explanation": "If exposed, attackers may still try to log in.",
               "advice": "Enable two-factor authentication if available.",
               "level": "High"
          },

          8080: {
               "service": "Alternate HTTP",
               "risk": "Used by smart devices or cameras for web control.",
               "explanation": "Attackers could access device settings if exposed.",
               "advice": "Change default passwords and disable remote access if not needed.",
               "level": "Medium"
          },

          8443: {
               "service": "Alternate HTTPS",
               "risk": "Secure admin pages for IoT or routers.",
               "explanation": "Attackers could attempt login if the port is open.",
               "advice": "Restrict access to trusted devices or networks.",
               "level": "Medium"
          },

          8888: {
               "service": "IoT Device Control Panel",
               "risk": "Used by smart devices for control or monitoring.",
               "explanation": "Attackers may try to access the device if the port is open.",
               "advice": "Disable remote access and use strong device passwords.",
               "level": "Medium"
          },

          32400: {
               "service": "Media Server (Plex)",
               "risk": "Streams movies and music from your home server.",
               "explanation": "Exposed ports could let outsiders access your media library.",
               "advice": "Keep it private and protect with a password.",
               "level": "Medium"
          },

          37215: {
               "service": "Smart Home Hub",
               "risk": "Controls smart devices like lights and locks.",
               "explanation": "Attackers could control your devices if exposed.",
               "advice": "Keep firmware updated and limit access to your home network.",
               "level": "Low"
          }

     }
    
     dctHostOpenPorts = {} # store in a dictionary if pass ports from dashboard in potential risk port

     for ip, ports in OpenPorts.items(): # Host ip 
          for ip in ports: # Port list within the host ip
               if ip in dctPotentialHighRiskPorts: # check if port in potential high-rosk dictionary
                    dctHostOpenPorts[ip] = dctPotentialHighRiskPorts[ip] 

     return dctHostOpenPorts



