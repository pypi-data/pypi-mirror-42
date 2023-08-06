import amncore.compat
import random
import struct

UpperAlpha = b"ABCDEFGHIJKLMNOPQRSTUVWXYZ"
LowerAlpha = b"abcdefghijklmnopqrstuvwxyz"
Numerals = b"0123456789"
Base32 = b"ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
Base64 = UpperAlpha + LowerAlpha + Numerals + b'+/'
Base64Url = UpperAlpha + LowerAlpha + Numerals + b'-_'
Alpha = UpperAlpha + LowerAlpha
AlphaNumeric = Alpha + Numerals
DefaultWrap = 60

try:
    # why bother with the extra list() cast if it's an extra step?
    HighAscii = amncore.compat.pack_s("128B", *range(0x80, 0xff + 1))
    LowAscii = amncore.compat.pack_s("32B", *range(0x00, 0x1f + 1))
    AllChars = amncore.compat.pack_s("256B", *range(0x00, 0xff + 1))
    Punctuation = amncore.compat.pack_s("31B", *(range(0x21, 0x2f + 1) + range(0x3a, 0x3F + 1) + range(0x5b, 0x60 + 1) + range(0x7b, 0x7e + 1)))
except Exception:
    # thanks py3 for saving us memory...NOT
    HighAscii = amncore.compat.pack_s("128B", *list(range(0x80, 0xff + 1)))
    LowAscii = amncore.compat.pack_s("32B", *list(range(0x00, 0x1f + 1)))
    AllChars = amncore.compat.pack_s("256B", *list(range(0x00, 0xff + 1)))
    Punctuation = amncore.compat.pack_s("31B", *(list(range(0x21, 0x2f + 1)) + list(range(0x3a, 0x3F + 1)) + list(range(0x5b, 0x60 + 1)) + list(range(0x7b, 0x7e + 1))))

TLDs = [b'com', b'net', b'org', b'gov', b'biz', b'edu']

States = [
    b"AK", b"AL", b"AR", b"AZ", b"CA", b"CO", b"CT", b"DE", b"FL", b"GA", b"HI",
    b"IA", b"ID", b"IL", b"IN", b"KS", b"KY", b"LA", b"MA", b"MD", b"ME", b"MI", b"MN",
    b"MO", b"MS", b"MT", b"NC", b"ND", b"NE", b"NH", b"NJ", b"NM", b"NV", b"NY", b"OH",
    b"OK", b"OR", b"PA", b"RI", b"SC", b"SD", b"TN", b"TX", b"UT", b"VA", b"VT", b"WA",
    b"WI", b"WV", b"WY"
    ]
    
Surnames = [
      b"adams", b"alexander", b"allen", b"anderson", b"bailey", b"baker", b"barnes",
      b"bell", b"bennett", b"brooks", b"brown", b"bryant", b"butler", b"campbell",
      b"carter", b"clark", b"coleman", b"collins", b"cook", b"cooper", b"cox",
      b"davis", b"diaz", b"edwards", b"evans", b"flores", b"foster", b"garcia",
      b"gonzales", b"gonzalez", b"gray", b"green", b"griffin", b"hall", b"harris",
      b"hayes", b"henderson", b"hernandez", b"hill", b"howard", b"hughes", b"jackson",
      b"james", b"jenkins", b"johnson", b"jones", b"kelly", b"king", b"lee", b"lewis",
      b"long", b"lopez", b"martin", b"martinez", b"miller", b"mitchell", b"moore",
      b"morgan", b"morris", b"murphy", b"nelson", b"parker", b"patterson", b"perez",
      b"perry", b"peterson", b"phillips", b"powell", b"price", b"ramirez", b"reed",
      b"richardson", b"rivera", b"roberts", b"robinson", b"rodriguez", b"rogers",
      b"ross", b"russell", b"sanchez", b"sanders", b"scott", b"simmons", b"smith",
      b"stewart", b"taylor", b"thomas", b"thompson", b"torres", b"turner", b"walker",
      b"ward", b"washington", b"watson", b"white", b"williams", b"wilson", b"wood",
      b"wright", b"young"
    ]
    
Names_Male = [
      b"aaron", b"adam", b"alan", b"albert", b"andrew", b"anthony", b"antonio",
      b"arthur", b"benjamin", b"billy", b"bobby", b"brandon", b"brian", b"bruce",
      b"carl", b"carlos", b"charles", b"chris", b"christopher", b"clarence", b"craig",
      b"daniel", b"david", b"dennis", b"donald", b"douglas", b"earl", b"edward",
      b"eric", b"ernest", b"eugene", b"frank", b"fred", b"gary", b"george", b"gerald",
      b"gregory", b"harold", b"harry", b"henry", b"howard", b"jack", b"james", b"jason",
      b"jeffrey", b"jeremy", b"jerry", b"jesse", b"jimmy", b"joe", b"john", b"johnny",
      b"jonathan", b"jose", b"joseph", b"joshua", b"juan", b"justin", b"keith",
      b"kenneth", b"kevin", b"larry", b"lawrence", b"louis", b"mark", b"martin",
      b"matthew", b"michael", b"nicholas", b"patrick", b"paul", b"peter", b"philip",
      b"phillip", b"ralph", b"randy", b"raymond", b"richard", b"robert", b"roger",
      b"ronald", b"roy", b"russell", b"ryan", b"samuel", b"scott", b"sean", b"shawn",
      b"stephen", b"steve", b"steven", b"terry", b"thomas", b"timothy", b"todd",
      b"victor", b"walter", b"wayne", b"william", b"willie"
    ]
    
Names_Female = [
      b"alice", b"amanda", b"amy", b"andrea", b"angela", b"ann", b"anna", b"anne",
      b"annie", b"ashley", b"barbara", b"betty", b"beverly", b"bonnie", b"brenda",
      b"carol", b"carolyn", b"catherine", b"cheryl", b"christina", b"christine",
      b"cynthia", b"deborah", b"debra", b"denise", b"diana", b"diane", b"donna",
      b"doris", b"dorothy", b"elizabeth", b"emily", b"evelyn", b"frances", b"gloria",
      b"heather", b"helen", b"irene", b"jacqueline", b"jane", b"janet", b"janice",
      b"jean", b"jennifer", b"jessica", b"joan", b"joyce", b"judith", b"judy", b"julia",
      b"julie", b"karen", b"katherine", b"kathleen", b"kathryn", b"kathy", b"kelly",
      b"kimberly", b"laura", b"lillian", b"linda", b"lisa", b"lois", b"lori", b"louise",
      b"margaret", b"maria", b"marie", b"marilyn", b"martha", b"mary", b"melissa",
      b"michelle", b"mildred", b"nancy", b"nicole", b"norma", b"pamela", b"patricia",
      b"paula", b"phyllis", b"rachel", b"rebecca", b"robin", b"rose", b"ruby", b"ruth",
      b"sandra", b"sara", b"sarah", b"sharon", b"shirley", b"stephanie", b"susan",
      b"tammy", b"teresa", b"theresa", b"tina", b"virginia", b"wanda"
    ]
    
def rand_base(length, bad, foo):
    """Random text generator"""

    list_one = list((amncore.compat.unpack_s("{}B".format(len(foo)), foo)))
    list_two = list((amncore.compat.unpack_s("{}B".format(len(bad)), bad)))

    cset = [x for x in list_one if x not in list_two]
    cset = list(set(cset))
    
    outp = []
    
    if len(cset) == 0:
        return ""
        
    for i in range(0, length):
        outp.append(random.choice(cset))
        
    return amncore.compat.pack_s("{}B".format(length), *outp)
    
def rand_text(length, bad = b'', chars = AllChars):
    """Returns random bytes of data"""
    return rand_base(length, bad, chars)

def rand_char(bad = b'', chars = AllChars):
    """Returns a random character"""
    return rand_text(1, bad, chars)
    
def rand_text_alpha(length, bad = b''):
    """Returns random bytes of alphabetical data"""
    foo = b""
    foo += UpperAlpha
    foo += LowerAlpha
    return rand_base(length, bad, foo)
    
def rand_text_alpha_lower(length, bad = b''):
    """Returns random bytes of lowercase alphabetical data"""
    foo = b""
    foo += LowerAlpha
    return rand_base(length, bad, foo)
    
def rand_text_alpha_upper(length, bad = b''):
    """Returns random bytes of uppercase alphabetical data"""
    foo = b""
    foo += UpperAlpha
    return rand_base(length, bad, foo)
    
def rand_text_alphanumeric(length, bad = b''):
    """Returns random bytes of alphanumeric data"""
    foo = b""
    foo += UpperAlpha
    foo += LowerAlpha
    foo += Numerals
    return rand_base(length, bad, foo)
    
def rand_text_hex(length, bad = b''):
    """Returns random bytes of alphanumeric hex data"""
    foo = b""
    foo += Numerals
    try:
        foo += LowerAlpha[0:6]
    except TypeError:
        # boo hoo we concatenated "bytes" and "str"...what the hell
        foo += bytes(LowerAlpha[0:6], 'latin-1')
    return rand_base(length, bad, foo)
    
def rand_text_numeric(length, bad = b''):
    """Returns random bytes of numeric data"""
    foo = Numerals
    return rand_base(length, bad, foo)

def rand_hostname():
    """Returns a random domain name"""
    host = []
    for i in range(0, random.randrange(3) + 1):
        host.append(rand_text_alphanumeric(random.randrange(10) + 1))
        
    host.append(random.choice(TLDs))
    return b'.'.join(host).lower()
    
def rand_state():
    """Returns a random US state name"""
    return random.choice(States)
    
def rand_surname():
    """Returns a random last name"""
    return random.choice(Surnames)
    
def rand_name():
    """Returns a random male or female name"""
    if random.randrange(10) % 2 == 0:
        return random.choice(Names_Male)
    else:
        return random.choice(Names_Female)
        
def rand_name_male():
    """Returns a random male name"""
    return random.choice(Names_Male)
    
def rand_name_female():
    """Returns a random female name"""
    return random.choice(Names_Female)
    
def rand_mail_address():
    """Returns a random email address"""
    return (rand_name() + b'.' + rand_surname() + b'@' + rand_hostname())
    
def rand_guid():
    """Returns a random GUID"""
    return b"{%s}" % (b"-".join(map(lambda a: rand_text_hex(a), [8, 4, 4, 4, 12])))

def to_rand_case(string):
    """Randomizes capitalization of a string"""
    buf = []
    for i in range(0, len(string)):
        if random.randrange(2) == 0:
            buf.append(string[i].upper())
        else:
            buf.append(string[i].lower())
    return b"".join(buf)
    
