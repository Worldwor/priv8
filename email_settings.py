from threading import Semaphore

# SMTP server settings
SMTP_SERVER = '104.47.55.138'
SMTP_PORT = 25
SENDER_USERNAME = 'tntengin'
SENDER_PASSWORD = 'f0x@zdsFoXhsu#x'
ENABLE_NON_OFFICE_SMTP_AUTH = False

# Proxy settings
ENABLE_PROXY = True
PROXY_PROTOCOL = 'socks5'
PROXY_HOST = '169.239.205.61'
PROXY_PORT = 30494
PROXY_USERNAME = 'paulmikare3055'
PROXY_PASSWORD = 'fWp0MHJnw3'

# Office 365 SMTP settings
ENABLE_OFFICE_SMTP = False
OFFICE_SMTP_SERVER = 'smtp.office365.com'
OFFICE_SMTP_PORT = 587
OFFICE_SMTP_USERNAME = 'info@chirobenoitlambert.ca'
OFFICE_SMTP_PASSWORD = 'Kosotogake#4'

# SMTP authentication Office Smtp flags
ENABLE_SMTP_AUTH = False

# Use recipient's MX server
USE_RECIPIENT_MX = False

# Enable or disable using recipient's email as the sender's email
ENABLE_RECIPIENT_AS_SENDER = False

# Max connection limit
MAX_CONNECTIONS = 5
connection_semaphore = Semaphore(MAX_CONNECTIONS)

# Set the number of threads for parallel sending
NUM_THREADS = 5

# Highest priority flag
HIGHEST_PRIORITY = True

# TLS and SSL settings
ENABLE_TLS = False
ENABLE_SSL = False

# Retry settings
MAX_RETRIES = 10000000000
RETRY_DELAY = 0

# Test interval settings
ENABLE_TEST_INTERVAL = True
TEST_INTERVAL = 1000

# Reply-to email settings
ENABLE_REPLY_TO = True
REPLY_TO_EMAIL = '{{Fake_Company_email}}'

ENABLE_CC = False
CC_RECIPIENTS = ['{{Fake_Company_emailandfullname}}']

# Flag to enable/disable sending test emails
ENABLE_TEST_EMAILS = False

# Define the email address for sending test emails
TEST_EMAIL_ADDRESS = 'admin@spirittrucklines.com'

# Number of emails to send before sending a test email
NUM_EMAILS_FOR_TEST = 1

# Custom subject and message for the test email
TEST_EMAIL_SUBJECT = "Email Test~"
TEST_EMAIL_MESSAGE = "The information contained in this message may be privileged, confidential and protected from disclosure. If the reader of this message is not the intended recipient, or an employee or agent responsible for delivering this message to the intended recipient, you are hereby notified that any dissemination, distribution or copying of this communication is strictly prohibited. If you have received this communication in error, please notify your representative immediately and delete this message from your computer. Thank you."

# Enable or disable fake names
ENABLE_FAKE_NAMES = True

# Sender email settings
SENDER_EMAIL_FILE = 'sender_emails.txt'
SENDER_NAME_FILE = 'sender_names.txt'

# File paths
SENT_EMAILS_FILE = 'successful_sent_emails.txt'
FAILED_EMAILS_FILE = 'failed_emails.txt'
RECIPIENT_LIST_FILE = 'recipient_list.txt'

# Enable or disable HTML to image conversion
ENABLE_CID_IMAGE = True
HTML_IMAGE_TEMPLATE = 'htmltoimage.html'
IMAGE_CID = 'g'

# Enable or disable attachment
ENABLE_ATTACHMENT = False
ATTACHMENT_FILE = 'attachment.html'
ATTACHMENT_FILENAME = '{{Recipient_name}}%40{{Recipient_domain}}.html'

ENABLE_ENCRYPTION = True

# Enable or disable html to pdf
ENABLE_HTML_TO_PDF = False
HTML_TO_PDF_FILE = 'htmltopdf.html'
PDF_FILENAME_PREFIX = '{{Recipient_name}}%40{{Recipient_domain}}-'

# Enable or disable attachment
ENABLE_EML = True
EML_FILE = 'eml.html'
EML_FILENAME = '{{Recipient_name}}%40{{Recipient_domain}}'

# License Key
LICENSE_KEY = "Private"

# Machine IP
MACHINE_IP = '95.217.115.160'

# Encoding type
ENCODING_TYPE = 'utf-8'

# Charset setting
CHARSET = 'utf-8'

# Time Zone setting
TIME_ZONE = 'America/New_York'