from dataclasses import dataclass
from turtle import update
import requests
from pprint import pprint
import argparse
import ase
import json
import pandas as pd
import io
from ase import io as ase_io
from collections import defaultdict
from tqdm import tqdm

GRAPHQL = 'http://api.catalysis-hub.org/graphql'

def fetch(query):
    return requests.get(
        GRAPHQL, {'query': query}
    ).json()['data']

def create_query(metal, adsorbate, page_size=50):
    reactions = []
    has_next_page = True
    start_cursor = ''
    page = 0
    while has_next_page:
        data = fetch("""{{
            reactions(first: {page_size}, after: "{start_cursor}", surfaceComposition: "{metal}", reactants: "{adsorbate}+star", products: "{adsorbate}star") {{
            totalCount
            pageInfo {{
            hasNextPage
            hasPreviousPage
            startCursor
            endCursor
            }}
            edges {{
            node {{
                Equation
                reactants
                products
                sites
                id
                facet
                chemicalComposition
                surfaceComposition
                activationEnergy
                reactionEnergy
                dftCode
                dftFunctional
                reactionSystems {{
                name
                systems {{
                    energy
                    InputFile(format: "json")
                }}
                }}
            }}
            }}
        }}
        }}""".format(start_cursor=start_cursor,
                    page_size=page_size,
                    metal=metal,
                    adsorbate=adsorbate,
        ))
        has_next_page = bool(data['reactions']['pageInfo']['hasNextPage'])
        start_cursor = data['reactions']['pageInfo']['endCursor']
        page += 1
        print(has_next_page, start_cursor, page_size * page, data['reactions']['totalCount'])
        reactions.extend(map(lambda x: x['node'], data['reactions']['edges']))
    return reactions

def get_data(metal, adsorbate):
    reactions = create_query(metal, adsorbate)
    data = aseify_reactions(reactions)
    data_dicts = []
    for reaction in data:
        data_dicts.append(parse_reaction(reaction))
    return data_dicts

def get_data_test(metal='Fe', adsorbate='H'):
    reactions = create_query(metal, adsorbate)
    data = aseify_reactions(reactions)
    data_dicts = []
    for reaction in data:
        data_dicts.append(parse_reaction(reaction))
    merged = defaultdict(list)
    for key in data_dicts[0]:
        for d in data_dicts:
            merged[key].append(d[key])
    return merged

def parse_reaction(reaction):
    avail_coords = False
    if 'N/A' not in list(reaction['reactionSystems'].keys()):
        syses = reaction['reactionSystems']
        for sys in syses:
            file_name = reaction['id'] + '_' + sys.upper() + '.xyz'
            ase_io.write("data/coordinates/{}".format(file_name), syses[sys], format='xyz')

        # ase_io.write('')
        avail_coords = True
    d = {
        "Equation": reaction['Equation'],
        "Energy": reaction['reactionEnergy'],
        "Facet": reaction['facet'],
        "Chemical_Composition": reaction['chemicalComposition'],
        "Coordinates_Available": str(avail_coords),
        "ID": reaction['id'],
    }
    return d



def aseify_reactions(reactions):
    for i, reaction in enumerate(reactions):
        for j, _ in enumerate(reactions[i]['reactionSystems']):
            with io.StringIO() as tmp_file:
                system = reactions[i]['reactionSystems'][j].pop('systems')
                tmp_file.write(system.pop('InputFile'))
                tmp_file.seek(0)
                atoms = ase_io.read(tmp_file, format='json')
            calculator = ase.calculators.singlepoint.SinglePointCalculator(
                atoms,
                energy=system.pop('energy')
            )
            atoms.set_calculator(calculator)
            #print(atoms.get_potential_energy())
            reactions[i]['reactionSystems'][j]['atoms'] = atoms
        # flatten list further into {name: atoms, ...} dictionary
        reactions[i]['reactionSystems'] = {x['name']: x['atoms']
                                          for x in reactions[i]['reactionSystems']}
    return reactions

def main():
    merged = defaultdict(list)
    data_dicts = []
    metals = ["Fe", "Ag", "Al", "As", "Au", "Cu", "Pt", "Ni", "Pd", "Rh", "Zn", "Zr", "Y", "Sn", "Se", "Si", "K", "Na", "Ir", "Mn", "Mg", "Os", "Nb", "La", "Ga", "Ge", "Pb", "Ba", "Be", "Bi", "Cd", "Ca", "Co", "Ru"]
    adsorbates = ["H2O", "O", "O2", "NH3", "HCN", "CO", "CO2", "CH2CH2", "CH3CH3", "NO", "Graphene"]
    count = 0
    for metal in tqdm(metals, desc='Iterating over metals'):
        for adsorbate in tqdm(adsorbates, desc='Iterating over adsorbates'):
            data = get_data(metal, adsorbate)
            data_dicts.extend(data)
            count += 1
    # Expand list of lists into a single list
    all_data = [item for sublist in data_dicts for item in sublist]
    merged = defaultdict(list)
    for key in data_dicts[0]:
        for d in data_dicts:
            merged[key].append(d[key])
    df = pd.DataFrame(merged)
    df.to_csv('data/Full_Dataset.csv', index=False)
    return merged


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download data from Catalysis-Hub')
    # Add debug option
    parser.add_argument('--debug', action='store_true', help='Print debug information')
    args = parser.parse_args()
    if args.debug:
        get_data_test()
        # Stop execution
        exit()
    main()
