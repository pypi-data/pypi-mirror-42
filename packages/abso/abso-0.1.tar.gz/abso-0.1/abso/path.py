import sys


def setAbsPath(path):
    print('Python %s on %s' % (sys.version, sys.platform))
    sys.path.extend([path])
