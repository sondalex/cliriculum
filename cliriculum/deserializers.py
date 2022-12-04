from datetime import date
from typing import Union, List, Dict


class Dates:
    """
    Deserializer of date metadata

    Attributes
    ----------
    periods: List[Periods]
    """

    def __init__(self, dictionary):
        """_summary_
        Examples
        --------
        >>> d = load_json("dates.json")
        >>> dates = Dates(d)
        """

        p = []
        for key in list(dictionary.keys()):
            p.append(Period(id=key, **dictionary[key]))
        self.periods = p

    def get_period(self, id):
        """
        Get period by id.
        First match returned.

        Parameters
        ----------
        id : _type_
            _description_
        """
        for period in self.periods:
            if period.idx == id:
                return period


class Period:
    """

    Attributes
    ----------
    start: str
    end: Union[str, None]
    idx: str
    logo: Union[str, None]
    width: Union[str, None]
    height: Union[str, None]
    classes: Union[str, None]
    classes has priority over logo in
    :py:mod:renderers
    """

    def __init__(
        self,
        id: str,
        start: date,
        end: Union[date, None] = None,
        logo: Union[str, None] = None,
        width: Union[str, None] = None,
        height: Union[str, None] = None,
        classes: Union[str, None] = None,
    ):
        """

        Parameters
        ----------
        id : str
            _description_
        start : str
            The start of the period
        end : Union[str, None]
            The end of the period
        logo: Union[str, None]
            A path towards a logo
        width: Union[str, None]
            Width of logo
        height:  Union[str, None]
            Height of logo
        classes: Union[str, None]
            css classnames
            `classes="class1 class2"`

        """
        if start is None:
            raise ValueError(
                "`start` of {classname} can not be set to None".format(
                    classname=self.__class__.__name__
                )
            )
        start = date.fromisoformat(start)
        if end is not None:
            end = date.fromisoformat(end)

        self.start = start
        self.end = end
        self.idx = id
        self.logo = logo
        self.width = width
        self.height = height
        self.classes = classes

    def __str__(self):
        return f"Index: {self.idx} with start:{self.start} and end: {self.end}"


class URL:
    """
    Attributes
    ----------
    logo: str
    url: str
    classes: str
        See :py:Period
    text: str
    """

    def __init__(
        self,
        url: str,
        logo: Union[str, None] = None,
        classes: Union[str, None] = None,
        text: Union[str, None] = None,
        width: Union[str, None] = None,
        height: Union[str, None] = None
    ):
        self.logo = logo
        self.url = url
        self.classes = classes
        self.text = text
        self.width = width
        self.height = height


class Website(URL):
    pass


class Social(URL):
    pass


class Number(URL):
    pass


class Email(URL):
    pass


class Socials:
    def __init__(self, socials_list: List[Dict]):
        """_summary_

        Parameters
        ----------
        socials_dict : List[Dict]
            A list of dictionaries
            with each dictionnary containing
            keys: "url" and "logo"

        Returns
        -------
        _type_
            _description_
        """

        self.children = [
            Social(
                logo=dict_["logo"],
                url=dict_["url"],
                classes=dict_["classes"],
                text=dict_["text"],
            )
            for dict_ in socials_list
        ]


class Contact:
    """
    Contact deserializer.

    Attributes
    ----------
    name: str
    profession: str
    email: Email
    website: Website
    socials: Socials
    number: Number
    """
    def __init__(self, name, profession, email, website, socials, number):
        """

        Examples
        --------

        >>> c = load_json("contact.json")
        >>> Contact(**c)
        """
        self.name = name
        self.profession = profession

        self.email = Email(**email)

        self.website = Website(**website)
        self.socials = Socials(socials)
        
        self.number = Number(**number)
