from metatype import Dict

from linkedin_driver import _login, __site_url__

from linkedin_driver.utils import (
    open_contact,
    scroll_to_bottom,
    open_interest,
    text_or_default_accomp,
    open_accomplishments,
    open_more,
    flatten_list,
    one_or_default,
    text_or_default,
    all_or_default,
    get_info,
    get_job_info,
    get_school_info,
    get_volunteer_info,
    get_skill_info,
    personal_info,
    experiences,
    skills,
    recommendations
)

from linkedin_driver.utils import (
    filter_contacts
)

from selenium.webdriver.support.wait import WebDriverWait


class Contact(Dict):

    @classmethod
    def _filter(cls, keyword=None):
        '''
        Returns:
            Iterator.
        '''
        driver = _login()

        for item in filter_contacts(driver, keyword):
            yield(cls(item))

        driver.quit()
        raise NotImplemented

    @classmethod
    def _get(cls, url):

        driver = _login()

        record = {}

        # INTERESTS
        interests_data = open_interest(driver, url)
        record.update({'interests': interests_data})

        # CONTACT
        contact_data = open_contact(driver, url)
        record.update({'contact': contact_data})

        # <<SCROLL-DOWN>>
        scroll_to_bottom(driver, contact_url=url)

        # ACCOMPLISHMENTS
        accomplishments_data = open_accomplishments(driver)
        record.update({'accomplishments': accomplishments_data})

        # RECOMMENDATIONS
        recommendations_data = recommendations(driver)
        record.update({'recommendations':recommendations_data})

        # <<EXPAND-TABS>>
        open_more(driver)
        import bs4

        # PERSONAL-INFO
        soup = bs4.BeautifulSoup(driver.page_source, 'html.parser')
        personal_info_data = personal_info(soup)
        record.update({'personal_info': personal_info_data})

        # EXPERIENCES
        experiences_data = experiences(soup)
        record.update({'experiences': experiences_data})

        # SKILLS
        skills_data = skills(soup)
        record.update({'skills': skills_data})

        # END
        driver.quit()

        return cls(record)


    def send_message(self):
        raise NotImplemented

class Message(Dict):

    @classmethod
    def _get(self):
        raise NotImplemented

    @classmethod
    def _filter(self):
        raise NotImplemented

    def _update(self):
        raise NotImplemented


class Post(Dict):

    @classmethod
    def _get(self):
        raise NotImplemented

    @classmethod
    def _filter(cls):
        raise NotImplemented

    def _update(self):
        raise NotImplemented

    def add_comment(self):
        raise NotImplemented


class Comment(Dict):

    @classmethod
    def _get(self):
        raise NotImplemented

    @classmethod
    def _filter(self):
        raise NotImplemented

    def _update(self):
        raise NotImplemented


class PostLike(dict):

    @classmethod
    def _get(self):
        raise NotImplemented

    @classmethod
    def _filter(self):
        raise NotImplemented

    def _update(self):
        raise NotImplemented


class CommentLike(Dict):

    @classmethod
    def _get(self):
        raise NotImplemented

    @classmethod
    def _filter(self):
        raise NotImplemented

    def _update(self):
        raise NotImplemented

