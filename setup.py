from setuptools import setup, find_packages

setup(
    name='fawkespy',
    version='0.1.0',
    author='Rohith R',
    author_email='example@email.com',
    url='https://github.com/intuit/fawkes',
    packages=find_packages(exclude=['test']),
    python_requires='>=3.6, <4',
    data_files=[('fawkes_config', ['app/fawkes-config.json', 'app/sample-mint-config.json'])],
    install_requires=[
        'pandas',
        'nltk',
        'python-twitter',
        'gsheets',
        'scikit-learn',
        'xmltodict',
        'sendgrid',
        'BeautifulSoup4',
        'html5lib',
        'tensorflow',
        'yapf',
        'coverage',
        'codecov',
        'pre-commit',
        'jsonschema',
        'splunk-sdk',
        'numpy',
        'tensorflow_hub',
        'vertica-python',
        'gensim',
        'sentence-transformers'
    ],
    entry_points={
        'console_scripts': [
            'fawkes=fawkes.__main__:main'
        ]
    }
)