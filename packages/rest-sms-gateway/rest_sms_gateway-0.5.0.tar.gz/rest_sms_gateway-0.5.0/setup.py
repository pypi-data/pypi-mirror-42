import setuptools


with open('requirements.txt') as f:
    reqs = f.read().splitlines()

with open('README.md') as d:
    long_description = d.read()

setuptools.setup(
    name='rest_sms_gateway',
    version='0.5.0',
    author='Geraldo Castro',
    author_email='victormatheuscastro@gmail.com',
    packages=['rest_sms_gateway'],
    install_requires=reqs,
    keywords='python api rest sms gateway',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='LGPLv3',
    url='https://github.com/exageraldo/RestSMSGateway',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Development Status :: 1 - Planning',
        'Topic :: Utilities',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Operating System :: OS Independent'
    ],
)