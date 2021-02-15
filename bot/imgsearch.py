import api
from saucenao_api.errors import *

from errors import *

saucenao = api.saucenao()

source_list = ['twitter', 'pixiv']


def imgSearch(imgURL: str) -> str:
    """
    Use SauceNao to get the source of the picture
    and  the source in string.
    :param imgURL: URL of the picture
    :return: URL of the source (pixiv or twitter). Else raise exception NoSourceFound.
    """
    try:
        imgSource = saucenao.from_url(imgURL)
        for result in imgSource.results:
            for url in result.urls:
                if any(url_source in url for url_source in source_list) and result.similarity > 87.00:
                    print(f"Source found: {url} - {result.similarity}%")
                    return url
                else:
                    raise NoSourceFound

    except UnknownServerError as e:
        print(e)

