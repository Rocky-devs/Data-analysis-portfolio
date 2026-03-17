import sys
from config import *
from reader import read_csv_safely
from cleaner import clean_frame
from writer import write_excel


def main():
    if len(sys.argv) != 3:
        print('Usage: python3 main.py input.csv output.xlsx')
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    print('Reading:', input_path)
    df = read_csv_safely(input_path)

    print('Cleaning:...')
    results_df, errors_df, summary = clean_frame(df, CLEANER_CONFIG, ID_COL, NOTE_COL)

    print('Writing...', output_path)
    write_excel(output_path, results_df, errors_df, summary)

    print('done')


if __name__ == '__main__':
    main()
