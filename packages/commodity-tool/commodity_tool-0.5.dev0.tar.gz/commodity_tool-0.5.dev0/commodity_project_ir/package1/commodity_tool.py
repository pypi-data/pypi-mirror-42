"""This module runs as a pseudo main function and data set into a dataframe"""

def load_data():
    """load_data takes no arugments (currently) and loads in the dataset identified in this project.
    it then calls TODO"""
    print("load data here")


def main():
    """Runs if this module is imported"""
    print("Other main ran")
    load_data()

if __name__ == 'main':
    #Psuedo main function. This construct is the entry point for the tool.
    print('main ran')
    load_data()
