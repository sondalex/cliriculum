from .markdown import ParseMd
from .renderers import SideBarRenderer, MainRenderer
from .deserializers import Contact, Dates
from .markdown import DescriptionBlock
from .loaders import load_json

HEAD = """
<!doctype html>
<head>
  <meta charset="UTF-8">
  <title>HTML Resume</title>
  <link rel="stylesheet" href="style.css" type="text/css">
  <link rel="stylesheet" href="fontawesome/css/all.css" type="text/css">
  <link rel="stylesheet" href="fontawesome/css/v4-shims.css" type="text/css">
  <script src="paged.polyfill.js"></script>
</head>
"""


class SideBarHTML:
    def __init__(self, path, contact):
        parsed = ParseMd(path)
        contact_d = load_json(contact)
        contact_o = Contact(**contact_d)
        parsed.add_contact(contact_o)
        doc = parsed.doc
        # find ...
        if parsed.top is True:
            contact = doc.children[0]
            description = doc.children[1:]
        else:
            contact = doc.children[-1]
            description = doc.children[:-1]
        # all except this element
        # either at beginning either at the end
        children = [contact, DescriptionBlock(children=description)]
        doc.children = children
        with SideBarRenderer() as r:
            self.html = r.render(doc)


class MainHTML:
    def __init__(self, path, dates):
        self.parsed = ParseMd(path)
        dates_d = load_json(dates)
        dates_o = Dates(dates_d)
        self.parsed.add_dates(dates_o)
        with MainRenderer() as r:
            self.html = r.render(self.parsed.doc)


class ResumeHTML:
    def __init__(self, sidebar: SideBarHTML, main: MainHTML):
        """
        Render Resume

        Parameters
        ----------
        sidebar : SideBarHTML
            _description_
        main : MainHTML
            _description_
        Returns
        -------
        _type_
            _description_
        """
        self.main = main
        self.sidebar = sidebar
    
    def join(self) -> str:    
        body = self.sidebar.html + "\n" + self.main.html  # union of sidebar and main
        template = "<html>{head}<body>{body}</body></html>"
        return template.format(head=HEAD, body=body)


def resume(sidebar_md: str, main_md: str, dates: str, contact: str) -> str:
    """

    Parameters
    ----------
    sidebar_md : str
        Path to sidebar markdown
    main_md : str
        Path to main markdown
    dates : str
        path to dates JSON
    contact : str
        Path to contact JSON

    Returns
    -------
    str
        HTML representation of the resume
    
    Examples
    --------
    >>> from cliriculum import resume
    >>> html = resume(sidebar_md="sidebar.md", main_md="main.md", contact="contact.json", dates="dates.json")
    """    
    sidebar = SideBarHTML(path=sidebar_md, contact=contact)
    main = MainHTML(path=main_md, dates=dates)
    resume = ResumeHTML(main=main, sidebar=sidebar)
    html = resume.join()
    return html
