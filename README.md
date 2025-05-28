# HULK - HTTP Unbearable Load King (Proxy Version)

**Disclaimer: This tool is for educational and authorized testing purposes only. Do not use it on networks or systems without explicit permission.**

## 🚨 Description
This is a modified version of the HULK DoS (Denial of Service) tool which uses **proxy rotation** to send massive HTTP requests to a target URL, aiming to overload the server.

## ⚙️ Features
- Rotates multiple proxies from `proxy.txt`
- Randomized headers: User-Agent, Referer, X-Forwarded, etc.
- Auto-stop on HTTP 500 errors (`safe` mode)
- Random IPs and payloads for obfuscation

## 🧠 Usage
```bash
python3 hulk.py <url> [safe]
```
- `<url>`: Target URL (e.g., `http://example.com`)
- `safe`: Optional keyword to stop attack on 500 error

**Example:**
```bash
python3 hulk.py http://example.com safe
```

## 📄 proxy.txt Format
Ensure `proxy.txt` exists in the same directory:

```
123.45.67.89:8080
98.76.54.32:3128
...
```

## 📁 Requirements
- Python 3.x
- Valid proxy list in `proxy.txt`

## ⚠️ Legal Warning
Use only on systems you have **explicit permission** to test. Unauthorized use is **illegal** and unethical. The author is **not responsible** for misuse.
