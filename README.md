# PyAnonWebBot

`PyAnonWebBot` helps to send or retrieve basic Web data using `POST` or `GET` methods.

User agent is randomized with the help of [`random_user_agent`](https://github.com/Luqman-Ud-Din/random_user_agent).

Tor can also be used to modify your IP.

[`Beautifulsoup4`](https://www.crummy.com/software/BeautifulSoup/) is used for parsing web pages (scraping) and the awesome [`requests`](https://github.com/psf/requests) library is used to handle requests with the web servers.

## I will take no responsibility !!! It is for educational purposes only

Moreover, it is a side project. My time is limited and valuable. Do not hesitate to make issue, then fork and ask for PR.

## Install

```bash
git clone https://github.com/rkt231/PyAnonWebBot.git
cd PyAnonWebBot
python3 -m pip install -r requirements.txt
```

Then to use tor:

```bash
# ubuntu / debian
apt install tor

# uncommenting some lines
sed -i "s/#CookieAuthentication/CookieAuthentication/" /etc/tor/torrc
sed -i "s/#ControlPort/ControlPort/" /etc/tor/torrc
# then setup a tor password
tor --hash-password mypassword > /tmp/hash
sed -ri "s/#HashedControlPassword .+$/HashedControlPassword `cat /tmp/hash`/g" /etc/tor/torrc

service tor restart
```

## Usage

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
./AnonWebBot.py --url https://ident.me -ws tor

# adding a dynamic IP and random sleep before request (between 3 and 5 seconds)
./AnonWebBot.py --url https://ident.me -ws -sc "." -m 3 -M 5 tor -td -tp mypassword
```

### checking headers

```bash
# using `-sc "."` to match any content
for i in {0..3}; do ./AnonWebBot.py -u https://httpbin.org/headers -m 1 -M 3 -sc "."; done
```

Otherwise you can set your custom headers with `-H` option.

## Sending data

`POST` data is still a bit complicated. However, on basic forms (without captcha), this could work.

```bash
# getting details about a form and inspect it
# to check where the action send data, the input values to send, etc. 
./AnonWebBot.py -u https://httpbin.org/forms/post -mt get -se_t form
# send data using this form
./AnonWebBot.py -u https://httpbin.org/post -mt post -v '{"custname": "JohnDoe", "custel": "00-00-000", "custemail": "john.doe@domain.tld", "size": "large", "topping": "cheese", "delivery":"19:45"}' -sc "." tor -td -tp mypassword
```
