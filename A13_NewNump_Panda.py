import numpy as np
import pandas as pd

df = pd.DataFrame({"Name":["A","B","C"],"Age":[20,30,40]})

print(df[df["Age"].values>25])
print(df[df["Age"]>25])
print("********************")
