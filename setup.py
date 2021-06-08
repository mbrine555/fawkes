from setuptools import setup, find_packages

setup(
    name='fawkes',
    version='0.1.0',
    author='Rohith R',
    author_email='example@email.com',
    url='https://github.com/intuit/fawkes',
    packages=find_packages(exclude=['test']),
    python_requires='>=3.6, <4',
    install_requires=[
        'pandas',
        'gensim'
    ],
    entry_points={
        'console_scripts': [
            'fawkes=fawkes.__main__:main'
        ]
    }
)