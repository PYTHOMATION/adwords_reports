class FinalUrl:
    """ Final url of a keyword or ad. Normally the final url of the Keyword determines where a user will
    be redirected to after clicking on an Ad.

    CAUTION: Might be necessary to be split into KeywordFinalUrl and AdFinalUrl later.
    """
    def __init__(self, url, https=True):
        self.url = url

        self.https = https
        self.enforce_protocol()

    def enforce_protocol(self):
        assert "http://" in self.url or "https://" in self.url
        if self.https:
            self.url = self.url.replace("http://", "https://")
        else:
            self.url = self.url.replace("https://", "http://")
