<p align="center">
  <img src="https://raw.githubusercontent.com/Darkrider0007/NetWatch/main/assets/logo.png" alt="NetWatch Logo" width="180">
</p>

<h1 align="center">🌐 NetWatch</h1>

<p align="center">
A modern Windows desktop application for monitoring live Internet connections made by applications.
</p>

<p align="center">

![Python](https://img.shields.io/badge/Python-3.13+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PySide6](https://img.shields.io/badge/PySide6-GUI-41CD52?style=for-the-badge&logo=qt)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite)
![Windows](https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge&logo=windows)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![GitHub release](https://img.shields.io/github/v/release/Darkrider0007/NetWatch?style=for-the-badge)
![GitHub Repo stars](https://img.shields.io/github/stars/Darkrider0007/NetWatch?style=for-the-badge)

</p>

---

# 📖 Overview

**NetWatch** is a modern desktop application that monitors **live Internet network connections** made by applications running on Windows.

Unlike traditional packet sniffers, NetWatch focuses on **which application is communicating over the Internet**, displaying rich process and connection information in a clean, real-time graphical interface.

Features include:

- 🌐 Live Internet Connection Monitoring
- 🖥 Process & Publisher Information
- 🌍 DNS Resolution
- 🌎 GeoIP Country Lookup
- 📊 Statistics Dashboard
- 🔍 Advanced Search & Filtering
- 🗃 SQLite Connection History
- 📤 CSV Export
- 🔔 Desktop Notifications
- 🖱 Process Context Menu
- 🌙 Modern Dark Theme

---

# 📸 Screenshots

<p align="left">
<img src="https://raw.githubusercontent.com/Darkrider0007/NetWatch/main/assets/SS1.png" width="600">
</p>

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

| IP | Country |
|----|----------|
|8.8.8.8|United States|
|1.1.1.1|Australia|

Powered by the **MaxMind GeoLite2 Country Database**.

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

- Incident Response
- Security Auditing
- Reports

---

## 🔔 Desktop Notifications

Detects new outbound Internet connections and displays desktop notifications.

---

## 🖱 Context Menu

Right-click a process to:

- Kill Process
- Open File Location
- View File Properties

---

## 🎨 Dark Theme

Modern dark interface built using Qt Style Sheets.

---

# 🏗 Architecture

```text
                +----------------------+
                |      MainWindow      |
                +----------+-----------+
                           |
          +----------------+----------------+
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

```text
NetWatch
│
├── assets/
├── database/
├── gui/
├── models/
├── monitor/
├── resources/
├── services/
├── themes/
├── utils/
├── logs/
│
├── config.py
├── main.py
├── requirements.txt
├── main.spec
└── README.md
```

---

# ⚙ Technologies Used

| Technology | Purpose |
|------------|----------|
| Python | Programming Language |
| PySide6 | GUI Framework |
| SQLite | Connection History |
| psutil | Network & Process Monitoring |
| socket | DNS Resolution |
| threading | Background Workers |
| GeoLite2 | Country Lookup |
| csv | CSV Export |
| logging | Application Logging |
| PyInstaller | Executable Packaging |

---

# 📦 Installation

```powershell
git clone https://github.com/Darkrider0007/NetWatch.git

cd NetWatch

python -m venv .venv

.venv\Scripts\activate

pip install -r requirements.txt
```

---

# 🌍 GeoLite2 Database

NetWatch uses the **MaxMind GeoLite2 Country Database**.

Due to MaxMind's licensing terms, the database file is **not included** in this repository.

Download the latest database from:

<https://dev.maxmind.com/geoip/geolite2-free-geolocation-data/>

Place

```text
GeoLite2-Country.mmdb
```

inside

```text
resources/
└── geoip/
    └── GeoLite2-Country.mmdb
```

If the file is missing, NetWatch will continue to work, but country information will not be displayed.

---

# ▶ Running

```powershell
python main.py
```

---

# 🛡 Microsoft Defender SmartScreen

Since NetWatch is an open-source project and is currently **not digitally signed**, Windows may display a Microsoft Defender SmartScreen warning when launching the application.

This is expected for new applications that have not yet built Microsoft SmartScreen reputation.

To continue:

1. Click **More info**
2. Click **Run anyway**

If you prefer, you can build the project yourself directly from source.

---

# 🏗 Building Executable

```powershell
pip install pyinstaller

pyinstaller main.spec
```

The executable will be generated in:

```text
dist/NetWatch/
```

---

# 🚀 Continuous Integration

GitHub Actions automatically builds NetWatch for every version tag.

```powershell
git tag v1.0.0
git push origin v1.0.0
```

The workflow automatically:

- Builds the project
- Downloads the GeoLite2 database
- Packages the application
- Publishes a GitHub Release

---

# 🔒 Security & Privacy

NetWatch performs all analysis locally on your computer.

The application:

- Does not upload network information
- Does not collect personal data
- Does not inspect packet contents
- Does not transmit telemetry

Only DNS and GeoIP lookups are performed when enabled.

---
---

# ✅ Testing & Quality Assurance

NetWatch uses **GitHub Actions** to automatically validate every code change.

### Continuous Integration

Every Push and Pull Request that modifies Python source code automatically:

- Installs all project dependencies
- Executes the complete test suite using `pytest`
- Generates a code coverage report
- Verifies that the project builds successfully

To reduce unnecessary workflow executions, changes to documentation and frontend assets such as:

- Markdown (`*.md`)
- HTML (`*.html`)
- CSS (`*.css`)
- JavaScript (`*.js`)

do **not** trigger the CI workflow.

### Branch Protection

The `main` branch is protected.

A Pull Request **cannot be merged** unless:

- ✅ All automated tests pass
- ✅ Every required GitHub Action completes successfully

This ensures that only verified, working code is merged into the main branch.

---
# 📚 Open Source Resources

- Python — <https://www.python.org/>
- PySide6 — <https://doc.qt.io/qtforpython/>
- Qt — <https://www.qt.io/>
- psutil — <https://github.com/giampaolo/psutil>
- SQLite — <https://sqlite.org/>
- MaxMind GeoLite2 — <https://dev.maxmind.com/geoip/geolite2-free-geolocation-data/>
- PyInstaller — <https://pyinstaller.org/>
- VirusTotal — <https://www.virustotal.com/>
- AbuseIPDB — <https://www.abuseipdb.com/>

---

# 🚀 Future Roadmap

- Firewall Rule Management
- Packet Capture
- WHOIS Integration
- VirusTotal API Integration
- Connection Graphs
- Bandwidth Monitoring
- Real-Time Alerts
- Startup Applications Monitor
- Digital Signature Verification
- Theme Switching
- Automatic Updates

---

# 🛡 Disclaimer

NetWatch is intended for:

- Network Monitoring
- Security Auditing
- Educational Purposes
- Software Diagnostics

It **does not capture packet contents**, decrypt encrypted traffic, or intercept communications. It only displays network connection metadata exposed by the Windows operating system.

---

# 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Open a Pull Request

---

# 📄 License

NetWatch is free and open-source software licensed under the **GNU General Public License v3.0 (GPL-3.0)**.

This means you are free to:
- ✅ Use the software for any purpose.
- ✅ Study how it works.
- ✅ Modify and improve it.
- ✅ Share the original or modified versions.

If you distribute this software or a modified version, you must also provide the source code under the same **GPL-3.0** license.

For complete terms and conditions, see the [LICENSE](LICENSE) file.

---

# 👨‍💻 Author

**Rohan Gope**

- GitHub: <https://github.com/Darkrider0007>
- LinkedIn: <https://www.linkedin.com/in/rohan-gope-a96072199/>

---

<p align="center">

### ⭐ If you found NetWatch useful, consider giving the repository a Star

</p>
