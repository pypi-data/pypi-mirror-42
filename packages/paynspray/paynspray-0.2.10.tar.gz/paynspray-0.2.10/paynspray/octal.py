
def to_octal(string, prefix = b"\\"):
    """Returns the octal representation of a string"""
    octal = b""
    
    for b in bytearray(string):
        try:
            octal = octal + prefix + bytes("{:o}".format(b), 'ascii')
        except TypeError:
            octal = octal + prefix + "{:o}".format(b)
        
    return octal