UPI Recovery AI

A Prototype for Understanding and Managing UPI Payment Issues

UPI Recovery AI is a web-based prototype designed to help users understand common UPI transaction problems, receive recovery guidance, generate bank complaint drafts, and track their reported cases.

Features

- Transaction Analysis: Accepts transaction details and identifies common payment issues.
- Recovery Guidance: Provides suggested next steps based on the reported issue.
- Complaint Generator: Creates a draft complaint that users can review and submit to their bank.
- Case Tracking: Stores reported cases locally and allows users to view their status.
- Dashboard: Displays recorded cases.

Technology Stack

- Python
- Flask
- HTML
- CSS
- JavaScript
- SQLite

Project Structure

UPI-Recovery-AI/
├── app.py
├── database.py
├── ai_engine.py
├── complaint_generator.py
├── requirements.txt
├── database/
├── templates/
└── static/
    ├── css/
    ├── js/
    └── images/

How to Run Locally

1. Clone this repository:
   
   git clone https://github.com/gauravchaurasiya/UPI-Recovery-AI.git

2. Open the project folder:
   
   cd UPI-Recovery-AI

3. Install dependencies:
   
   pip install -r requirements.txt

4. Run the application:
   
   python app.py

5. Open your browser and visit:
   
   "http://127.0.0.1:5000"

Important Limitations

This is an educational prototype.

- Transaction analysis currently uses rule-based keyword matching, not a trained AI model.
- It does not connect directly to banks, NPCI, or UPI payment systems.
- It cannot reverse transactions, process refunds, or guarantee recovery.
- Complaint drafts must be reviewed and submitted by the user.
- Case records are stored locally in SQLite.
- Do not enter real banking credentials or sensitive financial information.

Future Improvements

- Integration with a genuine AI model.
- Improved fraud-pattern detection.
- Secure user authentication.
- Stronger data protection.
- Integration with official complaint and grievance channels, subject to their APIs and permissions.

Disclaimer

UPI Recovery AI is an independent prototype developed for educational and hackathon purposes. It is not affiliated with NPCI, UPI, or any bank.
