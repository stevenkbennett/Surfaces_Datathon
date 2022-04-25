from pathlib import Path
from numpy.core.fromnumeric import mean
from numpy.lib.shape_base import _put_along_axis_dispatcher
from numpy.lib.ufunclike import _fix_and_maybe_deprecate_out_named_y
from pandas.io.pytables import AppendableMultiSeriesTable
from sklearn import metrics
import pandas as pd
import numpy as np
from github import Github
import os
from os.path import join
from math import floor, log10
from io import BytesIO
from cryptography.fernet import Fernet

def main():
    ak = os.environ.get("GITHUB_TOKEN", None)
    g = Github(ak)
    pr_id = os.environ.get("PR_NUMBER", None)
    if pr_id == "false" or pr_id == None:
        pr_id = 1
    repo = g.get_repo(483552301)
    pr = repo.get_pull(int(pr_id))
    issue_str = ""
    points_total = 0
    key = os.environ.get("KEY", None)
    # workspace = os.environ.get("GITHUB_WORKSPACE", None)
    f = Fernet(key)
    with open('data/Test_Energies_Enc.csv', 'rb') as encrypted_file:
        encrypted = encrypted_file.read()
    decrypted_csv = f.decrypt(encrypted)

    if Path("task_1_predictions.csv").exists():
        df = pd.read_csv(BytesIO(decrypted_csv))
        y_true = np.array(df["Energy"])
        y_pred_df = pd.read_csv("task_1_predictions.csv", header=None)
        y_pred = [j for i in y_pred_df.to_numpy() for j in i]
        mae = np.around(metrics.mean_absolute_error(y_true, y_pred), 3)
        r2 = np.around(metrics.r2_score(y_true, y_pred), 3)
        nMAE = np.around(calc_nMAE(y_true, y_pred), 3)
        npoints = points(1 - calc_nMAE(y_true, y_pred), max_points=60)
        points_total += npoints
        issue_str += "Task 1 Prediction - Adsorption Energy (No Coordinate Data\n-----------------\n"
        issue_str += f"Mean Absolute Error: {mae}\n"
        issue_str += f"R<sup>2</sup>: {r2}\n"
        issue_str += f"Normalised Mean Absolute Error (Assessed): {nMAE}\n"
        issue_str += f"__Points: {npoints}__\n\n"
    else:
        issue_str += "Task 1 Prediction - Adsorption Energy (No Coordinate Data)\n-----------------\n"
        issue_str += "No results submitted for task 1 prediction\n\n"

    if Path("task_2_predictions.csv").exists():
        df = pd.read_csv(BytesIO(decrypted_csv))
        y_true = np.array(df["Energy"])
        y_pred_df = pd.read_csv("task_2_predictions.csv", header=None)
        y_pred = [j for i in y_pred_df.to_numpy() for j in i]
        mae = np.around(metrics.mean_absolute_error(y_true, y_pred), 3)
        r2 = np.around(metrics.r2_score(y_true, y_pred), 3)
        nMAE = np.around(calc_nMAE(y_true, y_pred), 3)
        npoints = points(1 - calc_nMAE(y_true, y_pred), max_points=30)
        points_total += npoints
        issue_str += "Task 2 Prediction - Adsorption Energy (Coordinate Data)\n-----------------\n"
        issue_str += f"Mean Absolute Error: {mae}\n"
        issue_str += f"R<sup>2</sup>: {r2}\n"
        issue_str += f"Normalised Mean Absolute Error (Assessed): {nMAE}\n"
        issue_str += f"__Points: {npoints}__\n\n"
    else:
        issue_str += "Task 2 Prediction - Adsorption Energy (Coordinate Data)\n-----------------\n"
        issue_str += "No results submitted for task 2 prediction\n\n"

    pr.create_issue_comment(issue_str)


def calc_nMAE(true, pred):
    return sum(abs(true - pred)) / sum(abs(true))


def points(score, alpha=1.2, max_points=50):
    return np.minimum(
        (max_points + 2) ** (np.maximum(score, np.finfo(float).eps) ** alpha)
        - 1,
        max_points,
    ).astype(int)


if __name__ == "__main__":
    main()