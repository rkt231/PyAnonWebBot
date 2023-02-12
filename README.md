# PyAnonWebBot

`PyAnonWebBot` helps to send or retrieve basic Web data using `POST` or `GET` methods.

User agent is randomized with the help of [`random_user_agent`](https://github.com/Luqman-Ud-Din/random_user_agent).

Tor can also be used to modify your IP.

[`Beautifulsoup4`](https://www.crummy.com/software/BeautifulSoup/) is used for parsing web pages (scraping) and the awesome [`requests`](https://github.com/psf/requests) library is used to handle requests with the web servers.

> I will take no responsibility !!! It is for educational purposes only

_Moreover, it is a side project. My time is limited and valuable. Do not hesitate to make issue, then fork and ask for PR._

## Install

```bash
git clone https://github.com/rkt231/PyAnonWebBot.git
cd PyAnonWebBot
```

### Requirements

You can either use `requirements.txt` with `pip` or `poetry`:


With `requirements.txt`:

```bash
python3 -m pip install -r requirements.txt
```

With [`poetry`](https://python-poetry.org/):

```bash
poetry install

# then will have to run each next command with 
# poetry run ./AnonWebBot.py [options]
```

### Tor

To use tor, obviously, you need to install and configure it:

```bash
# ubuntu / debian
sudo apt install -y tor
# fedora / centos
sudo dnf install -y tor

# uncommenting some lines
sudo sed -i "s/#CookieAuthentication/CookieAuthentication/" /etc/tor/torrc
sudo sed -i "s/#ControlPort/ControlPort/" /etc/tor/torrc
# then setup a tor password
tor --hash-password mypassword > /tmp/hash
sudo sed -ri "s/#HashedControlPassword .+$/HashedControlPassword `cat /tmp/hash`/g" /etc/tor/torrc

sudo service tor restart
```

## Basic usage with the requests python package

### Basic scraping usage with GET method

```bash
# get a WebPage text content
./AnonWebBot.py --url https://httpbin.org/ 
# same with a session initialized
./AnonWebBot.py --url https://httpbin.org/ -ws
# get the whole content of the page (filter with <html> tag)
./AnonWebBot.py -u https://en.wikipedia.org/wiki/Web_scraping -se_t html > /tmp/scraping.html
# retrieve only a form 
./AnonWebBot.py -u https://httpbin.org/forms/post -se_t form
# filter on an input tag and a its name
./AnonWebBot.py -u https://httpbin.org/forms/post -se_n topping -se_t input
# limiting number of results (2):
./AnonWebBot.py -u https://httpbin.org/forms/post -se_t input -se_n size -sl 2
# searching text content in page
./AnonWebBot.py -u https://httpbin.org/forms/post -sc Bacon
```

### Using tor

```bash
sudo service tor start

# checking ip without tor
./AnonWebBot.py --url https://ident.me 

# with tor and a session
./AnonWebBot.py --url https://ident.me -ws -ts

# adding a dynamic IP from tor and random sleep before request (between 3 and 5 seconds)
# replace "mypassword" with your tor password
./AnonWebBot.py --url https://ident.me -ws -sc "." -m 3 -M 5 -td -tp mypassword
```

### checking headers

```bash
# using `-sc "."` to match any content
for i in {0..3}; do ./AnonWebBot.py -u https://httpbin.org/headers -m 1 -M 3 -sc "."|grep User-Agent; done
```

Otherwise you can set your custom headers with `-H` option.

## Sending data

`POST` data is still a bit complicated. However, on basic forms (without captcha), this could work.

```bash
# getting details about a form and inspect it
# to check where the action send data, the input values to send, etc. 
./AnonWebBot.py -u https://httpbin.org/forms/post -mt get -se_t form
# send data using this form
./AnonWebBot.py -u https://httpbin.org/post -mt post -v '{"custname": "JohnDoe", "custel": "00-00-000", "custemail": "john.doe@domain.tld", "size": "large", "topping": "cheese", "delivery":"19:45"}' -sc "." -td -tp mypassword
```

## A more advanced usage with selenium in python

> For now, Selenium version of this tool is not yet able to change IP dynamically using Tor (only the static one given by your Tor service). Moreover, the headers are not yet able to be customized.

### Basic selenium usage

First of all, you have to use the `-SBE` option (meaning _Selenium Browser Engine_...), followed by the browser you need (these browsers are valid options: chrome, chromium and firefox).
You will need to download these browsers before using it with Selenium (or at least, the corresponding engine (gecko, chromedriver (webkit))).

Last geckodriver can be found [here](https://github.com/mozilla/geckodriver/releases/). Then, add the `geckodriver` to your `$PATH`, eg:

```bash
sudo cp geckodriver /usr/local/bin/
```

Chrome expects a symbolic link to be found at `/usr/bin/google-chrome`. You can find `chromedriver` [here](https://chromedriver.chromium.org/downloads). Normaly, it is easier to install `chrome` and `chromium` from standard repositories and avoid `snap` or `flatpak`. Please refer to the [official selenium page for this](https://www.selenium.dev/documentation/webdriver/getting_started/install_drivers/).


There are two way to use the Selenium package :

- enter arguments for each action directly in CLI,
- enter each action in a separate file, which is more readable, particularly if you have many actions.

To read a file containing a sequence of action, use `-SAF` (Selenium Actions File). Otherwise, you will need the `-SA` argument, followed by your list of actions.

You can find an example of action file in `_selenium/examples` directory. It is a json file, written as a list of actions.

#### Without a specific action file

```bash
./AnonWebBot.py -u https://duckduckgo.com -SBE chromium -SA '[[{"type": "find_element_by_name", "value": "q"}, {"type": "send_keys", "value": "test"}]]'
```

If you just want to visit a website and you do not know what is the DOM structure of the site, you can just wait:

```bash
./AnonWebBot.py -u https://ident.me -SBE chrome -SA '[[{"type": "wait", "value": "2"}]]' -td -tp mypassword
```

#### With an action file

```bash
# we will start the tor service before
sudo service tor start
./AnonWebBot.py -u https://duckduckgo.com -td -tp mypassword -SBE firefox -SAF _selenium/examples/test_ddg.json
```

