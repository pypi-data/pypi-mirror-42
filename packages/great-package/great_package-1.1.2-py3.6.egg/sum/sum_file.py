from package.fact.fact_file import fact

def sum(n):
    if n == 1:
        return fact(1)
    else:
        return sum(n - 1) + fact(n)

if __name__ == '__main__':
    n = int(input())
    print(sum(n))