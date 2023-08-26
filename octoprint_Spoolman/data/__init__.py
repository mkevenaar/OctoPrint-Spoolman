# coding=utf-8

import requests

class Spoolman():

    def __init__(self, spoolman_url):
        self.spoolman_url = spoolman_url

    def get_all_spools(self, archived):
        endpoint = self.spoolman_url + '/api/v1/spool'
        response = requests.get(endpoint)
        return response.json()