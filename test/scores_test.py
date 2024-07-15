from generators.scores import get_midas


def test_midas():
    input_tests = [
        [1, 3, 5, 4, 10],
        [0, 0, 0, 0, 0],
        [95, 95, 95, 95, 95],
        [90, 45, 90, 45, 45],
        [45, 90, 45, 90, 45],
        [50, 50, 50, 50, 50],
    ]

    for test in input_tests:
        print(f"For: {test}\n")
        print(get_midas(test))
        print(test)
        print("\n--------------------------------\n")


if __name__ == '__main__':
    test_midas()
