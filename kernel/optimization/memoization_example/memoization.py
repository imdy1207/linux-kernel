fib_values = [0, 1]

def fibonacci_optimized2(n):
    if n > len(fib_values):
        for i in range(len(fib_values)-1, n+1):
            val = fib_values[i-1] + fib_values[i]
            fib_values.append(val)
        return val
    
    return fib_values[n-1] + fib_values[n-2]