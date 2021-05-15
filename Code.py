#########################################################################
#Task: # Program which lets the user import data from the NYT Bestseller list.
#        User can then perform inspection tasks such as search for title,
#        authors, books in certain periods etc.
#Date: xx.xx.2021
#Authors:
#########################################################################


#Setup
#########################################################################
import pandas as pd
import re
import io

#Definition of functions
#########################################################################

#function which tests that the input is an integer

#index is a vector of T/F which indicates which rows from the Data Frame Bestsellers should be chosen for display
def display_titles(index):
    output = bestsellers.loc[index]
    for i in range(output.__len__()):
        row = bestsellers.loc[i]
        print(row["Title"] + ", " + "by " + row["Author"] + " " + row["Year"].strftime("%d/%m/%Y"))

def input_integer(text):
    arg = input(text)
    while True:
        try:
            arg = int(arg)
            if int(arg) == float(arg):
                return(arg)
                break
            else:
                print("Please make sure to input a valid integer number")
        except ValueError:
            print("Please make sure to input a valid integer number")
            arg = input()

#function to display all books within a certain range of years (from start to end!)
def function1():

    while True:
        start_year =input_integer("Select start year:")
        end_year = input_integer("Select end year:")
        try:
            start = pd.Timestamp(start_year,1,1)
            end = pd.Timestamp(end_year,1,1)

            if end < start:
                print("Please make sure that your start value is before your end value")
                pass
            else:
                break
        except ValueError:
            min = pd.Timestamp.min.year
            max = pd.Timestamp.max.year
            print("Please make sure to only select values between " + str(min) + " and " + str(
                max))

    start_date = bestsellers["Year"] >= start
    end_date = bestsellers["Year"] <= end
    range_dates = start_date & end_date

    if bestsellers.loc[range_dates].empty:
        print("No titles were found within the specified range of years")
    else:
        print("All Titles between" + " " + str(start_year) + " " + "and"+ " " + str(end_year) + ":")
        display_titles(range_dates)

#function to display all books in a specific month and year
def function2():
    print()

#function to search for author
def function3():
    print()

#function to search for a title
def function4():
    print()


#execution of program
#########################################################################

#Function which asks the user for a file path and its separator.
#Based on the user input, the file is stored as a data frame under then name bestsellers

#store path and separator as defined by user
path = input("Please insert the path to the data file you want to input here:")

# if the path contains windows backslashes this must be replaced
if path.__contains__("\\"):
    path = path.replace("\\", "/")

#if path is copied from file explorer in windoes, quotes are wraped around which must be eliminated
if path.__contains__("\""):
    path = path.replace("\"", "")

#loop which stores the data in the data frame if all inputs are valid. If errors occur,
#user is asked to change his input

#when the document is downloaded, the taps are replaced by 4 spaces. We will revert this. Further, we will
#split each word before a capitalized letter since all titles, authors etc.. are written as one string...

#the original file should not be altered

fin = open(path, "rt")
data = fin.read()
fin.close()

data = data.replace("    ", "\t")
data = re.sub(r"([A-Z])", r" \1", data)
data = io.StringIO(data)

while True:
    try:
        bestsellers = pd.read_csv(data, sep = "\t")
        bestsellers.columns = ["Title", "Author", "Date", "Year", "Type"]
        bestsellers["Year"] = bestsellers["Year"].astype("datetime64")
        print("Thanks. Your data has been imported sucessfully")
        break

    except FileNotFoundError:
        print("whoops. Something seems to have gone wrong. \n"
                "Please make sure that your input path is correct")
        path = input("path:")

    #user can at any time break out of the loop by typing q or Q
    if path in ["Q", "q"]:
        print("Programm sucessfully quit")
        break

while True:
    selection = input("What would you like to do ? \n"
                      "1: Look up year range \n"
                      "2: Look up month/year \n"
                      "3: Search for author \n"
                      "4: Search for title \n"
                      "q: Quit\n")

    #user input is converted to integer if possible. If not, no conversion takes place
    try:
        selection = int(selection)
    except ValueError:
        pass

    #calls respective function based on which action the user wants to execute
    if selection in range(5):
        if selection == 1:
            function1()
        elif selection == 2:
            function2()
        elif selection == 3:
            function3()
        else:
            function4()
    elif selection in ["q", "Q"]:
        print("Program sucessfully quit")
        break
    else:
        print("Invalid Input. Please try again")


