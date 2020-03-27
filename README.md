## Clone the repo:<br>
  ```bash
  git clone https://github.com/MakwanaVihas/social_media_posting.git 
  cd social_media_posting
  pip install -r requirements.txt
  ```

## Running the app:<br>
**For twitter:**<br>
   -  Set up your twitter developer account on https://developers.twitter.com and create an app.<br>
   -  Get consumer key and consumer secret from you app's home page.<br>
   -  Enter https://127.0.0.1:8000/twitter/logged_in/ and https://127.0.0.1:8000/twitter/logged_in as callback in your app's home page. <br>
   -  Enter your key and secret in twitter_posting.views.<br>
   -  For running django server locally go to cmd and type:<br>
          ``` python manage.py runsslserver https://127.0.0.1:8000```<br> 
   -  For celery open another cmd window and cd into social_media_posting and run:<br>
   - on windows:
          ```
          celery -A social_media_posting worker --pool=eventlet -l info
          ```<br>
   - on mac or linux:
          ```
          celery -A social_media_posting worker -l info
          ```<br>
   - **MAKE SURE RUN BOTH THESE COMMANDS PARALLELLY**<br>
   -  Then go to https://127.0.0.1:8000 and choose twitter and enter your account credentials and schedule a post.
   -  **DO NOT TERMINATE OR CLOSE ANY TERMINAL WINDOWS**
  
### **For Facebook**
   - ```In facebook, to use your developer account to login into other users your app needs to pass through App Review which takes 6-7 days. So for no you can only schedule posts on your facebook pages only```
   
   -  Set you facebook developer account on https://developers.facebook.com/ and create an app.<br>
   -  Get consumer key and consumer secret from you app's home page.<br>
   -  Enter a product named Facebook Login in your app.
   -  Enter https://127.0.0.1:8000/facebook/logged_in/ and https://127.0.0.1:8000/facebook/logged_in as callback in your app's home page. <br>   
   -  Enter your key and secret in facebook_posting.views.<br>
   -  For running django server locally go to cmd and type:<br>
          ``` python manage.py runsslserver https://127.0.0.1:8000```<br> 
   -  For celery open another cmd window and cd into social_media_posting and run:<br>
          ```
          celery -A social_media_posting worker --pool=eventlet -l info
          ```<br>
   - **MAKE SURE RUN BOTH THESE COMMANDS PARALLELLY**<br>
   -  Then go to https://127.0.0.1:8000 and choose facebook and enter your account credentials and schedule a post.<br>
   -  **DO NOT TERMINATE OR CLOSE ANY TERMINAL WINDOWS**<br>
   
   
 ## Details about my django project.<br>
   - All the requirements are mentioned in requirements.txt file.<br>
   ### This django project contains three apps:<br>
      - twitter_posting (for dealing with twitter scheduling)<br>
      - facebook_posting (for dealing with facebook scheduling)<br>
      - base (which prove a bridge to connect both the apps and make it look on single app)<br>
   
   
 ###  If you decide to use django-rest-fremework then go to https://127.0.0.1:8000/rest after setting up the app locally.<br>
      
 ## MAKE SURE YOU RUN YOUR SERVER ON https://127.0.0.1:8000 locally and DON'T USE ANY OTHER PORT BECAUSE YOU HAVE ENETR VALID CALLBACK url IN YOU DEVELOPER ACCOUNT
   
   
