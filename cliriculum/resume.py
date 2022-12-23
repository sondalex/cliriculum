from cliriculum.markdown import ParseMd
from cliriculum.renderers import SideBarRenderer, MainRenderer
from cliriculum.deserializers import Contact, Dates
from cliriculum.markdown import DescriptionBlock
from cliriculum.loaders import load_json
from warnings import warn
from typing import Union
from cliriculum.utils import copy_files



HEAD = """
<!doctype html>
<head>
  <meta charset="UTF-8">
  <title>HTML Resume</title>
  <link rel="stylesheet" href="style.css" type="text/css">
  <link rel="stylesheet" href="fontawesome/css/all.css" type="text/css">
  <link rel="stylesheet" href="fontawesome/css/v4-shims.css" type="text/css">
  <script src="paged.polyfill.js"></script>
  <script src="style.js"></script>
</head>
"""


class SideBarHTML:
    def __init__(self, path, contact, rsrc_dst: Union[str, None] = None):
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
        if rsrc_dst is not None:
            warn("Currently, specifying rsrc_dst copies only contact profile picture")
            copy_files([contact_o.profile.logo], rsrc_dst)


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


def resume(sidebar_md: str, main_md: str, dates: str, contact: str, rsrc_dst: Union[str, None] = None) -> str:
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
    rsrc_dst: Union[str, None]
        If not None resources mentionned in JSON files are copied to destination directory `rsrc_dst`. Defaults to None.
    Returns
    -------
    str
        HTML representation of the resume
    
    Examples
    --------
    >>> from cliriculum import resume
    >>> html = resume(sidebar_md="sidebar.md", main_md="main.md", contact="contact.json", dates="dates.json")
    """    
    sidebar = SideBarHTML(path=sidebar_md, contact=contact, rsrc_dst=rsrc_dst)
    main = MainHTML(path=main_md, dates=dates)
    resume = ResumeHTML(main=main, sidebar=sidebar)
    html = resume.join()
    return html
