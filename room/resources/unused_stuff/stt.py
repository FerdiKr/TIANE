class Speech_to_Text:
    def __init__(self, vocabulary_list):
        self.vocabulary_list = vocabulary_list

    def recognize(self, audio_file_path):
        text = input('Hey Tiane,... ')
        if text == '':
            return "TIMEOUT_OR_INVALID"
        else:
            return text
