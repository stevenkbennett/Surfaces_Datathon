# Generate random numbers 
import numpy as np
import pandas as pd

# Set random seed
np.random.seed(42)

# Load data
train_set = pd.read_csv('Train.csv')
test_set = pd.read_csv('Test_Input.csv')
len_test = test_set.shape[0]
energies = train_set['Energy'].astype(np.float32).values

# Random predictions sampled from standard distribution of train set
mean = np.mean(energies)
std = np.std(energies)
random_preds = np.random.normal(loc=mean,scale=std,size=len_test)

# Save values
np.savetxt('task_1_predictions.csv',random_preds)

