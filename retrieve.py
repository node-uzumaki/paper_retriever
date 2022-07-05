
import requests
import json
import pandas as pd
import httpx
from xml.etree import ElementTree

# retrieve using scopus
base_url = "https://api.elsevier.com/content/search/scopus"
apiKey = "45c6063a93408d8c4f3925dcf8e02e01"
headers = {
    'X-ELS-APIKey': '45c6063a93408d8c4f3925dcf8e02e01',
    'Accept': 'application/json'
}
title = []
url = []

headers_xml = {
    'X-ELS-APIKey': '45c6063a93408d8c4f3925dcf8e02e01',
    'Accept': 'application/xml'
}


def get_xml(paper_doi: str):
    response = requests.get(
        f'https://api.elsevier.com/content/article/doi/' + paper_doi, headers=headers_xml
    )
    # print(response)
    if response.status_code != 404:
        root = ElementTree.fromstring(response.content)
        tree = ElementTree.ElementTree(root)
        file_name = '-'.join(paper_doi.split('/'))
        tree.write(f'./XML/{file_name}.xml')
    else:
        with open('./OC_404_doi.txt', 'a') as f:
            print(paper_doi,file=f,flush=False)
        return None            


def get_doi(query, entry,j,start):  
    
    count = 200
    response = requests.get(
        f'https://api.elsevier.com/content/search/scopus?query={query}&start={start}&count={count}',
        headers=headers
    )
    response_json = response.json()
    try:
        doi = response_json['search-results']['entry'][entry]['prism:doi']
    except:
        with open('./OC_404_doi.txt', 'a') as f:
            print(entry,file=f,flush=False)
        return None    

    # print(response_json)
    print(doi)
    return doi


def scopus_paper_date(paper_doi, apiKey=apiKey):
    timeout = httpx.Timeout(10.0, connect=60.0)
    client = httpx.Client(timeout=timeout, headers=headers)
    _query = "&view=FULL"
    _url = f"https://api.elsevier.com/content/article/doi/" + paper_doi
    r = client.get(_url)
    # print(r)
    if r.status_code == 404:
        with open('404_doi.txt', 'w') as f:
            print()
    return r

iter = 0   

def get_doi_csv(file_path):
    df = pd.read_csv("./scopus.csv",usecols=['Title','DOI'])
    return df 


# for j in range (0,100):
#     start = 200 * j 
   
#     for i in range(0, 200):
        
#         query = 'ALL("operational control" AND "thermal comfort" AND ("human" OR "building" OR "occupant"))'
#         paper_doi = get_doi_csv(query, i,j,start)
#         # y = scopus_paper_date(paper_doi)
#         if paper_doi:
#             get_xml(paper_doi)
#         iter += 1
#         print(iter)
#         # if y:
#         #     json_acceptable_string = y.text
#         #     d = json.loads(json_acceptable_string)
#         #     # print()
#         #     file_name = '-'.join(paper_doi.split('/'))
#         #     file_name = '-'.join(paper_doi.split('/'))
#         #     with open(f'./XML_Data/{file_name}.txt', 'w') as fp:
#         #         print(y, file=fp)

#         # else:
#         #     print('not able to retrieve')

#     # df = pd.DataFrame({'title':title,'url':url})
#     # df.to_csv('papers_info')

paper_dois = get_doi_csv('./scopus')

for doi in paper_dois["DOI"]:
    get_xml(str(doi))
    print(doi)