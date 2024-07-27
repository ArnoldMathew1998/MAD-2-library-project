from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

Mail = 'Librarian@example.com'
Password = '1234567890'
smtp_server = 'localhost'
Port = 1025

def send_email(receiver, Subject, message, user_name):
    msg = MIMEMultipart()
    msg['Subject'] = Subject
    msg['From'] = Mail
    msg['To'] = receiver
    msg.attach(MIMEText(generate_email_content(Subject, message, user_name), 'html'))

    with smtplib.SMTP(smtp_server, Port) as server:
        server.sendmail(Mail, receiver, msg.as_string())

def generate_email_content(subject, message, user_name):
    return f"""
    <html>
        <head>
            <style>
                body {{font-family: Arial, sans-serif; margin: 0; padding: 20px; color: #333;}}
                .container {{max-width: 600px; margin: auto; background: #f0f0f0; padding: 20px;}}
                h2 {{color: #007BFF;}}
            </style>
        </head>
        <body>
            <div class="container">
                <h2>{subject}</h2>
                <p>Dear {user_name},</p>
                <p>{message}</p>
                <p>Best wishes,</p>
                <p>Librarian</p>
            </div>
        </body>
    </html>
    """

def send_activity_summary_email(receiver, subject, pdf_file, user):
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = Mail
    msg['To'] = receiver

    body = f"Hi {user.first_name + ' ' + user.last_name},\n\nPlease find attached your monthly book activity summary.\n\nBest regards,\nLibrary Management Team"
    msg.attach(MIMEText(body, 'plain'))

    # Attach the PDF file
    pdf_attachment = MIMEApplication(pdf_file.read(), _subtype="pdf")
    pdf_attachment.add_header('Content-Disposition', 'attachment', filename="ActivitySummary.pdf")
    msg.attach(pdf_attachment)

    with smtplib.SMTP(smtp_server, Port) as server:
        server.sendmail(Mail, receiver, msg.as_string())
