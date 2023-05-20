import urllib3

def check_https(endpoint, port):
    http = urllib3.PoolManager()
    try:
        response = http.request('GET', 'https://{}:{}'.format(endpoint, port))
        if response.status_code == 200:
            return True
        else:
            return False
    except urllib3.exceptions.SSLError:
        return False

def get_ssl_cert_expiry_date(endpoint, port):
    http = urllib3.PoolManager()
    response = http.request('GET', 'https://{}:{}'.format(endpoint, port))
    if response.status_code == 200:
        cert = response.headers['content-type'].split(';')[1].split('/')[1]
        expiry_date = '{}-{}-{}'.format(cert[0:4], cert[5:7], cert[8:10])
        return expiry_date
    else:
        return None

if __name__ == '__main__':
    endpoint = 'www.google.com'
    port = 443

    is_https = check_https(endpoint, port)
    expiry_date = get_ssl_cert_expiry_date(endpoint, port)

    if is_https:
        print('The endpoint is HTTPS')
        print('The SSL cert expiry date is {}'.format(expiry_date))
    else:
        print('The endpoint is not HTTPS')
