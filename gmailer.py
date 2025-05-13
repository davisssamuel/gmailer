import argparse
from base64 import b64encode
from socket import AF_INET, SOCK_STREAM, socket
from ssl import create_default_context

# Create client socket and SSL socket
SMTP_SERVER = "smtp.gmail.com"
SSL_TLS_PORT = 465
CLIENT_SOCKET = socket(AF_INET, SOCK_STREAM)
CLIENT_SOCKET.connect((SMTP_SERVER, SSL_TLS_PORT))
CONTEXT = create_default_context()
SSL_SOCKET = CONTEXT.wrap_socket(CLIENT_SOCKET, server_hostname=SMTP_SERVER)
NL = "\r\n"


def send(s):
    SSL_SOCKET.send(s.encode())
    print("SENT:" + NL + s)


def recv(s=""):
    s += SSL_SOCKET.recv(1024).decode()
    print("RCVD:" + NL + s)


def send_email(sender_email: str, sender_password: str, spoofed_sender: str, receiver_email: str, email_subject: str, email_message: str):

    print(SSL_SOCKET.cipher())

    # Send "HELLO" command
    send("EHLO localhost" + NL)

    line = ""
    while "250" not in line:
        line += SSL_SOCKET.recv(1).decode()
    recv(line)

    # Send the "AUTH LOGIN" command to start authentication
    send("AUTH LOGIN" + NL)
    recv()

    # Authenticate Gmail account
    send(b64encode(sender_email.encode()).decode("utf-8") + NL)
    recv()
    send(b64encode(sender_password.encode()).decode("utf-8") + NL)
    recv()

    # Start the normal SMTP dialogue
    send(f"MAIL FROM: <{sender_email}>{NL}")
    recv()
    send(f"RCPT TO: <{receiver_email}>{NL}")
    recv()
    send("DATA" + NL)
    recv()

    send(f"From:{spoofed_sender}\nTo:{receiver_email}\nSubject:{email_subject}{NL}")
    send(f"{email_message}{NL}.{NL}")
    recv()

    # Send "QUIT" command
    send("QUIT" + NL)

    # Close connection
    SSL_SOCKET.close()


# Main
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--sender", type=str, required=True, help="the email to send from")
    parser.add_argument("--auth", type=str, required=True, help="the password for the sender email")
    parser.add_argument("--spoofed", type=str, required=True, help="the sender name to appear on the email")
    parser.add_argument("--receiver", type=str, required=True, help="the email to send to")
    parser.add_argument("--subject", type=str, required=True, help="the subject of the email")
    parser.add_argument("--file", type=str, required=True, help="the file for the email body")
    args = parser.parse_args()

    if len(args) < 6:
        exit(0)

    sender_email    = args.sender
    sender_password = args.auth
    spoofed_sender  = args.spoofed
    receiver_email  = args.receiver
    email_subject   = args.subject
    email_message   = ""

    with open(args.file) as file:
        for line in file:
            email_message += line

    send_email(sender_email=sender_password, sender_password=sender_password, spoofed_sender=sender_password,
               receiver_email=receiver_email, email_subject=email_subject, email_message=email_message)