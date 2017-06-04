import tempfile
import os
from .log_system import Log


##
# Write content in bytes to tmp file
# @param content content in bytes
# @param extension extension of file
# @return filename of tmp file
def content_to_tmp_file(content, extension="png"):
    tmp_file = tempfile.mkstemp()
    tmp_filename = "%s.%s" % (tmp_file[1], extension)
    file = open(tmp_filename, 'wb')
    file.write(content)
    file.close()
    return tmp_filename


##
# Create tmp and return its name
# @param extension extension of created file
# @return tmp filename in str
def get_tmp_file_name(extension="txt"):
    tmp_file = tempfile.mkstemp()
    tmp_filename = "%s.%s" % (tmp_file[1], extension)
    return tmp_filename


##
# Return all file content in str
# @param file_name
# @return content in str
# @error AssertionError
def get_str_content_from_file(file_name):
    assert os.path.exists(file_name)
    content_in_str = ""
    try:
        file_stream = open(file_name, "r", encoding="utf-8")
    except Exception:
        Log.log.critical("bad file path")
    else:
        for chunk in iter(lambda: file_stream.read(4096), ""):
            content_in_str += chunk
        file_stream.close()
    finally:
        return content_in_str
