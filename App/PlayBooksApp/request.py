import requests
from urllib.parse import urlparse
import base64 

from .markdown import MarkdownParser

class URLRequester():
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux; rv:31.0) Gecko/20100101 Firefox'
    }

    ALLOWED_IMAGE_CONTENT_TYPES = [
        'image/jpeg',
        'image/png'
    ]

    def __init__(self, url):
        self.url = url
        self.verify = False ## Do not verify per default
        self.response = None
        self.status_code = None
    
    def request(self, url=None):
        response = self.request_url(url=url)
        self.status_code = response.status_code
        self.response = response.text
        return response

    def is_valid_response(self):
        if( self.get_status_code() == 200 ):
            return True
        else:
            return False

    def request_url(self, url=None):
        request_url = url or self.url
        response = requests.get(url=request_url, headers=self.HEADERS, verify=self.verify)
        return response

    def resolve_images(self):
        md_parser = MarkdownParser()
        content = md_parser.replaceImages(self.response, self.path_validation, self.path_processing)
        self.response = content
        
    def request_subpath(self, path):
        parsedUrl = urlparse(self.url)
        subPaths = [ subPath for subPath in urlparse(self.url).path.split('/') if subPath ]
        for subPath in subPaths:
            subPath += '/' if subPath.endswith('') else ''
            subPath += path
            rootPath = parsedUrl.netloc
            rootPath += '/' if rootPath.endswith('') else ''
            full_url = "%s://%s%s" %(parsedUrl.scheme, rootPath, subPath)
            response = self.request_url(url=full_url)
            if( response.status_code == 200 ):
                return response

    def path_validation(self, path):
        response = self.request_subpath(path)
        if( response.headers['Content-Type'] in self.ALLOWED_IMAGE_CONTENT_TYPES ):
            return True 
        else:
            return False
        
    
    def path_processing(self, path):
        response = self.request_subpath(path)
        if( response.content ):
            return base64.b64encode(response.content).decode('ascii')
        else:
            return False

    
    def get_response(self):
        return self.response

    def get_status_code(self):
        return self.status_code