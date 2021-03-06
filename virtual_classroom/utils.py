from __future__ import print_function, unicode_literals
import os
import json

from .parameters import get_parameters

# Python3 and 2 compatible
try: input = raw_input
except NameError: pass


class CSVObject(object):
    def __init__(self, filename=None, content=None):
        if filename is None:
            self.raw_content = content
        else:
            self.raw_content = open(filename, "rb").read().decode("utf-8")
        self.values = []
        self._parse()

    def _parse(self):
        try:
            self._csv_read("utf-8")
        except:
            self._csv_read(None)

    def _csv_read(self, encoding):
        import csv
        if encoding is None:
            gen = self.raw_content.splitlines()
        else:
            gen = self.raw_content.encode(encoding).splitlines()
        reader = csv.reader(gen)
        # from IPython import embed; embed();
        for row in reader:
            if encoding is not None:
                row = [i.decode(encoding) for i in row]
            self.values.append(row)

    def __getitem__(self, item):
        return self.values[item]


def download_google_spreadsheet(name, filename=None):
    import gspread
    from oauth2client.service_account import ServiceAccountCredentials

    # Get password and username
    json_file = input("Path to Google credentials JSON file (see" \
                      " http://gspread.readthedocs.org/en/latest/oauth2.html): ")

    # Log on to disk
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file, scope)

    gc = gspread.authorize(credentials)
    try:
        wks = gc.open(name).sheet1.export()
    except gspread.SpreadsheetNotFound:
        json_key = json.load(open(json_file))
        print("The spreadsheet document '{}' not found. Maybe it does not exist?".format(name))
        print("Otherwise, make sure that you shared the spreadsheet with {} and try again.".format(
            json_key['client_email']))
        return None

    if filename is not None:
        with open(filename, "wb") as f:
            f.write(wks.encode("utf-8"))

    return wks.decode("utf-8")


def create_students_file_from_csv(csv_str=None, csv_filename=None, output_filename="students_base.txt"):
    csv = CSVObject(filename=csv_filename, content=csv_str)

    if os.path.isfile(output_filename):
        answ = input("The %s file exists, are you " % (output_filename) + \
                     "sure you want to overwrite this?! (yes/no): ")
        if "yes" != answ.lower():
            exit(1)

    string = 'Attendance // ' + ' // '.join(csv[0][1:]) + '\n'
    for row in csv[1:]:
        string += '- // ' + ' // '.join(row[1:]) + '\n'  # Remove timestamp from each row

    with open(output_filename, 'wb') as f:
        f.write(string.encode("utf-8"))

    print('Output written on %s.' % output_filename)
    return output_filename




