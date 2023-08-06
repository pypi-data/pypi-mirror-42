from selenium.webdriver.common.keys import Keys

class Topic:
    def __init__(self, topic_url, session):
        self.driver = session
        self.driver.get(topic_url)

    def add_comment(self, text):
        field = self.driver.find_element_by_class_name('mentions-texteditor__contenteditable')
        field.send_keys(text)
        button = self.driver.find_element_by_class_name('comments-comment-box__submit-button')
        button.click()

class Comment:
    pass

class Contact:
    pass

class Message:
    pass
