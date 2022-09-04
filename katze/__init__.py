from discatpy import Client

from .fake.http import FakeMixedHttpClient


def patch(client: Client):
    client.http = FakeMixedHttpClient(
        client.http.token, api_version=client.http._api_version
    )
