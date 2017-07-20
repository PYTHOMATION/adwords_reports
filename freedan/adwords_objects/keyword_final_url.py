class KeywordFinalUrl:
    """ Final url of a keyword. The final url determines where a user will be redirected to after clicking on an Ad """
    def __init__(self, final_url, force_https=True):
        self.final_url = final_url

        if force_https:
            self.final_url = self.final_url.replace("http://", "https://")

    def construct_final_url(self):
        """ Call this function to construct the final url using your individual business logic """
        error_text = "Please inherit from this class and write your own function using your business logic."
        raise NotImplementedError(error_text)
