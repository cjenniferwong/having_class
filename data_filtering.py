import re
import pandas as pd


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
            excluded_departments) & ~df['team'].isin(excluded_departments)]
        return excluded
    except Exception as e:
        print(e)
    # return excluded
