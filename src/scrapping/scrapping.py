import requests
from bs4 import BeautifulSoup
from io import StringIO
import pandas as pd
import numpy as np


class Scrapper:
    def __init__(self):
        pass

class DirectScrapper(Scrapper):
    def __init__(self):
        super().__init__()

    def get_data(self,url,encoding,sep):
        download_response = requests.get(url)

        if download_response.status_code == 200:
            csv_data = download_response.content.decode(encoding)
            df = pd.read_csv(StringIO(csv_data),sep=sep)
            df = df.replace([np.inf, -np.inf], np.nan)
            df = df.fillna('NaN')

            return df.to_dict(orient='records')
        else: 
            print("Fail to download data")