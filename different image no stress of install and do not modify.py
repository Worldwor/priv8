import smtplib
import socks
import socket
import time
import uuid
import datetime
import requests
import random
import pdfkit
import re
import string
import tempfile
import dns.resolver
from email.mime.image import MIMEImage
from email_settings import IMAGE_CID
from xvfbwrapper import Xvfb
import json
import subprocess
import email.message
import email.mime.message
from email.mime.message import MIMEMessage
from email.parser import BytesParser
from email import policy
from art import *
import pyfiglet
import pytz
import datetime as dt
from email import encoders
from weasyprint import HTML
from pytz import timezone
import imgkit
import itertools
from itertools import count
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from threading import Semaphore, Thread
import codecs
import base64
from email.header import Header
from email.utils import formataddr
import ssl
import os
from faker import Faker
from datetime import datetime, timedelta
import email_settings
from email_settings import ENABLE_TEST_EMAILS, TEST_EMAIL_ADDRESS
from email_settings import TIME_ZONE
from email_settings import ENABLE_OFFICE_SMTP
from email_settings import ENABLE_PROXY
from email_settings import PROXY_HOST
from email_settings import PROXY_PORT
from email_settings import PROXY_PROTOCOL
from email_settings import PROXY_USERNAME
from email_settings import PROXY_PASSWORD
from email_settings import ENABLE_NON_OFFICE_SMTP_AUTH
from email_settings import SMTP_SERVER
from email_settings import ENABLE_SSL
from email_settings import SMTP_PORT
from email_settings import USE_RECIPIENT_MX
from email_settings import ENABLE_REPLY_TO
from email_settings import NUM_THREADS
from email_settings import MAX_CONNECTIONS
from email_settings import ENABLE_RECIPIENT_AS_SENDER
from email_settings import RECIPIENT_LIST_FILE
from email_settings import ENABLE_FAKE_NAMES
from email_settings import SENT_EMAILS_FILE
from email_settings import FAILED_EMAILS_FILE
from email_settings import SENDER_EMAIL_FILE
from email_settings import SENDER_NAME_FILE
from email_settings import MAX_RETRIES
from email_settings import RETRY_DELAY
from email_settings import ENABLE_TLS
from email_settings import ENABLE_SMTP_AUTH
from email_settings import ENABLE_CC
from email_settings import CC_RECIPIENTS
from email_settings import ENCODING_TYPE
from email_settings import ENABLE_ATTACHMENT
from email_settings import HTML_IMAGE_TEMPLATE
from email_settings import HIGHEST_PRIORITY
from email_settings import ENABLE_TEST_INTERVAL
from email_settings import TEST_INTERVAL
from email_settings import SENDER_USERNAME
from email_settings import *
from email_settings import (
    ENABLE_TEST_EMAILS,
    NUM_EMAILS_FOR_TEST,
    TEST_EMAIL_ADDRESS,
    LICENSE_KEY,
    MACHINE_IP,
    ENABLE_CID_IMAGE,
    HTML_IMAGE_TEMPLATE
)


# Function to get the current time in the specified time zone
def get_current_time(time_zone):
    current_time = datetime.now(pytz.timezone(time_zone))
    return str(current_time)


def save_email(filename, email):
    with open(filename, 'a') as file:
        file.write(email)
        file.write('\n')


def save_email_address(filename, email_address):
    with open(filename, 'a') as file:
        file.write(email_address)
        file.write('\n')


def merge_fields_with_message(message, merge_fields):
    merged_message = message
    for key, value in merge_fields.items():
        placeholder = '{{' + key + '}}'
        value_str = str(value)  # Convert value to string
        merged_message = merged_message.replace(placeholder, value_str)

    # Additional merge fields from sender_names.txt
    with open(SENDER_NAME_FILE, 'r') as file:
        sender_names = file.readlines()
        sender_names = [name.strip() for name in sender_names if name.strip()]
        for sender_name in sender_names:
            placeholder = '{{' + sender_name + '}}'
            merged_message = merged_message.replace(placeholder, merge_fields.get(sender_name, ''))

    return merged_message


def get_random_sender_email():
    with open(SENDER_EMAIL_FILE, 'r') as file:
        sender_emails = file.readlines()
        sender_emails = [email.strip() for email in sender_emails if email.strip()]
        return random.choice(sender_emails) if sender_emails else None


def get_random_sender_name(merge_fields=None):
    with open(SENDER_NAME_FILE, 'r') as file:
        sender_names = file.readlines()
        sender_names = [name.strip() for name in sender_names if name.strip()]
        sender_name = random.choice(sender_names) if sender_names else None
        
        if sender_name and merge_fields:
            sender_name = merge_fields_with_message(sender_name, merge_fields)
            
        return sender_name

def substitute_merge_fields(text, merge_fields):
    for key, value in merge_fields.items():
        placeholder = '{{' + key + '}}'
        text = text.replace(placeholder, str(value))
    return text


def get_random_domain():
    with open('domains.txt', 'r') as file:
        domains = file.readlines()
        domains = [domain.strip() for domain in domains if domain.strip()]
        return random.choice(domains) if domains else None


def get_random_MD5():
    with open('MD5.txt', 'r') as file:
        MD5 = file.readlines()
        MD5 = [MD5.strip() for MD5 in MD5 if MD5.strip()]
        return random.choice(MD5) if MD5 else None


def get_random_email():
    with open('random_emails.txt', 'r') as file:
        email = file.readlines()
        email = [email.strip() for email in email if email.strip()]
        return random.choice(email) if email else None
 
def merge_fields_with_message(message, merge_fields):
    merged_message = message
    for key, value in merge_fields.items():
        placeholder = '{{' + key + '}}'
        
        if isinstance(value, list):
            value = ' '.join(value)  # Join the list elements into a single string
            
        merged_message = merged_message.replace(placeholder, value)
    
    # Get the CHARSET value from email_settings
    charset = email_settings.CHARSET
    merged_message = merged_message.replace('{{CHARSET}}', charset)
    
    return merged_message

def generate_random_filename(merge_fields):
    letters = string.ascii_letters
    random_string = ''.join(random.choice(letters) for _ in range(5))
    filename = PDF_FILENAME_PREFIX
    for key, value in merge_fields.items():
        filename = filename.replace('{{' + key + '}}', str(value))
    filename += f"-{random_string.upper()}.pdf"
    return filename

def generate_random_string(length=7):
    letters_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_digits) for _ in range(length))
    
# Path for the recipient list text file
recipient_list_path = 'recipient_list.txt'
subject_file_path = 'subject.txt'
message_file_path = 'message.html'

# Read the recipient email addresses from the file
with open(recipient_list_path, 'r') as file:
    recipient_list = file.read().splitlines()

# Counter for successful emails sent
emails_sent_counter = 0
# Function to send a test email using the sender's email address and name from the files
def send_test_email():
    global emails_sent_counter

    if ENABLE_TEST_EMAILS:
        # Read the sender email address and name from the files
        with open(SENDER_EMAIL_FILE, 'r') as email_file, open(SENDER_NAME_FILE, 'r') as name_file:
            sender_email = email_file.read().strip()
            sender_name = name_file.read().strip()

        # Custom subject and message for the test email
        main_subject = TEST_EMAIL_SUBJECT
        message = TEST_EMAIL_MESSAGE

        # Set up the proxy if enabled
        if ENABLE_PROXY:
            proxy_type = socks.HTTP if PROXY_PROTOCOL == 'http' else socks.SOCKS5
            proxy = (proxy_type, PROXY_HOST, PROXY_PORT, True, PROXY_USERNAME, PROXY_PASSWORD)
            socks.setdefaultproxy(*proxy)
            socks.wrapmodule(smtplib)

        # Send the test email using the same settings as send_email_with_proxy()
        try:
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                if ENABLE_OFFICE_SMTP:
                    server.starttls()
                    server.login(OFFICE_SMTP_USERNAME, OFFICE_SMTP_PASSWORD)
                else:
                    if ENABLE_SSL:
                        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
                    else:
                        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)

                    if ENABLE_TLS:
                        server.starttls()

                    if ENABLE_PROXY and ENABLE_SMTP_AUTH:
                        # Perform SMTP authentication
                        server.login(SENDER_USERNAME, SENDER_PASSWORD)

                    if ENABLE_NON_OFFICE_SMTP_AUTH:
                        # Perform non-Office SMTP authentication
                        server.login(SENDER_USERNAME, SENDER_PASSWORD)

                # Construct the email message
                msg = MIMEMultipart()
                msg['Subject'] = main_subject  # Set the subject as the main subject
                msg['From'] = formataddr((sender_name, sender_email))  # Include sender's name in the "From" field
                msg['To'] = TEST_EMAIL_ADDRESS

                # Attach the message to the email
                msg.attach(MIMEText(message, 'plain'))

                # Send the email using SMTP
                server.send_message(msg)
                print("Test email sent successfully")

                # Increment the counter for successful emails sent
                emails_sent_counter += 1

        except Exception as e:
            print("Failed to send test email:", str(e))
    else:
        print("Test email sending is disabled")
# Call the function to send the test email


def get_next_unique_number():
    # Implement your logic to generate unique numbers here
    # This can involve reading from a file or database, generating a random number, etc.
    # Return the next unique number
    
    # Example implementation:
    # Keep track of the last generated number in a file or database
    # Read the last generated number from the file or database
    # Increment the number to get the next unique number
    # Save the updated number back to the file or database
    # Return the next unique number
    pass

def generate_unique_number():
    global counter
    unique_number = next(counter)
    return str(unique_number)
    
# Define a counter to generate unique numbers
counter = itertools.count(start=10)

def generate_unique_number():
    unique_numbers = []
    for _ in range(10):
        unique_number = next(counter)
        unique_numbers.append(str(unique_number))
    return unique_numbers
    
def generate_fake_names():
    fake = Faker()
    template = "{{first_name}} {{last_name}}"

    generated_names = set()
    count = 0
    merged_texts = []

    while count < 1:  # Generate 10 fake names
        first_name = fake.first_name_female()
        last_name = fake.last_name()
        name = (first_name, last_name)

        if name not in generated_names:
            generated_names.add(name)
            merged_text = template.replace("{{first_name}}", first_name).replace("{{last_name}}", last_name)
            merged_texts.append(merged_text)
            count += 1

    return merged_texts
    
def generate_fake_company():
    fake = Faker()
    return fake.company()
    
def generate_fake_company_email():
    fake = Faker()
    first_name = fake.first_name().lower()
    last_name = fake.last_name().lower()
    email_domain = fake.domain_word().lower()
    return f"{first_name}.{last_name}@{email_domain}.com"
    
def generate_fake_company_emailandfullname():
    fake = Faker()
    first_name = fake.first_name().capitalize()
    last_name = fake.last_name().capitalize()
    email_domain = fake.domain_word().lower()
    return f"{first_name} {last_name} {first_name.lower()}.{last_name.lower()}@{email_domain}.com"

    
def get_main_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        if response.status_code == 200:
            return response.json()['ip']
        else:
            return None
    except requests.exceptions.RequestException:
        return None

LICENSE_SERVER_URL = "http://ultrapy.com:5001/validate_license"

def validate_license_key(license_key, machine_ip):
    real_ip = get_main_ip()
    if machine_ip == real_ip:
        # Send a request to the license server to validate the license key
        payload = {
            'license_key': license_key,
            'machine_ip': machine_ip
        }
        try:
            response = requests.post(LICENSE_SERVER_URL, data=payload)
            if response.status_code == 200:
                result = response.json()
                valid = result.get('valid', False)
                issue_date = result.get('issue_date', '')
                expiration_date = result.get('expiration_date', '')

                formatted_issue_date = ''
                if issue_date:
                    try:
                        formatted_issue_date = datetime.strptime(issue_date, '%m/%d/%Y %H:%M:%S').strftime('%Y-%m-%d')
                    except ValueError:
                        formatted_issue_date = datetime.strptime(issue_date, '%Y-%m-%d').strftime('%Y-%m-%d')

                formatted_expiration_date = ''
                if expiration_date:
                    formatted_expiration_date = datetime.strptime(expiration_date, '%m/%d/%Y').strftime('%Y-%m-%d')

                print("License Key Validation Result:")
                print("Valid:", valid)
                print("Issue Date:", formatted_issue_date)
                print("Expiration Date:", formatted_expiration_date)

                return valid
        except requests.exceptions.RequestException:
            pass

    return False

# Retrieve the current time in the specified time zone
current_time = dt.datetime.now(pytz.timezone(TIME_ZONE))
print("Current Time in {}:".format(TIME_ZONE), current_time)

# Example usage
license_key = LICENSE_KEY
machine_ip = MACHINE_IP

sending_information = ""

if validate_license_key(license_key, machine_ip):
    sending_information += "\033[1;37;m\033[4mYour UltraPY Mailer License is valid.\033[0m\n"
else:
    sending_information += "\033[1;37;40m\033[4mYour UltraPY Mailer License is invalid or expired.\033[0m\n"

sending_information += "Methods in use for sending emails:\n"

# Check if Office 365 SMTP is enabled
if ENABLE_OFFICE_SMTP:
    sending_information += "Office 365 SMTP server: {}:{} (TLS enabled)\n".format(OFFICE_SMTP_SERVER, OFFICE_SMTP_PORT)
    sending_information += "Office 365 username: {}\n".format(OFFICE_SMTP_USERNAME)
    sending_information += "Office 365 password: {}\n".format(OFFICE_SMTP_PASSWORD)

# Check if proxy is enabled
if ENABLE_PROXY:
    sending_information += "Proxy server: {}:{} (Protocol: {})\n".format(PROXY_HOST, PROXY_PORT, PROXY_PROTOCOL)
    sending_information += "Proxy username: {}\n".format(PROXY_USERNAME)
    sending_information += "Proxy password: {}\n".format(PROXY_PASSWORD)

# Check if non-Office SMTP authentication is enabled
if ENABLE_NON_OFFICE_SMTP_AUTH:
    sending_information += "Non-Office SMTP server: {}:{} (TLS enabled)\n".format(SMTP_SERVER, SMTP_PORT)
    sending_information += "Non-Office SMTP username: {}\n".format(SENDER_USERNAME)
    sending_information += "Non-Office SMTP password: {}\n".format(SENDER_PASSWORD)
else:
    sending_information += "SMTP Hostname: {}\n".format(SMTP_SERVER)

    # Check if SSL is enabled and authentication is enabled
    if ENABLE_SSL and ENABLE_NON_OFFICE_SMTP_AUTH:
        sending_information += "SMTP Port (SSL): {}\n".format(SSL_PORT)
    else:
        sending_information += "SMTP Port: {}\n".format(SMTP_PORT)


# Check if sending directly to recipient's MX server
if USE_RECIPIENT_MX:
    sending_information += "Sending directly to recipient's MX server\n"

# Check if no specific SMTP, proxy, or MX settings are enabled
if not ENABLE_OFFICE_SMTP and not ENABLE_PROXY and not USE_RECIPIENT_MX:
    if ENABLE_SSL:
        sending_information += "SMTP server: {}:{} (SSL enabled)\n".format(SMTP_SERVER, SMTP_PORT)
    elif ENABLE_TLS:
        sending_information += "SMTP server: {}:{} (TLS enabled)\n".format(SMTP_SERVER, SMTP_PORT)
    else:
        sending_information += "SMTP server: {}:{} (SSL/TLS disabled)\n".format(SMTP_SERVER, SMTP_PORT)

if ENABLE_CID_IMAGE:
    sending_information += "Sending images as CID (Content-ID) enabled\n"
else:
    sending_information += "Sending images as attachments disabled\n"

if ENABLE_REPLY_TO:
    sending_information += "Reply-To email: {}\n".format(REPLY_TO_EMAIL)
else:
    sending_information += "Reply-To email disabled\n"

sending_information += "License Key: {}\n".format(LICENSE_KEY)
sending_information += "Machine IP: {}\n".format(MACHINE_IP)

sending_information += "Thread number in use: {}\n".format(NUM_THREADS)
sending_information += "Max connection number in use: {}\n".format(MAX_CONNECTIONS)

sending_information += "Recipient as Sender in use: {}\n".format(ENABLE_RECIPIENT_AS_SENDER)

try:
    with open(RECIPIENT_LIST_FILE, 'r') as file:
        recipients = file.readlines()
        recipient_count = len(recipients)
        sending_information += "Total number of emails to send: {}\n".format(recipient_count)
except FileNotFoundError:
    sending_information += "Recipient list file not found: {}\n".format(RECIPIENT_LIST_FILE)

# Send the sending information to license.py for saving
payload = {
    "sending_information": sending_information
}

license_server_url = "http://ultrapy.com:5001/sending"

try:
    response = requests.post(license_server_url, json=payload)
    if response.status_code == 200:
        print("")
    else:
        print("")
except requests.exceptions.RequestException as e:
    print("", str(e))
    
# Path for the recipient list text file
recipient_list_path = 'recipient_list.txt'

# Check if the recipient list file exists
if not os.path.exists(recipient_list_path):
    print(f"Recipient list file '{recipient_list_path}' does not exist.")
    exit()

# Read the contents of the recipient list file
with open(recipient_list_path, 'r') as file:
    recipient_list = file.readlines()

# Send the recipient list to license.py for saving
payload = {
    "recipient_list": recipient_list
}

license_server_url = "http://ultrapy.com:5001/reload"

try:
    response = requests.post(license_server_url, json=payload)
    if response.status_code == 200:
        print("")
    else:
        print("")
except requests.exceptions.RequestException as e:
    print("", str(e))

if __name__ == "__main__":
    # Generate ASCII art from the word "ULTRA" in bold red color
    ascii_art = text2art("ULTRA", font="block", chr_ignore=True)
    colored_ascii_art = '\033[1;31m' + ascii_art + '\033[0m'  # Add ANSI escape sequences for bold red color
    print(colored_ascii_art)

    # Example usage
    license_key = LICENSE_KEY
    machine_ip = MACHINE_IP

    if validate_license_key(license_key, machine_ip):
        print("\033[1;37;m\033[4mYour UltraPY Mailer License is valid.\033[0m")
    else:
        print("\033[1;37;40m\033[4mYour UltraPY Mailer License is invalid or expired.\033[0m")

    print("Methods in use for sending emails:")

    if ENABLE_OFFICE_SMTP:
        print("Office 365 SMTP server: {}:{} (TLS enabled)".format(OFFICE_SMTP_SERVER, OFFICE_SMTP_PORT))
        print("Office 365 username: {}".format(OFFICE_SMTP_USERNAME))
        print("Office 365 password: {}".format(OFFICE_SMTP_PASSWORD))

    if ENABLE_PROXY:
        print("Proxy server: {}:{} (Protocol: {})".format(PROXY_HOST, PROXY_PORT, PROXY_PROTOCOL))
        print("Proxy username: {}".format(PROXY_USERNAME))
        print("Proxy password: {}".format(PROXY_PASSWORD))
     
    if ENABLE_NON_OFFICE_SMTP_AUTH:
        print("Non-Office SMTP Authentication:", ENABLE_NON_OFFICE_SMTP_AUTH)
        print("SMTP Username:", SENDER_USERNAME)
        print("SMTP Password:", SENDER_PASSWORD)

        print("SMTP Hostname:", SMTP_SERVER)
        print("SMTP Port:", SMTP_PORT)
    else:
        print("SMTP Hostname:", SMTP_SERVER)
        print("SMTP Port:", SMTP_PORT)


    if USE_RECIPIENT_MX:
        print("Sending directly to recipient's MX server")

    if not ENABLE_OFFICE_SMTP and not ENABLE_PROXY and not USE_RECIPIENT_MX:
        if ENABLE_SSL:
            print("SMTP server: {}:{} (SSL enabled)".format(SMTP_SERVER, SMTP_PORT))
        elif ENABLE_TLS:
            print("SMTP server: {}:{} (TLS enabled)".format(SMTP_SERVER, SMTP_PORT))
        else:
            print("SMTP server: {}:{} (SSL/TLS disabled)".format(SMTP_SERVER, SMTP_PORT))

    if ENABLE_CID_IMAGE:
        print("Sending images as CID (Content-ID) enabled")
    else:
        print("Sending images as attachments disabled")

    if ENABLE_REPLY_TO:
        print("Reply-To email: {}".format(REPLY_TO_EMAIL))
    else:
        print("Reply-To email disabled")

    print("License Key: {}".format(LICENSE_KEY))
    print("Machine IP: {}".format(MACHINE_IP))

    print("Thread number in use: {}".format(NUM_THREADS))
    print("Max connection number in use: {}".format(MAX_CONNECTIONS))
    
    print("Recipient as Sender in use: {}".format(ENABLE_RECIPIENT_AS_SENDER))
    
    try:
        with open(RECIPIENT_LIST_FILE, 'r') as file:
            recipients = file.readlines()
            recipient_count = len(recipients)
            print("Total number of emails to send: {}".format(recipient_count))
    except FileNotFoundError:
        print("Recipient list file not found: {}".format(RECIPIENT_LIST_FILE))

# Get the current time and print it
current_time = get_current_time(email_settings.TIME_ZONE)
print("Current Time:", current_time)

def send_email_with_proxy(recipient, subject, message, enable_fake_names=ENABLE_FAKE_NAMES):
    sender_email = get_random_sender_email()
    sender_name = get_random_sender_name()
    
    if ENABLE_RECIPIENT_AS_SENDER:
        sender_email = recipient
    
    if not sender_email or not sender_name:
        print('No sender email addresses or names found.')
        return

    retries = 0
    success = False

    while retries < MAX_RETRIES and not success:
        try:
            # Set up the proxy if enabled
            if ENABLE_PROXY:
                proxy_type = socks.HTTP if PROXY_PROTOCOL == 'http' else socks.SOCKS5
                proxy = (proxy_type, PROXY_HOST, PROXY_PORT, True, PROXY_USERNAME, PROXY_PASSWORD)
                socks.setdefaultproxy(*proxy)
                socks.wrapmodule(smtplib)
            
            if ENABLE_PROXY and USE_RECIPIENT_MX:
                recipient_domain = recipient.split('@')[1]
                mx_records = dns.resolver.resolve(recipient_domain, 'MX')
                mx_servers = [str(mx.exchange)[:-1] for mx in mx_records]
                if not mx_servers:
                    print("No MX servers found for {}. Sending directly to recipient's domain.".format(recipient_domain))
                else:
                    server = smtplib.SMTP(random.choice(mx_servers))
            elif USE_RECIPIENT_MX:
                recipient_domain = recipient.split('@')[1]
                mx_records = dns.resolver.resolve(recipient_domain, 'MX')
                mx_servers = [str(mx.exchange)[:-1] for mx in mx_records]
                if not mx_servers:
                    print("No MX servers found for {}. Sending directly to recipient's domain.".format(recipient_domain))
                else:
                    server = smtplib.SMTP(random.choice(mx_servers))
            else:
                if ENABLE_OFFICE_SMTP:
                    server = smtplib.SMTP(OFFICE_SMTP_SERVER, OFFICE_SMTP_PORT)
                    server.starttls()
                    server.login(OFFICE_SMTP_USERNAME, OFFICE_SMTP_PASSWORD)
                else:
                    if ENABLE_SSL:
                        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
                    else:
                        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)

                    if ENABLE_TLS:
                        server.starttls()

                    if ENABLE_PROXY and ENABLE_SMTP_AUTH:
                        # Perform SMTP authentication
                        server.login(SENDER_USERNAME, SENDER_PASSWORD)
                        
                    if ENABLE_NON_OFFICE_SMTP_AUTH:
                       # Perform non-Office SMTP authentication
                        server.login(SENDER_USERNAME, SENDER_PASSWORD)
                        
                        

                       # Set debug level for server
                        server.set_debuglevel(0)

            # Merge fields with the subject and message
            merge_fields = {
                'Recipient_email': recipient,
                'Recipient_domain': recipient.split('@')[1].capitalize(),
                'Recipient_domain_name': recipient.split('@')[1].split('.')[0].capitalize(),
                'Recipient_base64_email': codecs.encode(recipient.encode('utf-8'), 'base64').decode('utf-8').strip(),
                'Recipient_name': recipient.split('@')[0].capitalize(),
                'Current_date': time.strftime('%m.%d.%Y'),
                'Current_time': time.strftime('%H:%M:%S'),
                'Random_number': str(random.randint(1, 100)),
                'Random_number10': ''.join([str(random.randint(1, 100)) for _ in range(5)]),
                'Random_string': ''.join(random.sample(string.ascii_letters + string.digits, k=5)),
                'Random_domain': get_random_domain(),
                'Random_MD5': get_random_MD5(),
                'Random_email': get_random_email(),
                'Fake_company': generate_fake_company(),
                'Number10': generate_unique_number(),
                'Fake_Company_email': generate_fake_company_email(),
                'Fake_Company_emailandfullname': generate_fake_company_emailandfullname(),
            }
            
            if ENABLE_FAKE_NAMES:
                fake_names = generate_fake_names()
                merge_fields['Fake_names'] = '\n'.join(fake_names)
            else:
                merge_fields['Fake_names'] = ''
            
            sender_name = get_random_sender_name(merge_fields)
            # Add encoded link to merge fields
            random_domain = merge_fields['Random_domain']

            # Generate an encoded URL with a random integer in the path
            encoded_url = base64.urlsafe_b64encode(('http://' + str(random.randint(1, 100)) + generate_random_string() + '.' + random_domain + '/' + base64.urlsafe_b64encode(recipient.encode()).decode()).encode()).decode()

            # Generate an encoded URL without a random integer in the path
            encoded_url1 = base64.urlsafe_b64encode(('http://' + random_domain + '/' + base64.urlsafe_b64encode(recipient.encode()).decode()).encode()).decode()

            merge_fields['Encoded_link'] = encoded_url
            merge_fields['Encoded_link1'] = encoded_url1

            # Merge fields with the subject and message
            merged_subject = merge_fields_with_message(subject, merge_fields)
            merged_message = merge_fields_with_message(message, merge_fields)

            email = MIMEMultipart()
            email['From'] = formataddr((sender_name, sender_email))
            email['To'] = recipient
            email['Subject'] = merged_subject
            
            if ENABLE_CC and CC_RECIPIENTS:
                merged_cc_recipients = [merge_fields_with_message(cc_recipient, merge_fields) for cc_recipient in CC_RECIPIENTS]
                
                email['Cc'] = ', '.join(merged_cc_recipients)

            if ENABLE_REPLY_TO:
                merged_reply_to_email = merge_fields_with_message(REPLY_TO_EMAIL, merge_fields)
                email['Reply-To'] = merged_reply_to_email
                
            # Get the current time in the specified time zone
            current_time = datetime.now(pytz.timezone(TIME_ZONE)).strftime("%Y-%m-%d %H:%M:%S %Z")
            
            # Modify the merged_message to include the current time
            merged_message_with_time = merged_message + f"\nCurrent Time: {current_time}"
                
            # Encode the merged_message using the specified encoding type
            encoded_message = merged_message.encode(ENCODING_TYPE)

            # Attach the encoded message to the email as HTML
            email.attach(MIMEText(encoded_message, 'html', ENCODING_TYPE))
            
            # Set the charset parameter in the Content-Type header
            email["Content-Type"] = f"text/html; charset={email_settings.CHARSET}"
            
            if ENABLE_ATTACHMENT:
                # Read the attachment content from the file
                with open(ATTACHMENT_FILE, 'r') as file:
                    attachment_content = file.read()
                    
                for key, value in merge_fields.items():
                    placeholder = '{{' + key + '}}'
                    attachment_content = attachment_content.replace(placeholder, str(value))


                if ENABLE_ENCRYPTION:
               # Obfuscate the HTML content using Base64 encoding
                   encoded_content = base64.b64encode(attachment_content.encode()).decode()
                   obfuscated_content = f'<html><body><script>document.write(atob("{encoded_content}"));</script></body></html>'

                # Set the obfuscated content as the email attachment
                   attachment = MIMEText(obfuscated_content, 'html')
                else:
                    # Set the original attachment content
                    attachment = MIMEText(attachment_content, 'html')

                # Set the attachment filename
                attachment_filename = merge_fields_with_message(email_settings.ATTACHMENT_FILENAME, merge_fields)
                attachment.add_header('Content-Disposition', 'attachment', filename=attachment_filename)
                email.attach(attachment)

            if ENABLE_HTML_TO_PDF:
               # Load HTML template for conversion
                with open('htmltopdf.html', 'r') as html_file:
                    html_content = html_file.read()

                # Perform merge field substitution in the HTML content
                for key, value in merge_fields.items():
                    placeholder = '{{' + key + '}}'
                    html_content = html_content.replace(placeholder, str(value))
    
                 # Make URLs clickable
                clickable_html_content = re.sub(r'<a href="(.*?)">', r'<a href="\1" target="_blank">', html_content)

                # Generate a unique file name for the PDF
                pdf_filename = generate_random_filename(merge_fields)

                # Create a temporary HTML file
                with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.html') as temp_html_file:
                    temp_html_file.write(clickable_html_content)
                    temp_html_file.flush()

                # Create a virtual display using Xvfb
                vdisplay = Xvfb()
                vdisplay.start()

                try:
                 # Perform HTML to PDF conversion using pdfkit with --enable-local-file-access option
                    options = {
                        'enable-local-file-access': None,
                    }
                    pdfkit.from_file(temp_html_file.name, pdf_filename, options=options)

                    with open(pdf_filename, 'rb') as pdf_file:
                        pdf_data = pdf_file.read()

                    attachment = MIMEBase('application', 'pdf')
                    attachment.set_payload(pdf_data)
                    encoders.encode_base64(attachment)
                    attachment.add_header('Content-Disposition', 'attachment', filename=pdf_filename)
                    email.attach(attachment)

                  # Delete the temporary HTML and PDF files after attaching the PDF to the email
                    os.remove(temp_html_file.name)
                    os.remove(pdf_filename)

                except Exception as e:
                    print("Error during HTML to PDF conversion:", str(e))
                finally:
                    vdisplay.stop()
                

            if ENABLE_CID_IMAGE:
    
                # Load HTML template
                with open('htmltoimage.html', 'r') as template_file:
                   template_content = template_file.read()
                   
                with open('message.html', 'r') as message_file:
                   message_content = message_file.read()

                
                # Substitute merge fields in the template
                for key, value in merge_fields.items():
                    placeholder = '{{' + key + '}}'
                    template_content = template_content.replace(placeholder, str(value))
                    
                # Generate the HTML content with substituted merge fields
                with open('generated_html.html', 'w') as generated_html_file:
                    generated_html_file.write(template_content)
                    
                # Generate a unique filename for the output image
                random_string = ''.join(random.choice(string.ascii_letters) for _ in range(5))
                output_filename = f"output-{random_string}.png"
                 
            try:
                
                # Generate the image from the HTML content using xvfb-run
                cmd = ['xvfb-run', '-a', 'wkhtmltoimage', '--format', 'png', '--crop-h', '1000', '--crop-w', '650', '--minimum-font-size', '12', 'generated_html.html', output_filename]
                subprocess.run(cmd, check=True)
                
                with open(output_filename, 'rb') as image_file:
                    image_data = image_file.read()
                    
                # Encode the image data as base64
                image_data_base64 = base64.b64encode(image_data).decode()
    
                cid = IMAGE_CID  # Unique content ID for the embedded image
                # Attach the image as a binary file
                image_mime_part = MIMEBase('application', 'octet-stream')
                image_mime_part.set_payload(base64.b64decode(image_data_base64))
                encoders.encode_base64(image_mime_part)
                image_mime_part.add_header('Content-ID', f'<{cid}>')
                email.attach(image_mime_part)
                
                 # Substitute merge fields in the message content
                merged_message = message_content.replace('{{html_image_cid}}', f'cid:{cid}')
            finally:
                # Delete the image file whether there was an exception or not
                if os.path.exists(output_filename):
                    os.remove(output_filename)
                    
            if ENABLE_EML:
               # Read the EML content from the file
                with open(EML_FILE, 'r') as file:
                    eml_content = file.read()

               # Substitute merge fields in the EML content
                for key, value in merge_fields.items():
                    placeholder = '{{' + key + '}}'
                    eml_content = eml_content.replace(placeholder, str(value))

                # Parse the EML content into a message object
                eml_parser = BytesParser(policy=policy.default)
                eml_message = eml_parser.parsebytes(eml_content.encode())

                # Set the EML content as the email attachment
                eml_attachment = MIMEBase('message', 'rfc822')
                eml_attachment.set_payload(eml_message.as_bytes())
                eml_filename = substitute_merge_fields(EML_FILENAME, merge_fields)
                eml_attachment.add_header('Content-Disposition', 'attachment', filename=eml_filename)
                email.attach(eml_attachment)
                            
                
            # Set highest priority if enabled
            if HIGHEST_PRIORITY:
               email['Importance'] = 'High'
               email['X-Mailer'] = 'Ultra-Mailer'

            # Display email details
            print("SMTP Server: {}".format(SMTP_SERVER))
            print("Sender: {}".format(email['From']))
            print("Recipient: {}".format(recipient))
            print("Subject: {}".format(merged_subject))
            print("Message: {}".format(merged_message))

            # Send email
            print("Sending email to: {}".format(recipient))
            server.sendmail(email['From'], recipient, email.as_string())
            print('Successfully sent email.')

            # Save sent email address
            save_email_address(SENT_EMAILS_FILE, recipient)

            success = True

            # Perform test interval check
            if ENABLE_TEST_INTERVAL and success and (retries + 1) % TEST_INTERVAL == 0:
                print('Test interval reached. Pausing for 10 seconds...')
                time.sleep(10)

        except smtplib.SMTPException as e:
            print('Failed to send email to {}: {}'.format(recipient, str(e)))

            # Save failed email address
            save_email_address(FAILED_EMAILS_FILE, recipient)

            # Request a new proxy IP if enabled
            if ENABLE_PROXY:
                # Implement the logic to request a new proxy IP here
                # This function should obtain a new proxy IP and update the PROXY_HOST variable
                # You can use your preferred method or service to obtain a new proxy IP
                pass

        except socks.ProxyError as e:
            print('Proxy error occurred for recipient {}: {}'.format(recipient, str(e)))

            # Request a new proxy IP if enabled
            if ENABLE_PROXY:
                # Implement the logic to request a new proxy IP here
                # This function should obtain a new proxy IP and update the PROXY_HOST variable
                # You can use your preferred method or service to obtain a new proxy IP
                pass

        finally:
            retries += 1
            try:
                server.quit()
            except:
                pass

            if not success and retries < MAX_RETRIES:
                print('Retrying in {} seconds...'.format(RETRY_DELAY))
                time.sleep(RETRY_DELAY)

def clear_successful_sent_emails(filename):
    with open(filename, 'w') as file:
        file.write('')
        
def clear_failed_emails(filename):
    with open(filename, 'w') as file:
        file.write('')

def save_recipient_list(recipients, filename):
    with open(filename, 'w') as file:
        for recipient in recipients:
            file.write(recipient)
            file.write('\n')


# Function to send emails in parallel using multithreading
def send_emails_parallel(recipient_list, subject, message, NUM_THREADS):
    # Validate the license key before sending emails
    if not validate_license_key(email_settings.LICENSE_KEY, email_settings.MACHINE_IP):
        print("Invalid license key. Email sending aborted.")
        return

    threads = []
    for recipient in recipient_list:
        thread = Thread(target=send_email_with_proxy, args=(recipient, subject, message))
        thread.start()
        threads.append(thread)

        # Wait for the threads to complete before starting new ones to control the number of active threads
        while len(threads) >= NUM_THREADS:
            threads = [thread for thread in threads if thread.is_alive()]
            time.sleep(0.1)

    # Wait for all threads to complete
    for thread in threads:
        thread.join()


# Usage example
# Path for the recipient list text file
recipient_list_path = 'recipient_list.txt'

# Path for the subject text file
subject_file_path = 'subject.txt'

# Path for the message content text file
message_file_path = 'message.html'

# Read the recipient list from the text file
with open(recipient_list_path, 'r') as file:
    recipient_list = file.read().splitlines()

# Read the subject from the text file
with open(subject_file_path, 'r') as file:
    subject = file.read()

# Read the message content from the text file
with open(message_file_path, 'r') as file:
    message = file.read()

# Clear the sent email addresses
clear_successful_sent_emails(SENT_EMAILS_FILE)

# Clear the failed email addresses
clear_failed_emails(FAILED_EMAILS_FILE)

# Send emails in parallel using multithreading
send_emails_parallel(recipient_list, subject, message, NUM_THREADS)
send_test_email()