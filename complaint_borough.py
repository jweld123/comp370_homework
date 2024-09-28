import argparse
import csv
from datetime import datetime
from collections import defaultdict

def comp(inp, start, end):
    comp_data = defaultdict(lambda: defaultdict(int))

    with open(inp, mode='r') as file:
        read = csv.DictReader(file)

        for row in read:
            date = datetime.strptime(row['created_date'], '%Y-%m-%d')
            if start <= date <= end:
                borough = row['borough']
                complaint_type = row['complaint_type']
                comp_data[complaint_type][borough] += 1
    return comp_data

def output(comp_data, output_file=None):
    rows=[]
    for complaint_type, boroughs in complaint_data.items():
        for borough, count in boroughs.item():
            rows.append([complaint_type, borough, count])

    if output_file:
        with open(output_file, mode='w', newline='') as output:
            write = csv.writer(output)
            write.writerow(['complaint type', 'borough', 'count'])
            write.writerows(rows)
    else:
        print('complaint type, borough, count')
        for row in rows:
            print(f'{row[o]}, {row[1]}, {row[2]}')

def main():
    parser = argparse.ArgumentParser(description="Count complaint types per borough within a date range.")
    parser.add_argument('-i', '--input', required=True, help='Input CSV file containing complaint data')
    parser.add_argument('-s', '--start', required=True, help='Start date (YYYY-MM-DD)')
    parser.add_argument('-e', '--end', required=True, help='End date (YYYY-MM-DD)')
    parser.add_argument('-o', '--output', help='Optional output file to save the results')

    args = parser.parse_args()

    start_date = datetime.strptime(args.start, '%Y-%m-%d')
    end_date = datetime.strptime(args.end, '%Y-%m-%d')

    complaint_data = comp(args.input, start_date, end_date)
    output_results(complaint_data, args.output)

if __name__ == "__main__":
    main()
