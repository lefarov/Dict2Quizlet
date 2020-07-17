#!/usr/bin/env python
#
# Query the leo.org German/English dictionary.
#
# The following code is based on `leo.py` by Ian Denhardt
# https://github.com/zenhack/leo.py/blob/master/leo.
#

import six
import json
import requests
from lxml import etree
from io import StringIO
from tabulate import tabulate


class LeoDict:
    def __init__(self):
        self.section_mapping = {
            "subst": "Substantive",
            "verb": "Verbern",
            "adjadv": "Adjektive / Adverbien",
            "praep": "Präpositionen / Pronomen / ...",
            "definition": "Definition",
            "phrase": "Phrasen",
            "example": "Beispiele",
        }

    def search(self, term, uri="https://dict.leo.org/ende/"):
        ret = {}
        resp = requests.get(uri, params={"search": term})
        html = etree.parse(StringIO(resp.text), etree.HTMLParser())

        sections = html.findall(".//div[@data-dz-name]")
        for section in sections:
            ret[self.section_mapping[section.get("data-dz-name")]] = []

            results = section.findall(".//td[@lang='en']")
            for r_en in results:
                r_de = r_en.find("./../td[@lang='de']")
                ret[self.section_mapping[section.get("data-dz-name")]].append(
                    {
                        "en": LeoDict._get_text(r_en).strip(),
                        "de": LeoDict._get_text(r_de).strip(),
                    }
                )

        return ret

    @staticmethod
    def _get_text(elt):
        buf = StringIO()

        def _helper(_elt):
            if _elt.text is not None:
                buf.write(six.text_type(_elt.text))
            for child in _elt:
                _helper(child)
            if _elt.tail is not None:
                buf.write(six.text_type(_elt.tail))

        _helper(elt)
        return buf.getvalue()


if __name__ == "__main__":
    ld = LeoDict()
    trotzdem_en = ld.search("trotzdem")
    welt_en = ld.search("Welt")
    toll_en = ld.search("toll")
