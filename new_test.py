if __name__ == "__main__":

    upper = input("Please give me upper input: ")
    lower = input("Please give me lower input: ")

    if (not "$" in upper) and (not "%" in upper):
        print("problem with upper")

    if not "$" in lower or not "%" in lower:
        print("problem with lower")
