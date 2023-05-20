import subprocess

def get_certificate_expiry_days(hostname, port):
  """
  This function returns the number of days before the certificate expires for the given hostname and port.

  Args:
    hostname: The hostname of the server.
    port: The port of the server.

  Returns:
    The number of days before the certificate expires.
  """

  command = ['openssl', 's_client', '-connect', hostname + ':' + port]
  output = subprocess.check_output(command)

  for line in output.decode('utf-8').splitlines():
    if 'Not After' in line:
      expiry_date = line.split()[1]
      break

  expiry_date = expiry_date.replace(',', '')
  expiry_date = expiry_date.replace(' ', '')

  expiry_date_time = datetime.datetime.strptime(expiry_date, '%Y%m%d%H%M%SZ')
  now = datetime.datetime.now()

  days_until_expiry = (expiry_date_time - now).days

  return days_until_expiry
