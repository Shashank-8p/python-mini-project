import math

print("🧮 Advanced Scientific Calculator 🧮")
print("📚 Perform arithmetic and scientific operations\n")

history = []

while True:

    print("=" * 60)
    print("📋 Choose an Operation:")
    print("1️⃣   Addition (+)")
    print("2️⃣   Subtraction (-)")
    print("3️⃣   Multiplication (×)")
    print("4️⃣   Division (÷)")
    print("5️⃣   Modulus (%)")
    print("6️⃣   Power (^)")
    print("7️⃣   Square Root (√)")
    print("8️⃣   Percentage")
    print("9️⃣   Decimal Calculation")
    print("🔟  Sine (sin)")
    print("1️⃣1️⃣ Cosine (cos)")
    print("1️⃣2️⃣ Tangent (tan)")
    print("1️⃣3️⃣ Logarithm (log)")
    print("1️⃣4️⃣ Factorial (!)")
    print("1️⃣5️⃣ Show History")
    print("1️⃣6️⃣ Clear History")
    print("1️⃣7️⃣ Delete Last History")
    print("0️⃣   Exit")
    print("=" * 60)

    choice = input("\n🎯 Enter your choice: ")

    # EXIT
    if choice == '0':
        print("\n👋 Thanks for using the calculator. Goodbye!\n")
        break

    # SHOW HISTORY
    elif choice == '15':

        print("\n📜 Calculation History:\n")

        if len(history) == 0:
            print("📭 No calculations found.\n")

        else:
            for item in history:
                print(f"➡️ {item}")

        print()

    # CLEAR HISTORY
    elif choice == '16':

        history.clear()
        print("\n🗑️ History Cleared Successfully!\n")

    # DELETE LAST HISTORY
    elif choice == '17':

        if len(history) == 0:
            print("\n📭 No history to delete.\n")

        else:
            deleted = history.pop()
            print(f"\n🗑️ Deleted: {deleted}\n")

    # SQUARE ROOT
    elif choice == '7':

        try:
            num = float(input("\n📥 Enter number: "))

            if num < 0:
                print("\n❌ Cannot find square root of negative number!\n")
                continue

            result = math.sqrt(num)

            calculation = f"√{num} = {result}"

            history.append(calculation)

            print(f"\n✨ Result: {calculation}\n")

        except ValueError:
            print("\n❌ Invalid input!\n")

    # PERCENTAGE
    elif choice == '8':

        try:
            num = float(input("\n📥 Enter number: "))

            result = num / 100

            calculation = f"{num}% = {result}"

            history.append(calculation)

            print(f"\n✨ Result: {calculation}\n")

        except ValueError:
            print("\n❌ Invalid input!\n")

    # DECIMAL CALCULATION
    elif choice == '9':

        try:
            num1 = float(input("\n📥 Enter first decimal number: "))
            num2 = float(input("📥 Enter second decimal number: "))

            result = num1 + num2

            calculation = f"{num1} + {num2} = {result}"

            history.append(calculation)

            print(f"\n✨ Result: {calculation}\n")

        except ValueError:
            print("\n❌ Invalid decimal input!\n")

    # SINE
    elif choice == '10':

        try:
            angle = float(input("\n📥 Enter angle in degrees: "))

            result = math.sin(math.radians(angle))

            calculation = f"sin({angle}) = {result}"

            history.append(calculation)

            print(f"\n✨ Result: {calculation}\n")

        except ValueError:
            print("\n❌ Invalid input!\n")

    # COSINE
    elif choice == '11':

        try:
            angle = float(input("\n📥 Enter angle in degrees: "))

            result = math.cos(math.radians(angle))

            calculation = f"cos({angle}) = {result}"

            history.append(calculation)

            print(f"\n✨ Result: {calculation}\n")

        except ValueError:
            print("\n❌ Invalid input!\n")

    # TANGENT
    elif choice == '12':

        try:
            angle = float(input("\n📥 Enter angle in degrees: "))

            result = math.tan(math.radians(angle))

            calculation = f"tan({angle}) = {result}"

            history.append(calculation)

            print(f"\n✨ Result: {calculation}\n")

        except ValueError:
            print("\n❌ Invalid input!\n")

    # LOGARITHM
    elif choice == '13':

        try:
            num = float(input("\n📥 Enter number: "))

            if num <= 0:
                print("\n❌ Logarithm only works for positive numbers!\n")
                continue

            result = math.log10(num)

            calculation = f"log({num}) = {result}"

            history.append(calculation)

            print(f"\n✨ Result: {calculation}\n")

        except ValueError:
            print("\n❌ Invalid input!\n")

    # FACTORIAL
    elif choice == '14':

        try:
            num = int(input("\n📥 Enter positive integer: "))

            if num < 0:
                print("\n❌ Factorial not defined for negative numbers!\n")
                continue

            result = math.factorial(num)

            calculation = f"{num}! = {result}"

            history.append(calculation)

            print(f"\n✨ Result: {calculation}\n")

        except ValueError:
            print("\n❌ Invalid input!\n")

    # BASIC OPERATIONS
    elif choice in ['1', '2', '3', '4', '5', '6']:

        try:
            num1 = float(input("\n📥 Enter first number: "))
            num2 = float(input("📥 Enter second number: "))

            if choice == '1':

                result = num1 + num2
                calculation = f"{num1} + {num2} = {result}"

            elif choice == '2':

                result = num1 - num2
                calculation = f"{num1} - {num2} = {result}"

            elif choice == '3':

                result = num1 * num2
                calculation = f"{num1} × {num2} = {result}"

            elif choice == '4':

                if num2 == 0:
                    print("\n❌ Division by zero is not allowed!\n")
                    continue

                result = num1 / num2
                calculation = f"{num1} ÷ {num2} = {result}"

            # MODULUS
            elif choice == '5':

                if num2 == 0:
                    print("\n❌ Modulus by zero is not allowed!\n")
                    continue

                result = num1 % num2
                calculation = f"{num1} % {num2} = {result}"

            # POWER
            elif choice == '6':

                result = num1 ** num2
                calculation = f"{num1}^{num2} = {result}"

            history.append(calculation)

            print(f"\n✨ Result: {calculation}\n")

        except ValueError:
            print("\n❌ Please enter valid numbers!\n")

    # INVALID CHOICE
    else:

        print("\n❌ Invalid choice! Please select a valid option.\n")
