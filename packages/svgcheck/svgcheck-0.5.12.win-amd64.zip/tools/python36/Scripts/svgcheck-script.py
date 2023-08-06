#!d:\tools\python36\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'svgcheck==0.5.12','console_scripts','svgcheck'
__requires__ = 'svgcheck==0.5.12'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('svgcheck==0.5.12', 'console_scripts', 'svgcheck')()
    )
