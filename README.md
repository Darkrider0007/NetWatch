# 🌐 NetWatch

<p align="center">

![Python](https://img.shields.io/badge/Python-3.13+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PySide6](https://img.shields.io/badge/PySide6-GUI-41CD52?style=for-the-badge&logo=qt)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite)
![Windows](https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge&logo=windows)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

</p>

---

## 📖 Overview

**NetWatch** is a modern desktop application that monitors **live Internet network connections** made by applications running on Windows.

Unlike a traditional packet sniffer, NetWatch focuses on **which application is communicating over the Internet**, displaying detailed information such as:

- Process Name
- Publisher
- Executable Path
- Remote Host
- Country
- IP Address
- Port
- Protocol
- Connection Status
- Timestamp

The application continuously scans active network connections, filters out unnecessary Windows internal traffic, enriches the information with DNS and GeoIP lookups, and displays everything inside a clean desktop GUI.

---

# ✨ Features

## 🌍 Live Network Monitoring

- Detects active Internet connections
- Refreshes automatically
- Displays only useful application traffic
- Ignores localhost traffic
- Ignores Windows internal/system processes

---

## 🖥 Process Information

Displays

- Process Name
- PID
- Executable Path
- Publisher
- Application Icon

---

## 🌐 DNS Resolution

Automatically resolves

```
142.250.xxx.xxx
```

into

```
google.com
```

using asynchronous background workers.

---

## 🌎 GeoIP Lookup

Shows the country of every remote IP.

Example

| IP | Country |
|----|----------|
|8.8.8.8|United States|
|1.1.1.1|Australia|

Powered by:

- MaxMind GeoLite2 Country Database

---

## 🔍 Search & Filtering

Supports filtering by

- Process Name
- Publisher
- Protocol
- Country
- Hostname

---

## 📊 Statistics

Displays

- Active Connections
- Top Processes
- Top Countries
- Publisher Statistics

---

## 🗃 Connection History

Stores historical connections in SQLite.

Supports

- Viewing history
- Searching history
- Clearing history

---

## 📤 CSV Export

Export all visible connections into CSV format.

Useful for

- Incident response
- Security auditing
- Reports

---

## 🔔 Desktop Notifications

Detects new connections and displays desktop notifications.

---

## 🖱 Context Menu

Right click a process to

- Kill Process
- Open File Location
- View Properties


---

## 🎨 Dark Theme

Modern dark interface using Qt Style Sheets.

---

# 🏗 Architecture

```
                +----------------------+
                |      MainWindow      |
                +----------+-----------+
                           |
          +----------------+----------------+
          |                                 |
          |                                 |
     Process Table                  Details Panel
          |                                 |
          +----------------+----------------+
                           |
                   Connection Monitor
                           |
                    Network Scanner
                           |
        +--------+---------+---------+---------+
        |        |         |         |         |
   psutil   DNS Service  GeoIP   Publisher  Filters
                           |
                      SQLite History
```

---

# 📂 Project Structure

```
NetWatch
│
├── assets/
│
├── database/
│   ├── database.py
│   └── history.db
│
├── gui/
│
├── models/
│
├── monitor/
│
├── services/
│
├── themes/
│
├── utils/
│
├── logs/
│
├── config.py
├── main.py
├── requirements.txt
└── README.md
```

---

# ⚙ Technologies Used

| Technology | Purpose |
|------------|----------|
|Python|Programming Language|
|PySide6|GUI Framework|
|SQLite|History Database|
|psutil|Network & Process Monitoring|
|socket|DNS Resolution|
|threading|Background Tasks|
|GeoLite2|Country Lookup|
|csv|Export|
|logging|Application Logging|

---

# 📦 Installation

## Clone Repository

## Create Virtual Environment

Windows

```powershell
python -m venv .venv
```

Activate

```powershell
.venv\Scripts\activate
```

---

## Install Requirements

```powershell
pip install -r requirements.txt
```

---

# 🌍 GeoLite2 Database

NetWatch requires the **GeoLite2 Country Database** from MaxMind.

Due to MaxMind's licensing terms, the database file is **not included** in this repository.

## Download

<https://dev.maxmind.com/geoip/geolite2-free-geolocation-data/>

After downloading:

```
GeoLite2-Country.mmdb
```

Place it inside

```
NetWatch/

└── assets/
      GeoLite2-Country.mmdb
```

or the location configured in `config.py`.

Without this file, country detection will be unavailable.

---

# ▶ Running

```powershell
python main.py
```

---

# 🏗 Building Executable

Install

```powershell
pip install pyinstaller
```

Generate spec

```powershell
pyi-makespec --windowed main.py
```

Build

```powershell
pyinstaller main.spec
```

Executable will be inside

```
dist/
```

---

# 📋 Database

SQLite stores

- Connection History
- Process Information
- Remote Host
- Ports
- Country
- Status
- Timestamp

Database file

```
history.db
```

---

# 📁 Logging

Application logs are stored in

```
logs/
```

Includes

- Startup
- Errors
- Network Scanner
- Database
- Services

---

# 🔧 Configuration

Configuration can be modified in

```
config.py
```

Examples

- Refresh Interval
- Window Size
- Theme
- Database Path
- DNS Settings

---

# 📚 Open Source Resources Used

## Python

<https://www.python.org/>

---

## PySide6

<https://doc.qt.io/qtforpython/>

---

## psutil

<https://github.com/giampaolo/psutil>

---

## SQLite

<https://sqlite.org/>

---

## MaxMind GeoLite2

<https://dev.maxmind.com/geoip/geolite2-free-geolocation-data/>

---

## Qt

<https://www.qt.io/>

---

## PyInstaller

<https://pyinstaller.org/>

---

## VirusTotal

<https://www.virustotal.com/>

---

## AbuseIPDB

<https://www.abuseipdb.com/>

---

# 🚀 Future Improvements

- Firewall Rule Management
- Packet Capture
- Whois Integration
- Bandwidth Monitoring
- Connection Graphs
- Process Tree
- VirusTotal API Integration
- Startup Applications Monitor
- Digital Signature Verification
- Windows Service Detection
- Real-time Alerts
- Theme Switching
- Auto Update

---

# 🛡 Disclaimer

NetWatch is intended for:

- Network Monitoring
- Security Auditing
- Educational Purposes
- Software Diagnostics

The application does **not** capture packet contents or decrypt encrypted traffic. It only displays metadata about active network connections available through the operating system.

---

# 🤝 Contributing

Contributions are welcome.

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Open a Pull Request

---

# 📄 License

This project is licensed under the **MIT License**.

---

# 👨‍💻 Author

**Rohan Gope**

- GitHub: <https://github.com/Darkrider0007>
- LinkedIn: <https://www.linkedin.com/in/rohan-gope-a96072199/>

---

## ⭐ If you found this project useful, consider giving it a Star
