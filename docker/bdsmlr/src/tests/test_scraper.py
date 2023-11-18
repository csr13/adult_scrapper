import os
import pprint
import pdb
import sys
import unittest

sys.path.append("..")

from bdsmlr import main


class TestMain(unittest.TestCase):
    
    def setUp(self):
        self.blog_url = "https://queensofhearts.bdsmlr.com/"
        self.username = os.getenv("USERNAME")
        self.password = os.getenv("PASSWORD")
        self.blog_manager_name = "queensofhearts"
        
    def test_main_one_blog_scrape_no_tags(self):
        action, links, session = main(
            self.username, 
            self.password, 
            self.blog_url,
            self.blog_manager_name, 
            start_page=1, 
            random_pause=False,
            tags=[], 
            tag_method="or", 
            reusable_session=None
        )
        session.close()
        self.assertTrue(action)
    
    @unittest.skip(reason="TO DO testing")
    def test_main_one_blog_scrape_with_tags_or(self):
        raise NotImplementedError()

    @unittest.skip(reason="TO DO testing")
    def test_main_one_blog_scrape_with_tags_and(self):
        raise NotImplementedError()

    @unittest.skip(reason="Unfinished functionality")
    def test_reusable_session_two_pages(self):
        raise NotImplementedError()


if __name__ == "__main__":
    unittest.main()
