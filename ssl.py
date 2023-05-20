import requests
import ssl

def get_ssl_cert_expiry_date(endpoint):
    http = urllib3.PoolManager()
    response = http.request('GET', 'https://{}'.format(endpoint))
    if response.status_code == 200:
        cert = response.headers['content-type'].split(';')[1].split('/')[1]
        expiry_date = '{}-{}-{}'.format(cert[0:4], cert[5:7], cert[8:10])
        return expiry_date
    else:
        return None

def monitor_ssl_expiry(endpoints):
    for endpoint in endpoints:
        expiry_date = get_ssl_cert_expiry_date(endpoint)
        if expiry_date is not None:
            print('The SSL cert for {} expires on {}'.format(endpoint, expiry_date))
        else:
            print('The SSL cert for {} is not valid'.format(endpoint))

if __name__ == '__main__':
    endpoints = ['www.google.com', 'www.facebook.com', 'www.yahoo.com']
    monitor_ssl_expiry(endpoints)
