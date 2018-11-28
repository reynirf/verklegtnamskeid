from lib.color import Color

class NoccoList:
    def choose_one(question, alternatives, key):
        print('[{}] {}: {}'.format(Color.return_colored('?', 'yellow'), question, alternatives[0]))
    def write_many():
        pass
    def checkbox():
        pass
