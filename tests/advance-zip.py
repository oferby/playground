import zipfile
with zipfile.ZipFile("/tmp/unzip_me_for_instructions.zip", 'r') as f:
    f.extractall("/tmp/extract")
