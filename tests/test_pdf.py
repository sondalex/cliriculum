from cliriculum.pdf import chromium_print, ChDir
from http.server import SimpleHTTPRequestHandler, HTTPServer
import os
import requests
from threading import Thread
from pypdf import PdfReader


def test_chdir(fixtures_path):
    with ChDir("example") as d:
        current = os.getcwd()
        assert current.find("example") >= 0
        assert d.target.find("example") >= 0

        assert d.target == current, f"target: {d.target}, current: {current}"
        httpd = HTTPServer(("", 8000), SimpleHTTPRequestHandler)
        t = Thread(target=httpd.serve_forever)
        t.start()
        # get html from httpd server
        with requests.get("http://127.0.0.1:8000") as r:
            assert (
                r.text.find("cliriculum") >= 0
            ), r.text  # check word cliriculum in request (i.e example/index.html
            # is effectively served)
        httpd.shutdown()
    current = os.getcwd()
    assert d.origin == current, f"origin: {d.origin}, current: {current}"


def test_chromium_print():
    chromium_print("example/")
    # check if pdf exists
    filep = "example/output.pdf"
    assert os.path.exists(filep), "file: {filep} does not exist"
    # parse pdf
    reader = PdfReader(filep)
    page = reader.pages[0]
    text = page.extract_text()
    assert len(text) > 0, f"text:{text}"
