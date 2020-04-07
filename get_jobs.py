from sys import argv
import requests
import pandas as pd
import re
import webbrowser
import json


def get_settings(company_name):
    with open('company_params.json') as f:
        company_params = json.load(f)
        f.close()
    return company_params[company_name]


def get_all_listings(settings):
    api_url = settings['api_url']
    params = settings['params']
    headers = settings['headers']
    # print(params, headers)

    r = requests.get(api_url, params=params, headers=headers)
    data = r.json()
    jobs_df = pd.DataFrame(data)
    print(f'grabbed {len(jobs_df)} jobs')
    return jobs_df


def _get_signals(element,
                 regex_string='(?!data\sengineer)data\s|scien*|analy*|machine\slearning'
                 ):
    '''
    TODO: modify the regex string to exclude data engineering, infra, and product management

    '''
    return bool(re.search(regex_string, element,  flags=re.IGNORECASE))


def filter_jobs(df, column):
    '''
    TODO: if there are no jobs remaining after filter, pass empty df

    '''
    df['signal'] = df[column].apply(_get_signals)
    filtered = df[df['signal'] == True]
    print(f'{len(filtered)} remaining jobs')
    return filtered.drop(['signal'], axis=1)


def unnest_categories(df, column):
    unnested = pd.merge(df, df[column].apply(
        pd.Series), left_index=True, right_index=True)
    dropped = unnested.drop(column, axis=1)
    return dropped


def exclude_departments(df):
    excluded_departments = ['Accounting', 'Legal', 'Internal Audit',
                            'Finance', 'Financial Engineering and Fraud']

    try:
        excluded = df[~df['team'].isin(
            excluded_departments) & ~df['dept'].isin(excluded_departments)]
        return excluded
    except Exception as e:
        print(e)
    # return excluded


def open_urls(df, column):
    for url in df[column].head():
        webbrowser.open_new_tab(url)


def main(company_name, format):
    """
    TODO: i should look into creating a pipeline to make it easier to read
    """
    settings = get_settings(company_name)
    spotify_listings = get_all_listings(settings)
    filtered = filter_jobs(spotify_listings, 'text')
    unnested = unnest_categories(filtered, 'categories')
    excluded = exclude_departments(unnested)
    if format == 'csv':
        excluded.to_csv('~/Desktop/spotify_jobs.csv', index=False)
    if format == 'pretty':

        # if im being lazy and just want to look at a pretty page instead
        open_urls(excluded, 'hostedUrl')


if __name__ == '__main__':
    company_name = argv[1]
    format = argv[2]
    main(company_name, format)
