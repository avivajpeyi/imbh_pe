def render():

    html_code = MAIN_TEMPLATE.format(title="awddas", sections="sersa")

    return


def get_main_template(title: str, sections: list):
    return MAIN_TEMPLATE.format(title=title, sections=sections.join("\n"))


SECTION_TEMPLATE = """
    <div class="row">
        <!--CONTENT-->
        <h1>{section_title}</h1>
        <iframe width="1000" height="550" frameborder="0" seamless="seamless" scrolling="no" src="{section_html_code}"></iframe>
        <p>{section_text}</p>
    </div>
"""

MAIN_TEMPLATE = """
<html>
    <head>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">
        <style>body {
            margin: 0 100;
            background: white;
        }</style>
    </head>

    <body>

    <!-- Page Title -->
    <div class="container">
        <div class="row">
            <div class="col-sm-4">
                <img src="https://git.ligo.org/uploads/-/system/project/avatar/1846/bilby.jpg" alt="Bilby Logo">
            </div>
            <div class="col-sm-4">
                <h1 class="mt-4">{title}</h1>
            </div>
            <div class="col-sm-4">
                <img src="https://git.ligo.org/uploads/-/system/project/avatar/1846/bilby.jpg" alt="Bilby Logo">
            </div>
        </div>
    </div>


    <!-- Page Content -->
    <div class="container">
        <!--SECTION ROWS-->
        {sections}
    </div>


    </body>
</html>

"""
