import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random

class EmailSenderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Email Sender App")

        # Create a frame for the left side
        self.left_frame = tk.Frame(root)
        self.left_frame.pack(side="left", padx=20, pady=20)

        # Create a frame for the right side (log display)
        self.right_frame = tk.Frame(root)
        self.right_frame.pack(side="right", padx=20, pady=20)

        # Create labels
        tk.Label(self.left_frame, text="Select Contacts CSV:").grid(row=0, column=0, sticky="w")
        tk.Label(self.left_frame, text="Select Gmail CSV:").grid(row=1, column=0, sticky="w")
        tk.Label(self.left_frame, text="Select Subject CSV:").grid(row=2, column=0, sticky="w")
        tk.Label(self.left_frame, text="Select Email Template HTML:").grid(row=3, column=0, sticky="w")

        # Create buttons to select CSV files
        self.create_button("Browse", self.browse_contacts, 0, 2, "e", padx=(10, 0), pady=(10, 0))
        self.create_button("Browse", self.browse_gmail, 1, 2, "e", padx=(10, 0), pady=(10, 0))
        self.create_button("Browse", self.browse_subject, 2, 2, "e", padx=(10, 0), pady=(10, 0))
        self.create_button("Browse", self.browse_template, 3, 2, "e", padx=(10, 0), pady=(10, 0))

        # Create Send Email button
        self.create_button("Send Emails", self.send_emails, 4, 0, "we", padx=(10, 0), pady=(20, 0))

        # Create a scrolled text widget for log display
        self.log_text = scrolledtext.ScrolledText(self.right_frame, state="disabled", width=40, height=20)
        self.log_text.pack(fill="both", expand=True)

        # Initialize variables for file paths
        self.contacts_file = ""
        self.gmail_file = ""
        self.subject_file = ""
        self.template_file = ""

    def create_button(self, text, command, row, column, sticky, padx=None, pady=None):
        button = tk.Button(self.left_frame, text=text, command=command)
        button.grid(row=row, column=column, sticky=sticky, padx=padx, pady=pady)

    def log(self, message):
        self.log_text.configure(state="normal")
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)  # Scroll to the end of the log
        self.log_text.configure(state="disabled")

    def browse_contacts(self):
        self.contacts_file = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if self.contacts_file:
            self.log("Contacts CSV selected successfully!")

    def browse_gmail(self):
        self.gmail_file = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if self.gmail_file:
            self.log("Gmail CSV selected successfully!")

    def browse_subject(self):
        self.subject_file = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if self.subject_file:
            self.log("Subject CSV selected successfully!")

    def browse_template(self):
        self.template_file = filedialog.askopenfilename(filetypes=[("HTML Files", "*.html")])
        if self.template_file:
            self.log("Email Template HTML selected successfully!")

    def send_emails(self):
        if not self.contacts_file or not self.gmail_file or not self.subject_file or not self.template_file:
            messagebox.showerror("Error", "Please select all CSV files and the Email Template HTML.")
            return

        self.log("Sending emails...")

        # Your email sending logic here
        try:
            contactsData = pd.read_csv(self.contacts_file)
            emailData = pd.read_csv(self.gmail_file)
            subjectData = pd.read_csv(self.subject_file)

            for _, contact in contactsData.iterrows():
                email_account = emailData.sample(n=1).iloc[0]
                sender_email = email_account['email']
                sender_password = email_account['password']
                recipient_email = contact['email']
                subject = random.choice(subjectData['subject'])

                with open(self.template_file, 'r') as f:
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
            messagebox.showerror("Error", f"An error occurred: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = EmailSenderApp(root)
    root.mainloop()
