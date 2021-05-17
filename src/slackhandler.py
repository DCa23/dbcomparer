class SlackHandler:

    def __init__(self, token, channel, filename):
        import slack
        self.__token = token
        self.__slackchannel = channel
        self.__filename = filename
        self.__client = slack.WebClient(token=token)

    def notifySlack(self):
        try:
            self.__client.files_upload(
                channels=self.__slackchannel,
                file=self.__filename,
                filename=self.__filename,
            )
        except Exception as e:
            self.__client.chat_postMessage(
                channel=self.__slackchannel,
                text="The file report.md Could not be sent over slack probably because is too big, please connect to the machine to download it\n" +
                str(e)
            )
