"""Post bodies: clean the editor's HTML, then render it for reading.

`clean_html` runs on every save, so only a known set of tags and attributes is
stored. `render_html` adds syntax highlighting to code blocks with Pygments.
Pygments only emits <span class="..."> around escaped text, so its output is
as safe as its input.
"""

import html
import re

import nh3
from django.conf import settings
from django.utils.html import strip_tags
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.util import ClassNotFound

# Languages offered in the editor's code-block menu (value -> label)
LANGUAGES = {
    'python': 'Python',
    'javascript': 'JavaScript',
    'typescript': 'TypeScript',
    'html': 'HTML',
    'css': 'CSS',
    'sql': 'SQL',
    'bash': 'Shell',
    'json': 'JSON',
    'yaml': 'YAML',
    'java': 'Java',
    'c': 'C',
    'cpp': 'C++',
    'go': 'Go',
    'text': 'Plain text',
}

TAGS = {
    'p', 'br', 'h2', 'h3', 'strong', 'em', 'u', 's', 'code', 'pre', 'blockquote',
    'ul', 'ol', 'li', 'a', 'hr', 'img',
}
ATTRIBUTES = {
    'a': {'href'},
    'img': {'src', 'alt'},
    'code': {'class'},
}
UPLOAD_PREFIX = 'posts/'

EDITOR_HTML = re.compile(r'^\s*<(p|h2|h3|ul|ol|pre|blockquote|hr|img)\b', re.I)
EMPTY_IMG = re.compile(r'<img(?: alt="[^"]*")?>')
CODE_BLOCK = re.compile(r'<pre><code(?: class="language-([a-z+]+)")?>(.*?)</code></pre>', re.S)


def _attribute_filter(tag, attr, value):
    if tag == 'code' and attr == 'class':
        lang = value.removeprefix('language-')
        return value if value.startswith('language-') and lang in LANGUAGES else None
    if tag == 'img' and attr == 'src':
        # Only images uploaded through this site
        return value if value.startswith(settings.MEDIA_URL + UPLOAD_PREFIX) and '..' not in value else None
    return value


def text_to_html(text):
    """Plain text (old posts, or the no-JS textarea) -> paragraphs."""
    blocks = re.split(r'\n\s*\n', text.strip())
    return ''.join(
        '<p>' + '<br>'.join(html.escape(line) for line in block.splitlines()) + '</p>'
        for block in blocks if block.strip()
    )


def clean_html(raw):
    raw = raw or ''
    if not EDITOR_HTML.match(raw):
        raw = text_to_html(raw)
    clean = nh3.clean(
        raw,
        tags=TAGS,
        attributes=ATTRIBUTES,
        attribute_filter=_attribute_filter,
        url_schemes={'http', 'https', 'mailto'},
        link_rel='noopener noreferrer nofollow',
    )
    return EMPTY_IMG.sub('', clean)


BLOCK_END = re.compile(r'</(?:p|h2|h3|li|pre|blockquote)>|<br>')
CODE = re.compile(r'<pre>.*?</pre>', re.S)


def plain_text(clean, code=True):
    """Visible text; blocks are separated by a space. code=False drops code blocks."""
    if not code:
        clean = CODE.sub(' ', clean)
    return html.unescape(strip_tags(BLOCK_END.sub(lambda m: m.group(0) + ' ', clean)))


def render_html(clean):
    """Cleaned HTML -> HTML with highlighted code blocks."""
    def code_block(match):
        lang, code = match.group(1) or 'text', html.unescape(match.group(2))
        try:
            lexer = get_lexer_by_name(lang)
        except ClassNotFound:
            lexer = get_lexer_by_name('text')
        body = highlight(code, lexer, HtmlFormatter(nowrap=True))
        label = LANGUAGES.get(lang, 'Code')
        return f'<pre class="highlight" data-lang="{label}"><code class="language-{lang}">{body}</code></pre>'

    return CODE_BLOCK.sub(code_block, clean)


def pygments_css():
    return HtmlFormatter(style='monokai').get_style_defs('.highlight')
