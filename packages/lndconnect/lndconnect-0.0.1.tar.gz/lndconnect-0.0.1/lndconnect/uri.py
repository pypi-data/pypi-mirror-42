import base64
import os
import urllib.parse

def create(host, tls_path, macaroon_path):
	query_parameters = {}

	# cert
	tls_path = os.path.expanduser(tls_path)
	lines = [line.rstrip('\n') for line in open(tls_path)][1:-1]
	tls = ''.join(lines)

	tls_data = base64.b64decode(tls)
	cert = base64.urlsafe_b64encode(tls_data).decode('utf8').rstrip("=")

	query_parameters['cert'] = cert

	# macaroon
	macaroon_path = os.path.expanduser(macaroon_path)
	with open(macaroon_path, mode='rb') as file:
	    macaroon_data = file.read()
	macaroon = base64.urlsafe_b64encode(macaroon_data).decode('utf8').rstrip("=")

	query_parameters['macaroon'] = macaroon

	# build url
	query_string = urllib.parse.urlencode(query_parameters)
	url = urllib.parse.urlunparse(('lndconnect', host, '', None, query_string, None))

	return url

# create pem certificate from der certificate
def pem(der):
	lines = [der[i: i + 64].decode("utf-8") for i in range(0, len(der), 64)]
	cert = "\n".join(lines)
	return f"-----BEGIN CERTIFICATE-----\n{cert}\n-----END CERTIFICATE-----\n"

def pad_b64url(b64url):
	if len(b64url) % 4 != 0:
		b64url += "=" * (4 - (len(b64url) % 4))
	return b64url

def b64url_to_b64(string):
	string = pad_b64url(string)
	raw = base64.urlsafe_b64decode(string)
	return base64.b64encode(raw)

def parse(uri):
	parts = urllib.parse.urlparse(uri)

	if parts.scheme != 'lndconnect':
		print(f"wrong scheme: {parts.scheme}")
		return None

	host = parts.netloc
	query = urllib.parse.parse_qs(parts.query)
	cert = b64url_to_b64(query['cert'][0])
	pem_cert = pem(cert)
	macaroon = base64.urlsafe_b64decode(pad_b64url(query['macaroon'][0])).hex()
	
	return (host, pem_cert, macaroon)
