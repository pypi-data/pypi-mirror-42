import os.path


MAX_YOUTUBE_TITLE_LENGTH = 100
MAX_YOUTUBE_DESCRIPTION_LENGTH = 5000
MAX_YOUTUBE_TAGS_LENGTH = 500

#see list of categories in categories.txt
YOUTUBE_CATEGORIES_ID_LIST = (1, 2, 10, 15, 17, 18, 19, 20, 21, 22, 23, 24, 25,
                               26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37,
                               38, 39, 40, 41, 42, 43, 44)

YOUTUBE_CATEGORIES_DICT = {"film": 1, "animation": 1,
                        "autos": 2, "vehicles": 2,
                        "music": 10}

VALID_PRIVACY_STATUSES = ('public', 'private', 'unlisted')


class Video(object):


    def __init__(self, file_path=None, title="", description="", tags=[], category=None):
        self.file_path = self.set_file_path(file_path)
        self.title = self.set_title(title)
        self.description = set_description(description)
        self.tags = set_tags(tags)
        self.category = set_category(category)
        self.privacy_status = "private"


    def set_file_path(self, file_path):
        if file_path is not None and os.path.isfile(file_path):
            self.file_path = file_path
        elif file_path is not None:
            print("File path does not exist")
            self.file_path = None

    def get_file_path(self):
        return self.file_path


    def set_title(self, title):
        if len(title) > MAX_YOUTUBE_TITLE_LENGTH:
            print("Title is too long: " + len(title))
        else:
            self.title = title

    def get_title(self):
        return self.title


    def set_description(self, description):
        if len(description) > MAX_YOUTUBE_DESCRIPTION_LENGTH:
            print("Description is too long: " + len(description))
        else:
            self.description = description

    def get_description(self):
        return self.description


    def set_tags(self, tags):
        """Sets tags to the video

        Parameters
        -----------

        tags
          set tags for the video in list format

        """

        if len("".join(tags)) > MAX_YOUTUBE_TAGS_LENGTH:
            print("Description is too long: " + len("".join(tags)))
        else:
            self.tags = tags

    def get_tags(self):
        return self.tags


    def set_category(self, category):
        category = category.lower()
        if category in YOUTUBE_CATEGORIES_ID_LIST:
            self.category = category
        elif category in YOUTUBE_CATEGORIES_DICT.keys():
            self.category = YOUTUBE_CATEGORIES_DICT[category]
        elif category is None:
            category = None
        else:
            print("Not a valid category")
            self.category = None

    def get_category(self):
        return self.category


    def set_privacy_status(self, privacy_status):
        if privacy_status not in VALID_PRIVACY_STATUSES:
            print("Not a valid privacy status: " + privacy_status)
        else:
            self.privacy_status = privacy_status

    def get_privacy_status(self):
        return self.privacy_status
























