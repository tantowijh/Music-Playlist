import threading


def print_ini():
    print("Ini adalah fungsi ini")
    print(1)
    print(2)
    print(3)
    print(4)

def print_itu():
    print("Itu adalah fungsi itu")
    print(1)
    print(2)
    print(3)
    print(4)


# print_ini()
# print_itu()


# t1 = threading.Thread(target=print_ini)
# t1.start()
# t2 = threading.Thread(target=print_itu)
# t2.start()