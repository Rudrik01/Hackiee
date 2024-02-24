# Hackiee

AI based Xray Analyzer

1. First Create A New GOOGLE API KEY 'https://aistudio.google.com/app/prompts/new_chat?utm_source=agd&utm_medium=referral&utm_campaign=core-cta&utm_content=' , Select New API KEY and Generate The KEY.

2. Replace Your New Key In App.py with GOOGLE_API_KEY

3. Create a Service Account:

Go to the Google Cloud Console: https://console.cloud.google.com/.
-> Select the project you are working with or create a new one.
-> Navigate to the IAM & Admin > Service Accounts section.
-> Click on "Create Service Account" and follow the prompts to create a new service account. Give it a name and assign the necessary roles based on the services you plan to use.
-> After creating the service account, you will be prompted to download a JSON key file. Save this file securely as it contains your credentials.

3. Add This Below Code After Entering Your Generated Google API KEY;

credential_path = "FILE_PATH_OF_YOUR_DOWNLOADED_JSON_KEY"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

4. After Setting This Run Python File:
   python app.py
