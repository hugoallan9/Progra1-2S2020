x = 3
y = 3

if x < y:
    print(x, 'es menor que', y)
elif x > y:
    print(x, 'es mayor que', y)
else:
    print(x, 'es igual a', y)


if x < y:
    print(x, 'es menor que', y)
else:
    if x > y:
        print(x, 'es mayor que', y)
    else:
        print(x, 'es igual a', y)
