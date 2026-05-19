from math import sqrt, isqrt, gcd
from fractions import Fraction

print("\n\n", "=" * 20, " QUADRATIC EQUATION SOLVER ", "=" * 20)
print(
    "\nEasily find the roots of a quadratic equation in the form of ax^2 + bx + c = 0."
)
print("Input format should be: a, b, c\n")


#! Helper functions


def factor_radical(d):
    coeff = 1
    rem = d
    i = 2
    while i * i <= rem:
        while rem % (i * i) == 0:
            coeff *= i
            rem //= i * i  # rem = rem/(i*i) but in int format
        i += 1
    return coeff, rem


def simplify_fraction(whole, coeff, denom):
    g = gcd(gcd(abs(whole), abs(coeff)), abs(denom))
    return whole // g, coeff // g, denom // g


def format_non_rational(coeff, rem, unit=""):
    """
    returns the irrational/complex part of the final exact form
    unit="" for real roots, "i" for complex roots
    """
    rad = "" if rem == 1 else f"√{rem}"
    if coeff == 1 and rem == 1:
        return unit or "1"
    if coeff == 1:
        return f"{unit}{rad}"
    return f"{coeff}{unit}{rad}"


def format_roots(whole, nonrational, denom):
    if whole == 0:
        num1 = nonrational
        num2 = f"-{nonrational}"
    else:
        num1 = f"{whole} + {nonrational}"
        num2 = f"{whole} - {nonrational}"
    r1 = f"({num1}) / {denom}" if denom != 1 else num1
    r2 = f"({num2}) / {denom}" if denom != 1 else num2
    return r1, r2


#! Printing the roots


def rational_roots(a, b, r):
    x1 = Fraction(-b + r, 2 * a)
    x2 = Fraction(-b - r, 2 * a)
    print(f"🟢 Exact form:\n💠 {x1}\n💠 {x2}\n")
    print(f"🟢 Decimal form:\n💠 {float(x1):.4f}\n💠 {float(x2):.4f}\n")


def non_rational_roots(a, b, d, complex=False):
    """
    To display the exact form:
    - convert √D to coeff.√remainder form using factor_radical (returns coeff,rem)
    - divide numerator and denominator by gcd using simplify_fraction
    - convert coeff.√remainder to string using format_radical
    - format the final output using format_roots

    irrational roots looks like (whole_part +/- coeff.√rem) / denominator
    complex --> (whole_part +/- coeff.i√rem) / denominator
    """
    # For exact form
    coeff, rem = factor_radical(-d) if complex else factor_radical(d)
    whole, coeff, denom = simplify_fraction(-b, coeff, 2 * a)
    radical_part = (
        format_non_rational(coeff, rem, "i")
        if complex
        else format_non_rational(coeff, rem)
    )
    r1, r2 = format_roots(whole, radical_part, denom)

    # For decimal form (IRRATIONAL ROOTS ONLY)
    if not complex:
        x1 = (-b + sqrt(d)) / (2 * a)
        x2 = (-b - sqrt(d)) / (2 * a)
        print(f"🟢 Exact form:\n💠 {r1}\n💠 {r2}\n")
        print(f"🟢 Decimal form:\n💠 {x1:.4f}\n💠 {x2:.4f}\n")
    else:
        print(f"🟢 Complex roots:\n💠 {r1}\n💠 {r2}\n")


def find_roots(coeffs):
    a, b, c = coeffs
    if a == 0:
        print("Error: Not a quadratic equation (a=0)!")
        return
    d = b * b - 4 * a * c

    # REAL ROOTS
    if d >= 0:
        radical = sqrt(d)
        radical_int = isqrt(d)
        # Rational roots
        if radical_int * radical_int == d:
            rational_roots(a, b, radical_int)
        # Irrational roots
        else:
            non_rational_roots(a, b, d, complex=False)
    # COMPLEX ROOTS
    else:
        non_rational_roots(a, b, d, complex=True)


# User Input
inp = input("Enter a,b,c: ")
coeffs = [int(i.strip()) for i in inp.split(",") if i.strip()]

if len(coeffs) != 3:
    print("Please enter three coefficients.")
else:
    find_roots(coeffs)
