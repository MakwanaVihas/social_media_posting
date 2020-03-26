*Clone the repo:*
  > git clone https://github.com/MakwanaVihas/social_media_posting.git
  > cd social_media_posting
  > pip install -r requirements.txt


**For twitter:**
      1.) Set up your twitter developer account on https://developers.twitter.com and create an app.
      2.) Get consumer key and consumer secret from you app's home page.
      3.) Enter https://127.0.0.1:8000/twitter/logged_in/ and https://127.0.0.1:8000/twitter/logged_in as callback in your app's home page. 
      4.) Enter your key and secret in twitter_posting.views.
      5.) For running django server locally go to cmd and type:
          > python manage.py runsslserver https://127.0.0.1:8000
      
