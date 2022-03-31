# Made with PyCharm 2021 community edition
# Contributor(s): Robert Uszynski
# Date: 30/03/2022
# Version: 1.0

import os  # os used for file I/O
import sys  # sys used for command line
import subprocess  # subprocess used to install pandas if missing
import unittest  # unittest for testing framework
import argparse  # argparse to parse commandline arguments

# Install pandas if not already installed. Requires pip to be installed, may not be an "always works" solution on
# some systems.
try:
    import pandas as pd
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'pandas'])
finally:
    import pandas as pd  # pandas used for dataframe


def print_record(my_data, my_index):
    # Get individual data
    first_name = my_data.iloc[my_index]['firstname']
    last_name = my_data.iloc[my_index]['lastname']
    date = my_data.iloc[my_index]['date']
    division = my_data.iloc[my_index]['division']
    summary = my_data.iloc[my_index]['summary']

    # Multi-line string with the record using formatted string.
    out_string = f"""- name: {first_name} {last_name}
  details: In division {division} from {date} performing {summary}"""

    print(out_string)


# Main program
def main_program(csv_file_path):
    # Case where file path is incorrect
    if not os.path.exists(csv_file_path):
        print('Error! File path:', csv_file_path, 'is invalid (no such file or directory).')
        return False

    # Read data and clear NA data
    data = pd.read_csv(csv_file_path)
    data = data.dropna()
    # Note: in a more feature-full solution, missing data could be in some way imputed.
    # E.g. An NA points score could be replaced with 0.

    # Handle case if there exists mismatch between expected to actual column names
    cols = [data.columns[0], data.columns[1], data.columns[2], data.columns[3], data.columns[4], data.columns[5]]
    default_cols = ['firstname', 'lastname', 'date', 'division', 'points', 'summary']
    if not cols == default_cols:
        print('Error! Expected column names are', default_cols, 'instead found', cols)
        return False

    # Handle the case where the data-types may not be what is expected. Noting that date is considered a string.
    # Expect firstname, lastname, date and summary to be of type object and
    # division and points to be of type int64
    for col in data.columns:
        if col == 'firstname' or col == 'lastname' or col == 'date' or col == 'summary':
            if not isinstance(data[col].dtype, object):
                print('Error! Expected col:', col, 'to be of type object!')
                return False

        elif col == 'division' or col == 'points':
            if not data[col].dtype == 'int64':
                print('Error! Expected col:', col, 'to be of type int64!')
                return False

    # Used for handling case for data which has less than 3 rows
    max_rows = 3 if data.shape[0] >= 3 else data.shape[0]

    # Note: due to ambiguity in instruction, data is first sorted by points, then by division to get desired output.
    # This is not necessarily equivalent to sorting by division then by points.
    data = data.sort_values(by='points', ascending=False)
    data = data.sort_values(by='division', ascending=True)
    data = data[0:max_rows]

    # Actually print the records
    print('records:')
    for index in range(max_rows):
        print_record(data, index)

    return True


class TestCsv2Yaml(unittest.TestCase):
    base_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Testing')

    def setUp(self) -> None:
        pass

    # Default test on correct data -> should assert True
    def test_succeed(self):
        print('\n---- Run test succeed ----')
        self.assertTrue(main_program(os.path.join(self.base_file_path, 'testdata.csv')))

    # Test for passing invalid filepath -> should assert False (cannot read file)
    def test_invalid_filepath(self):
        print('\n---- Run test invalid filepath ----')
        self.assertFalse(main_program("garbage/path"))

    # Test for passing a csv file with incorrect col names -> should assert False (data cannot be interpreted)
    def test_wrong_cols(self):
        print('\n---- Run test wrong cols ----')
        self.assertFalse(main_program(os.path.join(self.base_file_path, 'testdata-wrongcols.csv')))

    # Test for passing a csv file with only 2 rows of data -> should assert True (but only print 2 records)
    def test_two_row_data(self):
        print('\n---- Run test two row data ----')
        self.assertTrue(main_program(os.path.join(self.base_file_path, 'testdata-tworows.csv')))

    # Test where firstnames have been replaced with numbers -> should assert True
    # Interestingly, I initially expected this to assert False, but pandas is smart enough to coerce the numbers into
    # strings (so their names will be 0.1, 1.1, 2.1, etc...)
    def test_numeric_names(self):
        print('\n---- Run test numeric names ----')
        self.assertTrue(main_program(os.path.join(self.base_file_path, 'testdata-numericnames.csv')))

    # Test where scores are replaced with strings -> should assert False (data cannot be interpreted)
    def test_string_score(self):
        print('\n---- Run test string points ----')
        self.assertFalse(main_program(os.path.join(self.base_file_path, 'testdata-stringpoints.csv')))

    # Test where there are NA values NOT in division or scores -> should assert True (but remove NA data)
    def test_NA_values(self):
        print('\n---- Run test NA values ----')
        self.assertTrue(main_program(os.path.join(self.base_file_path, 'testdata-NA.csv')))

    # Test where there are NA values IN division or scores -> should assert False (as there is dtype mismatch)
    def test_missing_scores_divisions(self):
        print('\n---- Run test missing scores & divisions ----')
        self.assertFalse(main_program(os.path.join(self.base_file_path, 'testdata-missingscoresdivisions.csv')))


if __name__ == '__main__':
    # Setup commandline argument parsing
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--version', action='store_true', help='Displays author and version, then terminates '
                                                                     'program')
    parser.add_argument('-t', '--tests', action='store_true', help='Set this flag to run tests')
    parser.add_argument('-f', '--file', type=str, help='If provided will execute main program on this file. Must be '
                                                       'full path, e.g. \'C:/Testing/Data/testdata.csv\'')
    args = parser.parse_args()

    # Print version if flagged to do so
    if args.version:
        print('Author(s): Robert Uszynski, Script version: 1.0, Last major update: 30/03/2021')
        print('Python version,', sys.version)
        exit(0)

    # Run tests if flagged to do so
    if args.tests:
        unittest.main(argv=['first-arg-is-ignored'], exit=False)

    # Attempt to run main program with provided file
    if args.file:
        print('\n---- Running main program with file:', args.file)
        main_program(args.file)

    # Case where no arguments are provided
    if not args.version and not args.tests and not args.file:
        print("""
No arguments provided! Try:
usage: main.py [-h] [-v] [-t] [-f FILE]

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         Displays author and version, then terminates program
  -t, --tests           Set this flag to run tests
  -f FILE, --file FILE  If provided will execute main program on this file.
                        Must be full path, e.g. 'C:/Testing/Data/testdata.csv'
""")

# Additional note:
#
# Python has a library called pyyaml designed for parsing and tokenizing yaml files.
# In a non test scenario where the goal would be to actually write the yaml string to a file and the yaml string would
# be more complicated, I would this library. After sorting data, I would do: 1. convert pandas dataframe to json string,
# then 2. use pyyaml to convert that json string to yaml format.
# In this case, I decided this solution was over-engineering.
