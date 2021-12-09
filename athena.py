import datetime
import fileinput
import glob
import os
import sys
import uuid
from datetime import timedelta, timezone
from urllib.parse import urljoin

from feedgen.feed import FeedGenerator
from flask import Flask, make_response, render_template, request
from flask_flatpages import FlatPages
from flask_frozen import Freezer
from flask_static_compress import FlaskStaticCompress

import config
from flatpandoc import FlatPagesPandoc

DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = ".md"
FREEZER_REMOVE_EXTRA_FILES = False
FREEZER_BASE_URL = "http://localhost/"
LOCAL_TIMEZONE = timezone(timedelta(seconds=7200), 'IST')

athena = Flask(__name__
        # , root_path='/Users/josh/Documents/research/dev/athena'
        )
athena.config.from_object(__name__)
pages = FlatPages(athena)
freezer = Freezer(athena)
athena.jinja_env.comment_start_string = "{##}"
FlatPagesPandoc("markdown+raw_tex+yaml_metadata_block", athena, pre_render=True)
compress = FlaskStaticCompress(athena)


@athena.route("/feed.rss")
def recent_feed():
    fg = FeedGenerator()
    fg.title(config.config["title"])
    fg.subtitle(config.config["title"] + " Atom Feed")
    fg.link(
        {
            "href": config.config["url"] + "/feed.rss",
            "rel": "self",
            "type": "application/rss+xml",
        }
    )

    for page in pages:
        if not page.meta.get("ispage"):
            fe = fg.add_entry()
            fe.title(page["title"])
            fe.description((str(page.__html__())))
            fe.link({"href": config.config["url"] + "/posts/" + page.path})
            fe.guid(str(uuid.uuid4()))
            fe.author({"name": config.config["author"]})
            fe.updated(
                datetime.datetime.combine(
                    page["date"], datetime.datetime.min.time(), tzinfo=LOCAL_TIMEZONE
                )
            )
            fe.published(
                datetime.datetime.combine(
                    page["date"], datetime.datetime.min.time(), tzinfo=LOCAL_TIMEZONE
                )
            )

    response = make_response(fg.rss_str(pretty=True))
    response.headers.set("Content-Type", "application/rss+xml")
    return response


@athena.route("/")
def index():
    posts = [page for page in pages if "ispage" not in page.meta]
    hpages = [page for page in pages if "ispage" in page.meta]
    return render_template(
        "index.html", pages=posts, hpages=hpages, config=config.config
    )


@athena.route("/<path:path>/")
def hardpagelink(path):
    hpage = ""
    for page in pages:
        if page.path == path:
            if page.meta["ispage"]:
                hpage = page
    hpages = [page for page in pages if "ispage" in page.meta]
    return render_template("hard.html", page=hpage, hpages=hpages, config=config.config)


@athena.route("/posts/<path:path>/")
def page(path):
    page = pages.get_or_404(path)
    hpages = [page for page in pages if "ispage" in page.meta]
    return render_template("page.html", page=page, hpages=hpages, config=config.config)


def cat():
    allp = os.path.join(os.getcwd(), "pages", "all.bib")
    bibs = os.path.join(os.getcwd(), "pages", "*.bib")
    with open(allp, "w") as f:
        for line in fileinput.input(glob.glob(bibs)):
            f.write(line)
        fileinput.close()


if __name__ == "__main__":
    # cat()
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()
    else:
        athena.run(port=5000)
