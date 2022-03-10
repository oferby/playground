
with open("file2.txt","r") as f:
    lst = []
    lst = f.readlines()
    f.close()


for i,t in enumerate(lst):
    lst[i] = int(t)

lst.sort()

for i,t in enumerate(lst):
    lst[i] = str(t) + '\n'


f = open("file3.txt","w")
f.writelines(lst)
f.close()
