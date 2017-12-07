from sentence import Sentence as S


def main():
    text = input("Insert a phrase: ")
    s = S(text)
    s.info()
    # s.help()


if __name__ == "__main__":
    main()
