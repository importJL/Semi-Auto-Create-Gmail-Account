# Semi-Autonomatic Google Mail Account Creator

A Python program that carries out a simple, mostly automatic generation of a Google mail account with randomized account and e-mail information generated and outputted for future reference.


## Disclaimer & Precautions
This tool does not require installation, application, or management of Google Cloud APIs.  All libraries used are for generic front-end web-scraping with Chromium webdriver for browser interface.

However, the program does utilize a phone number for account validation to create a Google e-mail account so successful activation of account is still dependent on both requirements set out by Google and the validity of the phone number provided.  Be warned that there a limited number of times that this program can be used for the same phone number before it becomes invalidated for further use.

As the program was developed with default Chinese (Hong Kong) language preferences, discrepancies due to region or language may influence automation process and outcomes. 

## Installation
1) Clone this repository: `git clone https://github.com/importJL/Semi-Auto-Create-Gmail-Account`
2) Create and activate a virtual envrionment: `python -m venv {envrionemnt name}` and `{environment name}\Scripts\activate`
3) Install requirements: `pip install -r requirements.txt`
5) As the script utilizes `nltk` library, ensure `nltk.corpus` is downloaded
6) Run script with <b>_real_</b> phone number (no spaces, dashes or decimals between numbers):<br> 
`python create_gmail_account.py #########`
