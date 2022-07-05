from typing import final
from lxml import etree
import re
doc = etree.parse('./test.xml')
query = "//e:full-text-retrieval-response/e:originalText/xocs:doc/xocs:serial-item/ja:article/ja:body/ce:sections/"
root = doc.getroot()
ns = root.nsmap.copy()
ns["e"] = ns.pop(None)


sections = root.xpath(query + f"ce:section/ce:section-title/text()", namespaces=ns)
# print(''.join(root.xpath(query + f"ce:section[2]/string()", namespaces=ns)))


def path_extract(file_parser):
    paths = []
    pattern = re.compile(r"ce:section[[0-9]{2}]$")
    for e in file_parser.iter():
        path = file_parser.getpath(e)
        path_ = re.search(pattern, path)
        if path_:
            final_path = path.split('/*/*[4]/ce:sections/')[1]
            if path_.group() == 'ce:section[1]':
                paths.append(final_path[::-1].replace("ce:section[1]"[::-1],"ce:section"[::-1], 1)[::-1])
            
            paths.append(final_path)
    return paths




with open("test.txt",'w', encoding="utf-8") as fp:
    paths = path_extract(doc)
    paths.pop(0)
    for path in paths:
        para_query  = query +path + f"/ce:para/text()"
        print(para_query)
        print(''.join(root.xpath(para_query, namespaces=ns)),file=fp,end='\n')