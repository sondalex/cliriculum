import re
from mistletoe.block_token import Heading
from mistletoe.span_token import RawText
from cliriculum.deserializers import Dates, Contact
from typing import List, Union
import os
from cliriculum.parsers import Document



class URLEntry:
    def __init__(self, src, width, height, url, classes, text):
        self.src = src
        self.url = url
        self.width = width
        self.height = height
        self.classes = classes
        self.text = text


class LogoEntry:
    def __init__(self, src, title, classes, width="18", height="18"):
        """
        A node intented to be added into the abstract
        syntax tree.
        The node contains the following attributes:

        src:
        title:
        width:
        height:

        Parameters
        ----------
        src : _type_
            Path to logo
        title : _type_
            A description
        width : str, optional
            Size of width of image, by default "18"
        height : str, optional
            Size of height of image, by default "18"
        """
        self.src = src
        self.title = title
        self.width = width
        self.height = height
        self.classes = classes


class ImageEntry:
    def __init__(self, src, width, height, id):
        self.id = id
        self.src = src
        self.width = width
        self.height = height


class TextEntry:
    def __init__(self, text, emphasis: Union[str, None] = None):
        """_summary_

        Parameters
        ----------
        text : _type_
            _description_
        emphasis : str
            s
        """        
        self.text = text
        _ = ["bold", "italic", None]
        if emphasis not in _:
            raise ValueError("`emphasis` accepts values : {}".format(_))
        self.emphasis = emphasis


class SocialBlock:
    def __init__(self, urlentries: List[URLEntry]):
        self.children = urlentries


class ContactBlock:
    def __init__(
        self, children: List[Union[SocialBlock, URLEntry, LogoEntry, TextEntry]]
    ):
        self.children = children


class DescriptionBlock:
    def __init__(
        self, children: List
    ):
        self.children = children


class ParseMd:
    """
    Parse Markdown Document and adds
    metadata to the tree depending on method called.

    Attributes
    ----------
    doc The tree representation of the document. Each public methods calls
    modifies this attribute
    top: Union[bool, None]
        Set on `self.add_contact` calls.
        If multiple calls, the top correspond
        to the last position of the last 
        added Contact node.
        Default None.
    """

    heading_id_pattern = re.compile(r"\{#([\w-]*[\w-])\}$")

    def __init__(self, path: str):
        """_summary_

        Parameters
        ----------
        path : str
            Path to markdown file.
            The file will be parsed by [mistletoe](https://github.com/miyuchina/mistletoe)
            And its tree representation stored in `self.doc`.
        """
        with open(path, mode="r") as f:
            self.doc = Document(f)
        self.periods = []
        self.top = None

    def _isHeading(self, leaf):
        if isinstance(leaf, Heading):
            return True

    def _headings_with_id_idx(self, doc: Document):
        """_summary_
        Iterates over the first layer leaves, and checks whether
        Level two headings have an id.
        Raises
        ------
        ValueError

        Return
        ------
        Single index
        """
        idx = []
        for i, leaf in enumerate(doc.children):
            # issubclass
            # isinstance
            if isinstance(leaf, Heading):
                if (leaf.level == 2) and self._has_heading_id(leaf):
                    idx.append(i)
        return idx

    def _has_heading_id(self, node):
        if self._isHeading(node):
            raw_leaf = node.children[0]  # select raw content
            if isinstance(raw_leaf, RawText) is False:
                error = """
                There might be an issue with the current version,
                could you report it ?
                """
                raise ValueError(error)

            match_obj = self.heading_id_pattern.search(raw_leaf.content)
            if match_obj is None:
                return False
            else:
                return True

        else:
            raise ValueError("Wrong type of node")

    def _add_to_top_paragraph(self, start, end, width, leveltwo_header_idx, src, classes):
        """_summary_
        Add LogoEntry node to the top of the paragraph with parent indexed at
        leveltwo_header_idx at node level 1.

        Parameters
        ----------
        leveltwo_header_idx : Integer
            The index of the level two Heading two which Dates should be added
        """
        startfmt = start.strftime("%B %Y")
        if end is not None:
            endfmt = end.strftime("%B %Y")
        else:
            endfmt = "Current"
        title = f"{startfmt} - {endfmt}"

        new_node = LogoEntry(
            src=src,
            title=title,
            width=width,
            classes=classes
        )
        self.doc.children.insert(leveltwo_header_idx + 1, new_node)

    def add_dates(self, dates: Dates):
        """_summary_
        Adds dates as a LogoEntry to the doc representation


        Parameters
        ----------
        dates : Dates
            Instanciated Dates object.

        Returns
        -------
        mistletoe.Document
            An extended document with date added for Dates.periods object
            who share a level two ATX heading common id.

        Examples
        -------

        >>> from cliriculum.renderers import Renderer
        >>> from cliriculum.deserializers import Dates
        >>> from cliriculum.markdown import ParseMd
        >>> from cliriculum.loaders import load_json
        >>> parsed = ParseMd("README.md")
        >>> dates = Dates(**load_json("dates.json"))
        >>> doc = parsed.add_dates(dates=dates).doc
        >>> with Renderer() as r:
        >>>     html = r.render(doc)
        """
        h_level_w_id = self._headings_with_id_idx(self.doc)
        for i, pos in enumerate(h_level_w_id):
            if pos > h_level_w_id[i - 1]:
                pos = pos + 1  # correction factor since
                # one node is added each time
            # Match with Dates
            heading = self.doc.children[pos]
            # extract id
            raw_leaf = heading.children[0]
            match_obj = self.heading_id_pattern.search(raw_leaf.content)
            _ = match_obj.regs[-1]
            indice = raw_leaf.content[_[0] : _[1]]
            # search for indice in Dates
            period = dates.get_period(indice)

            _ = match_obj.regs[0]
            self.doc.children[pos].children[0].content = raw_leaf.content.replace(
                raw_leaf.content[_[0] : _[1]], ""
            ).rstrip()

            if period is not None:
                self._add_to_top_paragraph(
                    start=period.start,
                    end=period.end,
                    width=period.width,
                    leveltwo_header_idx=pos,
                    src=period.logo,
                    classes=period.classes
                )  # operates directly on AST
        return self

    def add_contact(self, contact: Contact, top: bool = True):
        """_summary_

        Parameters
        ----------
        contact : Contact
            _description_
        top : bool, optional
            _description_, by default True

        Examples
        --------

        >>> from cliriculum.renderers import Renderer
        >>> from cliriculum.deserializers import Contact
        >>> from cliriculum.loaders import load_json
        >>> parsed = ParseMd("README.md")
        >>> dates = Contact(**load_json("contact.json"))
        >>> doc = parsed.add_contact(contact=contact).doc
        >>> with Renderer() as r:
        >>>     html = r.render(doc)
        """
        self.top = top
        name = TextEntry(contact.name, emphasis="bold")
        profession = TextEntry(contact.profession, emphasis="italic")
        email_url = contact.email.url
        if email_url is not None:
            email_url = "mailto: {}".format(contact.email.url)
        
        email = URLEntry(
            src=contact.email.logo, width=contact.email.width, height=contact.email.height, url=email_url,
            classes=contact.email.classes,
            text=contact.email.text
        )
        website = URLEntry(
            src=contact.website.logo, width=contact.website.width, height=contact.website.height, url=contact.website.url,
            classes=contact.website.classes, text=contact.website.text
        )
        socials = SocialBlock(
            [
                URLEntry(
                    src=social.logo,
                    width=social.width,
                    height=social.height,
                    url=social.url,
                    classes=social.classes,
                    text=social.text
                )
                for social in contact.socials.children
            ]
        )
        if contact.number.url is None:
            tel_url = contact.number.url
        else:
            tel_url = "tel:{}".format(contact.number.url)
        number = URLEntry(
            src=contact.number.logo,
            width=contact.number.width,
            height=contact.number.height,
            url=tel_url,
            classes=contact.number.classes,
            text=contact.number.text
        )
        profile = ImageEntry(src=os.path.basename(contact.profile.logo), height=contact.profile.height, width=contact.profile.width, id="profile_pic")
        children = [profile, name, profession, email, website, socials, number]

        contact_block = ContactBlock(children=children)

        if top is False:
            self.doc.children.append(contact_block)
        else:
            self.doc.children.insert(0, contact_block)

        return self

