from pathlib import Path
from typing import Iterator, NamedTuple, Optional
#
from promnesia.common import get_logger, Extraction, Url, PathIsh, Res, Loc, file_mtime, logger
#
#
import mistletoe # type: ignore
from mistletoe.span_token import AutoLink, Link, RawText # type: ignore
import mistletoe.block_token as BT # type: ignore
from mistletoe.html_renderer import HTMLRenderer # type: ignore
#
#
renderer = HTMLRenderer()
#
#
block_tokens = tuple(getattr(BT, name) for name in BT.__all__)

import re#
#
class Parsed(NamedTuple):
    url: Url
    title: Optional[str]
    # context: Optional[str]
#
#
HTML_MARKER = '!html '
Result = Res[Parsed]

RE_URL = "https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)"

def _ashtml(block) -> str:
    res = renderer.render(block)
    if res.startswith('<p>') and res.endswith('</p>'):
        res = res[3: -4] # meh, but for now fine
    return res


class Parser:
    def __init__(self, path: Path):
        self.doc = mistletoe.Document(path.read_text())

    def _extract(self, cur, last_block) -> Iterator[Parsed]:
        if not isinstance(cur, (AutoLink, Link, RawText)):
            return

        if isinstance(cur, (AutoLink, Link)):
            url = cur.target
            if cur.children and isinstance(cur.children[0], RawText):
                title = cur.children[0].content
            else:
                title = None
            matches = re.findall(RE_URL, url)
            if matches:
                yield Parsed(url=url, title=title)
        else:
            matches = re.findall(RE_URL, cur.content)
            if matches:
                yield Parsed(url=matches[0], title=None)
            return


    def _walk(self, cur, last_block) -> Iterator[Result]:
        if isinstance(cur, block_tokens):
            last_block = cur

        try:
            yield from self._extract(cur, last_block)
        except Exception as e:
            logger.exception(e)
            yield e

        children = getattr(cur, 'children', [])
        for c in children:
            yield from self._walk(c, last_block=last_block)


    def walk(self):
        yield from self._walk(self.doc, last_block=None)

class Visit(NamedTuple):
    url: Url
    title: Optional[str]


def extract_from_file(fname: PathIsh) -> Iterator[Extraction]:
    path = Path(fname)
    fallback_dt = file_mtime(path)

    p = Parser(path)
    for r in p.walk():
        if isinstance(r, Exception):
            yield r
        else:
            yield Visit(
                url=r.url,
                title=r.title
                # dt=fallback_dt,
                # locator=Loc.file(fname), # TODO line number
                # context=r.context,
            )
#

# class TextParser(Parser):
#     '''
#     Used to extract links/render markdown from text, e.g. reddit/github comments
#     Instead of chunking blocks like for files, this returns the entire
#     message rendered as the context
#     '''
#     def __init__(self, text: str):
#         self.doc = mistletoe.Document(text)
#
#
#     def _doc_ashtml(self):
#         '''
#         cached html representation of the entire html message/document
#         '''
#         if not hasattr(self, '_html'):
#             self._html = HTML_MARKER + _ashtml(self.doc)
#         return self._html
#
#
#     def _extract(self, cur, last_block = None) -> Iterator[Parsed]:
#         print(cur)
#         if not isinstance(cur, (AutoLink, Link)):
#             return
#         print(cur.content)
#         yield Parsed(url=cur.target, context=self._doc_ashtml())
#
#
# def extract_from_text(text: str) -> Iterator[Result]:
#     '''
#     assume this is rendering something like a github/reddit markdown message
#     use the entire contents of the comment/body as the context
#     '''
#     # note: returns Result (link/context), not Visit
#     # the callee function has to insert dt/duration etc.
#     print("extract from text")
#     yield from TextParser(text).walk()

#
# # fp="/home/f1/dev/notes/1/arch-config/apple-ios-iphone-support.md"
# # fp="/home/f1/tmp/markdown.md"
# fp="/home/f1/dev/notes/testparser.md"
# def read_file(fp):
#     f = open(fp, "r")
#     lines = f.readlines()
#     f.close()
#     return "".join(lines)
#
# from markdown_it import MarkdownIt
# from mdformat.renderer import MDRenderer
#
# mdit = MarkdownIt()
# env = {}
# tokens = mdit.parse(read_file(fp), env)
# for token in tokens:
#     print(tokens)
#     print("\n")
#
# # rendered_part = MDRenderer().render(tokens, mdit.options, env)
# # print(rendered_part)
# # ==========================================================
