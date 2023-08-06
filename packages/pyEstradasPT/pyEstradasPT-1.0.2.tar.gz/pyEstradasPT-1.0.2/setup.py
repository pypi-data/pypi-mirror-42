from setuptools import setup, find_packages


long_description = open('README.md').read()

setup(
    name='pyEstradasPT',
    version='1.0.2',
    license='MIT License',
    url='https://github.com/dpjrodrigues/pyEstradasPT',
    author='Diogo Rodrigues',
    author_email='dpjrodrigues@gmail.com',
    description='Python library to retrieve information from Estradas.pt',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['pyEstradasPT'],
    zip_safe=True,
    platforms='any',
    install_requires=[
        'aiohttp',
      ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
