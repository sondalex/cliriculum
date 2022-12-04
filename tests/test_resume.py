from cliriculum.resume import resume, SideBarHTML, MainHTML


def test_sidebar_html(fixtures_path):
    s = str(fixtures_path / "sidebar.md")
    c = str(fixtures_path / "contact.json")

    sidebar = SideBarHTML(path=s, contact=c)

def test_main_html(fixtures_path):
    m = str(fixtures_path / "main.md")
    d = str(fixtures_path / "dates.json")
    main = MainHTML(m, dates=d)

def test_resume(fixtures_path):
    s = str(fixtures_path / "sidebar.md")
    m = str(fixtures_path / "main.md")
    d = str(fixtures_path / "dates.json")
    c = str(fixtures_path / "contact.json")
    html = resume(sidebar_md=s, main_md=m, dates=d, contact=c)
