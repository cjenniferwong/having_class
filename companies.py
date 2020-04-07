import json
import requests
import pandas as pd


class Company():
    def __init__(self, company_name):
        self.company = company_name

    # def _get_settings(self):
        with open('company_params.json') as f:
            comp_params = json.load(f)
            settings = comp_params[self.company]
            f.close()
        self.settings = settings

    def get_all_listings(self):
        api_url = self.settings['api_url']
        params = self.settings['params']
        headers = self.settings['headers']

        r = requests.get(api_url, params=params, headers=headers)
        data = r.json()
        jobs_df = pd.DataFrame(data)
        print(f'grabbed {len(jobs_df)} jobs')
        return jobs_df
