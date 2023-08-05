'''
Created on 09/01/2019

@author: a16daviddss
'''


def calcularDNI(dni):
    try:
        tabla = "TRWAGMYFPDXBNJZSQVHLCKE"  # letras del dni
        dig_ext = "XYZ"
        reemp_dig_ext = {'X':'0', 'Y':'1', 'Z':'2'}
        # tabla letras extranjero
        # letras que identifican extranjero
        numeros = "1234567890"
        dni = dni.upper()  # pasa letras a mayúsculas
        if len(dni) == 9:  # el dni debe tener 9 caracteres
            dig_control = dni[8]  # la letra
            dni = dni[:8]  # el número que son los 8 primeros
            if dni[0] in dig_ext:  # comprueba que es extranjero
                dni = dni.replace(dni[0], reemp_dig_ext[dni[0]])
            return len(dni) == len([n for n in dni if n in numeros]) and tabla[int(dni) % 23] == dig_control  # devuelve true si se dan las 2 condiciones o si no false
        return False
    except:
        print ('Error en la aplicacion')
    return None
