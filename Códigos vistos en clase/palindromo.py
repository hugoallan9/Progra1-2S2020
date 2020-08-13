
def primera_letra(palabra):
    return palabra[0]

def ultima_letra(palabra):
    return palabra[-1]

def medio_palabra(palabra):
    if palabra == '':
        return ''
    else:
        return palabra[1:-1]

def es_palindromo(palabra):
    if len(palabra) <= 1:
        return True
    else:
        if (primera_letra(palabra)).upper() == ultima_letra(palabra).upper():
            return es_palindromo(medio_palabra(palabra))
        else:
            return False

print(es_palindromo('Neuquen'))



