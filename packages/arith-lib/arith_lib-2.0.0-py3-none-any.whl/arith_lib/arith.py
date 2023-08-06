# -*- coding: utf-8 -*-

""" Module for miscellaneous arithmetic calculation
"""

__all__ = ('gcd', 'lcm', 'bezout', 'modulo_inv', 'chinese_remainder',
           'chinese_reminder', 'gene_pseudo_primes', 'is_prime', 'next_prime',
           'previous_prime', 'prime_factorization', 'divisors', 'phi',
           'moebius', 'to_base', 'frobenius', 'isqrt', 'is_miller_rabin_witness',
           'frobenius', 'isqrt', 'is_miller_rabin_witness', 'get_random_prime',
           'is_strong_pseudoprime', '__version__')

__version__ = '2.0.0'
__copyright__ = "none"
__author__ = "jm allard"
__email__ = "jma214@gmail.com"

import random, math

def _gcd2(a, b):
    """ Calculates the greatest common divisor (gcd) of a and b

    Deprecated, use math.gcd instead.
    Implements Euclide's algorithm.
    If a and b are both 0, returns 0

    :type a:    int >= 0
    :type b:    int >= 0

    :return:       gcd(a, b)
    :rtype:        int

    :Example:

    >>> _gcd2(0, 0)
    0
    >>> _gcd2(11, 0)
    11
    >>> _gcd2(0, 7)
    7
    >>> _gcd2(7**5 * 3**4, 7**2 * 3**6)
    3969
    """

    import warnings
    warnings.warn('_gcd2() is deprecated. Use faster math.gcd() instead',
                  DeprecationWarning, 2)

    while b:              # gcd(a, b) = gcd(b, r) with r = a % b, 0 <= r < b
        a, b = b, a%b     # repeat until r==0. returns gcd(b, 0) ->  b
    return a


def gcd(*arg):
    """ Calculates the greatest common divisor (gcd) of a list of int
    Usage: gcd(15, 20, 10) -> 5

    Always returns a positive integer, whatever the data signs are
    Return 0 if arg contains only zeros

    :type arg: iterable of int
    :return:   gcd(a, b, c, ...)
    :rtype:    int

    :Example:

    >>> gcd()
    Traceback (most recent call last):
    ...
    ValueError: Empty list of arguments

    >>> gcd(7, 14.0)
    Traceback (most recent call last):
    ...
    ValueError: Arguments shall be integers

    >>> gcd(0,0,0,0)
    0
    >>> gcd(11)
    11
    >>> gcd(0, 7)
    7
    >>> gcd(-15, -20)
    5
    >>> gcd(7**5 * 3**4, 7**2 * 3**6, -7**2 * 3**3)
    1323
    """

    if not arg:
        raise ValueError("Empty list of arguments")

    if not all(isinstance(n, int) for n in arg):
        raise ValueError("Arguments shall be integers")

    gcd_tmp = 0

    for n in arg:    

        gcd_tmp = math.gcd(gcd_tmp, abs(n))

    return gcd_tmp


def _lcm2(a, b):
    """ Calculates the least common multiple (lcm) of a and b

    Private function, do not use. Use lcm instead
    a and b shall not be both 0
    Use the relationship: gcd(a, b) * lcm(a, b) = a * b

    :type a:    int >= 0
    :type b:    int >= 0

    :return:       lcm(a, b)
    :rtype:        int

    :Example:

    >>> _lcm2(0, 0)
    Traceback (most recent call last):
    ...
    ZeroDivisionError: integer division or modulo by zero

    >>> _lcm2(0, 67)
    0
    >>> _lcm2(77, 0)
    0
    >>> _lcm2(7**4 * 11**3, 7**2 * 11**5)
    386683451
    """

    return a*b // math.gcd(a, b)


def lcm(*arg):
    """ Calculates the least common multiple (lcm) of a list of int
    Usage: lcm(6, 9, 12) -> 36 

    Always returns a positive integer whatever the data signs are
    Return 0 if arg contains at least one zero

    :type arg: iterable of int
    :return:   lcm(a, b, c, ...)
    :rtype:    int

    :Example:

    >>> lcm()
    Traceback (most recent call last):
    ...
    ValueError: Empty list of arguments

    >>> lcm(6, 8.1)
    Traceback (most recent call last):
    ...
    ValueError: Arguments shall be integers
    
    >>> lcm(8,1,0,9)
    0
    >>> lcm(11)
    11
    >>> lcm(7, -7)
    7
    >>> lcm(-7**5 * 3**4, 7**2 * 3**6, 7**2 * 3**3)
    12252303
    """

    if not arg:
        raise ValueError("Empty list of arguments")

    if not all(isinstance(n, int) for n in arg):
        raise ValueError("Arguments shall be integers")

    if not all(arg): return 0       # at least one 0 in arg

    lcm_tmp = 1

    for n in arg:

        lcm_tmp = _lcm2(lcm_tmp, abs(n))

    return lcm_tmp


def bezout(a, b):
    """ bezout function finds a particular integer solution
    (u, v) to the diophantine equation a.u + b.v = gcd(a, b)
    Returns (u, v, gcd(a, b))
    Usage: bezout(5, 8) -> (-3, 2, 1)   
    
    Implements extended Euclide's algorithm.

    :type a:    int 
    :type b:    int (a and b not both 0)

    :return:  (u, v, gcd(a,b))
    :rtype:   int x3

    :Example:

    >>> bezout(0, 0)
    Traceback (most recent call last):
    ...
    ValueError: a and b shall not be both 0

    >>> bezout(7.8, 9)
    Traceback (most recent call last):
    ...
    ValueError: a and b shall be integers
    
    >>> bezout(120, 23); bezout(-120, 23); bezout(-120, -23); bezout(120, -23)
    (-9, 47, 1)
    (9, 47, 1)
    (9, -47, 1)
    (-9, -47, 1)
    >>> bezout(1, 10); bezout(1, -10); bezout(10, 1); bezout(-10, 1)
    (1, 0, 1)
    (1, 0, 1)
    (0, 1, 1)
    (0, 1, 1)
    >>> bezout(-1, 10); bezout(-1, -10); bezout(10, -1); bezout(-10, -1)
    (-1, 0, 1)
    (-1, 0, 1)
    (0, -1, 1)
    (0, -1, 1)
    >>> bezout(0, 10); bezout(0, -10); bezout(-10, 0); bezout(10, 0)
    (0, 1, 10)
    (0, -1, 10)
    (-1, 0, 10)
    (1, 0, 10)
    >>> bezout(1, 0); bezout(-1, 0)
    (1, 0, 1)
    (-1, 0, 1)
    >>> bezout(1, 1); bezout(-1, 1); bezout(1, -1); bezout(-1, -1)
    (0, 1, 1)
    (0, 1, 1)
    (0, -1, 1)
    (0, -1, 1)
    >>> def test_bezout(a, b):
    ...     u, v, g = bezout(a, b)
    ...     return a*u+b*v==g and g==gcd(a, b)
    >>> all(test_bezout(a, b) \
    for a in range(-1000, 2000, 99) for b in range(-1000, 1000, 51))
    True
    """
    
    if a == 0  and b == 0:
        raise ValueError("a and b shall not be both 0")

    if not (type(a) is type(b) is int):
        raise ValueError("a and b shall be integers")
            
    sign_a = 1             # Do the calculation with abs(a) and abs(b)
    if a < 0:              # and change the sign of solutions (u, v)
        a = -a             # at the end if a or b are negative
        sign_a = -1
    
    sign_b = 1;
    if b < 0:
        b = -b
        sign_b = -1

    if a == 0: return 0, sign_b, b  # 0*u+b*v = gcd(0, b) = abs(b) -> 0, sign_b, b   
    if b == 0: return sign_a, 0, a  # a*u+0*b = gcd(a, 0) = abs(a) -> sign_a, 0, a
        
    u1, v1 = 1, 0                 # a = 1*a + 0*b  
    u2, v2 = 0, 1                 # b = 0*a + 1*b

    while True:                   # r(n-1) = u1*a + v1*b
                                  # r(n)   = u2*a + v2*b
                                  
        q, r = divmod(a, b)       # a = b*q + r

        if r == 0:
            return sign_a * u2, sign_b * v2, b
        
        u1, v1, u2, v2 = u2, v2, u1-q*u2, v1-q*v2
        a, b = b, r


def modulo_inv(a, b):
    """ This function provides the inverse of a modulo b
    (a integer != 0, b integer >= 2, gcd(a, b) == 1)
    Usage: modulo_inv(4, 11) -> 3   (4*3 = 12 = 1 (mod 11))
        

    :param a: The number to be inverted
    :type a: int != 0

    :param b: The modulo
    :type b: int >= 2, gcd(a,b) shall be 1

    :return: The inverse of a (mod b)
    :rtype: int, 1 <= modulo_inv(a, b) < b

    :Example:

    >>> modulo_inv(23.6, 12)
    Traceback (most recent call last):
    ...
    ValueError: a shall be an integer != 0

    >>> modulo_inv(0, 12)
    Traceback (most recent call last):
    ...
    ValueError: a shall be an integer != 0

    >>> modulo_inv(3, 2.5)
    Traceback (most recent call last):
    ...
    ValueError: b shall be an integer >= 2

    >>> modulo_inv(3, 1)
    Traceback (most recent call last):
    ...
    ValueError: b shall be an integer >= 2
    
    >>> modulo_inv(14, 21)
    Traceback (most recent call last):
    ...
    ValueError: gcd(a, b) shall be 1
    
    >>> for a in range(-1000, 1000, 11):
    ...     for b in range(2, 100, 7):
    ...         if not gcd(a, b)==1: continue
    ...         inv = modulo_inv(a, b)
    ...         assert 1 <= inv < b and (a*inv) % b == 1
    
    """

    if not (type(a) is int and a != 0):
        raise ValueError("a shall be an integer != 0")
    
    if not(type(b) is int and b >= 2):
        raise ValueError("b shall be an integer >= 2")
    
    if not gcd(a, b) == 1:
        raise ValueError("gcd(a, b) shall be 1")

    u, v, g = bezout(a, b)

    return u % b         # % b to get a number between 0 and b-1 (included)


def chinese_remainder(r, m):
    """ Solves the modular system (x is the integer unknow):   
    x = r1 mod m1
    x = r2 mod m2       Usage: chinese_remainder((3, 4, 5), (17, 11, 6)) -> 785
    ...                 for r1=3, r2=4, r3=5 and m1=17, m2=11, m3=6   -> x=785
    x = r_n mod m_n   
    
    r1, r2, ..., r_n, m1, m2, ..., m_n are some parameters
    m1, m2, ..., m_n shall be >= 2 and primes 2 per 2
    r=(r1, r2, ..., r_n) and m=(m1, m2, ..., m_n)

    :param r: The rests r1, r2, ... r_n
    :type r: An iterable of int (r1, r2, ... r_n)

    :param m: The modulo m1, m2, ..., m_n
    :type m: An iterable of int >= 1 (m1, m2, ..., m_n)

    :Example:

    >>> chinese_remainder((3, 4, 5), (17, 11, 6))
    785
    >>> chinese_remainder((2, 3, 2), (3, 5, 7))
    23
    >>> chinese_remainder((3, 5), (4, 9))
    23
    >>> chinese_remainder((2, 3, 2, 8), (12, 5, 7, 121))
    32678
    >>> chinese_remainder((3, 0), (2, 9))
    9
    """

    if not all(mi>=2 for mi in m):
        raise ValueError("Modulos shall be integers >= 2")
    
    for i in range(len(m)-1):    #  checks that modulo mi are prime 2 per 2
        for j in range(i+1, len(m)):
            if not gcd(m[i], m[j])==1:
                raise ValueError("modulo shall be prime 2 per 2")
    
    prod=1                 # prod = m1 * m2 * m3 * ...
    for mi in m:
        prod=prod*mi

    M=[]                   # M=[m2*m3*m4..., m1*m3*m4*..., m1*m2*m4*..., ...]
    for mi in m:
        M.append(prod // mi)

    U=[]
    for Mi, mi in zip(M, m):  # calculates all Mi inverse mod mi
        U.append(modulo_inv(Mi, mi))

    return sum(Ui*Mi*ri for Ui, Mi, ri in zip(U, M, r)) % prod

chinese_reminder = chinese_remainder # compatibility with older releases

    
def to_base(n, base=16, use_AF=True, sep=''):
    """Convert integer n from base 10 to base 'base'. Return a string.
    If use_AF is True, then characters A, ..., F are used instead
    of 10, ..., 15 when base is between 11 to 16.
    sep is a separator between digits after conversion. If sep is ''
    then digits are left justified with 0 if needed

    :param n:      The number to be converted
    :type n:       int >= 0

    :param base:   The base after conversion
    :type base:    int >= 2

    :param use_AF: Chars A-F used when True for base between 11 to 16
    :type use_AF:  Boolean

    :param sep:    A one char (or '') separator between digit after conversion
    :type sep:     str  (1 char or empty string '')

    :return:       nrepresentation in base 'base'
    :rtype:        str

    :Example:

    >>> to_base(0, base=9)
    '0'
    >>> to_base(167, base=2)
    '10100111'
    >>> to_base(351, base=17)
    '010311'
    >>> to_base(351, base=17, sep='.')
    '1.3.11'
    >>> to_base(347, base=12, use_AF=True)
    '24B'
    >>> to_base(65000, base=16, use_AF=True)
    'FDE8'
    >>> to_base(347, base=12, use_AF=True, sep='.')
    '2.4.B'
    >>> to_base(347, base=12, use_AF=False)
    '020411'
    >>> to_base(347, base=12, use_AF=False, sep='.')
    '2.4.11'
    """

    ## Checking function's parameters

    n=int(n)
    if n < 0:
        raise ValueError("Negative numbers not supported")

    base = int(base)
    if base < 2:
        raise ValueError("Base shall be at least 2")

    use_AF = bool(use_AF)

    sep = str(sep)
    if len(sep) > 1:
        raise ValueError("sep shall be a single char or an empty string")

    # Start conversion

    conv = ''
    mapping = "0123456789ABCDEF"
    l_base = len(str(base))

    if n== 0:
        return '0'

    first = True

    while n != 0:

        sep2 = '' if first else sep
        first = False

        n, remains = divmod(n, base)

        if base <= 16 and use_AF:
            conv = mapping[remains] + sep2 + conv

        elif sep != "":
            conv = str(remains) + sep2 + conv

        else:
            conv = str(remains).rjust(l_base, '0') + conv

    return conv


def is_miller_rabin_witness(a, n):
    """ Return True if 'a' is a Miller-Rabin witness for n.
        The existance of a witness for n proves that n is a
        composite integer. Return False otherwise
        
        If False, n is a strong probable prime in base a.
        In that case n can be prime or not
        
        n shall be an integer > 2
        a shall be an integer > 0 and non multiple of n

    Code for doctest:
    
    >>> is_miller_rabin_witness(0, 18)
    Traceback (most recent call last):
    ...
    ValueError: a shall be an int > 0 and non multiple of n

    >>> is_miller_rabin_witness(36, 18)
    Traceback (most recent call last):
    ...
    ValueError: a shall be an int > 0 and non multiple of n

    >>> is_miller_rabin_witness(18, 2)
    Traceback (most recent call last):
    ...
    ValueError: n shall be an integer > 2

    >>> is_miller_rabin_witness(3.4, 19)
    Traceback (most recent call last):
    ...
    ValueError: a shall be an int > 0 and non multiple of n

    >>> is_miller_rabin_witness(3, 19.1)
    Traceback (most recent call last):
    ...
    ValueError: n shall be an integer > 2
     
    >>> is_miller_rabin_witness(973, 4698)
    False
    >>> is_miller_rabin_witness(975, 4698)
    True
    >>> is_miller_rabin_witness(105, 447)
    True
    >>> is_miller_rabin_witness(2, 2039)
    False
    >>> is_miller_rabin_witness(105, 451)
    False
    >>> is_miller_rabin_witness(105, 449)
    False
    """

    # Check function arguments

    if not (isinstance(n, int) and n > 2):
        raise ValueError("n shall be an integer > 2")

    if not (isinstance(a, int) and a > 0 and a%n != 0):
        raise ValueError("a shall be an int > 0 and non multiple of n")
        
    
    d = n-1
    s = 0
    
    while d % 2 == 0:   # n-1 = 2**s * d with d odd
        s += 1
        d //= 2

    mod_exp = pow(a, d, n)  # a^b mod n
    
    if mod_exp == 1:
        return False

    if s > 0:
        if mod_exp == n-1:   # n-1 is -1 in modulo-n operations
            return False
    
    for r in range(1, s):
        mod_exp = pow(mod_exp, 2, n)
        if mod_exp == n-1:
            return False
        
    return True       


def is_prime(n, probabilist=True, k=100, seed=None, report=False):
    """ Return True if 'n' is detected as a prime, False if 'n'
        is detected as a composite integer
        
        -For n strictly below 3317044064679887385961981 the test is
        determinist, so the result is sure.
        -For n above, if probabilist=True, the test is probabilist
        and k is the number of random bases which are tested. If n is
        prime then the test will always answers True but if n is composite
        there is a tiny probability 4**(-k) that the test also answers
        True. With k=100, this probability is less than 6E-61.
        -For n above, if probabilist=False, the test is determinist 
        (provided that the Riemann Hypothesis is true), but at the 
        expense of a large execution time for large numbers.

        If seed is None, the default behavior of the random generator is
        kept and initial state is derived from the system clock.
        If seed is a string, the state of the random generator used in
        probabilist mode is initialized with this string. So two runs
        will always provide the same result.

        if report=True, then a star "*" is printed every time about
        1% of the job is done, for n above 3317044064679887385961981.
        (With composite integers, the result is generally found quickly,
        before the first "*" is printed)

    Code for doctest:

    >>> is_prime(6.7)
    Traceback (most recent call last):
    ...
    ValueError: n shall be an integer

    >>> is_prime(0)
    False
    >>> is_prime(1)
    False
    >>> is_prime(2)
    True
    >>> is_prime(3)
    True
    >>> is_prime(4)
    False
    >>> is_prime(1009)
    True
    >>> is_prime(2047)
    False
    >>> is_prime(2053)
    True
    >>> is_prime(1373653)
    False
    >>> is_prime(25326001)
    False
    >>> is_prime(3215031751)
    False
    >>> is_prime(2152302898747)
    False
    >>> is_prime(3474749660383)
    False
    >>> is_prime(341550071728321)
    False
    >>> is_prime(3825123056546413051)
    False
    >>> is_prime(318665857834031151167461)
    False
    >>> is_prime(318665857834031151167483, seed="GHTExccx23")
    True
    >>> is_prime(3317044064679887385961981)
    False
    >>> n = 203163210419094069136593904378798659907
    >>> is_prime(n, True, k=100, seed="AZDFrteGGG")
    False
    >>> n = 3403311684869894502849877741894548647053253996789390142601
    >>> is_prime(n, k=201, report=True) #doctest: +NORMALIZE_WHITESPACE
    ********************************************************************************
    *********************True
    >>> n = 296667954763133900345829497663630705603
    >>> r=is_prime(n,False,report=True) #doctest: +NORMALIZE_WHITESPACE
    ********************************************************************************
    ********************
    >>> r
    True
    >>> is_prime(n,False)
    True
    """

    if not isinstance(n, int):
        raise ValueError("n shall be an integer")
    
    if n <= 3:
        if n==0 or n==1: return False
        if n==2 or n==3: return True
        
    if n % 2 == 0: return False

    # at that point, n is an odd integer >= 5

    A014233 = [2047, 1373653, 25326001, 3215031751, 2152302898747,
               3474749660383, 341550071728321, 341550071728321,
               3825123056546413051, 3825123056546413051,
               3825123056546413051, 318665857834031151167461,
               3317044064679887385961981]

    prime_list = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]

    for nprime, elt in enumerate(A014233, 1):       
        if n < elt:
            for a in prime_list[:nprime]:
                if is_miller_rabin_witness(a, n):
                    return False
            return True

    # at that point, n >= 3317044064679887385961981
    
    if probabilist == True:  # probabilist test

        if not seed is None:
            random.seed(seed)
        
        k100 = k//100 if k//100 else 1
        z=1
    
        for i in range(k):
            a = random.randint(2, n-2)
            if is_miller_rabin_witness(a, n):
                random.seed(None)
                return False
            if report:
                if i % k100 == 0:
                    print("*", end= "" if z%80 else "\n")
                    z+=1
                
        random.seed(None)
        return True

    else:  # determinist test

        stop = math.ceil(2*math.log(n)**2)
        stop100 = stop//100 if stop//100 else 1
        z=1
                                 
        for a in range(2, stop):
            if is_miller_rabin_witness(a, n):
                return False
            if report:
                  if a % stop100 == 0:
                      print("*", end= "" if z%80 else "\n")
                      z+=1
        return True


def is_strong_pseudoprime(a, n, test_if_composite=True):
    """ Return True is n is a strong pseudo prime to a base 'a',
        otherwise return False.
        A strong pseudo prime to a base 'a' is an odd number,
        composite, which pass the Miller-Rabin test on base 'a'
        if test_if_composite is False, n compositeness is assumed

    Code for doctest:

    >>> # Finds the 10 first strong pseudo primes in bases 2,3,4,5
    >>>
    >>> for a in (2, 3, 4, 5):  # doctest: +NORMALIZE_WHITESPACE
    ...     n, found = 4, 0
    ...     while found < 10:
    ...         if is_strong_pseudoprime(a, n):
    ...             found += 1
    ...             print(n)
    ...         n += 1
    2047 3277 4033 4681 8321 15841 29341 42799 49141 52633
    121  703  1891 3281 8401 8911  10585 12403 16531 18721
    341  1387 2047 3277 4033 4371  4681  5461  8321  8911
    781  1541 5461 5611 7813 13021 14981 15751 24211 25351
    >>>
    >>> # Finds the smallest strong pseudo prime in base 1 to 128
    >>>
    >>> for a in range(1, 129):  # doctest: +NORMALIZE_WHITESPACE
    ...     n = 4
    ...     while True:
    ...         if a%n != 0:
    ...             if is_strong_pseudoprime(a, n):
    ...                 print(n, end=" ")
    ...                 break
    ...         n += 1
    9 2047 121 341 781 217 25 9 91 9 133 91 85 15 1687 15 9 25 9 21 221 21
    169 25 217 9 121 9 15 49 15 25 545 33 9 35 9 39 133 39 21 451 21 9 481
    9 65 49 25 49 25 51 9 55 9 55 25 57 15 481 15 9 529 9 33 65 33 25 35 69
    9 85 9 15 91 15 39 77 39 9 91 9 21 85 21 85 247 87 9 91 9 91 25 93 1891
    95 49 9 25 9 25 133 51 15 451 15 9 91 9 111 55 65 57 115 57 9 49 9 15 91
    15 65 85 25 9 25 9 49
    >>>
    >>> # Test that C is a strong pseudo prime with base from 2 to 306
    >>>
    >>> all(is_strong_pseudoprime(a, C, False) for a in range(2, 307))
    True
    >>> is_strong_pseudoprime(307, C, False)
    False
    """

    if n % 2 == 0:                     # test odd parity
        return False

    if test_if_composite:              # test compositeness
        if is_prime(n):
            return False
    
    if is_miller_rabin_witness(a, n):  # does Miller Rabin test passes ?
        return False
    else:
        return True
    

# C is a strong pseudo prime relatively to all bases
# from 2 to 306 !
        
C = int(
"28871482380507712126714295971303939919776094592797"
"22700926516024197432303799152733116328983144639225"
"94197780311092934965557841894944174093380561511397"
"99994215424169339729054237110027510420801349667317"
"55152859226962916775325475044445856101949404200039"
"90443211677661994962953925045269871932907037356403"
"22737012784538991261203092448414947289768854060249"
"76768122077071687938121709811322297802059565867")


def gene_seq(n, reverse = False):
    """ when parameter n is 0, this function  provides a generator which
        yields 4, 2, 4, 2, 4, 6, 2, 6 and again 4, 2, 4, 2, 4, 6, 2, 6
        and again endless.

        If n is not 0, start occurs at sequence[n] instead
        (sequence = [4, 2, 4, 2, 4, 6, 2, 6])

        if reverse = True, data are provided in the reverse order

        :Exemple:

        >>> seq = gene_seq(0)
        >>> [next(seq) for i in range(20)]
        [4, 2, 4, 2, 4, 6, 2, 6, 4, 2, 4, 2, 4, 6, 2, 6, 4, 2, 4, 2]
        >>> seq = gene_seq(5)
        >>> [next(seq) for i in range(20)]
        [6, 2, 6, 4, 2, 4, 2, 4, 6, 2, 6, 4, 2, 4, 2, 4, 6, 2, 6, 4]
        >>> seq = gene_seq(0, reverse=True)
        >>> [next(seq) for i in range(20)]
        [6, 2, 6, 4, 2, 4, 2, 4, 6, 2, 6, 4, 2, 4, 2, 4, 6, 2, 6, 4]
        >>> seq = gene_seq(2, reverse=True)
        >>> [next(seq) for i in range(20)]
        [2, 4, 6, 2, 6, 4, 2, 4, 2, 4, 6, 2, 6, 4, 2, 4, 2, 4, 6, 2]
    """
    
    sequence = [4, 2, 4, 2, 4, 6, 2, 6]

    n = n%8
    sequence = sequence[n:] + sequence[:n]

    if reverse:
        sequence = sequence[::-1]
        
    while True:
        yield from sequence
        


def gene_pseudo_primes():
    """ A function which provides a generator which yields 2, 3, 5
    and then all integers non multiple of 2, 3, 5, endless

    :Exemple:

    >>> divisors = gene_pseudo_primes()
    >>> [next(divisors) for n in range(20)]
    [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 49, 53, 59, 61, 67]

    """

    seq = gene_seq(0)        
    div = 7
    
    yield from (2, 3, 5)

    while True:
        yield div
        div += next(seq)
        

offset = (                                (1, 7), (0, 7),
          (5, 0), (4, 0), (3, 0), (2, 0), (1, 0), (0, 0),
                          (3, 1), (2, 1), (1, 1), (0, 1),
                                          (1, 2), (0, 2),
                          (3, 3), (2, 3), (1, 3), (0, 3),
                                          (1, 4), (0, 4),
                          (3, 5), (2, 5), (1, 5), (0, 5),
          (5, 6), (4, 6), (3, 6), (2, 6), (1, 6), (0, 6)
          )

offset2 = ((-1, 6),
           ( 0, 7), (-1, 7), (-2, 7), (-3, 7), (-4, 7), (-5, 7),
           ( 0, 0), (-1, 0), (-2, 0), (-3, 0),
           ( 0, 1), (-1, 1),
           ( 0, 2), (-1, 2), (-2, 2), (-3, 2),
           ( 0, 3), (-1, 3),
           ( 0, 4), (-1, 4), (-2, 4), (-3, 4),
           ( 0, 5), (-1, 5), (-2, 5), (-3, 5),(-4, 5), (-5, 5),
           ( 0, 6)
           )

def next_prime(n=None, _state={"first":True, "n":None, "gen":None}):
    """ This function provides the first prime greater or equal to n.
        If n is not provided, the function outputs the first prime
        strictly greater than the previously found prime
        _state is reserved. Do not use

    Code for doctest:

    >>> next_prime(_state={"first":True, "n":None, "gen":None})
    Traceback (most recent call last):
    ...
    ValueError: n shall not be None at very first function use

    >>> next_prime(-1)
    Traceback (most recent call last):
    ...
    ValueError: n shall be a positive integer or None

    >>> next_prime(8.9)
    Traceback (most recent call last):
    ...
    ValueError: n shall be a positive integer or None

    >>> [next_prime(i) for i in range(17)]
    [2, 2, 2, 3, 5, 5, 7, 7, 11, 11, 11, 11, 13, 13, 17, 17, 17]

    >>> [next_prime(0)] + [next_prime() for i in range(17)]
    [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61]

    >>> [next_prime(i) for i in range(30,101)] # doctest: +NORMALIZE_WHITESPACE
    [31, 31, 37, 37, 37, 37, 37, 37, 41, 41, 41, 41, 43, 43, 47, 47, 47, 47,
    53, 53, 53, 53, 53, 53, 59, 59, 59, 59, 59, 59, 61, 61, 67, 67, 67, 67,
    67, 67, 71, 71, 71, 71, 73, 73, 79, 79, 79, 79, 79, 79, 83, 83, 83, 83,
    89, 89, 89, 89, 89, 89, 97, 97, 97, 97, 97, 97, 97, 97, 101, 101, 101]
     
    >>> n = 1000; lst = []
    >>> while n <= 2000:
    ...     p = next_prime(n)
    ...     lst.append(p)
    ...     n = p + 1
    >>> lst # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    [1009, 1013, 1019, 1021, 1031, 1033, 1039, 1049, 1051, 1061, 1063, 1069,
    1087, 1091, 1093, 1097, 1103, 1109, 1117, 1123, 1129, 1151, 1153, 1163,
    ...
    1879, 1889, 1901, 1907, 1913, 1931, 1933, 1949, 1951, 1973, 1979, 1987,
    1993, 1997, 1999, 2003]


    >>> len(lst)
    136

    >>> n=1
    >>> p=next_prime(0)
    >>> while next_prime() <= 100000:
    ...     n+=1
    >>> n
    9592
     
    """

    if not (n is None or (isinstance(n, int) and n >= 0)):
        raise ValueError("n shall be a positive integer or None")

    if _state["first"]:
        if n is None:
            raise ValueError("n shall not be None at very first function use")
        _state["first"] = False

    if n is None:
        
        n = _state["n"]
        seq = _state["gen"]
        if seq is None:
            return next_prime(n+1)
        else:
            n += next(seq)
               
    else:
        
        if n <= 7:
            for i in 2, 3, 5, 7:
                if n <= i:
                    _state["n"] = i
                    _state["gen"] = None
                    return i         
        
        rmd = n % 30
        n = n + offset[rmd][0]  
        rot = offset[rmd][1]    
        seq = gene_seq(rot)     
                              
    while True:

        if is_prime(n):
            _state["n"] = n
            _state["gen"] = seq
            return n

        n += next(seq)


def previous_prime(n=None, _state={"first":True, "n":None, "gen":None}):
    """ This function provides the first prime smaller or equal to n.
        If 0 <= n < 2, the function outputs None.
        If n is not provided, the function outputs the first prime
        strictly smaller than the previously found prime
        _state is reserved. Do not use

    Code for doctest:

    >>> previous_prime(_state={"first":True, "n":None, "gen":None})
    Traceback (most recent call last):
    ...
    ValueError: n shall not be None at very first function use

    >>> previous_prime(-1)
    Traceback (most recent call last):
    ...
    ValueError: n shall be a positive integer or None

    >>> previous_prime(8.9)
    Traceback (most recent call last):
    ...
    ValueError: n shall be a positive integer or None

    >>> print(previous_prime(0))
    None

    >>> [previous_prime(i) for i in range(17, 0, -1)]
    [17, 13, 13, 13, 13, 11, 11, 7, 7, 7, 7, 5, 5, 3, 3, 2, None]

    >>> [previous_prime(63)] + [previous_prime() for i in range(18)]
    [61, 59, 53, 47, 43, 41, 37, 31, 29, 23, 19, 17, 13, 11, 7, 5, 3, 2, None]

    >>> lst = [previous_prime(i) for i in range(101,30,-1)]
    >>> lst # doctest: +NORMALIZE_WHITESPACE
    [101, 97, 97, 97, 97, 89, 89, 89, 89, 89, 89, 89, 89, 83, 83, 83, 83, 83,
    83, 79, 79, 79, 79, 73, 73, 73, 73, 73, 73, 71, 71, 67, 67, 67, 67, 61, 61,
    61, 61, 61, 61, 59, 59, 53, 53, 53, 53, 53, 53, 47, 47, 47, 47, 47, 47, 43,
    43, 43, 43, 41, 41, 37, 37, 37, 37, 31, 31, 31, 31, 31, 31]
     
    >>> n = 2000; lst = []
    >>> while n >= 1000:
    ...     p = previous_prime(n)
    ...     lst.append(p)
    ...     n = p - 1
    >>> lst # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    [1999, 1997, 1993, 1987, 1979, 1973, 1951, 1949, 1933, 1931, 1913, 1907,
    1901, 1889, 1879, 1877, 1873, 1871, 1867, 1861, 1847, 1831, 1823, 1811,
    ...
    1093, 1091, 1087, 1069, 1063, 1061, 1051, 1049, 1039, 1033, 1031, 1021,
    1019, 1013, 1009, 997]
    >>> len(lst)
    136

    >>> n=1
    >>> p=previous_prime(100000)
    >>> while previous_prime() is not None:
    ...     n+=1
    >>> n
    9592
     
    """

    if not (n is None or (isinstance(n, int) and n >= 0)):
        raise ValueError("n shall be a positive integer or None")

    if _state["first"]:
        if n is None:
            raise ValueError("n shall not be None at very first function use")
        _state["first"] = False

    if n is None:
        
        n = _state["n"]
        seq = _state["gen"]

        if seq is None:
            return previous_prime(n-1)
        else:
            n -= next(seq)
        
    else:
        if n <= 7:
            for i in 7, 5, 3, 2:
                if n >= i:
                    _state["n"] = i
                    _state["gen"] = None
                    return i
                
            _state["n"] = 1
            _state["gen"] = None
            return None
        
     
        rmd = n % 30
        n = n + offset2[rmd][0]         
        rot = offset2[rmd][1]    
        seq = gene_seq(rot, reverse=True) 
                                      
    while True:

        if is_prime(n):
            _state["n"] = n
            _state["gen"] = seq if n > 7 else None
            return n

        n -= next(seq)


def get_random_prime(nbits, lessthan=False):
    """ Generate a random prime with 'nbits' bits
        If lessthan is False, prime has exactly 'nbits' bits
        If lessthan is True, prime has at most 'nbits' bits
        nbits shall be an integer >= 2

    Code for doctest:
    
    >>> get_random_prime(1)
    Traceback (most recent call last):
    ...
    ValueError: nbits shall be an integer >= 2

    >>> get_random_prime(7.9)
    Traceback (most recent call last):
    ...
    ValueError: nbits shall be an integer >= 2

    >>> get_random_prime(10, 4)
    Traceback (most recent call last):
    ...
    ValueError: lessthan shall be a boolean, True or False

    >>> s = set()
    >>> for i in range(1000):
    ...     s.add(get_random_prime(2))
    >>> s
    {2, 3}
    
    >>> s = set()
    >>> for i in range(1000):
    ...     s.add(get_random_prime(2, lessthan=True))
    >>> s
    {2, 3}
    
    >>> s = set()
    >>> for i in range(1000):
    ...     s.add(get_random_prime(3))
    >>> s
    {5, 7}
    
    >>> s = set()
    >>> for i in range(1000):
    ...     s.add(get_random_prime(3, lessthan=True))
    >>> s
    {2, 3, 5, 7}

    >>> for i in range(1000):
    ...     nbits = random.randint(64, 80)
    ...     n = get_random_prime(nbits)
    ...     assert n.bit_length() == nbits
    ...     assert is_prime(n)

    >>> for i in range(1000):
    ...     nbits = random.randint(64, 80)
    ...     n = get_random_prime(nbits, True)
    ...     assert n.bit_length() <= nbits
    ...     assert is_prime(n)
    
    """
        

    if not (isinstance(nbits, int) and nbits >= 2):
        raise ValueError("nbits shall be an integer >= 2")

    if not isinstance(lessthan, bool):
        raise ValueError("lessthan shall be a boolean, True or False")
    
    if lessthan:         # at most nbits

        n = random.getrandbits(nbits)
        p = next_prime(n)
        if p.bit_length() <= nbits:
            return p
        else:
            return previous_prime(n)

            
    else:                # exactly nbits
        n = random.getrandbits(nbits-1)
        n = (1 << nbits-1) | n             # set msb to 1
        p = next_prime(n)
        if p.bit_length() == nbits:
            return p
        else:
            return previous_prime(n)
        

def prime_factorization(n, frmt='tuple'):
    """ Provides the prime factorization of n (n >= 2)
    if frmt is set to 'str', a string is provided, eg '3**2 * 7**4 * 13'
    if frmt is set to 'tuple', a tuple is provided, eg ((3, 2), (7, 4), (13, 1))

    :Exemple:

    >>> prime_factorization(280917, frmt='str')
    '3**2 * 7**4 * 13'
    >>> prime_factorization(280917)
    ((3, 2), (7, 4), (13, 1))
    >>> prime_factorization(2, frmt='str')
    '2'
    >>> prime_factorization(2)
    ((2, 1),)

    >>> for i in range(2, 10000):
    ...     j = eval(prime_factorization(i, frmt='str'))
    ...     if i != j:
    ...         print(i, ' != ', j)

    >>> prime_factorization(1)
    Traceback (most recent call last):
    ...    
    ValueError: nber shall be an integer >= 2

    >>> prime_factorization(4, frmt='foo')
    Traceback (most recent call last):
    ...
    ValueError: frmt shall be 'tuple' or 'str'
    
    """

    nber = n

    divisors = gene_pseudo_primes()  # 2, 3, 5 then all non multiple of 2, 3, 5
    div = next(divisors)
    factors = []
    stop = math.sqrt(nber)

    ## checking inputs
    
    if not (isinstance(nber, int) and nber >= 2):
        raise ValueError("nber shall be an integer >= 2")

    if not (frmt == 'tuple' or frmt == 'str'):
        raise ValueError("frmt shall be 'tuple' or 'str'")

        
    ## main calculation
    
    while True:

        exp = 0

        while nber % div == 0:            # found div**exp as a factor
            nber //= div
            exp += 1

        if exp != 0:
            factors.append((div, exp))    # store found factor and updates
            stop = math.sqrt(nber)        # the search bound
            
        if div > stop:                    # a single prime with no exponent
            if nber != 1:                 # is still here
                factors.append((nber, 1))
            break

        div = next(divisors)              # possibly primes are run through

    ## format and provide output        

    if frmt == 'tuple':          ## provides a tuple eg ((3, 2), (7, 4), (13, 1))
        return tuple(factors)
    else:                        ## processing to return a string '3**2 * 7**4 * 13'
        return (''.
                join([str(tpl[0]) + "**" + str(tpl[1]) + " * " for tpl in factors]).
                replace('**1 ', ' ').
                rstrip(' *')
                )


def divisors(n):
    """ This function returns the list of the positive divisors
        of n including 1 and n. (n > 0)

    :Example:
    
    >>> divisors(1)
    [1]
    >>> divisors(45)
    [1, 3, 9, 5, 15, 45]
    >>> divisors(645)
    [1, 3, 5, 15, 43, 129, 215, 645]
    >>> all(n%d==0 for n in range(1000, 2000) for d in divisors(n) )
    True
    >>> divisors(0)
    Traceback (most recent call last):
    ...
    ValueError: n shall be > 0
       
    """

    if n <= 0: raise ValueError("n shall be > 0")

    if n==1: return [1]  # prime_factorization() fails when n=1

    # n = p1**m1 * p2**m2 + ...   (prime factorization of n)
    # factors = ((p1, m1), (p2, m2), ...)
    
    factors = prime_factorization(n)

    # P = (p1, p2, ...) and M = (m1, m2, ...)
    
    P, M = zip(*factors)  
    E = [0 for _ in M]

    def nxt():                  # "Increments" E 
                                # digit E(i) goes from 0 to M(i)
        for i in range(len(E)):          
            if E[i] == M[i]:
                E[i] = 0
                if i == len(E)-1:
                    return True
            else:
                E[i] += 1                
                return False

    divisors_list = []

    end = False
    
    while not end:

        prod = 1               # Calculation of p1**e1 * p2**e2 * ...
        for p, e in zip(P, E): # All n divisors are found when e1, e2, ...
            prod *= p**e       # goes from 0 to m1, 0 to m2, ...
            
        divisors_list.append(prod)

        end = nxt()

    return divisors_list        


def phi(n):
    """ Euler indicator function
        phi(n) provides the number of integers <= n and prime
        with n. (n shall be > 0)       

    >>> for n in range(1, 100): # doctest: +NORMALIZE_WHITESPACE
    ...    print(phi(n))  
            1   1   2   2   4   2   6   4   6
	4   10	4   12	6   8	8   16	6   18
	8   12	10  22	8   20	12  18	12  28
	8   30	16  20	16  24	12  36	18  24
	16  40	12  42	20  24	22  46	16  42
	20  32	24  52	18  40	24  36	28  58
	16  60	30  36	32  48	20  66	32  44
	24  70	24  72	36  40	36  60	24  78
	32  54	40  82	24  64	42  56	40  88
	24  72	44  60	46  72	32  96	42  60

    >>> phi(75409883)
    75409882
    >>> phi(0)
    Traceback (most recent call last):
    ...
    ValueError: n shall be > 0
    """

    if n <= 0: raise ValueError("n shall be > 0")
    
    if n==1: return 1

    # n = p1**m1 * p2**m2 *
    # factors = ((p1, m1), (p2, m2), ...)
    # phi(n) = (p1-1)*p1**(m1-1) * (p2-1)*p2**(m2-1) * ...
    
    product = 1
    for factors in prime_factorization(n):
        product *= (factors[0]-1)*factors[0]**(factors[1]-1)

    return product


def moebius(n):
    """ moebius function is defined from N* to {-1, 0, 1}
        - moebius(1) = 1, else
        - if n is a multiple of a square then moebius(n) = 0, else
        - if n if the product of an even number of primes, moebius(n) = 1, else
        - n is the product of an odd number of primes, moebius(n) = -1

        :Example:

        >>> moebius(1)
        1

        >>> for n in range(1, 31):  # doctest: +NORMALIZE_WHITESPACE
        ...     print(moebius(n), end=" ")
        1 -1 -1 0 -1 1 -1 0 0 1 -1 0 -1 1 1 0 -1 0 -1 0 1 1 -1 0 0 1 0 0 -1 -1

        >>> L = []
        >>> for n in range(1, 201):  # doctest: +NORMALIZE_WHITESPACE
	...     sum = 0; sum2 = 0
	...     for d in divisors(n):
	...	    sum += moebius(d)
	...         sum2 += moebius(d) * n // d
	...     L.append(phi(n)==sum2)
	...     print(sum, end="")
	...     if n%40==0: print()
	1000000000000000000000000000000000000000
	0000000000000000000000000000000000000000
	0000000000000000000000000000000000000000
	0000000000000000000000000000000000000000
	0000000000000000000000000000000000000000	
	>>> all(L)
	True

        >>> moebius(-5) 
        Traceback (most recent call last):
        ...
        ValueError: Parameter n shall be an integer >= 1
    """

    if not (isinstance(n, int) and n >= 1):
        raise ValueError("Parameter n shall be an integer >= 1")
        
            
    if n == 1:
        return 1

    # n = p1**m1 * p2**m2 *
    # factorization = ((p1, m1), (p2, m2), ...)
    
    factorization = prime_factorization(n)

    for factor in factorization: 
        if factor[1] >= 2:        # a square is found
            return 0

    if len(factorization) % 2 == 0:
        return 1                  # even number of primes
    else:
        return -1                 # odd number of primes
    

def frobenius(*A, n=None):
    """ frobenius function copes with equation "a1.x1 + a2.x2 + .. + ap.xp = n"
    where (a1, a2 ...) are the coefficients (at least 2 integers >= 2, with
    GCD(a1, a2, ...) == 1), (x1, x2 ...) are the unknows (integers >= 0) and
    n a parameter (integer >= 0).

    ## If n is not provided or n is None, function frobenius provides the
    greatest n denoted g(a1, a2 ...) for which the equation has no integer
    solution, nri the Number of Non Representable Integers (n for which the
    equation has no solution), and nri_list the list of these integers.
    frobenius is invoked like that: g, nri, nri_list = frobenius(a1, a2, ...)

    :Example:

    >>> g, nri, nri_list = frobenius(6, 9, 20)
    >>> g
    43
    >>> nri
    22
    >>> nri_list # doctest: +NORMALIZE_WHITESPACE
    (1, 2, 3, 4, 5, 7, 8, 10, 11, 13, 14, 16, 17, 19, 22, 23, 25, 28, 31, 34, 37, 43)

    >>> g, nri, nri_list = frobenius(31, 41)
    >>> g == 31*41 - 31 - 41 == 1199
    True
    >>> nri == (31-1)*(41-1)//2 ==  600
    True
    >>> nri_list # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22,
    ...
    922, 931, 932, 941, 942, 951, 952, 953, 962, 963, 972, 973, 982, 983, 993, 994,
    1003, 1004, 1013, 1014, 1024, 1034, 1035, 1044, 1045, 1055, 1065, 1075, 1076,
    1086, 1096, 1106, 1117, 1127, 1137, 1158, 1168, 1199)

    >>> frobenius(17, 18, 31, 32) # doctest: +NORMALIZE_WHITESPACE
    (109, 56, (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 19, 20, 21,
    22, 23, 24, 25, 26, 27, 28, 29, 30, 33, 37, 38, 39, 40, 41, 42, 43, 44, 45,
    46, 47, 55, 56, 57, 58, 59, 60, 61, 73, 74, 75, 76, 77, 78, 91, 92, 109))
    
    ## If n is provided, function frobenius yields all solutions to equation
    "a1.x1 + a2.x2 + .. + ap.xp = n", if any.

    :Example:

    >>> frobenius(11, 25, 47, n=342)  # five solutions
    ((22, 4, 0), (20, 3, 1), (18, 2, 2), (16, 1, 3), (14, 0, 4))
    
    >>> frobenius(17, 97, 51, n=577)  # no solution
    ()

    Some tests for bad inputs
    
    >>> frobenius(6.0, 7, 4)
    Traceback (most recent call last):
    ...
    ValueError: Coefficients shall be integers >= 2

    >>> frobenius(77, 1, 12, n=None)
    Traceback (most recent call last):
    ...
    ValueError: Coefficients shall be integers >= 2

    >>> frobenius(5, 88, 654, n=-5)
    Traceback (most recent call last):
    ...
    ValueError: Parameter n shall be a positive integer or None

    >>> frobenius(9, 33, 21)
    Traceback (most recent call last):
    ...
    ValueError: GCD of coefficients shall be 1
           
    """

    if not all([isinstance(a, int) and (a > 1) for a in A]):
        raise ValueError("Coefficients shall be integers >= 2")

    if not ((isinstance(n, int) and n >= 0) or n is None):
        raise ValueError("Parameter n shall be a positive integer or None")
    
    if gcd(*A) != 1:
        raise ValueError("GCD of coefficients shall be 1")

    def nxt():
        """ This function updates X to next value, and possibly updates M

            X is the list of variables x1, x2 ... of eq "a1.x1 +a2.x2 + ... = n"
            M is the list of max possible values for x1, x2 ..
            0 <= xi <= M(i)
            A is the list of coefficients a1, a2, ... of eq "a1.x1 +a2.x2 + ... = n"

            The function returns True when all X values have been scanned, else False
        """
                
        for i in range(len(X)):   # "increments" X, X[i] from 0 to M[i]
            if X[i] == M[i]:
                X[i] = 0
                if i == len(X)-1:
                    return True
            else:
                X[i] += 1
                for j in range(i):
                    M[j] = (n-sum(a*x for a, x in zip(A[i:], X[i:]))) // A[j] ## always >= 0
                    
                return False


    if n is None:  ## n not provided, search for g(a1, a2, ...), nri and nri_list
    
        n = 0               ## right member of equation "a1.x1 +a2.x2 + ... = n"
        successive_hit = 0
        previous_n_hit = -2 ## -2 because no successive hit wanted with n=0
        last_n_not_hit = 1
        nri = 0             ## Non Representable Integers (numbers "n" with no
                            ## solution to equation "a1.x1 +a2.x2 + ... = n"
        nri_list = []       ## List of all non representable integers
        list_n_hit = []     ## List of n for which a solution to equation has been found
                            ## multiple of already stored n are not stored again
        shortcut = 0

        while True:  ## "n" loop

            if any([n%d == 0 for d in list_n_hit]): ## is n a multiple of a previous found n
                                                    ## with a solution to equation ?
                if n == previous_n_hit + 1:          
                    successive_hit += 1
                else:
                    successive_hit = 1

                if successive_hit == min(A):  ## job finished
                    return last_n_not_hit, nri, tuple(nri_list)

                previous_n_hit = n
                n += 1
                shortcut += 1

                continue ## go to "n" loop              

            X = [0 for a in A]     ## variables x1, x2 ... of eq "a1.x1 +a2.x2 + ... = n"
            M = [n//a for a in A]  ## Max possible values of X coefficients

            while True:   ## "X" loop

                summation = sum([a*x for a, x in zip(A, X)])
                             
                if summation == n:    # A solution to "a1.x1 +a2.x2 + ... = n" has been found
                    
                    if n == previous_n_hit + 1:  ## looking for min(A) consecutive hits
                        successive_hit += 1
                    else:
                        successive_hit = 1

                    if successive_hit == min(A):  ## job finished
                        return last_n_not_hit, nri, tuple(nri_list)

                    previous_n_hit = n
                    
                    if n != 0:                    ## 0 excluded because these values
                        list_n_hit.append(n)      ## are used to test divisors of n
                    n += 1
                    
                    break  ## breaks "X" loop, so go to "n" loop

                else:
                    
                    end = nxt()  ## provides next X and possibly updates M

                    if end:      ## All X have been scanned, no solutions found
                        
                        last_n_not_hit = n
                        nri += 1
                        nri_list.append(last_n_not_hit)
                        n += 1
                        
                        break ## breaks "X" loop, so go to "n" loop
        

    else:  # n is provided, solve equation "a1.x1 +a2.x2 + ... = n"

        solutions = []
        X = [0 for a in A]
        M = [n//a for a in A]
        end = False

        while not end:

            if sum([a*x for a, x in zip(A, X)]) == n:
                solutions.append(tuple(X))
                
            end = nxt()

        return tuple(solutions)

def isqrt(n):
    """ Return the integer part of the square root of n
        n is an integer of any size

    Code for doctest:

    >>> isqrt(-1)
    Traceback (most recent call last):
    ...
    ValueError: n shall be an integer >= 0
    
    >>> isqrt(7.8)
    Traceback (most recent call last):
    ...
    ValueError: n shall be an integer >= 0

    >>> isqrt(0)
    0
    
    >>> isqrt(1)
    1
    
    >>> for n in range(100000):
    ...     sqr = isqrt(n)
    ...     assert sqr**2 <= n < (sqr+1)**2

    >>> for n in range(100000):
    ...     n**=2
    ...     sqr = isqrt(n)
    ...     assert sqr**2 == n
    
    >>> for i in range(1000):
    ...     n = random.getrandbits(256)
    ...     sqr = isqrt(n)
    ...     assert sqr**2 <= n < (sqr+1)**2
    
    >>> for i in range(1000):
    ...     n = random.getrandbits(128)
    ...     n**=2
    ...     sqr = isqrt(n)
    ...     assert sqr**2 == n

    """

    if not (isinstance(n, int) and n >= 0):
        raise ValueError("n shall be an integer >= 0")

    if n <= 1: return n
    
    # x0 = Initial value, choosen strictly greater that sqrt(n)

    x0 = 2**((n.bit_length()+1)//2)

    # Implementing Heron's method

    x1 = (x0 + n//x0) // 2       # this x1 is always < x0
    
    while x1 < x0:
        x0, x1 = x1, (x1 + n//x1) // 2

    return x0
                
## running doctest when module is executed

if __name__ == "__main__":
    import doctest
    doctest.testmod()
