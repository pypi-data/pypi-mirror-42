# Auto fetch Meta data Entries

This repository is intended as a starting point for fetching metadata from online sites.

It is to be integrated into the ColLi backend for the collaborative Literature management.

## Install

The following packages have to be installed:

python3
BeautifulSoup4
URLlib
python bibtexparser

to install under Ubuntu:

```bash
apt install python3 python3-bs4 python3-urllib3 python3-bibtexparser
```

Alternatively, just install python3 and do the rest via pip from the project directory:

```bash
pip install -r requirements.txt
```

## Adding more sites.

If there is no parser for a specific site, it can be created in the sites folder.

Naming convention is, that the file name and the class name inside this file must be the domain name without any subdomains or top-level domains.
So for `https://dl.acm.org/` it is just `acm`

An example is provided in sites/example.py

Every class must be a subclass of `landingPage` and can implement one of the following functions:

```python
    def getBibTeX(self, link, soup):
        return None

    def getDict(self, link, soup):
        return None
```

Parameters are in both cases the URL of the landing page of the DOI resolver and the page as a parsed beautifulsoup object.

They are seperated by their return value.

getBibTeX must return a valid BibTeX entry or None.
getDict must return a python Dictionary with the field names according to the Dublin Core Standard.
