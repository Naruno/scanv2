from setuptools import setup


setup(name='naruno_scan',
version='0.1.0',
description="""Scan website for Naruno""",
long_description="".join(open("README.md", encoding="utf-8").readlines()),
long_description_content_type='text/markdown',
url='https://github.com/Naruno/scanv2',
author='Onur Atakan ULUSOY',
author_email='onur.atakan.ulusoy@naruno.org',
license='MPL-2.0',
packages=["scan"],
package_dir={'':'src'},
install_requires=[
    "flet==0.8.4",
    "kot==0.20.0",
    "naruno==0.59.0",
    "requests==2.28.0"
],
entry_points = {
    'console_scripts': ['narunoscan=scan.scan:main'],
},
python_requires=">= 3",
include_package_data=True,
zip_safe=False)