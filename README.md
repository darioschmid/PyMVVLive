mvv_sbahn
=========

Python-Library to get punctuality information for S-Bahns in munich from hafas.de. Relies on scraping a website due to the lack of official API in this specific case.
This project *not* associated with neither MVV, MVG, Deutsche Bahn, etc.


## mvv_sbahn.get_punctuality()
Retrieve the next departures from http://s-bahn-muenchen.hafas.de/bin/540/query.exe/dn?&statusWidget.

Configuration variables:
 
- **line** (*Required*): Name of the S-Bahn line. Can be any of the 8 S-Bahn lines `S1, S2, S3, S4, S6, S7, S8, S20`.

