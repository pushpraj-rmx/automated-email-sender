import sys
import random
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QMessageBox, QTextEdit, QLineEdit

class EmailSenderApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Email Sender App")
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()

        self.contacts_file = QLineEdit()
        self.gmail_file = QLineEdit()
        self.subject_file = QLineEdit()
        self.template_file = QLineEdit()

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.layout.addWidget(self.log_text)

        self.browse_contacts_btn = QPushButton("Select Contacts CSV")
        self.browse_gmail_btn = QPushButton("Select Gmail CSV")
        self.browse_subject_btn = QPushButton("Select Subject CSV")
        self.browse_template_btn = QPushButton("Select Email Template HTML")
        self.send_emails_btn = QPushButton("Send Emails")

        self.browse_contacts_btn.clicked.connect(self.browse_contacts)
        self.browse_gmail_btn.clicked.connect(self.browse_gmail)
        self.browse_subject_btn.clicked.connect(self.browse_subject)
        self.browse_template_btn.clicked.connect(self.browse_template)
        self.send_emails_btn.clicked.connect(self.send_emails)

        self.layout.addWidget(self.contacts_file)
        self.layout.addWidget(self.browse_contacts_btn)
        self.layout.addWidget(self.gmail_file)
        self.layout.addWidget(self.browse_gmail_btn)
        self.layout.addWidget(self.subject_file)
        self.layout.addWidget(self.browse_subject_btn)
        self.layout.addWidget(self.template_file)
        self.layout.addWidget(self.browse_template_btn)
        self.layout.addWidget(self.send_emails_btn)

        self.central_widget.setLayout(self.layout)

    def log(self, message):
        self.log_text.append(message)

    def browse_file(self, file_var):
        options = QFileDialog.Option.ReadOnly  # Use QFileDialog.Option instead of QFileDialog.Options
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*)", options=options)
        if file_path:
            file_var.setText(file_path)
            self.log(f"File selected successfully: {file_path}")

    def browse_contacts(self):
        self.browse_file(self.contacts_file)

    def browse_gmail(self):
        self.browse_file(self.gmail_file)

    def browse_subject(self):
        self.browse_file(self.subject_file)

    def browse_template(self):
        self.browse_file(self.template_file)

    def send_emails(self):
        if not all([self.contacts_file.text(), self.gmail_file.text(), self.subject_file.text(), self.template_file.text()]):
            QMessageBox.critical(self, "Error", "Please select all CSV files and the Email Template HTML.")
            return

        self.log("Sending emails...")

        try:
            # Read CSV files
            contacts_data = pd.read_csv(self.contacts_file.text())
            email_data = pd.read_csv(self.gmail_file.text())
            subject_data = pd.read_csv(self.subject_file.text())

            for _, contact in contacts_data.iterrows():
                email_account = email_data.sample(n=1).iloc[0]
                sender_email = email_account['email']
                sender_password = email_account['password']
                recipient_email = contact['email']
                subject = random.choice(subject_data['subject'])

                with open(self.template_file.text(), 'r') as f:
                    email_html = f.read()

                email_html = email_html.replace('$name', contact['name'])

                message = MIMEMultipart()
                message['From'] = sender_email
                message['To'] = recipient_email
                message['Subject'] = subject

                message.attach(MIMEText(email_html, 'html'))

                with smtplib.SMTP('smtp.gmail.com', 587) as server:
                    server.starttls()
                    server.login(sender_email, sender_password)
                    server.sendmail(sender_email, recipient_email, message.as_string())

                self.log(f"Email sent to {recipient_email} successfully")

            self.log("All emails sent successfully!")

        except Exception as e:
            self.log(f"Error: {e}")
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EmailSenderApp()
    window.show()
    sys.exit(app.exec())
