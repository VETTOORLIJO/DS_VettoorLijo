import numpy as np
import pandas as pd


#Create a numpy array containing the numbers from 1 to 10, and then reshape it to a 2x5
#matrix. (Score:1)
num_array= np.array([1,2,3,4,5,6,7,8,9,10]).reshape(2,5)
print("num_array with 2x5")
#print(num_array)
num_array1= np.arange(1,11).reshape(2,5)
print("num_array with 2x5")
print(num_array1)
# Create a numpy array containing the numbers from 1 to 20, and then extract the
# elements between the 5th and 15th index. (Score:1)
num_array3=np.arange(1,21)
print("num_array [4] value",num_array3[4])
print("num_array [19] value",num_array3[19])
# 4. Write a NumPy program that creates a 2D array x of shape (3, 4) and a 1D array y of
# shape (4,). Subtract y from each row of x using broadcasting. (Score: 2)
x=np.arange(11,23).reshape(3,4)
y=np.arange(1,5)
arr_broadcast =x-y
print("arr_broadcast")
print(arr_broadcast)
# 5. Create a dataframe with the following columns: name, age, and gender. The dataframe
# should have 10 rows of data. (Score: 2)
df= pd.DataFrame({"Name":["Ram", "Remo","Madusa","Thor","Bob","John Wick","John Connor","Sam","Jack","Tom"],
                  "Age":[12,32,46,51,12,78,54,45,45,12],
                  "Gender":["M", "M","F","M","M","M","M","M","M","M"]},)
print("DataFrame with 10 values")
print(df)
# 5.1) Add a new column to the data frame created in question 1, called occupation.
# The values for this column should be Programmer, Manager, and Analyst,
# corresponding to the rows in the dataframe. (Score: 1)
df["Occupation"] =["Programmer", "Manager", "Analyst","Programmer", "Manager", "Analyst","Programmer", "Manager","Analyst","Programmer"]
print("df added Occupation")
print(df)
# 2) Select the rows of the dataframe where the age is greater than or equal to 30.
# (Score: 1)
age_above30 = df[df["Age"]>30]
print("age_above30")
print( age_above30)
# 3) Convert this dataframe to a CSV file and read that CSV file, and finally display
# the contents. (Score: 1)
df.to_csv("Emp.csv", index=False)
print("saved as CSV")
new_df= pd.read_csv("Emp.csv")
print("new_df")
print(new_df.head())