1. Install python3 and pip3 packages if it is not installed.
2. Install packages in requirements.txt:
   pip3 install -r requirements.txt
3. Enable drive api for your google account:
   https://developers.google.com/drive/api/v3/quickstart/python >> ENABLE THE DRIVE API, download credentials.json and put it to script's folder.
4. Start script: 
   ./share [email]
   You will need to select a google account.
5. To re-select an account, you must delete token.json from script's folder.
