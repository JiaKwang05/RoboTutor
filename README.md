# 🤖 RoboTutor: Educational Robotics Diagnostics

**An Expert System for Beginner Robotics Troubleshooting**

RoboTutor is a pedagogical diagnostic tool designed to help beginner students troubleshoot complex hardware and software bugs in introductory robotics (e.g., Arduino C++, Scratch). Built to support **UN SDG 4 (Quality Education)**, RoboTutor acts as an accessible, 24/7 technical assistant that bridges the gap between software logic and physical hardware realities.

---

## ✨ Key Features & Architecture

RoboTutor is built on a decoupled 3-tier architecture, separating domain data, logic, and presentation.

### 1. Goal-Driven Inference Engine (Python)
Powered by a **Backward Chaining** algorithm, the engine does not bombard users with irrelevant questions. Instead, it tests specific hypotheses (Goals) and dynamically works backward to verify the required physical and logical states, pruning the decision tree in real time.

### 2. Uncertainty Handling (Fuzzy Logic)
Beginner students are often unsure of their observations. RoboTutor utilizes a **Fuzzy Logic** uncertainty module. Users input their confidence level, and the system dynamically calculates the final Certainty Factor (CF) of the diagnosis based on the "weakest link" (minimum confidence) in their reported facts.

### 3. Hybrid Explanation Facility (Streamlit)
To fulfill its educational mandate, RoboTutor explains its reasoning. When a diagnosis is reached, the UI provides a two-part explanation:
* **Dynamic Trace:** Loops through the engine's memory to show exactly which facts and confidence scores were verified.
* **Pedagogical Context:** Pulls human-expert theory from the database to teach the *why* behind the bug (e.g., why a missing `delay()` function causes a processor deadlock).

### 4. Decoupled Knowledge Base (JSON)
All domain expertise is stored externally as formal **Production Rules (IF-THEN)** in a JSON file (`kb.json`). This allows the diagnostic logic to be safely edited or expanded without altering the core Python source code.

---

## 🚀 How to Install and Run Locally

To run RoboTutor on your own machine, you will need Python installed. 

### Step 1: Clone the Repository
Download this repository to your local machine and navigate into the project folder using your terminal or command prompt:
```bash
git clone [https://github.com/JiaKwang05/RoboTutor](https://github.com/JiaKwang05/RoboTutor)
```

Step 2: Install Dependencies
RoboTutor relies on the Streamlit framework for its interactive web interface. Install it using pip:

```bash
pip install streamlit
```
(Tip: If you have a requirements.txt file, you can run pip install -r requirements.txt)

Step 3: Launch the Expert System
Start the local web server by running the following command in your terminal:
```bash
streamlit run robotutor.py
```
Windows Troubleshooting: If your terminal says streamlit is not recognized, your Python Scripts folder might not be in your System PATH. You can bypass this by running the module directly through Python:

```bash
python -m streamlit run robotutor.py
```

Once running, a new tab will automatically open in your default web browser containing the RoboTutor application!

## 📁 Repository Structure
robotutor.py — The core Inference Engine and Streamlit User Interface.

kb.json — The Knowledge Base containing the physical-logical bug production rules.

README.md — Project documentation.

requirements.txt — Python dependencies (Streamlit).

## 🔮 Future Enhancements
As outlined in our project proposal, future iterations of RoboTutor aim to include:

Support for advanced components (Ultrasonic sensors, Bluetooth modules, IoT).

Integration of an LLM-powered chatbot for natural language querying.

Automatic code syntax analysis prior to physical hardware evaluation.

Developed for WID2001 Knowledge Representation & Reasoning.