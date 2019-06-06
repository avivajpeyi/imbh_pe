from typing import List

from pe_result.templates import links
from pe_result.templates.section_template import SectionTemplate
from pe_result.templates.template_base import HTMLTemplate


class SummaryTemplate(HTMLTemplate):
    def __init__(self, title: str, sections: List[SectionTemplate]):
        self.title = title
        self.sections = "\n".join([section.render() for section in sections])

    def render(self) -> str:
        return self.html.format(
            stylesheet=links.STYLESHEET,
            documentation_link=links.BILBY_DOCS,
            repo_link=links.BILBY_REPO,
            logo_link=links.BILBY_LOGO,
            title=self.title,
            sections=self.sections,
        )

    @property
    def html(self) -> str:
        return """
        <html>
            <head>
                <link rel="stylesheet" href="{stylesheet}">
            </head>

            <body>
                 <!-- NAV BAR -->
                <nav class="blue">
                    <div class="nav-wrapper">
                      <a href="{documentation_link}" class="brand-logo">
                          <img src="{logo_link}" height="65" width="65" alt="Bilby">
                      </a>
                        <ul id="nav-mobile" class="right hide-on-med-and-down">
                            <li><a href="{documentation_link}">Documentation</a></li>
                            <li><a href="{repo_link}">Repository</a></li>
                        </ul>
                    </div>
                </nav>


                <!-- PAGE TITLE -->
                <div class="container">
                    <div class="row">
                        <div class="col-sm-4">
                            <h1 class="mt-4">{title}</h1>
                        </div>
                    </div>
                </div>


                <!-- PAGE CONTENT -->
                <div class="container">
                    {sections}
                </div>


            </body>
        </html>
        """
