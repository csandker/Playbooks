import markdown2
import codecs
import re

class MarkdownParser():
    EXTRAS = [
        "fenced-code-blocks", 
        "cuddled-lists", 
        "code-friendly", 
        "numbering", 
        "smarty-pants", 
        "tables", 
        "task_list"
    ]
    ALLOWED_MIME_TYPES = [
        'text/plain',
        'text/markdown'
    ]
    ALLOWED_FILE_EXTENSIONS = [
        'md',
        'txt'
    ]
    IMG_REPLACE_PATCH = 'data-action="replace-image" '
    IMG_REPLACE_CLASS = "action image-replace "

    def __init__(self, extras=None):
        self.extras = extras or self.EXTRAS

    def parseMD(self, mdText):
        markdowner = markdown2.Markdown(self.extras)
        html = markdowner.convert(mdText)

        return html

    def replaceImages(self, content, path_validation_callback, path_processing_callback, **kwargs):
        ## try to contained images
        pImgTag = re.compile(r"\!\[.+\]\(.+\)")
        pImgLoc = re.compile(r"\(.+\)$")
        for match in pImgTag.finditer(content):
            ## get image tag ![..](.../...)
            mdImageTag = match.group()
            ## grab out image location (.../...)
            mdImgLocTag = pImgLoc.search(mdImageTag).group()
            ## strip out '(' and ')'
            imgSubPath = mdImgLocTag.lstrip('(').rstrip(')')
            ## path validation
            try:
                path_valid = path_validation_callback( imgSubPath, **kwargs)
                if( path_valid ):
                    base64Img = path_processing_callback( imgSubPath, **kwargs )
                    if( base64Img ):
                        imgTag = "<img src='data:image/png;base64, %s' alt='%s' />" %(base64Img, imgSubPath)
                        content = content.replace(mdImageTag, imgTag)
            except Exception as e:
                pass
        
        return content
