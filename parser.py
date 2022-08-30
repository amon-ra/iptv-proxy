from http import HTTPStatus
import os
import re
import requests
from urllib.parse import urlparse

class Parser:
    def is_url(self, url):
        url_parsed = urlparse(url)
        return url_parsed.scheme in ('http', 'https')

    def parse_m3u(self, m3u_location: str, host: str, port: int, output_path: str):
        content = str()

        if self.is_url(m3u_location):
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
            response = requests.get(m3u_location, headers=headers)

            if response.status_code != HTTPStatus.OK:
                raise Exception(response.text)

            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            content = response.text
        else:
            with open(m3u_location, 'r') as input:
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                content = input.read()

        with open(output_path, 'w') as output:
            port_str = f':{str(port)}' if port != 0 else ''
            
            content = re.sub(r'(EXTM3U.*url-tvg=")(http)', rf'\1http://{host}{port_str}/proxy/data/\2', content, flags=re.M)
            content = re.sub(r'(EXTINF.*tvg-logo=")(http)', rf'\1http://{host}{port_str}/proxy/data/\2', content, flags=re.M)
            content = re.sub(r'^(http)', rf'http://{host}{port_str}/proxy/stream/\1', content, flags=re.M)
            output.write(content)
