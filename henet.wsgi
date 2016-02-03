import site
import sys
import os
import codecs

# Remember original sys.path.
prev_sys_path = list(sys.path)

# Add the new site-packages directory.
site.addsitedir(os.path.join(os.path.dirname(__file__), 'lib', 'python2.7', 
                             'site-packages'))

# Reorder sys.path so new directories at the front.
new_sys_path = []
for item in list(sys.path):
    if item not in prev_sys_path:
        new_sys_path.append(item)
        sys.path.remove(item)
sys.path[:0] = new_sys_path

os.chdir(os.path.dirname(__file__))

from henet.app import make_app

application = make_app('config.ini')
