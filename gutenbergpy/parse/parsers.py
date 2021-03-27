from typing import List, Union
from gutenbergpy.settings import settings


NS = {
    'cc': "http://web.resource.org/cc/",
    'dcam': "http://purl.org/dc/dcam/",
    'dcterms': "http://purl.org/dc/terms/",
    'rdfs': "http://www.w3.org/2000/01/rdf-schema#",
    'rdf': "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    'pgterms': "http://www.gutenberg.org/2009/pgterms/"
}


def parse_title(doc) -> List[str]:
    xpath = [
        '//dcterms:title/text()',
        '//dcterms:alternative/text()'
    ]

    for xpth in xpath:
        result = doc.xpath(xpth, namespaces=NS)
        if result:
            if isinstance(result, list):
                return result[0]
            else:
                return result

    return []


def parse_type(doc) -> str:
    xpth = '//dcterms:type/rdf:Description/rdf:value/text()'
    return doc.xpath(xpth, namespaces=NS)[0]


def parse_languages(doc) -> List[str]:
    xpth = '//dcterms:language/rdf:Description/rdf:value/text()'
    return doc.xpath(xpth, namespaces=NS)


def parse_author_id(doc) -> Union[int, None]:
    try:
        xpath = '//dcterms:creator/pgterms:agent/@rdf:about'
        result: List[str] = doc.xpath(xpath, namespaces=NS)
        id = result[0].split('/').pop()
        return int(id)
    except Exception:
        return None


def parse_author(doc) -> List[str]:
    xpaths = [
        '//dcterms:creator/pgterms:agent/pgterms:alias/text()',
        '//dcterms:creator/pgterms:agent/pgterms:name/text()'
    ]

    author_aliases = set()

    for item in xpaths:
        result: List[str] = doc.xpath(item, namespaces=NS)
        [author_aliases.add(a) for a in result]

    return list(author_aliases)


def parse_formats(doc):
    xpth = '//dcterms:hasFormat'
    book_files = doc.xpath(xpth, namespaces=NS)
    result = []
    for bk in book_files:
        xpath_results_type = bk.xpath('.//dcterms:format/rdf:Description/rdf:value/text()', namespaces=NS)
        xpath_results_link = bk.xpath('.//pgterms:file/@rdf:about', namespaces=NS)

        if xpath_results_link and xpath_results_type:
            result.append({
                'fileType': xpath_results_type[0],
                'fileLink': xpath_results_link[0],
            })

    return result


def parse_publisher(doc) -> str:
    xpath = '//dcterms:publisher/text()'
    return doc.xpath(xpath, namespaces=NS)[0]


def parse_rights(doc) -> str:
    xpath = '//dcterms:rights/text()'
    return doc.xpath(xpath, namespaces=NS)[0]


def parse_date_issued(doc) -> str:
    date_issued_x = doc.xpath('//dcterms:issued/text()', namespaces=NS)
    date_issued = '1000-10-10' if not date_issued_x or date_issued_x[0] == 'None' else str(date_issued_x[0])
    return date_issued


def parse_downloads(doc) -> int:
    num_downloads_x = doc.xpath('//pgterms:downloads/text()', namespaces=NS)
    num_downloads = -1 if not num_downloads_x else int(num_downloads_x[0])
    return num_downloads


def parse_subjects(doc) -> List[str]:
    xpath = '//dcterms:subject/rdf:Description/rdf:value/text()'
    return doc.xpath(xpath, namespaces=NS)


def parse_bookshelves(doc) -> List[str]:
    xpath = '//pgterms:bookshelf/rdf:Description/rdf:value/text()'
    return doc.xpath(xpath, namespaces=NS)
