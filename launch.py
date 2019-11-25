import sys
from tmod_file import TmodFile
import os

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python launch.py path1 [path2] ...')
    else :
        for path in sys.argv[1:]:
            print('Extraction begin <======== ' + path)
            tmod_file = TmodFile(path).extract()
            print('Extraction finish ========> ' + path.replace('.tmod', '') + '/')