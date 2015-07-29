# This is a parser designed to try to parse CUSIP's and issue names out of any document that might contain them.
# A limitation of this is that since it's intended for a much broader set of input documents, it might be more
# prone to errors, as the inputs might not have been tested before. "Garbage in, garbage", although one man's
# garbage is another random SEC filing.

from ScrapeEdgar.parsers.base_parser import BaseParser
from ScrapeEdgar.cleaning_functions import remove_duplicates

import re

class GenericParser(BaseParser):

    def extract_cusips(self, text):
        pat = re.compile(r'CUSIP\s+(no|number|num|#)*\.*:*\s*(\w{6}\W*\w{3})\b', re.IGNORECASE | re.MULTILINE)
        matches = re.findall(pat, text)
        if matches:
            return self.normalize_results([match[1] for match in matches])

        return None

    def normalize_string(self, string):
        string = re.sub(r'\s+', ' ', string.upper().strip())
        # Standardize pluralization
        return re.sub(r'NOTE\b', 'NOTES', string, flags=re.IGNORECASE)

    def normalize_results(self, results):
        normalized_results = map(self.normalize_string, results)
        return remove_duplicates(normalized_results)

    def extract_issue_names(self, text):
        # Common Stock
        common_stock_pat = re.compile(r'(Common Stock(, \$[0-9]+\.[0-9]+ par value per share)*)', re.IGNORECASE | re.MULTILINE)
        match = common_stock_pat.search(text)
        if match:
            return match.group(1)

        # Notes
        notes_pat = re.compile(r'([0-9]+\.*\s*[0-9/]+%\s+(Senior|Convertible|Convertible Senior){0,1}\s*Notes*\s+due\s+[0-9]{4})', re.IGNORECASE | re.MULTILINE)
        matches = re.findall(notes_pat, text)

        if matches:
            results = self.normalize_results([match[0] for match in matches])
            return results

        return None

    def parse_text(self, text, **kwargs):
        cusips = self.extract_cusips(text)
        issue_names = self.extract_issue_names(text)
        return {'cusip' : cusips, 'issue_name' : issue_names}