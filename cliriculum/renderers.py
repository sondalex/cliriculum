from textwrap import dedent

from mistletoe.html_renderer import HTMLRenderer

from cliriculum.markdown import (
    Class,
    ContactBlock,
    DescriptionBlock,
    ImageEntry,
    LocationEntry,
    PeriodEntry,
    SocialBlock,
    Span,
    TextEntry,
    URLEntry,
)


class Renderer(HTMLRenderer):
    def __init__(self):
        super().__init__(
            DescriptionBlock,
            ContactBlock,
            SocialBlock,
            TextEntry,
            URLEntry,
            ImageEntry,
            LocationEntry,
            PeriodEntry,
            Class,
            Span,
        )

    @staticmethod
    def _image_html(token):
        if token.width is None:
            width = ""
        else:
            width = 'width="{}"'.format(token.width)
        if token.height is None:
            height = ""
        else:
            height = 'height="{}"'.format(token.height)
        identifier = ""
        if hasattr(token, "id"):
            if token.id is not None:
                identifier = 'id="{}"'.format(token.id)

        html = '<img src="{src}" {width} {height} {identifier}/>'
        return html.format(
            src=token.src, width=width, height=height, identifier=identifier
        )

    @staticmethod
    def _i_image_html(token):
        template = '<i class="{classes}"></i>'
        return template.format(classes=token.classes)

    def render_logo_entry(self, token):
        text = token.title
        parent_o = '<div class="box">'
        parent_c = "</div>"

        if token.classes is not None:
            html = "\n".join(
                [parent_o, self._i_image_html(token), f"<span>{text}</span>", parent_c]
            )
        else:
            if token.src is None:
                html = "\n".join([parent_o, f"<span>{text}</span>", parent_c])
            else:
                html = "\n".join(
                    [
                        parent_o,
                        self._image_html(token),
                        f"<span>{text}</span>",
                        parent_c,
                    ]
                )
        return dedent(html)

    def render_period_entry(self, token):
        return self.render_logo_entry(token)

    def render_location_entry(self, token):
        return self.render_logo_entry(token)

    def render_image_entry(self, token):
        if token.src is not None:
            return self._image_html(token)
        else:
            return ""

    def render_text_entry(self, token):
        pre = "<p>"
        post = "</p>"
        if token.emphasis == "bold":
            html = """
            <strong>{text}</strong>
            """.format(text=token.text)
        elif token.emphasis == "italic":
            html = """
            <i>{text}</i>
            """.format(text=token.text)
        else:
            html = """
            <p>{text}</p>
            """.format(text=token.text)
        return pre + dedent(html) + post

    def render_class(self, token):
        print(f"CLASSES: {token.classes}")
        return f'<i class="{token.classes}"> </i>'

    def render_span(self, token):
        return f"<span>{self.render_raw_text(token.text)}</span>"

    def render_url_entry(self, token):
        parent_o = '<div class="box">'
        parent_c = "</div>"
        url = token.url
        if token.text is None and token.url is not None:
            text = token.url
        elif token.text is None and token.url is None:
            return ""
        text = token.text
        if token.classes is not None:
            html = "\n".join(
                [
                    parent_o,
                    self._i_image_html(token),
                    f'<a href="{url}">{text}</a>',
                    parent_c,
                ]
            )
        else:
            if token.src is None:
                html = "\n".join([parent_o, f'<a href="{url}">{text}</a>', parent_c])

            else:
                html = "\n".join(
                    [
                        parent_o,
                        self._image_html(token),
                        f'<a href="{url}">{text}</a>',
                        parent_c,
                    ]
                )
        return dedent(html)

    def render_contact_block(self, token):
        template = """
        <div class="contact" id="contact">
        <div class="content">
        {inner}
        </div>
        </div>
        """

        return dedent(template.format(inner=self.render_inner(token)))

    def render_social_block(self, token):
        template = '<div class="social">\n{inner}\n</div>'
        inner = self.render_inner(token)
        return template.format(inner=inner)

    def render_description_block(self, token):
        template = (
            '<div class="description">\n<div class="content">\n{inner}\n</div>\n</div>'
        )
        inner = self.render_inner(token)
        return template.format(inner=inner)


class MainRenderer(Renderer):
    html_template = """
        <main id = "main" class="main">
        <div class="content">
        {main}
        </div>
        </main>
        """

    def render_document(self, token):
        """
        Renders document to html representation in `<main>...</main>` tags

        Parameters
        ----------
        token:

        Returns
        -------
        str
            An HTML snippet using template :py:attr:`MainRenderer.html_template`
        """
        return dedent(self.html_template.format(main=self.render_inner(token)))


class SideBarRenderer(Renderer):
    """
    Attributes
    ----------
    html_template: str
    """

    html_template = '<aside id="aside" class="aside">\n{sidebar}\n</aside>'

    def render_document(self, token) -> str:
        """
        Renders document to html representation in `<aside>...</aside>` tags

        Parameters
        ----------
        token:
            A node

        Returns
        -------
        str
            An HTML snippet using template :py:attr:`SideBarRenderer.html_template`
        """

        return self.html_template.format(sidebar=self.render_inner(token))
