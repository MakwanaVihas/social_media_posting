## Clone the repo:<br>
  ```bash
  git clone https://github.com/MakwanaVihas/social_media_posting.git <br>
  cd social_media_posting<br>
  pip install -r requirements.txt<br>
  ```

## Running the app:<br>
**For twitter:**<br>
   -  Set up your twitter developer account on https://developers.twitter.com and create an app.<br>
   -  Get consumer key and consumer secret from you app's home page.<br>
   -  Enter https://127.0.0.1:8000/twitter/logged_in/ and https://127.0.0.1:8000/twitter/logged_in as callback in your app's home page. <br>
   -  Enter your key and secret in twitter_posting.views.<br>
   -  For running django server locally go to cmd and type:<br>
          ``` python manage.py runsslserver https://127.0.0.1:8000<br>```
   -  For celery open another cmd window and cd into social_media_posting and run:<br>
          ```
          celery -A social_media_posting worker --pool=eventlet -l info<br>
          ```<br>
   - **MAKE SURE RUN BOTH THESE COMMANDS PARALLELLY**<br>
      
