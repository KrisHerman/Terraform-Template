import os
import pandas as pd


import jwt
import datetime as dt

from api import access_secret_version, make_request
from dt_utils import get_formatted_offset_date

######################################################

client_id = ''
team_id = '' 
key_id = '' 
audience = 'https://appleid.apple.com'
alg = 'ES256'

SECRET_FILE_PATH = ''
SEARCHADS_ORG_ID = ''
URL = "https://api.searchads.apple.com/api/v1/reports/campaigns"

project_id = 'dev-area-318003'
secret_id = 'sample_app_secret'
version_id = 'latest'

staging_bucket = 'sample_app_dev'

# So that we can pass a statics value and dynamically generate dates...
startTimeDaysBack  = os.environ.get('startTimeDaysBack', 1)
endTimeDaysForward = os.environ.get('endTimeDaysForward', 0)


######################################################


def main(request):
    output_file_name = 'sample_file.csv'
    output_object_path = f"gcs://{staging_bucket}/{output_file_name}"

    request_json = request.get_json()

    if request.args and 'message' in request.args:
        print('Inside first part of if')
        return request.args.get('message')
    elif request_json and 'message' in request_json:
        print('Inside elif')
        return request_json['message']
    else:
        print('Inside else')

        # Get date parameters
        starting_date = get_formatted_offset_date(startTimeDaysBack)
        ending_date = get_formatted_offset_date(endTimeDaysForward)
        print(f"Starting date {starting_date}")
        print(f"Ending date {ending_date}")

        # Access a secret
        fake_secret = access_secret_version(project_id, secret_id, version_id)
        print("fake secret: " + str(fake_secret))

        # creating sample data...
        df = pd.DataFrame({'numbers': [1, 2, 3], 'colors': ['red', 'white', 'blue']})

        # Write to bucket
        df.to_csv(output_object_path)

        # Read from bucket
        df2 = pd.read_csv(output_object_path)

        # Write to bq
        df2.to_gbq(
            destination_table='sample_app_dataset.sample_app_table',
            project_id=project_id,
            if_exists='replace',
            #location=job_location
        )

        return f'Hello World!'
