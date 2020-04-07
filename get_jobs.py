from sys import argv
import requests
import pandas as pd
import re
import webbrowser
import json

from companies import Company
from data_filtering import *


def open_urls(df, column):
    for url in df[column].values:
        webbrowser.open_new_tab(url)


def main(company_name, format):
    """
    TODO: i should look into creating a pipeline to make it easier to read
    """
    company = Company(company_name)
    company_listings = company.get_all_listings()

    filtered = filter_jobs(company_listings, 'text')
    unnested = unnest_categories(filtered, 'categories')
    excluded = exclude_departments(unnested)
    if format == 'csv':
        excluded.to_csv(f'~/Desktop/{company_name}_jobs.csv', index=False)
    if format == 'pretty':
        # if im being lazy and just want to look at a pretty page instead
        open_urls(excluded, 'hostedUrl')


if __name__ == '__main__':
    company_name = argv[1]
    format = argv[2]
    main(company_name, format)
