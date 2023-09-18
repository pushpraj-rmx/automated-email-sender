import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
import tkinter as tk
from tkinter import filedialog, messagebox

class EmailSenderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Email Sender App")

        # Create labels
        self.contacts_label = tk.Label(root, text="Select Contacts CSV:")
        self.gmail_label = tk.Label(root, text="Select Gmail CSV:")
        self.subject_label = tk.Label(root, text="Select Subject CSV:")
        self.template_label = tk.Label(root, text="Select Email Template HTML:")

        # Create buttons to select CSV files
        self.contacts_button = tk.Button(root, text="Browse", command=self.browse_contacts)
        self.gmail_button = tk.Button(root, text="Browse", command=self.browse_gmail)
        self.subject_button = tk.Button(root, text="Browse", command=self.browse_subject)
        self.template_button = tk.Button(root, text="Browse", command=self.browse_template)

        # Create Send Email button
        self.send_button = tk.Button(root, text="Send Emails", command=self.send_emails)

        # Create status label
        self.status_label = tk.Label(root, text="Status: Idle")

        # Layout using grid
        self.contacts_label.grid(row=0, column=0, sticky="e")
        self.contacts_button.grid(row=0, column=1)
        self.gmail_label.grid(row=1, column=0, sticky="e")
        self.gmail_button.grid(row=1, column=1)
        self.subject_label.grid(row=2, column=0, sticky="e")
        self.subject_button.grid(row=2, column=1)
        self.template_label.grid(row=3, column=0, sticky="e")
        self.template_button.grid(row=3, column=1)
        self.send_button.grid(row=4, column=0, columnspan=2)
        self.status_label.grid(row=5, column=0, columnspan=2)

        # Initialize variables for file paths
        self.contacts_file = ""
        self.gmail_file = ""
        self.subject_file = ""
        self.template_file = ""

    def browse_contacts(self):
        self.contacts_file = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if self.contacts_file:
            messagebox.showinfo("Info", "Contacts CSV selected successfully!")

    def browse_gmail(self):
        self.gmail_file = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if self.gmail_file:
            messagebox.showinfo("Info", "Gmail CSV selected successfully!")

    def browse_subject(self):
        self.subject_file = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if self.subject_file:
            messagebox.showinfo("Info", "Subject CSV selected successfully!")

    def browse_template(self):
        self.template_file = filedialog.askopenfilename(filetypes=[("HTML Files", "*.html")])
        if self.template_file:
            messagebox.showinfo("Info", "Email Template HTML selected successfully!")

    def send_emails(self):
        if not self.contacts_file or not self.gmail_file or not self.subject_file or not self.template_file:
            messagebox.showerror("Error", "Please select all CSV files and the Email Template HTML.")
            return

        try:
            # Load data from CSV files
            contacts_data = pd.read_csv(self.contacts_file)
            gmail_data = pd.read_csv(self.gmail_file)
            subject_data = pd.read_csv(self.subject_file)

            # Load email template
            with open(self.template_file, 'r') as template_file:
                email_template = template_file.read()

            # Iterate through contacts and send emails
            for _, contact in contacts_data.iterrows():
                # Choose a random email account
                email_account = random.choice(gmail_data.to_dict('records'))

                # Create an email message
                message = MIMEMultipart()
                message['From'] = email_account['email']
                message['To'] = contact['email']
                message['Subject'] = random.choice(subject_data['subject'])

                # Customize the email template
                email_body = email_template.replace('$name', contact['name'])

                # Attach the email body
                message.attach(MIMEText(email_body, 'html'))

                # Connect to the email server and send the email
                with smtplib.SMTP('smtp.gmail.com', 587) as server:
                    server.starttls()
                    server.login(email_account['email'], email_account['password'])
                    server.sendmail(email_account['email'], contact['email'], message.as_string())

                print(f"Email sent to {contact['email']} successfully")

            self.status_label.config(text="Status: Emails Sent Successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = EmailSenderApp(root)
    root.mainloop()
