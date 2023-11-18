import datetime
import json
import logging
import os
import pprint
import random
import subprocess
import sys
import time
import tempfile

import requests

from bdsmlr import main
from logger import get_logger
from settings import THIS_DIR, MANAGER_URL, PUBLISHER_URL

logger = get_logger(__name__)


class Environment(object):
    def __init__(self):
        self.start_time = datetime.datetime.timestamp(
            datetime.datetime.now()
        )
        self.on = False
        self.streak_limit = 5
        self.max_images = 15
        self.blogs = {}
        self.credentials = []
        self.runs = {
            "main_runs" : 0, 
            "blog_runs" : []
        }
        self.load_blogs_from_manager()
        self.load_credentials_from_manager()

    def load_credentials_from_manager(self):
        try:
            query = requests.get(
                "%s/api/feed/get-feed-credentials" % MANAGER_URL
            )
            if query.status_code != 200:
                logger.info("Unable to load blogs from manager.")
        except Exception as error:
            logger.info(
                "Manager not available, if running docker-compose wait .."
            )
            exit(1)
        self.credentials = query.json()
        return True
 

    def load_blogs_from_manager(self):
        try:
            blogs_query = requests.get(
                "%s/api/blogs" % MANAGER_URL
            )
            if blogs_query.status_code != 200:
                logger.info("Unable to load blogs from manager.")
        except Exception as error:
            logger.info(
                "Manager not available, if running docker-compose wait .."
            )
            exit(1)
        blogs = blogs_query.json()
        logger.info("Loading blogs")
        for each in blogs:
            uid = each["uid"]
            self.blogs[uid] = each
        logger.info("Blogs loaded")


    def on_switch(self, status):
        if status == "on":
            self.on = True
        else:
            self.on = False
        return True


    def single_run(self, blog_uid):
        try:
            blog = self.blogs[blog_uid]
        except KeyError:
            return False, "Blog is not availalble in feed"

        blog_url = blog["url"]
        blog_name = blog["name"]
        blog_uid = blog["uid"]
        blog_pk = blog["pk"]
        start_time = datetime.datetime.now()
        run_data = {
            "blog_url" : blog_url,
            "blog_name" : blog_name,
            "blog_uid" : blog_uid,
            "times" : {
                "start_time" : start_time,
                "end_time" : None
            },
            "success" : False
        }

        try:
            creds = random.choice(self.credentials)
            email = creds.get("email")
            password = creds.get("password")
            scrape_result, image_links, session = main(
                email,
                password,
                blog_url, 
                blog_name,
                start_page=1,
            )
        except Exception as error:
            logger.error(str(error))
            run_data["error"] = str(error)
            scrape_result = False
        
        end_time = datetime.datetime.now()
        run_data["times"]["end_time"] = end_time 

        if scrape_result:
            logger.info(
                "successful run for %s" % blog_name
            )
            run_data["success"] = True
            self.runs["blog_runs"].append(run_data)
            self.download_and_upload_images(
                session, 
                image_links, 
                blog_name, 
                blog_uid
            )
        else:
            run_data["success"] = False
            self.runs["blog_runs"].append(run_data)
            return False, run_data

        return True, run_data


    @staticmethod
    def download_and_upload_images(
        session, 
        image_links, 
        blog_name, 
        blog_uid
    ):
        """
        Main Job to download and upload images
        """
        for image in image_links:
            bites = session.get(image)
            if not bites.status_code == 200:
                logger.info("Failed to download %s" % image)
                continue
            
            ext = image.split(".")[-1]
            link = image.split("/")[-1].split(".")[0] 
            name = "%s.%s" % (link, ext)
            server_image_name = name.split("-")[-1]
            server_image_model_name = server_image_name.split(".")[0]
            
            #########################################
            # Check to see if the resource exists
            # Before making a download.
            #########################################

            check = requests.get(
                "%s/api/images/image-exists/%s" % (
                    MANAGER_URL, 
                    server_image_model_name
                )
            )

            if check.json()["exists"]:
                continue

            tmp_location = "/tmp/{}".format(server_image_name)
            with open(tmp_location, 'wb') as ts:
                ts.write(bites.content)

            data = {
                "name" : server_image_model_name,
                "blog_uid" : blog_uid,
            }

            try:
                resp = requests.post(
                    "%s/api/images/" % MANAGER_URL,
                    data=data,
                    files={'image' : open(tmp_location, 'rb')}
                )
                if resp.status_code != 201:
                    pprint.pprint(resp.json())
                    raise Exception("Unable to upload")
                logger.info("Image uploaded successfully")
            except Exception as error:
                logger.info(str(error))

            os.unlink(tmp_location)
            continue

        return True, "tmp"
