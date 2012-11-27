from django.http import HttpResponse, HttpResponseNotModified
from django.utils.http import http_date
from email.Utils import formatdate, parsedate_tz, mktime_tz
from fingerblog.settings import STATIC_ROOT, ABS_PROJECT_ROOT
import time
import os
import stat
import re
import zipfile
import mimetypes

zipfile_cache={}
MAX_AGE=1200

def SetCachingHeaders(response):
    response['Cache-Control'] = 'public, max-age=%d'%(MAX_AGE)
    response['Expires']=formatdate(time.time() + MAX_AGE, usegmt=True)
    response["Content-Length"] = len(response.content)

def tinymce(request,path):
    zipfileName = STATIC_ROOT+'/tinymce.zip'
    
    zf_object = zipfile_cache.get(zipfileName)
    if zf_object is None:
        try:
            zf_object = zipfile.ZipFile(zipfileName, "r")
        except (IOError, RuntimeError):
            zf_object=''
        zipfile_cache[zipfileName]=zf_object
    if zf_object == '':
        return HttpResponse('Not Found')
   
    mimetype = mimetypes.guess_type(path)[0] or 'application/octet-stream'
    content=zf_object.read(path)
    response = HttpResponse(content,mimetype=mimetype)
    SetCachingHeaders(response)
    return response

def theme(request,path):
    file_path = os.path.normpath(os.path.join(ABS_PROJECT_ROOT, 'templates/themes', path))
    statobj = os.stat(file_path)
    mimetype = mimetypes.guess_type(file_path)[0] or 'application/octet-stream'
    if not _was_modified_since(request.META.get('HTTP_IF_MODIFIED_SINCE'),
                              statobj[stat.ST_MTIME], statobj[stat.ST_SIZE]):
        return HttpResponseNotModified(mimetype=mimetype)
    contents = open(file_path, 'rb').read()
    response = HttpResponse(contents, mimetype=mimetype)
    response["Last-Modified"] = http_date(statobj[stat.ST_MTIME])
    response["Content-Length"] = len(contents)
    return response

def _was_modified_since(header=None, mtime=0, size=0):
    try:
        if header is None:
            raise ValueError
        matches = re.match(r"^([^;]+)(; length=([0-9]+))?$", header,
                           re.IGNORECASE)
        header_mtime = mktime_tz(parsedate_tz(matches.group(1)))
        header_len = matches.group(3)
        if header_len and int(header_len) != size:
            raise ValueError
        if mtime > header_mtime:
            raise ValueError
    except (AttributeError, ValueError):
        return True
    return False
