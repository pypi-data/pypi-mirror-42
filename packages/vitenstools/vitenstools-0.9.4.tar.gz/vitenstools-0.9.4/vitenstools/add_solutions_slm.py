import json
from phreeqpython import PhreeqPython
from . import chemistry

def add_solutions_slm(self, path):
    """ Create PhreeqPython solutions using well models in a .slm file """
    with open(path, 'r') as f:
        slm = json.load(f)

    wells = {}
    for model in slm['models'].values():
        if model['type'] == 'well':
            elements = model['configuration']['solution']['composition']
            composition = {}
            charge = 0
            for name, value in elements.items():
                if name in chemistry.chemicals:
                    mmol = float(value) / chemistry.chemicals[name][0]
                    charge += mmol * chemistry.chemicals[name][1]
                    composition[name] = mmol
            if charge > 0:
                composition['Nmod'] = charge
            if charge < 0:
                composition['Pmod'] = -charge

            temperature = model['configuration']['solution']['temperature']
            wells[model['title']] = self.add_solution_simple(composition, temperature)
 
    return wells

PhreeqPython.add_solutions_slm = add_solutions_slm
