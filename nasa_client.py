import requests


class NasaClient:

    def __init__(self, api_key: str):
        self.base_url = "https://api.nasa.gov/planetary/apod"
        self.api_key = api_key

    def get_apod(self, date: str = None):
        params = {"api_key": self.api_key}
        if date:
            params["date"] = date
        response = requests.get(self.base_url, params=params)
        response.raise_for_status()
        return response.json()
