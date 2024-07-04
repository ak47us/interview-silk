import aiohttp
import os
import unittest
from typing import List
from urllib import parse


class SilkClient:
    """
    Use this client to access Silk's interview data sources.
    :param silk_api_token: str
    """
    def __init__(self, silk_api_token: str):
        self.base_url       = 'https://api.recruiting.app.silk.security'
        self.silk_api_token = silk_api_token
        self.session        = None
        self.http_limit     = 1  # Set this to one because the API has a hard limit of 7 hosts. Otherwise, we can set it to limit=2

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        if self.session:
            await self.session.close()

    async def get(self, url: str) -> List:
        """
        Perform an HTTP get operation against the Silk Interview API.
        Uses pagination.
        :param url:
        :return test:
        """
        all_data = list()
        skip     = 0
        try:
            # Loop through the API pages until we get a server error (which means it is the last page):
            while True:
                params  = {'limit': self.http_limit,
                           'skip':  skip}
                headers = {'accept': 'application/json',
                           'token': self.silk_api_token}
                async with self.session.post(headers = headers,
                                             url     = url,
                                             verify_ssl = False,
                                             params  = params) as response:
                    text = await response.text()  # Grab this so we can check the error code.
                    response.raise_for_status()
                    data = await response.json()
                    if not data:  # No more data returned
                        break
                    all_data.extend(data)
                    skip += self.http_limit  # Increment skip to fetch the next page
        except aiohttp.ClientResponseError as e:
            print(f"HTTP error: {e.status} - {e.message} - {text} - {url}?{parse.urlencode(params)}")
            if text == 'Error invalid skip/limit combo (>number of hosts)':
                return all_data
            else:
                return list([None])
        except ValueError as e:
            print(f"Error parsing JSON: {e}")
            return list([None])
        # except Exception as e:
        #     print(f"Error: {e} - {text} - {url}?{parse.urlencode(params)}")
        #     exit(1)

        return all_data

    async def get_crowdstrike_data(self) -> List:
        """Use the Silk API to get scans from Crowdstrike."""
        url     = f"{self.base_url}/api/crowdstrike/hosts/get"
        results = await self.get(url)
        return results

    async def get_qualys_data(self) -> List:
        """Use the Silk API to get scans from Qualys."""
        url     = f"{self.base_url}/api/qualys/hosts/get"
        results = await self.get(url)
        return results

    async def get_tenable_data(self, ) -> List:
        """
        Perform an HTTP get operation against the Silk Interview API for Tenable hosts.
        Uses pagination.
        :return list:
        """
        url = f"{self.base_url}/api/tenable/hosts/get"
        all_data = list()
        cursor     = ""
        try:
            # Loop through the API pages until we get a server error (which means it is the last page):
            while True:
                params  = {'limit': self.http_limit,
                           'cursor':  cursor}
                headers = {'accept': 'application/json',
                           'token': self.silk_api_token}
                async with self.session.post(headers = headers,
                                             url     = url,
                                             ssl = False,
                                             params  = params) as response:
                    text = await response.text()  # Grab this so we can check the error code.
                    response.raise_for_status()
                    data = await response.json()
                    if len(data['hosts']) == 0:  # No more data returned
                        break
                    all_data.extend(data['hosts'])
                    cursor = data['cursor']
        except Exception as e:
            print(f"Exception: {e}")

        return all_data


class SilkClientTests(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        if (silk_api_token := os.getenv('silk_api_token')) is None:  # Attempt to get environment variable
            print(f"Environment variable silk_api_token is not set.")
            self.fail('API token error')
        self.silk_client = SilkClient(silk_api_token=silk_api_token)

    async def asyncTearDown(self):
        if self.silk_client.session:
            await self.silk_client.session.close()

    async def test_get_crowdstrike_data_success(self):
        async with self.silk_client:
            crowdstrike_response = await self.silk_client.get_crowdstrike_data()
            print(f"Retrieved {len(crowdstrike_response)} hosts.")
            self.assertIsInstance(crowdstrike_response, list, 'Retrieved a list of hosts from Crowdstrike.')

    async def test_get_qualys_data_success(self):
        async with self.silk_client:
            qualys_response = await self.silk_client.get_qualys_data()
            print(f"Retrieved {len(qualys_response)} hosts.")
            self.assertIsInstance(qualys_response, list, 'Retrieved a list of hosts from Qualys.')

    async def test_get_tenable_data_success(self):
        async with self.silk_client:
            tenable_response = await self.silk_client.get_tenable_data()
            print(f"Retrieved {len(tenable_response)} hosts.")
            self.assertIsInstance(tenable_response, list, 'Retrieved a list of hosts from Qualys.')


if __name__ == '__main__':
    unittest.main()
