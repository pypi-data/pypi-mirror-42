import sys
import webbrowser
import functools
import operator
from distutils.core import setup

name = 'vcdriver2'
version = '0.0.2'
url = 'https://pypi.org/project/vcdriver'
message = (
    name + ' is no-longer available, please install vcdriver, see '
    'also: ' +
    url
)


argv = functools.partial(operator.contains, set(sys.argv))


if (argv('install') or  # pip install ..
        (argv('--dist-dir') and argv('bdist_egg'))):  # easy_install
    webbrowser.open_new(url)
    raise Exception(message)


if argv('bdist_wheel'):  # modern pip install
    raise Exception(message)


setup(
    name=name,
    version=version,
    maintainer='Thomas Grainger',
    maintainer_email=name + '@graingert.co.uk',
    long_description=message,
    url=url,
)
