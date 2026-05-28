print("=" * 50)
print("PRIME NUMBER GENERATOR & ANALYZER")
print("=" * 50)

while True:
    print("\nChoose an option:")
    print("1. Check if a number is prime")
    print("2. Generate prime numbers up to N")
    print("3. Find primes in a range")
    print("4. Prime factorization")
    print("5. Find the Nth prime number")
    print("6. Exit")

    choice = input("\nEnter your choice (1-6): ")

    if choice == '1':
        print("\n" + "-" * 50)
        print("CHECK IF A NUMBER IS PRIME")
        print("-" * 50)
        
        try:
            is_prime = True
            num = int(input("Enter a number: "))
            
            if num < 2:
                print(f"\n{num} is NOT a prime number.")
                print("(Prime numbers must be greater than 1)")
            else:
                if num == 2:
                    is_prime = True
                elif num % 2 == 0:
                    is_prime = False
                else:
                    i = 3
                    while i * i <= num:
                        if num % i == 0:
                            is_prime = False
                            break
                        i += 2
                if is_prime:
                    print(f"\n{num} is a prime number.")
                else:
                    print(f"\n{num} is NOT a prime number.")
        
        except ValueError:
            print("Please enter a valid number!")
    
    elif choice == '2':
        print("\n" + "-" * 50)
        print("GENERATE PRIME NUMBERS UP TO N")
        print("-" * 50)
        
        try:
            limit = int(input("Enter the limit (N): "))
            
            if limit < 2:
                print("\nNo prime numbers exist below 2.")
            else:
                prime = [True] * (limit + 1)
                prime[0] = prime[1] = False

                p = 2

                while p * p <= limit:
                    if prime[p]:
                        multiple = p * p

                        while multiple <= limit:
                            prime[multiple] = False
                            multiple += p
                    p += 1
                primes = []
                for num in range(2, limit + 1):
                    if prime[num]:
                        primes.append(num)
                
                print(f"\nPrime numbers up to {limit}:")
                print(primes)
                print(f"\nTotal prime numbers: {len(primes)}")
                
                if len(primes) > 0:
                    print(f"Smallest prime: {primes[0]}")
                    print(f"Largest prime: {primes[-1]}")
        
        except ValueError:
            print("Please enter a valid number!")
    
    elif choice == '3':
        print("\n" + "-" * 50)
        print("FIND PRIMES IN A RANGE")
        print("-" * 50)
        
        try:
            start = int(input("Enter start of range: "))
            end = int(input("Enter end of range: "))
            
            if start > end:
                print("\nError: Start must be less than or equal to end!")
            elif end < 2:
                print("\nNo prime numbers exist below 2.")
            else:
                if start < 2:
                    start = 2
                
                prime = [True] * (end + 1)
                prime[0] = prime[1] = False

                p = 2

                while p * p <= end:
                    if prime[p]:
                        multiple = p * p

                        while multiple <= end:
                            prime[multiple] = False
                            multiple += p
                    p += 1

                primes = []

                for num in range(start, end + 1):
                    if prime[num]:
                        primes.append(num)
                
                print(f"\nPrime numbers between {start} and {end}:")
                if len(primes) == 0:
                    print("No prime numbers found in this range.")
                else:
                    print(primes)
                    print(f"\nTotal prime numbers: {len(primes)}")
        
        except ValueError:
            print("Please enter valid numbers!")
    
    elif choice == '4':
        print("\n" + "-" * 50)
        print("PRIME FACTORIZATION")
        print("-" * 50)
        
        try:
            num = int(input("Enter a number: "))
            
            if num < 2:
                print(f"\n{num} cannot be factorized into primes.")
            else:
                original_num = num
                factors = []
                divisor = 2
                
                while divisor * divisor <= num:
                    while num % divisor == 0:
                        factors.append(divisor)
                        num = num // divisor
                    divisor += 1
                
                if num > 1:
                    factors.append(num)
                
                print(f"\nPrime factorization of {original_num}:")
                print(f"{original_num} = {' × '.join(map(str, factors))}")
                
                unique_factors = []
                for factor in factors:
                    if factor not in unique_factors:
                        unique_factors.append(factor)
                
                print(f"\nUnique prime factors: {unique_factors}")
                print(f"Total prime factors (with repetition): {len(factors)}")
        
        except ValueError:
            print("Please enter a valid number!")
    
    elif choice == '5':
        print("\n" + "-" * 50)
        print("FIND THE NTH PRIME NUMBER")
        print("-" * 50)
        
        try:
            n = int(input("Enter the value of n: "))
            
            if n <= 0:
                print("\nPlease enter a positive number!")
            else:
                limit = 100

                while True:
                    prime = [True] * (limit + 1)
                    prime[0] = prime[1] = False

                    p = 2

                    while p * p <= limit:
                        if prime[p]:
                            multiple = p * p

                            while multiple <= limit:
                                prime[multiple] = False
                                multiple += p

                        p += 1

                    primes = []

                    for num in range(2, limit + 1):
                        if prime[num]:
                            primes.append(num)

                    if len(primes) >= n:
                        print(f"\nThe {n}th prime number is: {primes[n - 1]}")
                        break

                    limit *= 2
        
        except ValueError:
            print("Please enter a valid number!")
    
    elif choice == '6':
        print("\n" + "=" * 50)
        print("Thank you for using Prime Number Analyzer!")
        print("=" * 50)
        break
    
    else:
        print("\nInvalid choice! Please enter a number between 1 and 6.")
    
    print("\n" + "=" * 50)
