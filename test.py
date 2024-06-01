def is_prime(n) -> bool:
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True


def sum_of_primes(start, end) -> int:
    total = 0
    for num in range(start, end + 1):
        if is_prime(num):
            total += num
    return total


def main():
    # Specify the range (e.g., from 1 to 50)
    start_range = 1
    end_range = 10000

    # Calculate the sum of prime numbers within the specified range
    result = sum_of_primes(start_range, end_range)

    # Display the result
    print(f"The sum of prime numbers between {start_range} and {end_range} is {result}")
