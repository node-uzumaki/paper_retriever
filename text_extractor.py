from lxml import etree

doc = etree.parse('./test.xml')

print(doc.nsmap)

# print(doc.xpath('//full-text-retrieval-response/originalText/xocs:doc/xocs:serial-item/article/body/ce:sections/ce:section/ce:para[2]'))