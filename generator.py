import os
import re
import markdown
from jinja2 import Template

settings = dict()
settings['page_name'] = 'testpage'
settings['style_sheet'] = 'style.css'


def gen_site_from_template(template, **kwargs):
    with open(template, 'r') as fh:
        content = fh.read()
    return Template(content).render(kwargs)


def convert_and_save_articles_to_html(filename):
    url = 'pages/%s.html' % os.path.splitext(os.path.basename(filename))[0]
    with open(filename, 'r') as fh:
        content = fh.read()
    html_article = markdown.markdown(content, extensions=['markdown.extensions.codehilite'])
    html_article = re.sub(r"<h1>(.*)</h1>", r'<h1><a href="%s">\1</a></h1>' % url.split("/")[1], html_article)
    write_to_file(url, gen_site_from_template('template.html', articles=[html_article], settings=settings))
    return html_article


def write_to_file(filename, content):
    with open(filename, 'w') as fh:
        fh.write(content)


if __name__ == '__main__':
    articles = [os.path.join('articles', f) for f in os.listdir('articles')]
    articles.sort(key=lambda x: os.path.getmtime(x))
    articles = list(map(convert_and_save_articles_to_html, articles))
    all_articles_page = gen_site_from_template('template.html', articles=articles, settings=settings)
    landing_page = gen_site_from_template('template.html', articles=articles[:3], settings=settings, landing=True)
    write_to_file('pages/all_articles.html', all_articles_page)
    write_to_file('pages/index.html', landing_page)
