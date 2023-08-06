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


from pyscience.datam import Data, Condition as C
from os import path

periodic_table = Data(path.join(path.split(path.abspath(__file__))[0], 'periodic_table.csv'))

def split_element_symbol(e):
    charge = None
    mass = None
    element = e
    
    if '(' in e:
        # Se ha especificado la masa
        element = e.split('(')
        mass, charge = element[1].split(')')
        element = element[0]
    else:
        if '+' in e or '-' in e:
            if e[1] in list('123456789'):
                element = e[0]
                charge = e[1:]
            else:
                element = e[0:1]
                charge = e[2:]
    
    return element, charge, mass


class ChemicalElement():
    
    def __init__(self, element):
        self.charge = None
        
        e = None
        mass = None
        
        if isinstance(element, str):
            name, charge, mass = split_element_symbol(element)
            
            if charge:
                if charge.endswith('-'):
                    self.charge = -int(charge[:-1] or 1)
                else:
                    self.charge = int(charge[:-1] or 1)
            
            e = periodic_table.where(C('symbol') == name)
        elif isinstance(element, int):
            if not 0 < element < 120:
                raise ValueError(f'Element with atomic number {element} doesn\'t exist')
            
            e = periodic_table.where(C('atomic_number') == element)
        
        if not e:
            raise ValueError(f'Element "{element}" doesn\'t exist')
        
        e = e[0]
        
        self.symbol = e['symbol']
        self.Z = e['atomic_number']
        
        if mass:
            self.A = float(mass)
        else:
            self.A = e['mass']
        
        self.name = e['name']
        self.family = e['family']
    
    def _charge(self, c):
        if c > 0:
            return str(c) + '+'
        return str(abs(c)) + '-'
    
    @property
    def protons(self):
        return self.Z
    
    @property
    def neutrons(self):
        return round(self.A) - self.Z
    
    @property
    def electrons(self):
        if self.charge:
            # Iones
            return self.protons - self.charge
        return self.protons
    
    @property
    def mass(self):
        return self.A
    
    @property
    def info(self):
        return \
        f'''{self.name.title()}{self._charge(self.charge) if self.charge else '' } ({self.symbol})
=======================================
Atomic number (Z):           {self.Z:10d}
Mass (u):                    {self.A:14.3f}
Family:                      {self.family:>10}

Charge:                      {'{:>10}'.format(self._charge(self.charge)) if self.charge else 'neutral':>10}

Number of protons (Z):       {self.protons:10d}
Number of neutrons (N):      {self.neutrons:10d}
Number of electrons:         {self.electrons:10d}
'''
    
    def __repr__(self):
        return f'<ChemicalElement \'{self.symbol}\'>'
    
    def __str__(self):
        return self.info
