# youtube_sniff_logger.py
from mitmproxy import http

# Change this to your preferred log file location
LOG_FILE = "mitmproxy_log.txt"

def write_log(message: str) -> None:
    with open(LOG_FILE, "a") as log_file:
        log_file.write(message + "\n")

TARGET_URL = "https://run.steam-powered-games.com/fullstate/html5/evoplay/blackjack/?operator=6227"

def request(flow: http.HTTPFlow) -> None:
    # Filter only requests to youtube.com or its subdomains
    if flow.request.pretty_url == TARGET_URL:
        log_message = f"Request: {flow.request.method} {flow.request.url}"
        write_log(log_message)

def response(flow: http.HTTPFlow) -> None:
    if flow.request.pretty_url == TARGET_URL:
        log_message_1 = f"Response Status: {flow.response.status_code}"
        log_message_2 = f"Body: {flow.response.text[:500]}"
        write_log(log_message_1)
        write_log(log_message_2)