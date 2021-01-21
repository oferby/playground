# run using mpirun python3 test1.py
# or
#   mpirun -oversubscribe -np 10 python3 test1.py
#
from mpi4py import MPI

comm = MPI.COMM_WORLD

my_rank = comm.Get_rank()
p = comm.Get_size()

if my_rank != 0:
    msg = "Hello from process " + str(my_rank)
    comm.send(msg, dest=0)
else:
    for pid in range(1, p):
        msg = comm.recv(source=pid)
        print("pid 0 received from " + str(pid) + ": " + msg)

MPI.Finalize()
