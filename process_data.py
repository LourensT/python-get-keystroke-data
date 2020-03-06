import csv
import os
'''
WARNING:
This code is very much specific to the following string.
I got lazy in handling the edge cases and hardcoded the errorhandling
for commonly occuring problems with the following.
Additionally, this code is pretty ugly, but it serves it purpose well.

Issues to deal with:
* make a header and make all other rows just numbers
* h in front from last entry -> discard previous entry and restore new entry with correct timestamps
* t lowercase when shift was released before release of T
* it appears that some entries that end on a space are automatically expected
'''

class CleanData:

    def __init(self):
        print('initialized')

    def get_header(self, string):
        header = []
        for c in string:
            if c.isupper():
                header.append("shift_down")
                header.append("{}_down".format(c))
                header.append("{}_up".format(c))
                header.append("shift_up")
            else:
                header.append("{}_down".format(c))
                header.append("{}_up".format(c))

        return header

    def clean(self, filepath):
        STRING = "Thanks 4 fish"
        clean_fp =filepath[0:-4] + "_clean.csv"

        #load in data and discard all which have lost the "h" on the next page
        with open(filepath,'r') as input:
            reader = csv.reader(input)
            new_file = []
            prev_row = [eval(r) for r in next(reader)]
            init_length = 1
            for row in reader:
                init_length += 1
                row = [eval(r) for r in row]
                if row[0][0] == 'shift':
                    new_file.append(prev_row)
                    prev_row = row
                if row[0][0] == 'h':
                    prev_row = row[1::]
                else:
                    prev_row = row

        #Clean data
        with open(clean_fp, 'w', newline='') as output:
            writer = csv.writer(output)
            header = self.get_header(STRING)
            writer.writerow(header)
            for entry in new_file:
                if len(entry) == len(header):
                    row = [0,]*len(header)
                    encountered = header.copy() #keep track of which character events have been encountered
                    for event in entry:
                        expr = event[0]+'_'+event[2]
                        if expr in encountered:
                            row[encountered.index(expr)] = event[1]
                            encountered[encountered.index(expr)] = 0
                        else:
                            if event[0] == 't': #t - lowercase when released
                                expr = 'T_'+event[2]
                                row[encountered.index(expr)] = event[1]
                                encountered[encountered.index(expr)] = 0
                            else:
                                print('this should not happen')
                                print(expr)

                    if row[0] != 0:     #cases where h was discarded have to be gauged on first event
                        t0 = row[0]
                        row = [(r - t0) for r in row]

                    writer.writerow(row)

        # Sanity Checks to see wheter data is correct
        with open(clean_fp, 'r') as input:
            reader = csv.reader(input)
            next(reader)
            final_length = 0
            errorcounter = 0
            for row in reader:
                final_length += 1
                if row.count('0') != 1:
                    errorcounter += 1
                    print(row)
            print('cleaned result saved in {}'.format(clean_fp))
            print("{} suspicious case(s), printed above".format(errorcounter))
            print("Started with {} entries, ended up with {}".format(init_length, final_length))

cd = CleanData()
for file in os.listdir(os.getcwd()+ "\\datasets\\"):
    cd.clean(os.getcwd()+ "\\datasets\\"+file)
