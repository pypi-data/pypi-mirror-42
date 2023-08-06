"""
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
"""
"""
Created by Manuel Alcaraz on 22 May, 2018
"""

# 'Polynomial' module

from pyscience import algebra
from fractions import Fraction

class Polynomial:
    def __init__(self, *args, **kargs):
        self.monomials = kargs.get('monomials', [])
        self.numerical_term = kargs.get('numerical_term', 0)
    
    @property
    def degree(self):
        return max([x.degree for x in self.monomials])

    def __add__(self, value):
        if isinstance(value, algebra.Monomial):
            n=0
            len_monomials = len(self.monomials)
            for x in self.monomials:
                try:
                    # Intentar sumar los monomials
                    # "x += value" no vale porque devuelve un polinomio si no son iguales
                    if algebra.monomial.count_variables(x.variables) == algebra.monomial.count_variables(value.variables):
                        if self.monomials[self.monomials.index(x)].coefficient + value.coefficient != 0:
                            self.monomials[self.monomials.index(x)] += value
                        else:
                            del self.monomials[self.monomials.index(x)]
                    else:
                        raise ValueError
                    break
                except ValueError:
                    pass
                n+=1
            if n >= len_monomials: # No ha habido ninguno que sea igual
                self.monomials.append(value)
            if len(self.monomials) == 0:
                return self.numerical_term
            return self
        elif isinstance(value, Polynomial):
            R = Polynomial()
            R.numerical_term = self.numerical_term
            nm = 0
            for m in value.monomials:
                found = False
                
                for x in self.monomials:
                    if algebra.monomial.count_variables(x.variables) == algebra.monomial.count_variables(m.variables):
                        if x.coefficient + m.coefficient != 0:
                            R.monomials.append(x+m)
                            nm += 1
                        found = True
                        
                if not found:
                    R.monomials.append(m)
            
            if value.numerical_term:
                R.numerical_term += value.numerical_term
                
            if nm == 0:
                # Se han eliminado todos los monomios. Devolver un int
                return R.numerical_term
            
            return R
        elif isinstance(value, int):
            self.numerical_term += value
            return self
        elif isinstance(value, algebra.Variable):
            return self + algebra.Monomial(variables=value.name)
        else:
            raise TypeError(f'Cann\'t add a Polynomial to {type(value)}')
    
    def __radd__(self, value):
        return self + value

    def __sub__(self, value):
        if isinstance(value, algebra.Monomial):
            n=0
            len_monomials = len(self.monomials)
            for x in self.monomials:
                try:
                    # Intentar restar los monomials
                    # "x -= value" no vale porque devuelve un polinomio si no son iguales
                    if algebra.monomial.count_variables(x.variables) == algebra.monomial.count_variables(value.variables):
                        if self.monomials[self.monomials.index(x)].coefficient - value.coefficient != 0:
                            self.monomials[self.monomials.index(x)] -= value
                        else:
                            del self.monomials[self.monomials.index(x)]
                    else:
                        raise ValueError
                    break
                except ValueError:
                    pass
                n+=1
            if n >= len_monomials:
                # No ha habido ninguno que concuerde
                self.monomials.append(value)
            
            if len(self.monomials) == 0:
                return self.numerical_term
            return self
        elif isinstance(value, Polynomial):
            R = Polynomial()
            R.numerical_term = self.numerical_term
            nm = 0
            for m in value.monomials:
                found = False
                
                for x in self.monomials:
                    if algebra.monomial.count_variables(x.variables) == algebra.monomial.count_variables(m.variables):
                        if x.coefficient - m.coefficient != 0:
                            R.monomials.append(x-m)
                            nm += 1
                        found = True
                        
                if not found:
                    R.monomials.append(m)
            
            if value.numerical_term:
                R.numerical_term -= value.numerical_term
                
            if nm == 0:
                # Se han eliminado todos los monomios. Devolver un int
                return R.numerical_term
            
            return R
                
        elif type(value) is int:
            self.numerical_term -= value
            return self
        elif type(value) is algebra.Variable:
            return self - algebra.Monomial(variables=value.name, coefficient=-1)
        else:
            raise TypeError(f'Cann\'t subtract a Polynomial to {type(value)}')

    def __truediv__(self, value):
        if isinstance(value, int):
            R=[]
            for x in self.monomials:
                R.append(x/value)
            if self.numerical_term != 0:
                if self.numerical_term % value == 0:
                    numerical_term = int(self.numerical_term / value)
                else:
                    numerical_term = Fraction(self.numerical_term, value)
            else:
                numerical_term=0
            return algebra.Polynomial(monomials=R, numerical_term=numerical_term)
        elif isinstance(value, Fraction):
            R=[]
            for x in self.monomials:
                R.append(x/value)
            if self.numerical_term != 0:
                if self.numerical_term % value == 0:
                    numerical_term = int(self.numerical_term / value)
                else:
                    numerical_term = Fraction(self.numerical_term, value)
            else:
                numerical_term = 0
            return algebra.Polynomial(monomials=R, numerical_term=numerical_term)
        elif isinstance(value, algebra.Variable):
            raise NotImplementedError
        elif isinstance(value, algebra.Monomial):
            #print('dividing', self, value)
            R=[]
            numerical_term = 0
            for x in self.monomials:
                result = x/value
                if result.variables == "":
                    numerical_term += result.coefficient
                else:
                    R.append(result)
            if self.numerical_term != 0:
                if self.numerical_term % value.coefficient == 0:
                    result = self.numerical_term / value.coefficient
                    if type(result) is float:
                        result = int(result)
                    R.append(algebra.Monomial(coefficient=result, variables=value.variables))
                else:
                    R.append(algebra.Monomial(coefficient=Fraction(self.numerical_term, value.coefficient),variables=value.variables))
            return Polynomial(monomials=R, numerical_term=numerical_term)
        elif isinstance(value, Polynomial):
            raise NotImplementedError
        else:
            return TypeError(f'Cann\'t divide a Polynomial by {type(value)}')

    def __mul__(self, value):
        if isinstance(value, (algebra.Monomial, int)):
            for x in range(len(self.monomials)):
                self.monomials[x]*= value
            if isinstance(value, int):
                self.numerical_term*=value
            return self
        elif isinstance(value, Polynomial):
            R = Polynomial(monomials=[], numerical_term=0)
            for x in self.monomials:
                for y in value.monomials:
                    #R.monomials.append(x * y)
                    R += x * y
                if value.numerical_term != 0:
                    #R.monomials.append(x * value.numerical_term)
                    R += x * value.numerical_term
            
            if value.numerical_term != 0:
                if self.numerical_term != 0:
                    #print(self.numerical_term, value.numerical_term)
                    R.numerical_term = self.numerical_term * value.numerical_term
                    for x in value.monomials:
                        #R.monomials.append(self.numerical_term * x)
                        R += self.numerical_term * x
            return R
        elif isinstance(value, algebra.Variable):
            found = False
            for x in self.monomials:
                if algebra.monomial.count_variables(x.variables) == {value.name: 1}:
                    #print(self.monomials[self.monomials.index(x)] * value, value)
                    #print(x, x.variables)
                    self.monomials[self.monomials.index(x)] *= value
                    found = True
                    break
            if not found:
                self.monomials.append(value)
                
            if self.numerical_term:
                self.monomials.append(self.numerical_term * value)
                self.numerical_term = 0
            return self
        else:
            raise TypeError(f'Cann\'t multiply a Polynomial by {type(value)}')
    
    def __rmul__(self, value):
        return self * value

    def __pow__(self, value, mod=None):
        if mod:
            raise NotImplementedError
        
        R = []
        
        for x in self.monomials:
            R.append( x ** value )

        if self.numerical_term != 0:
            R.append(self.numerical_term ** value)
        
        RT = 0
        #print(R)
        for x in R:
            RT += x
        return RT
        

    def __str__(self):
        #print(self.monomials, self.numerical_term)
        R=''
        for x in self.monomials:
            R+= '+'+str(x) if x.coefficient > 0 else str(x)
        if self.numerical_term != 0:
            if self.numerical_term <0:
                R+=str(self.numerical_term)
            else:
                R+='+'+str(self.numerical_term)
        return R

    def __neg__(self):
        for x in range(len(self.monomials)):
            self.monomials[x] = -self.monomials[x]
        
        self.numerical_term = -self.numerical_term
        return self
    
    def __pos__(self):
        return self

    def __repr__(self):
        return f'<Polynomial {self}>'
