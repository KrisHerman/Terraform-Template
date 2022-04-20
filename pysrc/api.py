import requests
import jwt
import datetime as dt

def access_secret_version(project_id, secret_id, version_id):
    """
    Access the payload for the given secret version if one exists. The version
    can be a version number as a string (e.g. "5") or an alias (e.g. "latest").
    """

    # Import the Secret Manager client library.
    from google.cloud import secretmanager

    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret version.
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

    # Access the secret version.
    response = client.access_secret_version(request={"name": name})

    # Verify payload checksum.
    #crc32c = google_crc32c.Checksum()
    #crc32c.update(response.payload.data)
    #if response.payload.data_crc32c != int(crc32c.hexdigest(), 16):
    #    print("Data corruption detected.")
    #    return response

    # Print the secret payload.
    #
    # WARNING: Do not print the secret in a production environment - this
    # snippet is showing how to access the secret material.
    payload = response.payload.data.decode("UTF-8")
    print("Plaintext: {}".format(payload))


def make_request():
    url = 'https://www.w3schools.com/python/demopage.php'
    myobj = {'somekey': 'somevalue'}
    x = requests.post(url, data = myobj)
    print(x.text)


class Apple_ads_authenticator(object):

    def __init__(self, client_id, team_id, key_id, key_file='private-key.pem'):
        self.client_id = client_id
        self.team_id = team_id
        self.key_id = key_id
        self.audience = 'https://appleid.apple.com'
        self.alg = 'ES256'
        self.client_secret_output_path = 'client_secret.txt'
        self.key_file = key_file

    def generate_client_secret_file(self):
        # Define issue timestamp.
        issued_at_timestamp = int(dt.datetime.utcnow().timestamp())
        # Define expiration timestamp. May not exceed 180 days from issue timestamp.
        expiration_timestamp = issued_at_timestamp + 86400*180 

        # Define JWT headers.
        headers = dict()
        headers['alg'] = alg
        headers['kid'] = key_id
        
        # Define JWT payload.
        payload = dict()
        payload['sub'] = client_id
        payload['aud'] = audience
        payload['iat'] = issued_at_timestamp
        payload['exp'] = expiration_timestamp
        payload['iss'] = team_id 
        
        
        with open(self.key_file,'r') as key_file:
            key = ''.join(key_file.readlines())
        
        client_secret = jwt.encode(
            payload=payload,  
            headers=headers,
            algorithm=self.alg,
            key=key
        )
        
        with open(self.client_secret_output_path, 'w') as output:
            output.write(client_secret.decode("utf-8"))