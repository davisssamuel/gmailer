# Gmailer

A simple Python script to send (spoofed) emails

# Required Arguments 

All of the following arguments are required for the script to function properly.

| Flag         | Description                            |
| ------------ | -------------------------------------- |
| `--sender`   | the email to send from                 |
| `--auth`     | the password for the sender email      |
| `--spoofed`  | the sender name to appear on the email |
| `--receiver` | the email to send to                   |
| `--subject`  | the subject of the email               |
| `--file`     | the file for the email body            |


NOTE: the final flag requires a file (or file path) to read the email body content from. 

# Additional Info

If you wish you can import this script and use the `send_email` function in your own scripts without having to use the command line interface.