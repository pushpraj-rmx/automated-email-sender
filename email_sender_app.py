import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import pandas as pd
from utilities import send_email, read_csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random

class EmailSenderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Email Sender App")

        # Create frames
        self.create_left_frame()
        self.create_right_frame()

        # Initialize variables for file paths
        self.contacts_file = ""
        self.gmail_file = ""
        self.subject_file = ""
        self.template_file = ""

    # ... (Rest of the EmailSenderApp class)
