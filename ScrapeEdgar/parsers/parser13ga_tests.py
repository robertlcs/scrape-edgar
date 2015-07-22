import unittest

from ScrapeEdgar.parsers.parser13ga import Parser13ga
from ScrapeEdgar.parsers.test_utils import load_file_contents

class Parser13gaTests(unittest.TestCase):
    def setUp(self):
        self.parser = Parser13ga()

    def test_parser13ga(self):
        contents = load_file_contents("example_filings/twitter13ga.html")
        results = self.parser.parse(contents)
        self.assertEqual("90184L 102", results.get('cusip'))
        self.assertEqual("1355 Market Street, Suite 900, San Francisco, California 94103", results.get('address'))

    def test_parse13ga_txt(self):
        contents = load_file_contents("example_filings/albemarle_13ga.txt")
        results = self.parser.parse(contents, 'text/plain')
        self.assertEqual("012653101", results.get('cusip'))
        self.assertEqual("451 Florida Street, Baton Rouge, LA 70801", results.get('address'))

    def test_parse13ga_txt_dnb_none_type_for_address(self):
        contents = load_file_contents("example_filings/13ga-dun.bradstreet.corp.txt")
        results = self.parser.parse(contents, 'text/plain')
        self.assertEqual("26483E100", results.get('cusip'))
        self.assertEqual("103 JFK PARKWAY SHORT HILLS NJ 07078", results.get('address'))

    def test_parse13ga_html_missing_address(self):
        contents = load_file_contents("example_filings/twitter_sc13ga_did_not_parse_address.html")
        results = self.parser.parse(contents, content_type="text/html")
        self.assertEqual("90184L102", results.get('cusip'))
        # TBD: Fix this
        self.assertEqual("1355 Market Street, Suite 900, San Francisco, CA 94103", results.get('address'))

    def test_missing_cusip_number_for_dnb_13ga(self):
        # The title says "13G," but below there is text that says "Ammendment #1 and this comes back in the
        # search results as a 13G/A:
        # http://www.sec.gov/Archives/edgar/data/1115222/000114036115006261/doc1.htm

        contents = load_file_contents("example_filings/dnb13ga_missing_cusip.html")
        results = self.parser.parse(contents, content_type="text/html")

        self.assertEqual("26483E100", results.get('cusip'))

    def test_missing_cusip_number_for_dnb_13ga_txt(self):
        print "Not yet implemented"
        # http://www.sec.gov/Archives/edgar/data/1115222/000031506615001878/filing.txt
        pass

    def test_extract_issue_name_from_13ga(self):
        #Example: http://www.sec.gov/Archives/edgar/data/1115222/000021545715000168/dun.bradstreet.corp.txt
        # appears under "Title of Class of Securities"
        # TBD
        # DNB
        contents = load_file_contents("example_filings/dnb13ga.html")
        results = self.parser.parse(contents, content_type="text/html")
        self.assertEqual("COMMON STOCK", results.get('issue_name'))

        # Twitter
        contents = load_file_contents("example_filings/twitter13ga.html")
        results = self.parser.parse(contents, content_type="text/html")
        self.assertEqual("Common Stock, par value $0.000005 per share", results.get("issue_name"))

    def test_extract_issue_name_from_13ga_text(self):
        contents = load_file_contents("example_filings/13ga-dun.bradstreet.corp.txt")
        results = self.parser.parse(contents, content_type="text/plain")
        self.assertEqual("Common Stock", results.get('issue_name'))

if __name__ == '__main__':
    unittest.main()