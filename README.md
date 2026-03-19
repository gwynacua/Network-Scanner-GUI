
Copyright © 2026, Gwyn Villegas                                                                                                  

This project is developed for learning and educational purposes only

This project is a Python-based automated network scanner that integrates with Nmap and with GUI.
The program scans a home network, including potential IoT devices, to identify connected 
devices and their open ports. It flags preconfigured high-risk ports and provides a brief 
discussion of the associated security risks, helping users understand potential vulnerabilities. 
The project is simple and user-friendly, making it suitable for non-technical homeowners, 
and aims to educate users about security risks within their home network.

------------------------------------------------------------------------------------------------
                          THIS TOOL SHOULD ONLY BE USED ON AUTHORIZED NETWORKS.
------------------------------------------------------------------------------------------------

REQUIREMENTS
The following libraries, components and application need to install:
- Install nmap from nmap.org

Install libraries using pip:
1. Python-nmap
2. Psutil - to get system and hardware information such as network activity
3. Apscheduler - for scheduler feature
3. Plyer - for desktop notification


FEATURES
1. User Authentication
2. Nmap Integration
3. Scan report generation
4. Preconfigure High Risk Port Detection
5. Desktop Notification
6. Scheduled Scanning


OUT-OF-SCOPE
- Does not support automatic blocking or closing ports – Display only preconfigured potential high-risk port.
- Does not support large enterprise network – Designed for SOHO network 
- Does not support multiple user creation – Only support single account
- Exploiting devices or advanced vulnerability detection – Focus only on open ports
- Device Identification – program cannot determine the exact type or brand of devices from there IP or Mac Address.


LIMITATIONS
- If the computer goes to sleep, the scan will stop and will continue only after the computer wakes up.
- If a user logs in and starts a scan, then switches networks, the scan will not proceed—even if the progress bar 
running and seems scanning. The user must log out and log back in for the scan to work properly again.


------------------------------------------------------------------------------------------------
  Feel free to fork this repository, make changes, submit a pull request. 
  If you find any issues, please open an issue. Thanks :)
------------------------------------------------------------------------------------------------





