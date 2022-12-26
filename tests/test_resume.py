from cliriculum.resume import resume, SideBarHTML, MainHTML
import pytest
import os


def test_sidebar_html(fixtures_path):
    s = str(fixtures_path / "sidebar.md")
    c = str(fixtures_path / "contact.json")

    sidebar = SideBarHTML(path=s, contact=c)

def test_main_html(fixtures_path):
    m = str(fixtures_path / "main.md")
    d = str(fixtures_path / "dates.json")
    main = MainHTML(m, dates=d)

def test_resume(tmp_path, fixtures_path):
    s = str(fixtures_path / "sidebar.md")
    m = str(fixtures_path / "main.md")
    d = str(fixtures_path / "dates.json")
    c = str(fixtures_path / "contact.json")
    add_css = str(fixtures_path / "custom.css")
    html = resume(sidebar_md=s, main_md=m, dates=d, contact=c)
    with pytest.raises(ValueError):
        resume(sidebar_md=s, main_md=m, dates=d, contact=c, rsrc_dst=None, stylesheet="apath")
    resume(sidebar_md=s, main_md=m, dates=d, contact=c, rsrc_dst=tmp_path, stylesheet=add_css)
    files = os.listdir(tmp_path)
    assert set(files).symmetric_difference(["custom.css", "image.png"]) == set()
