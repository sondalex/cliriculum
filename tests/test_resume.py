from cliriculum.resume import resume, SideBarHTML, MainHTML, ResumeHTML
import pytest
import os
# could paremetrize with location


ARGS = ["location_path", "location_none"]


def test_sidebar_html(fixtures_path):
    s = str(fixtures_path / "sidebar.md")
    c = str(fixtures_path / "contact.json")

    sidebar = SideBarHTML(path=s, contact=c)


@pytest.mark.parametrize("location", ARGS)
def test_main_html(location, fixtures_path, request):
    m = str(fixtures_path / "main.md")
    d = str(fixtures_path / "dates.json")
    main = MainHTML(m, dates=d, location=request.getfixturevalue(location))


@pytest.mark.parametrize("location", ARGS)
def test_resume(location, tmp_path, fixtures_path, request):
    s = str(fixtures_path / "sidebar.md")
    m = str(fixtures_path / "main.md")
    d = str(fixtures_path / "dates.json")
    c = str(fixtures_path / "contact.json")
    add_css = str(fixtures_path / "custom.css")
    html = resume(sidebar_md=s, main_md=m, dates=d, contact=c)
    with pytest.raises(ValueError):
        resume(sidebar_md=s, main_md=m, dates=d, contact=c, rsrc_dst=None, stylesheet="apath", location=request.getfixturevalue(location))
    resume(sidebar_md=s, main_md=m, dates=d, contact=c, rsrc_dst=tmp_path, stylesheet=add_css, location=request.getfixturevalue(location))
    files = os.listdir(tmp_path)
    assert set(files).symmetric_difference(["custom.css", "image.png"]) == set()


@pytest.mark.parametrize("location", ARGS)
def test_resume_html(location, tmp_path, fixtures_path, request):
    s = str(fixtures_path / "sidebar.md")
    m = str(fixtures_path / "main.md")
    d = str(fixtures_path / "dates.json")
    c = str(fixtures_path / "contact.json")
    sidebar = SideBarHTML(path=s, contact=c, rsrc_dst=tmp_path)
    main = MainHTML(path=m, dates=d, location=request.getfixturevalue(location))
    resume = ResumeHTML(main=main, sidebar=sidebar, stylesheet=fixtures_path / "custom.css", rsrc_dst=tmp_path)
    assert resume.additionalcss != ""
