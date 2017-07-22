import string
from unidecode import unidecode

ADWORDS_FORBIDDEN_CHARS = "!=?@%^*;~’`´,(){}<>|"


class TextHandler:
    """ Handling special characters and standardization.
    Often needed when working with queries, e.g. when matching them with keywords
    It's also useful when uploading keywords or ads since some characters aren't permitted
        -> see method "remove_forbidden_adwords_chars"
    """
    def __init__(self, text):
        assert isinstance(text, str)
        self.text = text
        self.without_punctuation = self.without_dashes_and_punctuation(text)
        self.decoded = self.decode(text)
        self.standardized = self.without_dashes_and_punctuation(self.decoded)
        self.variations = {self.text, self.decoded, self.without_punctuation, self.standardized}

    @staticmethod
    def decode(text):
        """ Convert utf8 characters to their closest representation
            ß -> ss
            é -> e
            ä -> a
            ...
        """
        return unidecode(text)

    @staticmethod
    def replace_dashes(text):
        """ Replace dashes and their close variants with spaces
        See https://en.wikipedia.org/wiki/Wikipedia:Hyphens_and_dashes
        Really fucked up shit...
        """
        text = text.replace("–", "-")  # en dash to hyphen
        text = text.replace("—", "-")  # em dash to hyphen
        text = text.replace("−", "-")  # minus to hyphen
        text = text.replace("-", " ")  # hyphen replace
        return text

    @staticmethod
    def remove_double_white_space(text):
        """ CAUTION: This removes other white space characters as well
                     Leading and trailing white spaces are also gone
        """
        return " ".join(text.split())

    @staticmethod
    def remove_punctuation(iterable, forbidden_chars=string.punctuation):
        """ Remove certain punctuation from text or iterable of text
        By default it removes all punctuation
        """
        type_of_input = type(iterable)
        if isinstance(iterable, str):
            new_text = iterable.translate({ord(c): None for c in forbidden_chars})
            return TextHandler.remove_double_space(new_text)
        elif isinstance(iterable, (set, list, tuple)):
            return type_of_input([TextHandler.remove_punctuation(elem, forbidden_chars=forbidden_chars)
                                  for elem in iterable])
        else:
            raise TypeError("Can't handle this data type: {type}".format(type=type_of_input))

    @staticmethod
    def remove_forbidden_adwords_chars(iterable):
        """ Removing Characters that aren't allowed by AdWords to be part of keyword texts """
        return TextHandler.remove_punctuation(iterable, forbidden_chars=ADWORDS_FORBIDDEN_CHARS)

    @staticmethod
    def without_dashes_and_punctuation(text):
        """ dashes to space and remove punctuation """
        text = TextHandler.replace_dashes(text)
        text = TextHandler.remove_punctuation(text)
        return text

    @staticmethod
    def standardize(text, to_lower=False):
        """ Standardized version without punctuation and special characters """
        text = TextHandler.decode(text)
        text = TextHandler.without_dashes_and_punctuation(text)
        text = text.lower() if to_lower else text
        return text
