from flask import Flask
from threading import Thread

app = Flask(__name__)


@app.route('/')
def main():
    return "Alive"


def run():
    # app.run(host="0.0.0.0", port=8080, debug=True)
    app.run(host="0.0.0.0", port=8080)


def keep_alive():
    server = Thread(target=run)
    server.start()


"""
{
    "Join": {
        "des": "des",
        "Syntax": "des",
        "Aliases": "des",
        "Uses": "des",
        "footer": "Argument in {} are Optional argument and in [] are required.",
        "cat": "com"
    },
    "Leave": {
        "des": "des",
        "Syntax": "des",
        "Aliases": "des",
        "Uses": "des",
        "footer": "Argument in {} are Optional argument and in [] are required.",
        "cat": "com"
    },
    "Play": {
        "des": "des",
        "Syntax": "des",
        "Aliases": "des",
        "Uses": "des",
        "footer": "Argument in {} are Optional argument and in [] are required.",
        "cat": "com"
    },
    "Pause": {
        "des": "des",
        "Syntax": "des",
        "Aliases": "des",
        "Uses": "des",
        "footer": "Argument in {} are Optional argument and in [] are required.",
        "cat": "com"
    },
    "Resume": {
        "des": "des",
        "Syntax": "des",
        "Aliases": "des",
        "Uses": "des",
        "footer": "Argument in {} are Optional argument and in [] are required.",
        "cat": "com"
    },
    "Now": {
        "des": "des",
        "Syntax": "des",
        "Aliases": "des",
        "Uses": "des",
        "footer": "Argument in {} are Optional argument and in [] are required.",
        "cat": "com"
    },
    "Stop": {
        "des": "des",
        "Syntax": "des",
        "Aliases": "des",
        "Uses": "des",
        "footer": "Argument in {} are Optional argument and in [] are required.",
        "cat": "com"
    },
    "Skip": {
        "des": "des",
        "Syntax": "des",
        "Aliases": "des",
        "Uses": "des",
        "footer": "Argument in {} are Optional argument and in [] are required.",
        "cat": "com"
    },
    "Queue": {
        "des": "des",
        "Syntax": "des",
        "Aliases": "des",
        "Uses": "des",
        "footer": "Argument in {} are Optional argument and in [] are required.",
        "cat": "com"
    },
    "Shuffle": {
        "des": "des",
        "Syntax": "des",
        "Aliases": "des",
        "Uses": "des",
        "footer": "Argument in {} are Optional argument and in [] are required.",
        "cat": "com"
    },
    "Remove": {
        "des": "des",
        "Syntax": "des",
        "Aliases": "des",
        "Uses": "des",
        "footer": "Argument in {} are Optional argument and in [] are required.",
        "cat": "com"
    },
    "Loop": {
        "des": "des",
        "Syntax": "des",
        "Aliases": "des",
        "Uses": "des",
        "footer": "Argument in {} are Optional argument and in [] are required.",
        "cat": "com"
    },
    "avatar": {
        "des": "des",
        "Syntax": "des",
        "Aliases": "des",
        "Uses": "des",
        "footer": "Argument in {} are Optional argument and in [] are required.",
        "cat": "com"
    },
    "userbanner": {
        "des": "des",
        "Syntax": "des",
        "Aliases": "des",
        "Uses": "des",
        "footer": "Argument in {} are Optional argument and in [] are required.",
        "cat": "com"
    },
    "icon": {
        "des": "des",
        "Syntax": "des",
        "Aliases": "des",
        "Uses": "des",
        "footer": "Argument in {} are Optional argument and in [] are required.",
        "cat": "com"
    },
    "banner": {
        "des": "des",
        "Syntax": "des",
        "Aliases": "des",
        "Uses": "des",
        "footer": "Argument in {} are Optional argument and in [] are required.",
        "cat": "com"
    },
    "serverinfo": {
        "des": "des",
        "Syntax": "des",
        "Aliases": "des",
        "Uses": "des",
        "footer": "Argument in {} are Optional argument and in [] are required.",
        "cat": "com"
    },
    "dictionary": {
        "des": "des",
        "Syntax": "des",
        "Aliases": "des",
        "Uses": "des",
        "footer": "Argument in {} are Optional argument and in [] are required.",
        "cat": "com"
    },
    "sinpe": {
        "des": "des",
        "Syntax": "des",
        "Aliases": "des",
        "Uses": "des",
        "footer": "Argument in {} are Optional argument and in [] are required.",
        "cat": "com"
    },
    "esnipe": {
        "des": "des",
        "Syntax": "des",
        "Aliases": "des",
        "Uses": "des",
        "footer": "Argument in {} are Optional argument and in [] are required.",
        "cat": "com"
    },
    "invite": {
        "des": "des",
        "Syntax": "des",
        "Aliases": "des",
        "Uses": "des",
        "footer": "Argument in {} are Optional argument and in [] are required.",
        "cat": "com"
    }
"""