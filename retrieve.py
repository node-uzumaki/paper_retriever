
import requests
import pandas as pd
import xml.etree.ElementTree as ET
from urllib.error import HTTPError
from text_extractor import text_extract
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

ns = {  
        'bk': 'http://www.elsevier.com/xml/bk/dtd', 
        'cals': 'http://www.elsevier.com/xml/common/cals/dtd', 
        'ce': 'http://www.elsevier.com/xml/common/dtd', 
        'ja': 'http://www.elsevier.com/xml/ja/dtd', 
        'mml': 'http://www.w3.org/1998/Math/MathML',
        'sa': 'http://www.elsevier.com/xml/common/struct-aff/dtd',
        'sb': 'http://www.elsevier.com/xml/common/struct-bib/dtd', 
        'tb': 'http://www.elsevier.com/xml/common/table/dtd', 
        'xlink': 'http://www.w3.org/1999/xlink', 'xocs': 'http://www.elsevier.com/xml/xocs/dtd', 
        'dc': 'http://purl.org/dc/elements/1.1/', 
        'dcterms': 'http://purl.org/dc/terms/', 
        'prism': 'http://prismstandard.org/namespaces/basic/2.0/', 
        'xsi': 'http://www.w3.org/2001/XMLSchema-instance', 
        'e': 'http://www.elsevier.com/xml/svapi/article/dtd'
    }


def get_xml(paper_doi,folder_name):
     
    url =  'https://api.elsevier.com/content/article/doi/' + paper_doi
    try:
        r = requests.get(url,headers=headers_xml)
        print(r.status_code)
        tree = tree = ET.ElementTree(ET.fromstring(r.text))
        print(tree.getroot().nsmap)
  
    except HTTPError as e:
        print(e)


# def get_doi(query, entry,j,start):  
    
#     count = 200
#     response = requests.get(
#         f'https://api.elsevier.com/content/search/scopus?query={query}&start={start}&count={count}',
#         headers=headers
#     )
#     response_json = response.json()
#     try:
#         doi = response_json['search-results']['entry'][entry]['prism:doi']
#     except:
#         with open('./OC_404_doi.txt', 'a') as f:
#             print(entry,file=f,flush=False)
#         return None    

#     # print(response_json)
#     print(doi)
#     return doi


def get_doi_csv(file_path):
    df = pd.read_csv("./scopus.csv",usecols=['Title','DOI'])
    return df 


def retrieve_from_scopus():
    for j in range (0,100):
        start = 200 * j 
        for i in range(0, 200):   
            query = 'ALL("operational control" AND "thermal comfort" AND ("human" OR "building" OR "occupant"))'
            paper_doi = get_doi_csv(query, i,j,start)
            # y = scopus_paper_date(paper_doi)
            if paper_doi:
                get_xml(paper_doi)
            iter += 1
            print(iter)


# def get_csv():


# def retrieve_from_csv(path):
#     paper_dois = get_doi_csv(path)
#     for doi in paper_dois["DOI"]:
#         get_text(str(doi))
#         print(doi)


get_xml("10.1016/j.scitotenv.2022.155128",'.')