from zipfile import ZipFile


with ZipFile("sample.zip") as myzip:
    with myzip.open('file1.txt') as my_file:

        line = my_file.readline()

        print(line)


