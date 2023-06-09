"""
Module for working with scholarly works from the OpenAlex API.
"""

import requests


class Works:
    """
    A class representing a scholarly work.

    Attributes:
        oaid (str): The OpenAlex identifier of the work.
        data (dict): The JSON data for the work obtained from the OpenAlex API.
    """

    def __init__(self, oaid):
        """
        Constructs a new Works object.

        Args:
            oaid (str): The OpenAlex identifier of the work.
        """
        self.oaid = oaid
        self.req = requests.get(f"https://api.openalex.org/works/{oaid}")
        self.data = self.req.json()

    def new(self):
        """
        A class to check test function.

        Returns:
            str: Returns title.
        """
        titles = self.data["title"]
        return titles

    def bibtex(self):
        """
        Returns the BibTeX string for the work.

        Returns:
            str: The BibTeX string.
        """
        _authors = [au["author"]["display_name"] for au in self.data["authorships"]]
        if len(_authors) == 1:
            authors = _authors[0]
        else:
            authors = ", ".join(_authors[0:-1]) + " and" + _authors[-1]

        title = self.data["title"]

        volume = self.data["biblio"]["volume"]

        issue = self.data["biblio"]["issue"]
        if issue is None:
            issue = ", "
        else:
            issue = ", " + issue

        pages = "-".join(
            [self.data["biblio"]["first_page"], self.data["biblio"]["last_page"]]
        )
        year = self.data["publication_year"]

        seq = (
            f"author = {authors},\n"
            f"title = {title},\n"
            f"volume = {volume},\n"
            f"number = {issue},\n"
            f"pages = {pages},\n"
            f"year = {year},\n"
            f'doi = "{self.data["doi"]}",\n'
            f'url = "{self.oaid}",\n'
            f'DATE_ADDED = {self.data["updated_date"]}'
        )

        return seq

    def ris(self):
        """
        Returns the ris  for the work.

        Returns:
            html: The ris string.
        """
        fields = []
        if self.data["type"] == "journal-article":
            fields += ["TY  - JOUR"]
        else:
            raise Exception("Unsupported type {self.data['type']}")

        for author in self.data["authorships"]:
            fields += [f'AU  - {author["author"]["display_name"]}']

        fields += [f'PY  - {self.data["publication_year"]}']
        fields += [f'TI  - {self.data["title"]}']
        fields += [f'JO  - {self.data["host_venue"]["display_name"]}']
        fields += [f'VL  - {self.data["biblio"]["volume"]}']

        if self.data["biblio"]["issue"]:
            fields += [f'IS  - {self.data["biblio"]["issue"]}']

        fields += [f'SP  - {self.data["biblio"]["first_page"]}']
        fields += [f'EP  - {self.data["biblio"]["last_page"]}']
        fields += [f'DO  - {self.data["doi"]}']

        ris = "\n".join(fields)
        return ris
