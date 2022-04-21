# Python script to make 2D descriptors
# I will make a set of descriptors for just the metal slabs, and the metal slab and adsorbate pair
# The descriptor will be composed of the meredig composistional descriptor generated from matminer and a 1-hot encoding of the facet structure

import re
import numpy as np
import pandas as pd
from tqdm import tqdm
from matminer.featurizers.conversions import StrToComposition
from matminer.featurizers.composition import ElementProperty, Meredig, AtomicOrbitals, ValenceOrbital
# link to extra featurizers https://hackingmaterials.lbl.gov/matminer/featurizer_summary.html

def main():
    # Generate training set descriptors
    train_set = pd.read_csv('Train.csv',index_col=0)
    metal_df = pd.DataFrame(train_set['Chemical_Composition'],index=train_set.index)
    metal_df = StrToComposition().featurize_dataframe(metal_df, 'Chemical_Composition')

    # Metal only descriptors
    # Define the compositional featurisers
    metal_magpie_desc = ElementProperty.from_preset(preset_name="magpie").featurize_dataframe(metal_df, col_id="composition").iloc[:,2:]
    metal_meredig_desc = Meredig().featurize_dataframe(metal_df, col_id="composition").iloc[:,2:]
    metal_atomic_desc = AtomicOrbitals().featurize_dataframe(metal_df, col_id="composition",ignore_errors=True).iloc[:,2:]
    metal_valence_desc = ValenceOrbital().featurize_dataframe(metal_df, col_id="composition",ignore_errors=True).iloc[:,2:]

    # one hot encode facets
    # find all unique facets
    seen = []
    print('Finding all unique facets')
    for i, _ in enumerate(tqdm(train_set.index)):
        temp = train_set.iloc[i,2]
        seen.append(temp) if temp not in seen else 0
    one_hot_encodings = np.zeros(shape=(len(train_set),len(seen)))
    # save facet order
    np.savetxt('2d_descriptors/facet_list.txt',np.array(seen,dtype=str),fmt='%s')
    # one-hot encode
    print('One-hot encoding facets')
    for i, _ in enumerate(tqdm(train_set.index)):
        temp = train_set.iloc[i,2] 
        one_hot_encodings[i,seen.index(temp)] = 1

    # Get molecule SMILES
    print('Get molecular smiles')
    smiles = []
    for i, _ in enumerate(tqdm(train_set.index)):
        temp = train_set.iloc[i,0] 
        smiles.append(eq_to_mol(temp))
    smiles = pd.Series(smiles,index=train_set.index,name='molecular_smiles')

    # Get descriptors for metal + molecule
    all_df = pd.concat([metal_df,smiles],axis=1)
    all_df.drop('composition',axis=1,inplace=True)
    all_df['total_composition'] = all_df['Chemical_Composition'] + all_df['molecular_smiles']
    all_df = StrToComposition().featurize_dataframe(all_df, 'total_composition')
    print(all_df)
    total_magpie_desc = ElementProperty.from_preset(preset_name="magpie").featurize_dataframe(all_df, col_id="composition").iloc[:,4:]
    total_meredig_desc = Meredig().featurize_dataframe(all_df, col_id="composition").iloc[:,4:]
    total_atomic_desc = AtomicOrbitals().featurize_dataframe(all_df, col_id="composition",ignore_errors=True).iloc[:,4:]
    total_valence_desc = ValenceOrbital().featurize_dataframe(all_df, col_id="composition",ignore_errors=True).iloc[:,4:]

    # Save all of the descriptors
    metal_magpie_desc.to_csv('2d_descriptors/metal_magpie_desc.csv')
    metal_meredig_desc.to_csv('2d_descriptors/metal_meredig_desc.csv')
    metal_atomic_desc.to_csv('2d_descriptors/metal_atomic_desc.csv')
    metal_valence_desc.to_csv('2d_descriptors/metal_valence_desc.csv')

    total_magpie_desc.to_csv('2d_descriptors/total_magpie_desc.csv')
    total_meredig_desc.to_csv('2d_descriptors/total_meredig_desc.csv')
    total_atomic_desc.to_csv('2d_descriptors/total_atomic_desc.csv')
    total_valence_desc.to_csv('2d_descriptors/total_valence_desc.csv')


def eq_to_mol(eq):
    subbed = re.sub("\s+", ",", eq.strip()).split(',')
    last = subbed[-1][:-1] # get last string of equation up to the last letter of the string  (which is always*)
    return last


if __name__ == '__main__':
    main()


