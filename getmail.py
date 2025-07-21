
import yaml
import logging
import imaplib


# loads credentials securely from given yaml file.
# returns: email, password
def loading_credentials(filepath):
    try:
        with open(filepath, 'r') as file:
            credentials = yaml.safe_load(file)
            email = credentials['email']
            password = credentials['password']

            if email == None or password == None:
                raise ValueError("Missing email or password in credentials file.")
            return email, password

    except Exception as e:
        logging.error(f"failed to load email credentials from {filepath}: {e}")
        raise


# loads emails from gmail inbox using IMAP and SSL
# returns: IMAP mail object, containing all details
def connect_to_gmail_imap(email, password):
    imap_url = 'imap.gmail.com'
    try:
        mail = imaplib.IMAP4_SSL(imap_url)
        mail.login(email, password)
        return mail
    except Exception as e:
        logging.error(f"failed to connect to gmail imap: {e}")
        raise