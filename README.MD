# Welcome to the IMSE Datathon!

## Data
--------

Data has been obtained from the Catalysis-Hub (https://catalysis-hub.org/).
The `data` directory contains the following files:
- `Test_Input.csv` - contains the input data for the test set including descriptors.
- `Train.csv` - contains the input (including descriptors) and output files for the training set.
- `coordinates`
  - Files of the name `{ID}_{ADSORBANT}_STAR.xyz` contain the XYZ coordinates of surface of the metal.
  - Files of the name `{ID}_{ADSORBANT}_COSTAR.xyz` contain the XYZ coordinates of surface of the metal with the adsorbent.
  - `Test_Energies_Enc.csv` - contains the energies of the test set.

## Tasks
--------
### Task 1:

In task 1 your goal will be to predict the energy of the adsorbed molecule given the metal, surface plane, and absorbate using input data in `Train.csv`.
In this file you will find a list of pre-calculated descriptors for the metal, including the HOMO-LUMO gap of both the metal and adsorbates. The same set of pre-calculated descriptors are provided for the test set of molecules.

Some descriptors will be better predictors than others, so you may want to use feature selection to select the most important ones.
You may also calculate the additional features using Python packages such as [RDKit](https://www.rdkit.org) and [ASE](https://wiki.fysik.dtu.dk/ase/).


We also provide some additional descriptors in the `additional_descriptors` folder, however, these will require manual matching to the rows in the train and test sets using the `ID` column across the files.

### Task 2:

In task 2 your goal will be to predict the energy of the adsorbed mole