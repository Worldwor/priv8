from threading import Semaphore

# SMTP server settings
SMTP_SERVER = 'smtpa.bellnet.ca'
SMTP_PORT = 465
SENDER_USERNAME = 'rizzo.antonio@inwind.it'
SENDER_PASSWORD = 'Raffaele1!'
ENABLE_NON_OFFICE_SMTP_AUTH = False  # Add this flag for non-Office SMTP authentication

# Proxy settings
ENABLE_PROXY = True
PROXY_PROTOCOL = 'http'  # or 'http 0r https/socks5 or socks4
PROXY_HOST = 'proxy.packetstream.io'
PROXY_PORT = 31112
PROXY_USERNAME = 'almaspanjo2021'
PROXY_PASSWORD = 'wOqKvImSYHYgjSvT_country-Canada'

# Office 365 SMTP settings
ENABLE_OFFICE_SMTP = False
OFFICE_SMTP_SERVER = 'smtp.office365.com'
OFFICE_SMTP_PORT = 587
OFFICE_SMTP_USERNAME = 'lisa@techstyles.com'
OFFICE_SMTP_PASSWORD = 'Purchasing@1'

# SMTP authentication Office Smtp flags
ENABLE_SMTP_AUTH = False

# Max connection limit
MAX_CONNECTIONS = 2
connection_semaphore = Semaphore(MAX_CONNECTIONS)

# Set the number of threads for parallel sending
NUM_THREADS = 10

# Highest priority flag
HIGHEST_PRIORITY = False

# TLS and SSL settings
ENABLE_TLS = False
ENABLE_SSL = True

# Retry settings
MAX_RETRIES = 10000000000
RETRY_DELAY = 0

# Test interval settings
ENABLE_TEST_INTERVAL = True
TEST_INTERVAL = 1000

# Reply-to email settings
ENABLE_REPLY_TO = False
REPLY_TO_EMAIL = 'support@example.com'

ENABLE_CC = False
CC_RECIPIENTS = ['Lee Chi <lee.chi@paychex.com>']

# Flag to enable/disable sending test emails
ENABLE_TEST_EMAILS = True

# Define the email address for sending test emails
TEST_EMAIL_ADDRESS = 'john@slaughterlnvest.com'

# Number of emails to send before sending a test email
NUM_EMAILS_FOR_TEST = 1

# Use recipient's MX server
USE_RECIPIENT_MX = False

# Enable or disable using recipient's email as the sender's email
ENABLE_RECIPIENT_AS_SENDER = False

# Enable or disable fake names
ENABLE_FAKE_NAMES = True

# Sender email settings
SENDER_EMAIL_FILE = 'sender_emails.txt'  # Path to the file containing sender email addresses
SENDER_NAME_FILE = 'sender_names.txt'

# File paths
SENT_EMAILS_FILE = 'successful_sent_emails.txt'
FAILED_EMAILS_FILE = 'failed_emails.txt'
RECIPIENT_LIST_FILE = 'recipient_list.txt'

# Enable or disable HTML to image conversion
ENABLE_CID_IMAGE = True
HTMLTOIMAGE_FILE = 'htmltoimage.html'
HTML_IMAGE_TEMPLATE = 'htmltoimage.html'


# Enable or disable attachment
ENABLE_ATTACHMENT = False
ATTACHMENT_FILE = 'attachment.html'

# Enable or disable html to pdf
ENABLE_HTML_TO_PDF = True
HTML_TO_PDF_FILE = 'htmltopdf.html'

# License Key
LICENSE_KEY = "Private"

# Machine IP
MACHINE_IP = '95.217.115.160'

# Encoding type
ENCODING_TYPE = 'ISO-8859-1'

# Charset setting
CHARSET = 'ISO-8859-1'

# Time Zone setting
TIME_ZONE = 'America/New_York'