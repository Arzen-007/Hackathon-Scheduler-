# Hackathon-Scheduler-
# 🛡️ Cybersecurity Hackathon Scheduler

A modern, stylish, and fully interactive Python GUI application designed to manage cybersecurity-themed tournaments. Built using `tkinter` and `Pillow`, this project helps organize team data, group division, automatic match scheduling, and winner announcement — all in one place!


---

## 📂 Project Overview

This tool simulates the full tournament lifecycle:

* Load teams from a `.txt` file
* Divide into **Group A** and **Group B**
* Automatically schedule matches round by round
* Display results and **announce the champion**
* View a full tournament summary at the end

---

## ✨ Features

✅ Clean dark-themed GUI (with SF Pro + Fira Code fonts)
✅ Team grouping based on rank
✅ Randomized match outcomes
✅ Interactive tournament rounds:

* Round 1
* Quarter Final
* Semi Final
* Final
  ✅ Winner display with members
  ✅ TreeView visualization of teams
  ✅ Summary panel with all match results

---

## 📁 File Structure

```
📁 cybersecurity-tournament/
├── tournament.py       # Main Python GUI logic
├── teams.txt           # Input team data
├── screenshots/        # GUI screenshots here
└── README.md
```

---

## 🧾 teams.txt Format

The app reads teams from `teams.txt`. Format each line like this:

```
Team Name;Member1,Member2;Rank
```

### ✅ Sample:

```
Team Alpha;Alice,Bob;1
Team Bravo;John,Doe;2
Cyber Ninjas;Zara,Ali;3
...
```


## 🚀 Getting Started

### 🔧 Prerequisites

* Python 3.10+ (tested with 3.13)
* `tkinter` (usually pre-installed)
* `Pillow` image library

### ⚙️ Setup Instructions

```bash
# Clone the repository (or download ZIP)
git clone https://github.com/yourusername/cybersecurity-tournament.git
cd cybersecurity-tournament

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install Pillow

# Run the application
python3 tournament.py
```

---

## 🔮 Future Enhancements

* ✅ Export results as PDF or CSV
* ✅ Add team images or logos
* ✅ Real-time scoring (manual entry)
* ✅ Drag-and-drop team assignment
* ✅ Save/load tournaments (via JSON)

---

## 🧠 Tech Stack

* **Language**: Python 🐍
* **GUI**: tkinter
* **Image Support**: Pillow
* **Fonts**: SF Pro Display, Fira Code (optional)

---

## 🏅 Credits

Developed by Syed Muhammad Qammar Abbas Zaidi 💻
As part of a cybersecurity learning project.

Special thanks to the open-source Python community!

---

## 📜 License

This project is licensed for **educational and academic use** only.
Please do not use it for real-money or commercial tournament management.

