from test_package_cookiebus.fact.fact_file import fact


def sum(n):

    if n == 1:
        return fact(1)

    return sum(n - 1) + fact(n)

