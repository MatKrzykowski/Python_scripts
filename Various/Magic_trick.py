import random as rd

def main():
    number = 11 + int(rd.random() * 88)
    print(number**3)
    print(input() == str(number))


if __name__ == "__main__":
    main()
