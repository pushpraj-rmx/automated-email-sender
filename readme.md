# Automated Email Sender

This script automates the process of sending personalized emails to a list of recipients using Gmail accounts. It reads recipient information from a CSV file and sends emails with customized content.

## Prerequisites

- Python 3.x
- Gmail accounts (with less secure app access enabled)

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/pushpraj-rmx/automated-email-sender.git
   cd automated-email-sender
   ```

2. **Install the required Python packages:**
   ```bash
   pip install pandas smtplib pdfkit
   ```

3. **Configure Gmail Accounts:**
   - Create a CSV file named `gmail.csv` with the following format:
     ```csv
     email,password
     your.email1@gmail.com,YourPassword1
     your.email2@gmail.com,YourPassword2
     ```
   - Ensure that less secure app access is enabled for these Gmail accounts. You can do this by going to your Google Account settings.

4. **Create the `contact.csv` file:**
   - Create a CSV file named `contact.csv` with the following format:
     ```csv
     name,email
     John,john@example.com
     Jane,jane@example.com
     ```
   - The `name` column is optional. If not provided, the script will use the email address for personalized parts.

5. **Customize Email Template:**
   - Modify the `email_template.html` file to suit your email content.
   - Use placeholders like `$name` to personalize the emails.

6. **Run the Script:**
   ```bash
   python send_emails.py
   ```

7. **Sent emails will be logged in the `mail.log` file.**

## Important Note

- Use this script responsibly and in compliance with Gmail's terms of use.
- The script might require adjustments based on your email server's security settings.
- Make sure to handle sensitive information (such as passwords) securely.

## License

This project is licensed under the [MIT License](LICENSE).
```