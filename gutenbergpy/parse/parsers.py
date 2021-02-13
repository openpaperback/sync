
from typing import List
from gutenbergpy.gutenbergcachesettings import GutenbergCacheSettings


def parse_title(doc) -> List[str]:
    xpath = [
        '//dcterms:title/text()',
        '//dcterms:alternative/text()'
    ]

    for xpth in xpath:
        result = doc.xpath(xpth, namespaces=GutenbergCacheSettings.NS)
        if result:
            if isinstance(result, list):
                return result[0]
            else:
                return result

    return ''


def parse_type(doc) -> str:
    xpth = '//dcterms:type/rdf:Description/rdf:value/text()'
    return doc.xpath(xpth, namespaces=GutenbergCacheSettings.NS)[0]


def parse_languages(doc) -> List[str]:
    xpth = '//dcterms:language/rdf:Description/rdf:value/text()'
    return doc.xpath(xpth, namespaces=GutenbergCacheSettings.NS)


def parse_author(doc):
    xpth = [
        '//dcterms:creator/pgterms:agent/pgterms:alias/text()',
        '//dcterms:creator/pgterms:agent/pgterms:name/text()'
    ]

    for xpth in xpth:
        result = doc.xpath(xpth, namespaces=GutenbergCacheSettings.NS)
        if result:
            return result[0]


def parse_formats(doc):
    xpth = '//dcterms:hasFormat'
    book_files = doc.xpath(xpth, namespaces=GutenbergCacheSettings.NS)
    result = []
    for bk in book_files:
        xpath_results_type = bk.xpath('.//dcterms:format/rdf:Description/rdf:value/text()', namespaces=GutenbergCacheSettings.NS)
        xpath_results_link = bk.xpath('.//pgterms:file/@rdf:about', namespaces=GutenbergCacheSettings.NS)

        if xpath_results_link and xpath_results_type:
            result.append({
                'fileType': xpath_results_type[0],
                'fileLink': xpath_results_link[0],
            })

    return result


def parse_publisher(doc) -> str:
    xpath = '//dcterms:publisher/text()'
    return doc.xpath(xpath, namespaces=GutenbergCacheSettings.NS)[0]


def parse_rights(doc) -> str:
    xpath = '//dcterms:rights/text()'
    return doc.xpath(xpath, namespaces=GutenbergCacheSettings.NS)[0]


def parse_date_issued(doc) -> str:
    date_issued_x = doc.xpath('//dcterms:issued/text()', namespaces=GutenbergCacheSettings.NS)
    date_issued = '1000-10-10' if not date_issued_x or date_issued_x[0] == 'None' else str(date_issued_x[0])
    return date_issued


def parse_downloads(doc) -> int:
    num_downloads_x = doc.xpath('//pgterms:downloads/text()', namespaces=GutenbergCacheSettings.NS)
    num_downloads = -1 if not num_downloads_x else int(num_downloads_x[0])
    return num_downloads


def parse_subjects(doc) -> List[str]:
    xpath = '//dcterms:subject/rdf:Description/rdf:value/text()'
    return doc.xpath(xpath, namespaces=GutenbergCacheSettings.NS)


def parse_bookshelves(doc) -> List[str]:
    xpath = '//pgterms:bookshelf/rdf:Description/rdf:value/text()'
    return doc.xpath(xpath, namespaces=GutenbergCacheSettings.NS)
