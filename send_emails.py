import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random

# Load data from CSV files
contactsData = pd.read_csv('contacts.csv')
emailData = pd.read_csv('gmail.csv')
subjectData = pd.read_csv('subject.csv')

# Iterate through each contact and send an email
for _, contact in contactsData.iterrows():
    # Choose a random email account from the available ones
    email_account = emailData.sample(n=1).iloc[0]

    # Email configuration
    sender_email = email_account['email']
    sender_password = email_account['password']
    recipient_email = contact['email']
    # Choose a random subject from the available ones
    subject = random.choice(subjectData['subject'])
    
    # Load email body from an HTML template file
    with open('email_template.html', 'r') as f:
        email_html = f.read()

    
    # Replace placeholders in the HTML content
    email_html = email_html.replace('$name', contact['name'])
    
    # Create a new email message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = subject

    # Attach the email HTML body
    message.attach(MIMEText(email_html, 'html'))

    # Connect to the email server and send the email
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, message.as_string())
            print(f"Email sent to {recipient_email} successfully")
    except Exception as e:
        print(f"Failed to send email to {recipient_email}: {e}")
