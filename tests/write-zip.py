from zipfile import ZipFile

zipObj = ZipFile('sample.zip', 'w')

zipObj.write('file1.txt')

zipObj.close()