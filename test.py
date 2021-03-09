def solution(s):
    braille = ""
    for char in s:
        b0_asc = ord(char)
        if 65 <= b0_asc <= 90:
            braille += ("000001")
            braille += (ascToBraille(b0_asc - 33))

        elif 97 <= b0_asc <= 122:
            braille += (ascToBraille(b0_asc - 65))

        else:
            braille += ("000000")

    return braille


def ascToBraille(num):
    num = bin(num)[2:]

    while len(num) < 6:
        num += "0"

    evens = ""
    odds = ""

    for x in range(6):
        if (x + 1) % 2 == 0:
            evens += num[x]
        else:
            odds += num[x]
            
    return odds + evens

if __name__ == "__main__":
    print(solution("code"))
