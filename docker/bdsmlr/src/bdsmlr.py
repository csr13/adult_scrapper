import random
import os
import pdb
import time
import sys
import uuid

import requests
from lxml import html

from logger import get_logger
from settings import THIS_DIR, random_user_agent


logger = get_logger(__name__)



def get_image_links(page, tags=None, tag_method="or"):
    images_srcs = []
    posts = page.xpath('//div[@class="searchpost"]')
    for post in posts:
        imgs = []
        for img in post.cssselect("img"):
            for value in img.values():
                # technically could use .attrib['src']?
                imgs.append(value.strip())
        if tags:
            post_tags = [
                t.text_content().strip().replace("#", "")
                for t in post.cssselect("a.tag")
            ]
            if tag_method == "or":
                if any([t in post_tags for t in tags]):
                    images_srcs.extend(imgs)
            else:
                if all([t in post_tags for t in tags]):
                    images_srcs.extend(imgs)
        else:
            images_srcs.extend(imgs)
    return images_srcs


def main(
    username,
    password,
    url,
    blog_manager_name,
    start_page=1,
    random_pause=False,
    tags=[],
    tag_method="or",
    reusable_session=None
):
    url = url.rstrip("/")
    blog_name = url.replace("https://", "").rstrip("/").split(".")[0]
    ua = random_user_agent()

    ########################################################################
    # Handle tags.
    # ######################################################################
    # - Tags should be a string '#one #two #three # four'
    # - Tags are for only grabbing posts with those tags.
    ########################################################################

    if tag_method not in ["and", "or"]:
        raise SystemExit("Only AND or OR for tag method allowed.")

    if tags:
        if isinstance(tags, str):
            tags = [tags,]
        tags = [t.strip().lower().replace("#", "") for t in tags]
        logger.info(
            f'[{blog_name}] {tag_method.upper()}ing posts with tags: {", ".join(tags)}',
        )
    else:
        logger.info(f"[{blog_name}] No tags set, grabbing all posts")

    tags_str = "_{tag_method}_".join(tags)
    
    ###########################################################################
    # Start the session or check if it reusable, no login again, that theows
    # off backends.
    ###########################################################################

    if reusable_session is not None:
        if reusable_session.cookies.get("bdsmlr7_session") is not None:
            session = reusable_session
    else:
        session = requests.Session()
        session.headers.update({"User-Agent" : ua})
        login_page = html.fromstring(session.get("https://bdsmlr.com/login").text)
        login_hidden_value = login_page.xpath('//*[@class="form_loginform"]/input[@type="hidden"]/@value')[0]
        form_values = {
            "email": username, 
            "password": password, 
            "_token": login_hidden_value
        }
        rv = session.post("https://bdsmlr.com/login", data=form_values)
        if rv.ok:
            logger.info(f"[{blog_name}] Logged in ...")
    
    page = html.fromstring(session.get(f"{url}/archive", timeout=300).text)

    logger.info(f"[{blog_name}] Getting {blog_name} ({url}) archive ...")
    logger.info(f"[{blog_name}] Fetching images, page {start_page} ...")

    url = f"{url}/archive"
    params = {"page" : start_page}
    try:
        page_text = session.get(url,  params=params, timeout=300).text
    except Exception as error:
        logger.info("Could not get page %s from blug %s" % (
                current_page,
                blog_name
            )
        )
        return False, [], session

    page = html.fromstring(page_text)
    links = get_image_links(page, tags, tag_method)

    if random_pause:
        logger.info("random pause .. ")
        time.sleep(random.randint(0, 3))

   
    links = [l for l in links if l.startswith("https://")]
    
    logger.info(
        f"[{blog_name}] Done! Collected {len(links)} images on page {start_page}"
    )
     
    return True, links, session
