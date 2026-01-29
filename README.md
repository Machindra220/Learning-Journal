
# 📘 Learning Journal App

A personal productivity and journaling app built with **Streamlit**.  
It helps you track **daily notes**, **resources**, and visualize progress with a **calendar view** and structured **schedules**.

---

## ✨ Features
- ➕ Add Notes: Save notes by date and section.
- 📒 Show Notes: View notes grouped by date, with edit/delete functionality.
- 🔗 Add & Show Resources: Manage useful links/resources with descriptions and dates.
- 📆 Calendar: See notes count and status (✅) across days. To check streak.
- 📋 Schedule: Daily, Weekly, and Monthly schedules displayed in tables.

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/Machindra220/Learning-Journal.git
cd Learning-Journal
```

### 2. Create a virtual environment (recommended)
```bash
python -m venv .venv
source .venv/bin/activate   # On Linux/Mac
.venv\Scripts\activate      # On Windows
```

### 3. Install dependencies
After cloning, contributors should install all required packages using:

```bash
pip install -r requirements.txt
```

This ensures everyone has the same versions of Streamlit, Pandas, and other libraries.

### 4. Run the app
```bash
streamlit run app.py
```

Then open the app in your browser at:
```
http://localhost:8501
```

---

## 📂 Project Structure
```
Learning-Journal/
│
├── app.py              # Main Streamlit app
├── data/
│   ├── notes.json      # Stores notes
│   └── resources.json  # Stores resources
├── requirements.txt    # Dependencies
└── README.md           # Project documentation
```
