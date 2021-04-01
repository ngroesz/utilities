import io
import subprocess
import sys
import unittest
import decode

class TestDecode(unittest.TestCase):

    def test_base64_gzip(self):
        self.assertEqual(
            decode.decode_string('H4sIABJVZmAC/03MMRLCMAxE0T6n2I7Gt6DKCagFVhKDLGUseTK5PWbS0L79szOUOXPGaR3VGiccjIM0hnWHsPt0ty4ZaoFPcU94dw80XttvnAO1rFtc+mS8hKkleKm7jDvSjF2o6PRgEcRGcfMrXoqO4F9MGbagnlCq7F9KW573ngAAAA==', ['b64', 'gz']),
            "I needed you more, we wanted us less\nCould not kiss, just regress\nIt might just be clear, simple, and plain\nWell that's just fine, that's just one of my names"
        )

    def test_base64_zip(self):
        self.assertEqual(
            decode.decode_string('UEsDBBQAAAAIABV6gVJo31znEwAAABEAAAAPAAAAdGVzdF9maWxlXzEudHh0K87PTVVIy8xJVUjOzytJzSsBAFBLAwQUAAAACAAVeoFSUeLDoRMAAAARAAAADwAAAHRlc3RfZmlsZV8yLnR4dMvNL0pVSMvMSVVIzs8rSc0rAQBQSwECFAMUAAAACAAVeoFSaN9c5xMAAAARAAAADwAAAAAAAAAAAAAAgAEAAAAAdGVzdF9maWxlXzEudHh0UEsBAhQDFAAAAAgAFXqBUlHiw6ETAAAAEQAAAA8AAAAAAAAAAAAAAIABQAAAAHRlc3RfZmlsZV8yLnR4dFBLBQYAAAAAAgACAHoAAACAAAAAAAA=', ['b64', 'z']),
            "some file contentmore file content"
        )

if __name__ == '__main__':
    unittest.main()
