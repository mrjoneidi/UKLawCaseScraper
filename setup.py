from setuptools import setup, find_packages

setup(
    name='UKLawCaseScraper',
    version='0.4.4',
    packages=find_packages(),
    install_requires=[
        # list your dependencies here
    ],
    entry_points={
        'console_scripts': [
            # if you have any scripts to run from the command line
        ],
    },
    author='Mohammadreza Joneidi Jafari',
    author_email='m.r.joneidi.02@gmail.com',
    description='A package for scrape case law informations.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/mrjoneidi/UKLawCaseScraper',  # replace with your package's URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Framework :: Scrapy',
    ],
    python_requires='>=3.6',
)
