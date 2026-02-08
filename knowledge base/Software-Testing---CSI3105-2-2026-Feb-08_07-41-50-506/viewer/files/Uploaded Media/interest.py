def calculate_compound_interest(p, r, n):
    """
    Calculate compound interest over n years.

    :param p: Principal amount (initial investment)
    :param r: Annual interest rate (as a decimal)
    :param n: Number of years
    :return: Final amount after n years
    """
    a = p * (1 + r) ** n
    return a


# Given values
p = 1000  # Initial investment
r = 0.05  # Interest rate (5%)
n = 5  # Number of years

# Compute and print the total amount
final_amount = calculate_compound_interest(p, r, n)
print(f"Total amount after {n} years: ${final_amount:.2f}")
