#!/usr/bin/env python3
# Download and verify all raw data from
# https://election-results.eu/tools/download-datasheets/
import os
from urllib import request
import crypto


# list of all resources
resources = [
    "https://election-results.eu/data-sheets/csv/turnout/turnout-eu.csv",
    "https://election-results.eu/data-sheets/csv/turnout/turnout-country.csv",
    "https://election-results.eu/data-sheets/csv/labels.csv",
    "https://election-results.eu/data-sheets/csv/2019-2024/election-results/groups.csv",
    "https://election-results.eu/data-sheets/csv/2019-2024/election-results/parties.csv",
    "https://election-results.eu/data-sheets/csv/2019-2024/election-results/results-parties/results-parties-de.csv"
]

# constants
download_dir = 'data/'

# helper functions
def signature_url(resource_url):
    parts = resource_url.rsplit('.', 1)
    parts[1] = 'sig'
    return '.'.join(parts)

def filename(resource_url):
    return resource_url.rsplit('/', 1)[1]

def download_file(resource_url):
    return download_dir + filename(resource_url)

def create_download_dir():
    if not os.path.exists(download_dir):
        os.mkdir(download_dir)

def has_cache(resource_url):
    return os.path.exists(download_file(resource_url))

def download(resource_url):
    if has_cache(resource_url):
        return
    
    sig_url = signature_url(resource_url)
    sig_download_path = download_file(sig_url)
    download_path = download_file(resource_url)
    
    # download both files
    request.urlretrieve(resource_url, download_path)
    request.urlretrieve(sig_url, sig_download_path)
    
    # verify signature
    if not crypto.verify_file_sig(download_path, sig_download_path):
        raise Exception('Signature could not be validated for {}'.format(resource_url))
            
def download_all():
    for path in resources:
        print('Downloading {}'.format(path))
        try:
            download(path)
            print('Successfully downloaded {}'.format(path))
        except Exception as err:
            print('Download failed.\nReason: {}'.format(err))
            
        
# exec
if __name__ == "__main__":
    create_download_dir()
    download_all() 