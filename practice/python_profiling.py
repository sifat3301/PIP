import cProfile
spam_words = list(range(100000000))  # list

def is_spam1(message):
    return message in spam_words

spam_words = set(range(100000000))

def is_spam2(message):
    return  message in spam_words


def main():
    is_spam1(500)
    is_spam2(500)

cProfile.run("main()")


