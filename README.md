A Python command line tool that scrapes data from Amazon.


## With Docker

### Setup

Copy `credentials.sample.py` to `credentials.py` and specify your Amazon credentials there.

```
sudo docker build -t crawl-amazon .
```

### Run

```
sudo docker run -ti crawl-amazon
```

It asks for search string and may ask for verification code wich is sent in email that Amazon requires for login.


## Locally

### Setup

Copy `credentials.sample.py` to `credentials.py` and specify your Amazon credentials there.

Setup requirements with

`pip install -r requirements.txt`

ChromeDriver needs to be installed from <https://sites.google.com/a/chromium.org/chromedriver/>.

### Run

Run with `python main.py`.

It asks for search string and may ask for verification code wich is sent in email.

See configuration parameters in `main.py` that may be useful for testing and debugging.
