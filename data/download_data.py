import requests
import pprint
import argparse
import ase

GRAPHQL = 'http://api.catalysis-hub.org/graphql'

def fetch(query):
    return requests.get(
        GRAPHQL, {'query': query}
    ).json()['data']

def create_query(metal, adsorbate):
    return """reactions ( surfaceComposition: "{metal}, reactants: "reactant+star", products: "~" )
    {
    totalCount
    pageInfo {
      hasNextPage
      hasPreviousPage
      startCursor
      endCursor
    }
    edges {
      node {
        Equation
        sites
        id
        pubId
        dftCode
        dftFunctional
        reactants
        products
        facet
        chemicalComposition
        facet
        reactionEnergy
        activationEnergy
        surfaceComposition
        chemicalComposition
        reactionSystems {
          name
          energyCorrection
          aseId
        }
      }
    }
    }}""".format(metal=metal, adsorbate=adsorbate)

def get_data(metal, adsorbate):
    query = create_query(metal, adsorbate)
    data = fetch(query)
    pprint(data)
    return data

def get_data_test():
    query = create_query('Fe', 'O')
    data = fetch(query)
    pprint(data)
    return data

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download data from Catalysis-Hub')
    # Add debug option
    parser.add_argument('--debug', action='store_true', help='Print debug information')
    args = parser.parse_args()
    if args.debug:
        get_data_test()
        # Stop execution
        exit()
    get_data(args.metal, args.adsorbate)