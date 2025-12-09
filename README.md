# scrape
A Scraper script to control the HTTP headers sent to a server.
The code works like a proxy.
It spins up an HTTP web server that connects to the set HOST and allows you to remove HTTP headers

Example:
trying to display a web server inside an iFrame that the target WebServer sends X-Frame-Options to block cross origin, the scripts opens this up.
It is impossible to mitigate this script because of how HTTP works.

Install:
pip install requests
