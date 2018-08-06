A Python command line tool that scrapes data from Amazon.


## Setup to run without Docker

Copy `credentials.sample.py` to `credentials.py` and specify your Amazon credentials.

Setup requirements with

`pip install -r requirements.txt`

ChromeDriver needs to be installed from <https://sites.google.com/a/chromium.org/chromedriver/>.


## Run

Run with `python main.py`.

It asks for search string and may ask for verification code wich is sent in email.

See configuration parameters in `main.py` that may be useful for testing.
