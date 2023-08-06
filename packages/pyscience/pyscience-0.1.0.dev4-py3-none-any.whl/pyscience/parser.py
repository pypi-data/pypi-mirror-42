'''
pyscience - python science programming
Copyright (c) 2019 Manuel Alcaraz Zambrano

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
import pyscience

EXPONENTES = {
    '⁰': 0,
    '¹': 1,
    '²': 2,
    '³': 3,
    '⁴': 4,
    '⁵': 5,
    '⁶': 6,
    '⁷': 7,
    '⁸': 8,
    '⁹': 9,
}

def split_expression(expr):
    last_type = None
    tmp = ''
    result = []
    
    for c in list(expr):
        if last_type == 'str' and c != "'":
            tmp += c
            continue
        if c in list('1234567890'):
            typ = 'number'
        elif c in list('+-*/'):
            typ = 'operator'
        elif c in list(')'):
        #    typ = 'symbol'
            typ = 'none'
        elif c.islower():
            typ = 'none'
        #elif c == ')':
        #    typ = 'none'
        elif c in list('¹²³⁴⁵⁶⁷⁸⁹⁰'):
            typ = 'none'
        elif c == "'":
            if last_type != 'str':
                typ = 'str'
            else:
                result.append(tmp+c)
                last_type = 'str'
                tmp = ''
                continue
        else:
            typ = 'string'
        
        #tmp += c
        
        if typ != last_type or typ == 'none':
            
            result.append(tmp)
            tmp = ''
            last_type = typ
        tmp += c
    
    if tmp:
        result.append(tmp)
    
    return result[1:]

def expand(expr):
    expr = expr.replace(' ', '')
    expr = split_expression(expr)
    
    if pyscience.DEBUG:
        print('split:', expr)
    
    last_type = None
    result = ''
    
    for x in expr:
        #print(x)
        if x.islower():
            typ = 'variable'
        elif x.isupper() and x[-1] == '(':
            typ = 'function'
        elif x in list('+-*/') or x == '**':
            typ = 'operator'
        elif x[0] == x[-1] == "'":
            typ = 'string'
        elif x in list('¹²³⁴⁵⁶⁷⁸⁹⁰'):
            typ = 'exponent'
        elif x.isdigit():
            typ = 'number'
        elif x == ')':
            typ = 'symbol'
            #print('zsldflsdf')
        elif x == '(':
            typ = 'start_parenthesis'
        elif x in list(',\''):
            typ = 'none'
        else:
            raise SyntaxError("'" + x + "'")
        
        #if pyscience.DEBUG:
        #    print('Type:', last_type, typ)
        
        if (last_type in ('variable', 'exponent', 'symbol')) and (typ in ('number', 'variable')):
            result += '*'
        elif last_type == 'number' and typ == 'variable':
            result += '*'
        elif last_type in ('variable', 'number', 'symbol') and typ == 'start_parenthesis':
            result += '*'
        elif typ == 'exponent':
            if last_type != 'exponent':
                result += '**'
            result += str(EXPONENTES[x])
            last_type = 'exponent'
            continue
        
        result += x
        last_type = typ
    
    return result
        
    
    
