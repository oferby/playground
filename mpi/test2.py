# use broadcast
from mpi4py import MPI

comm = MPI.COMM_WORLD

my_rank = comm.Get_rank()
p = comm.Get_size()


def get_data():
    a = None
    b = None

    if my_rank == 0:
        a = 10
        b = 15

    a = comm.bcast(a, root=0)
    b = comm.bcast(b, root=0)
    return a, b


a, b = get_data()
total = a * my_rank + b

print("rank: " + str(my_rank) + ", my total: " + str(total))

# reduce
total = comm.reduce(total)
if my_rank == 0:
    print("total: " + str(total))

MPI.Finalize()
