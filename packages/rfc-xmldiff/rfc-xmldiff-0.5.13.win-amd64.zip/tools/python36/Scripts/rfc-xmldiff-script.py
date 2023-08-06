#!d:\tools\python36\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'rfc-xmldiff==0.5.13','console_scripts','rfc-xmldiff'
__requires__ = 'rfc-xmldiff==0.5.13'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('rfc-xmldiff==0.5.13', 'console_scripts', 'rfc-xmldiff')()
    )
