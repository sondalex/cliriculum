import os
import re
from collections import OrderedDict
from typing import Any, List, Optional, Tuple, Type, Union

from mistletoe.block_token import Heading
from mistletoe.span_token import RawText

from cliriculum.deserializers import Contact, Dates, Locations
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
    def __init__(self, src, title, classes, width: str = "18", height: str = "18"):
        """
        A node intented to be added into the abstract
        syntax tree.

        Attributes
        ----------
        src:
        title:
        width:
        height:

        Parameters
        ----------
        src:
            Path to logo
        title:
            A description
        width: Optional[str]
            Size of width of image, by default "18"
        height: Optional[str]
            Size of height of image, by default "18"
        """
        self.src = src
        self.title = title
        self.width = width
        self.height = height
        self.classes = classes

    def __str__(self):
        return f"< Instance of type: {self.__class__.__name__} with attributes src={self.src}, title={self.title}, width={self.width}, height={self.height}, classes=({self.classes})>"


class PeriodEntry(LogoEntry):
    def __init__(self, idx, start, end, logo, width, height, classes):
        startfmt = start.strftime("%B %Y")
        if end is not None:
            endfmt = end.strftime("%B %Y")
        else:
            endfmt = "Current"
        title = f"{startfmt} - {endfmt}"
        super().__init__(
            src=None, title=title, classes=classes, height=None, width=None
        )


class LocationEntry(LogoEntry):
    def __init__(self, idx, classes, location):
        title = location
        super().__init__(
            src=None, title=title, classes=classes, height=None, width=None
        )


class ImageEntry:
    def __init__(self, src, width, height, id):
        self.id = id
        self.src = src
        self.width = width
        self.height = height


class TextEntry:
    def __init__(self, text: str, emphasis: Optional[str] = None):
        """
        Parameters
        ----------
        text : str
        emphasis : str
            One of ["bold", "italic", None]
        """
        self.text = text
        valid = ["bold", "italic", None]
        if emphasis not in valid:
            raise ValueError("`emphasis` accepts values : {}".format(valid))
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
    def __init__(self, children: List):
        self.children = children


class Class:
    def __init__(self, classes):
        self.classes = classes


class Span:
    def __init__(self, text: RawText):
        self.text = text


class ParseMd:
    """
    Parse Markdown Document and adds
    metadata to the tree depending on method called.

    Attributes
    ----------
    doc:
        The tree representation of the document. Each public methods calls
        modifies this attribute
    top: Union[bool, None]
        Set on `self.add_contact` calls. If multiple calls, the top correspond
        to the last position of the last added Contact node.
        Default None.
    """

    heading_id_pattern = re.compile(r"\{#([\w-]*[\w-])\}$")
    classes_pattern = re.compile(r'\{classes=\s{0,}"([^"]*)"\s{0,}\}')
    _error = """
    There might be an issue with the current version,
    could you report it ?
    """

    def __init__(self, path: str):
        """

        Parameters
        ----------
        path : str
            Path to markdown file.
            The file will be parsed by `mistletoe <https://github.com/miyuchina/mistletoe>`_
            And its tree representation stored in `self.doc`.
        """
        with open(path, mode="r") as f:
            self.doc = Document(f)
        self.periods = []
        self.top = None
        self.heading_index = OrderedDict()  # maybe should set it to private

    def _is_heading(self, leaf):
        if isinstance(leaf, Heading):
            return True

    def _headings_with_id_idx(self, doc: Document) -> OrderedDict:
        """

        Parameters
        ----------
        doc : Document

        Returns
        -------
        OrderedDict
            An ordered dict with key corresponding to position in first tree layer
            and value the string identifier extracted from the header.
        """
        heading_index = OrderedDict()
        for i, leaf in enumerate(doc.children):
            # issubclass
            # isinstance
            if isinstance(leaf, Heading):
                outer_and_inner_span = self._get_heading_id_spans(leaf)
                if (leaf.level == 2) and (outer_and_inner_span is not None):
                    raw_leaf = leaf.children[0]
                    _, indice_span = outer_and_inner_span
                    indice = raw_leaf.content[indice_span[0] : indice_span[1]]
                    heading_index[i] = indice
        return heading_index

    def _get_heading_id_spans(
        self, node
    ) -> Union[Tuple[Tuple[int, int], Tuple[int, int]], None]:
        """

        Parameters
        ----------
        node:

        Returns
        -------
        Union[Tuple[str, str], None]
            If match returns the outer and inner span of match.

        Example
        -------

        >>> self._get_heading_id_spans(node)
        >>> ((7, 15), (9, 14))

        Raises
        ------
        ValueError
        """
        if self._is_heading(node):
            raw_leaf = node.children[0]
            match_obj = self.heading_id_pattern.search(raw_leaf.content)
            if match_obj is not None:
                return match_obj.regs
            else:
                return None
        else:
            raise ValueError("Wrong type of node")

    def _heading_class_spans(self, node):
        if self._is_heading(node):
            raw_leaf = node.children[0]
            if isinstance(raw_leaf, RawText) is False:
                raise ValueError(self._error)
            match_obj = self.classes_pattern.search(raw_leaf.content)
            if match_obj is not None:
                return match_obj.regs
            else:
                return None, None
        else:
            raise TypeError("Wrong type of node")

    def _add_to_top_paragraph(self, leveltwo_header_idx, new_node):
        """
        Add LogoEntry node just below `leveltwo_header_idx` (Second level with id's node index)

        Parameters
        ----------
        leveltwo_header_idx : Integer
            The index of the level two Heading two which Dates should be added
        """
        self.doc.children.insert(leveltwo_header_idx + 1, new_node)

    def add_node_by_match_idx(
        self, nodes: Union[Locations, Dates], new_node_class: Type[Any]
    ):
        """
        General method for adding node by matching
        idx. The matching is made on secondary level headers.

        Parameters
        ----------
        nodes: Union[Locations, Dates]
            Object derived from collections.UserDict class.
        new_node_class: Type[Any]
            A Class callable.
            On node match, the attributes of the matched node(s) from `nodes`
            are passed to new_node_class instanciation.

        Warning
        -------
        If you wish to render the parsed document, you have to make sure all `new_node_class` are registered
            in the renderer.
        """
        if len(self.heading_index) == 0:
            self.heading_index = self._headings_with_id_idx(self.doc)
            replace = True
        else:
            replace = False

        for i in range(len(self.heading_index)):
            pos = list(self.heading_index.keys())[i]
            # Match with Dates
            if replace:  # replace on first call
                heading = self.doc.children[pos]
                # extract id
                outer_span, inner_span = self._get_heading_id_spans(heading)
                raw_leaf = heading.children[0]
                indice = raw_leaf.content[inner_span[0] : inner_span[1]]
                to_replace = raw_leaf.content[outer_span[0] : outer_span[1]]
                self.doc.children[pos].children[0].content = raw_leaf.content.replace(
                    to_replace, ""
                ).rstrip()  # replace the {#id} with empty string
            else:
                indice = self.heading_index[pos]
            try:
                node = nodes[indice]
            except KeyError:
                node = None

            if node is not None:
                node_attributes = (
                    name for name in dir(node) if not name.startswith("_")
                )
                dictionnary = {key: getattr(node, key) for key in node_attributes}
                new_node = new_node_class(**dictionnary)
                self._add_to_top_paragraph(
                    leveltwo_header_idx=pos, new_node=new_node
                )  # operates directly on AST

            # Correct registered indices for addition of node
            h_index_items = list(self.heading_index.items())
            self.heading_index = OrderedDict(
                [(key, value) for key, value in h_index_items[0 : i + 1]]
                + [(key + 1, value) for key, value in h_index_items[i + 1 :]]
            )

        return self

    def add_dates(self, dates: Dates):
        """
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

        Example
        --------

        >>> from cliriculum.renderers import Renderer
        >>> from cliriculum.deserializers import Dates
        >>> from cliriculum.markdown import ParseMd
        >>> from cliriculum.loaders import load_json
        >>> parsed = ParseMd("README.md")
        >>> d = load_json("dates.json")
        >>> dates = Dates(d)
        >>> doc = parsed.add_dates(dates=dates).doc
        >>> with Renderer() as r:
        >>>     html = r.render(doc)
        """
        self.add_node_by_match_idx(nodes=dates, new_node_class=PeriodEntry)
        return self

    def _search_for_classes(self, doc):
        classes_location = OrderedDict()
        for i, leaf in enumerate(doc.children):
            # issubclass
            # isinstance
            if isinstance(leaf, Heading):
                outer_span, inner_span = self._heading_class_spans(leaf)
                if (leaf.level == 1) and (outer_span is not None):
                    classes_location[i] = outer_span, inner_span
        return classes_location

    def add_class(self):
        """
        Adds class to heading such as:

        .. code-block:: markdown

           Heading {class="<i class="fa-solid fa-graduation-cap"}

        """
        classes = self._search_for_classes(self.doc)
        for i, v in classes.items():
            outer_span, inner_span = v
            heading = self.doc.children[i]
            raw_leaf = heading.children[0]
            class_ = raw_leaf.content[inner_span[0] : inner_span[1]]
            to_replace = raw_leaf.content[outer_span[0] : outer_span[1]]
            new_text = raw_leaf.content.replace(to_replace, "").rstrip()
            heading.children[0].content = new_text
            print(f"NEW_TEXT {new_text}")
            print(self.doc.children[i].children)
            self.doc.children[i].children[0] = Span(
                heading.children[0]
            )  # not necessary
            self.doc.children[i].children.insert(0, Class(class_))

        return self

    def add_contact(self, contact: Contact, top: bool = True):
        """

        Parameters
        ----------
        contact : Contact
        top : bool, optional
            Whether to add to the top, by default True

        Example
        -------

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
            src=contact.email.logo,
            width=contact.email.width,
            height=contact.email.height,
            url=email_url,
            classes=contact.email.classes,
            text=contact.email.text,
        )
        website = URLEntry(
            src=contact.website.logo,
            width=contact.website.width,
            height=contact.website.height,
            url=contact.website.url,
            classes=contact.website.classes,
            text=contact.website.text,
        )
        socials = SocialBlock(
            [
                URLEntry(
                    src=social.logo,
                    width=social.width,
                    height=social.height,
                    url=social.url,
                    classes=social.classes,
                    text=social.text,
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
            text=contact.number.text,
        )
        children = [name, profession, email, website, socials, number]

        if contact.profile.logo is not None:
            profile = ImageEntry(
                src=os.path.basename(contact.profile.logo),
                height=contact.profile.height,
                width=contact.profile.width,
                id="profile_pic",
            )
            children = [profile] + children

        contact_block = ContactBlock(children=children)

        if top is False:
            self.doc.children.append(contact_block)
        else:
            self.doc.children.insert(0, contact_block)

            self.heading_index = {
                key + 1: value for key, value in self.heading_index.items()
            }

        return self

    def add_location(self, locations: Locations):
        self.add_node_by_match_idx(nodes=locations, new_node_class=LocationEntry)
        return self
