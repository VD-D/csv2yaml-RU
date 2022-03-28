# Made with PyCharm 2021 community edition
import os  # os used for file I/O
import sys  # sys used for command line
import subprocess  # subprocess used to install pandas if missing

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
if __name__ == '__main__':
    # Case where no arguments are provided (error)
    if len(sys.argv) < 1:
        print('Error! First argument must be path to csv file!')
        exit(1)

    # Case where file path is incorrect
    if not os.path.exists(sys.argv[0]):
        print('Error! File path:', sys.argv[1], 'is invalid (no such file or directory).')
        exit(1)

    # Read data and clear NA data
    data = pd.read_csv(sys.argv[1])
    data = data.dropna()
    # Note: in a more feature-full solution, missing data could be in some way imputed.
    # E.g. An NA points score could be replaced with 0.

    # Handle case if there exists mismatch between expected to actual column names
    cols = [data.columns[0], data.columns[1], data.columns[2], data.columns[3], data.columns[4], data.columns[5]]
    default_cols = ['firstname', 'lastname', 'date', 'division', 'points', 'summary']
    if not cols == default_cols:
        print('Error! Expected column names are', default_cols, 'instead found', cols)
        exit(1)

    # Handle the case where the data-types may not be what is expected. Noting that date is considered a string.
    # Expect firstname, lastname, date and summary to be of type object and
    # division and points to be of type int64
    for col in data.columns:
        if col == 'firstname' or col == 'lastname' or col == 'date' or col == 'summary':
            if not isinstance(data[col].dtype, object):
                print('Error! Expected col:', col, 'to be of type string!')
                exit(1)

        elif col == 'division' or col == 'points':
            if not data[col].dtype == 'int64':
                print('Error! Expected col:', col, 'to be of type int64!')
                exit(1)

    # Note: due to ambiguity in instruction, data is first sorted by points, then by division to get desired output.
    # This is not necessarily equivalent to sorting by division then by points.
    data = data.sort_values(by='points', ascending=False)
    data = data.sort_values(by='division', ascending=True)
    data = data[0:3]

    # Actually print the records
    print('records:')
    for index in range(3):
        print_record(data, index)

    # # Case where less than 2 arguments are provided
    # if len(sys.argv) < 2:
    #     flag = 0
    # # Case where help is requested
    # if len(sys.argv) > 2:
    #     if sys.argv[1] == 'h' or sys.argv[1] == 'help':
    #         # TODO
    #         flag = -1
    #     # Case where flag is terminal only output.
    #     elif sys.argv[1] == 't' or sys.argv[1] == 'terminal':
    #         flag = 0
    #     # Case where flag is file only output.
    #     elif sys.argv[1] == 'f' or sys.argv[1] == 'file':
    #         flag = 1
    #     # Case where flag is terminal and file output.
    #     elif sys.argv[1] == 'b' or sys.argv[1] == 'both':
    #         flag = 2
    #     else:
    #         flag = 0
    #         print('Warning! Argument two: \"', sys.argv[1],
    #               '\" does not match any known flag. (Try \'csv2yaml.py help\')'
    #               , sep='')

    # print('Argument List:', str(sys.argv))
