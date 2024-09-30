import urllib
import argparse
import requests

import google.auth.transport.requests
import google.oauth2.id_token

METADATA_URL = "http://metadata.google.internal/computeMetadata/v1/"
METADATA_HEADERS = {"Metadata-Flavor": "Google"}
SERVICE_ACCOUNT = "default"


def make_authorized_get_request():
    """
    make_authorized_get_request makes a GET request to the specified HTTP endpoint
    by authenticating with the ID token obtained from the google-auth client library
    using the specified audience value.
    """

    # Cloud Functions uses your function's URL as the `audience` value
    # audience = https://project-region-projectid.cloudfunctions.net/myFunction
    audience = "https://us-central1-feedmapping.cloudfunctions.net/function"

    # For Cloud Functions, `endpoint` and `audience` should be equal
    # Ref: https://cloud.google.com/functions/docs/securing/authenticating
    endpoint = audience
    req = urllib.request.Request(endpoint)

    auth_req = google.auth.transport.requests.Request()
    id_token = google.oauth2.id_token.fetch_id_token(auth_req, audience)

    req.add_header("Authorization", f"Bearer {id_token}")
    response = urllib.request.urlopen(req)

    return response.read()
    

def get_access_token() -> str:
    """
    Retrieves access token from the metadata server.

    Returns:
        The access token.
    """
    url = f"{METADATA_URL}instance/service-accounts/{SERVICE_ACCOUNT}/token"

    # Request an access token from the metadata server.
    # Ref: https://cloud.google.com/compute/docs/access/authenticate-workloads#applications
    r = requests.get(url, headers=METADATA_HEADERS)
    r.raise_for_status()

    # Extract the access token from the response.
    access_token = r.json()["access_token"]

    return access_token


def list_buckets(project_id: str, access_token: str) -> dict:
    """
    Calls Storage API to retrieve a list of buckets.

    Args:
        project_id: name of the project to list buckets from.
        access_token: access token to authenticate with.

    Returns:
        Response from the API.
    """
    url = "https://www.googleapis.com/storage/v1/b"
    params = {"project": project_id}
    headers = {"Authorization": f"Bearer {access_token}"}

    r = requests.get(url, params=params, headers=headers)
    r.raise_for_status()

    return r.json()


def main(project_id: str) -> None:
    """
    Retrieves access token from metadata server and uses it to list
    buckets in a project.

    Args:
        project_id: name of the project to list buckets from.
    """
    #access_token = get_access_token()
    access_token = make_authorized_get_request()
    #buckets = list_buckets(project_id, access_token)
    #print(buckets)
    return access_token


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("project_id", help="Your Google Cloud project ID.")

    args = parser.parse_args()

    main(args.project_id)
