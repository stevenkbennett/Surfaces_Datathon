import numpy as np
import pandas as pd


def main():
    df = pd.read_csv('data/Full_Dataset.csv')
    # Only include cells in the training set that have coordinate values
    df = df.set_index('ID')
    n_samples = int(np.floor(len(df)*0.2))
    print(f"The percentage size of test set is {n_samples/len(df)*100}%")
    coords_available = df[df['Coordinates_Available'] == True]
    test = coords_available.sample(n_samples, random_state=42)
    train = df.drop(test.index)
    # Drop the reaction energy column
    test_energies = test.loc[:,'Energy']
    test_energies.to_csv('data/Test_Energies.csv')
    test_input = test.drop('Energy', axis=1)
    test_input.to_csv('data/Test_Input.csv')
    train.to_csv('data/Train.csv')


if __name__=='__main__':
    main()