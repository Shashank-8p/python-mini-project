print("🔢 Armstrong Number Checker 🔢")
print("An Armstrong number equals the sum of its digits raised to the power of number of digits")
print("Example: 153 = 1³ + 5³ + 3³ = 1 + 125 + 27 = 153\n")

while True:
    try:
        num = int(input("➡️  Enter a number to check: "))
        break
    except ValueError:
        print("⚠️ Oops! That doesn't look like a valid number. Please try again.\n")

if num < 0:
    print("❌ Please enter a positive number!")
else:
    original_num = num
    num_digits = len(str(num)) if num > 0 else 1
    total = 0
    temp = num

    while temp > 0:
        digit = temp % 10
        total += digit ** num_digits
        temp //= 10

    print(f"\n📊 Number: {original_num}")
    print(f"📐 Number of digits: {num_digits}")

    print(f"\n🔍 Calculation:")
    temp = original_num
    digits = []
    while temp > 0:
        digits.append(temp % 10)
        temp //= 10
    digits.reverse()

    if num == 0:
        digits = [0]

    calculation_parts = [f"{d}^{num_digits}" for d in digits]
    print(f"   {' + '.join(calculation_parts)}")

    values = [f"{d**num_digits}" for d in digits]
    print(f"   = {' + '.join(values)}")
    print(f"   = {total}")

    if total == original_num or num == 0:
        print(f"\n✅ {original_num} is an Armstrong Number! 🎉")
    else:
        print(f"\n❌ {original_num} is NOT an Armstrong Number.")

    print("\n💡 Some Armstrong Numbers:")
    print("   1-digit: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9")
    print("   3-digit: 153, 370, 371, 407")
    print("   4-digit: 1634, 8208, 9474")