import sys

if (sys.version_info > (3, 0)):
    # Python 3 code in this block
    basestring = str
else:
    # Python 2 code in this block
    basestring = basestring