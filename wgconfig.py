from walnutgen.function import Function
from pathlib import Path
import os
import markdown

POSTS = [
    "posts/go-didnt-nail-simplicity.html",
]

class FnPostList(Function):
    def invoke(self, filename):
        html = ""
        for post in POSTS:
            meta = open(post[:-5], mode="r").read().split(" - ")
            html += f'<a href="/{post}">{meta[0]} <span class="gray"> - {meta[1]}</span></a><br />\n'
        
        return html

class FnGetTitle(Function):
    def invoke(self, filename):
        try:
            return open(filename[:-5], mode="r").read().split(" - ")[0]
        except:
            return "NO TITLE FOR " + filename

class FnFromMarkdown(Function):
    def invoke(self, filename):
        try:
            with open(filename[:-5] + ".md", mode="r") as f:
                content = f.read()
                return markdown.markdown(content, extensions=["fenced_code"])
        except:
            return "POST"

config = {
    "headers": [
        "templates/header.html",
    ],
    "footers": [
        "templates/footer.html"
    ],
    "files": [
        "index.html",
    ] + POSTS,
    "to_copy": [
        "res",
    ],
    "output_dir": "docs",

    "functions": {
        "post_list": FnPostList(),
        "get_post_title": FnGetTitle(),
        "from_markdown": FnFromMarkdown(),
    }
}