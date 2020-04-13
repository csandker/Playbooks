
from .models import Playpage
from PlayBooksWeb.models import IncludedFolder

from .request import URLRequester
from .markdown import MarkdownParser

class SourceResolver():

    def __init__(self, page):
        if( page and isinstance(page, Playpage) ):
            self.playpage = page
        else:
            raise Exception("Invalid Page Given To Source Resolver")

    def resolve_type(self):
        source_type = self.playpage.source_type
        if( source_type == Playpage.SOURCE_HTTP ):
            return self.resolve_from_http(url=self.playpage.source)
        elif( source_type == Playpage.SOURCE_DISK ):
            return self.resolve_from_disk(self.playpage.included_folder.id, self.playpage.source)

    def resolve_from_http(self, url=None):
        if( url ):
            requester = URLRequester(url)
            requester.request()
            if( requester.is_valid_response() ):
                requester.resolve_images()
                response = requester.get_response()
                return response
            else:
                return False
        else:
            return False

    def resolve_from_disk(self, selected_included_folder, selected_included_folder_path):
        md_parser = MarkdownParser()
        content = IncludedFolder.get_file_content(selected_included_folder, selected_included_folder_path)
        content = md_parser.replaceImages(content, IncludedFolder.path_validation, IncludedFolder.path_processing, folderID=selected_included_folder, subpath=selected_included_folder_path)
        if( content ):
            return content
        else:
            return False
