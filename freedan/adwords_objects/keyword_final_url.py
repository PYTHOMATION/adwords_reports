class KeywordFinalUrl:
    """ Final url of a keyword. The final url determines where a user will be redirected to after clicking on an Ad """
    def __init__(self, final_url, https=True):
        self.url = final_url

        self.https = https
        self.enforce_protocol()

    def enforce_protocol(self):
        if self.https:
            self.url = self.url.replace("http://", "https://")
            assert "https://" in self.url
        else:
            self.url = self.url.replace("https://", "http://")
            assert "http://" in self.url
