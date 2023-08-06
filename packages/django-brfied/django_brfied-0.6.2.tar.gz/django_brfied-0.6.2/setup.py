# -*- coding: utf-8 -*-
from distutils.core import setup
setup(
    name='django_brfied',
    description='Django Application specific brazilian fields types',
    long_description='Utils classes for EGE project',
    license='MIT',
    author='Kelson da Costa Medeiros',
    author_email='kelsoncm@gmail.com',
    packages=['django_brfied', 'django_brfied/migrations', 'django_brfied/management/commands', 'django_brfied/static', ],
    package_data = {'static': ['*'], },
#    package_dir={'django_brfied': 'django_brfied'},
#    packages=['ege_theme', 'ege_theme/migrations', 'ege_theme/static', 'ege_theme/templates', 'ege_theme/templatetags'],
    include_package_data=True,
    version='0.6.2',
    download_url='https://github.com/kelsoncm/django_brfied/releases/tag/0.6.2',
    url='https://github.com/kelsoncm/django_brfied',
    keywords=['django', 'BR', 'Brazil', 'Brasil', 'model', 'form', 'locale', ],
    classifiers=[]
)

