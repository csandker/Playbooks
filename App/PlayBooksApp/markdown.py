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
    
    # def insert_image_replace_patch(self, html):
    #     print("in image replace ")
    #     html1 = '<p><p><p> <p><img src="Images/wmic-spawn.png" alt="wmic-spa"><B<ayadsaod asdasd asdj saidj <img src="Images/wmic-spawn.png" alt="wmic-spa" class="foobar">'
        
    #     import pdb
    #     pdb.set_trace()
        
    
    # def find_unpatched_img(self, html):
    #     newHtml = html
    #     pImgTag = re.compile( "<img\s[^<]+" )
    #     #pImgTag = re.compile( "<img\s([^<][^%s])+" %self.IMG_REPLACE_PATCH )
    #     imageTagOffset = len('<img ')
    #     pClass = re.compile(r"class\=[\"\']")
    #     match = re.search(pImgTag, html)
    #     #for match in pImgTag.finditer(html):
    #     if( match ):
    #         imgTag = match.group()
    #         print("MATCH: %s" %imgTag)
    #         ## add in REPLACHE PATCH
    #         indexAfterImg = match.span()[0] + imageTagOffset
    #         print("IMAGE REPLACE PATCH")
    #         print( html[indexAfterImg-100:indexAfterImg+100] )
    #         #import pdb
    #         #pdb.set_trace()
    #         newHtml = html[:indexAfterImg] + self.IMG_REPLACE_PATCH + html[indexAfterImg:]
    #         ## add in REPLACHE Class
    #         class_match = re.search(pClass, imgTag)
    #         if( class_match ):
    #             indexAfterClass = class_match.span()[1]
    #             newHtml = newHtml[:indexAfterClass] + self.IMG_REPLACE_CLASS + newHtml[indexAfterImg:]
    #         else:
    #             classOffset = indexAfterImg + len(self.IMG_REPLACE_PATCH)
    #             classTag = 'class="%s" ' %self.IMG_REPLACE_CLASS
    #             newHtml = newHtml[:classOffset] + classTag + newHtml[classOffset:]
    #         return newHtml
    #     else:
    #         return False

    #     #import pdb
    #     #pdb.set_trace()
    #     return newHtml
