from typing import Optional

from pe_result.templates.template_base import HTMLTemplate


class SectionTemplate(HTMLTemplate):
    def __init__(
        self,
        html_path: str,
        title: str,
        width: Optional[str] = "100%",
        height: Optional[str] = "100%",
        text: Optional[str] = "100%",
    ):
        self.title = title
        self.width = width
        self.height = height
        self.html_path = html_path
        self.text = text

    def render(self) -> str:
        return self.html.format(
            title=self.title,
            width=self.width,
            height=self.height,
            html_path=self.html_path,
            text=self.text,
        )

    @property
    def html(self) -> str:
        return """
                <div class="row">
                    <!--CONTENT-->
                    <h1>{title}</h1>
                    <iframe
                        width="{width}"
                        height="{height}"
                        frameborder="0"
                        seamless="seamless"
                        scrolling="no"
                        src="{html_path}"
                    ></iframe>
                    <p>{text}</p>
                </div>
                """
