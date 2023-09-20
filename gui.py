import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
import datetime
import os

class EmailSenderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Email Sender App")

        # Initialize StringVar variables for file paths
        self.contacts_file_var = tk.StringVar()
        self.gmail_file_var = tk.StringVar()
        self.subject_file_var = tk.StringVar()
        self.template_file_var = tk.StringVar()

        # Create frames
        self.create_left_frame()
        self.create_right_frame()

        # Create a log directory if it doesn't exist
        self.log_directory = "email_logs"
        os.makedirs(self.log_directory, exist_ok=True)

        # Create a log file with a timestamp
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
        self.log_file = os.path.join(self.log_directory, f"email_log_{timestamp}.txt")

    def create_left_frame(self):
        self.left_frame = tk.Frame(self.root)
        self.left_frame.pack(side="left", padx=20, pady=20)

        # Create labels and buttons
        self.create_label("Select Contacts CSV:", 0, 0)
        self.create_label("Select Gmail CSV:", 1, 0)
        self.create_label("Select Subject CSV:", 2, 0)
        self.create_label("Select Email Template HTML:", 3, 0)

        self.create_button("Browse", self.browse_contacts, 0, 2)
        self.create_button("Browse", self.browse_gmail, 1, 2)
        self.create_button("Browse", self.browse_subject, 2, 2)
        self.create_button("Browse", self.browse_template, 3, 2)

        # Create Send Email button
        self.create_button("Send Emails", self.send_emails, 4, 0, padx=10)

    def create_right_frame(self):
        self.right_frame = tk.Frame(self.root)
        self.right_frame.pack(side="right", padx=20, pady=20)

        # Create a scrolled text widget for log display
        self.log_text = scrolledtext.ScrolledText(self.right_frame, state="disabled", width=40, height=20)
        self.log_text.pack(fill="both", expand=True)

    def create_label(self, text, row, column):
        tk.Label(self.left_frame, text=text).grid(row=row, column=column, sticky="w")

    def create_button(self, text, command, row, column, padx=None, pady=None):
        button = tk.Button(self.left_frame, text=text, command=command, padx=padx, pady=pady)
        button.grid(row=row, column=column)

    def log(self, message):
        self.log_text.configure(state="normal")
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)  # Scroll to the end of the log
        self.log_text.configure(state="disabled")

    def browse_file(self, file_type, file_var):
        file_path = filedialog.askopenfilename(filetypes=[(file_type, f"*.{file_type.lower()}")])
        if file_path:
            file_var.set(file_path)
            self.log(f"{file_type} selected successfully!")

    def browse_contacts(self):
        self.browse_file("CSV", self.contacts_file_var)

    def browse_gmail(self):
        self.browse_file("CSV", self.gmail_file_var)

    def browse_subject(self):
        self.browse_file("CSV", self.subject_file_var)

    def browse_template(self):
        self.browse_file("HTML", self.template_file_var)

    def send_emails(self):
        if not all([self.contacts_file_var.get(), self.gmail_file_var.get(), self.subject_file_var.get(), self.template_file_var.get()]):
            messagebox.showerror("Error", "Please select all CSV files and the Email Template HTML.")
            return

        self.log("Sending emails...")

        try:
            # Read CSV files
            contacts_data = pd.read_csv(self.contacts_file_var.get())
            email_data = pd.read_csv(self.gmail_file_var.get())
            subject_data = pd.read_csv(self.subject_file_var.get())

            # Create a new log file with a timestamp for this run
            now = datetime.datetime.now()
            timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
            self.log_file = os.path.join(self.log_directory, f"email_log_{timestamp}.txt")

            with open(self.log_file, 'w') as log:
                for _, contact in contacts_data.iterrows():
                    try:
                        email_account = email_data.sample(n=1).iloc[0]
                        sender_email = email_account['email']
                        sender_password = email_account['password']
                        recipient_email = contact['email']
                        subject = random.choice(subject_data['subject'])

                        with open(self.template_file_var.get(), 'r') as f:
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

                        # Log the successful email in the log file
                        log.write(f"Sent to {recipient_email}: {subject}\n")

                    except Exception as e:
                        # Log the failed email in the log file
                        log.write(f"Failed to send to {recipient_email}: {e}\n")

            self.log("All emails sent successfully!")

        except Exception as e:
            self.log(f"Error: {e}")
            messagebox.showerror("Error", f"An error occurred: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = EmailSenderApp(root)
    root.mainloop()
