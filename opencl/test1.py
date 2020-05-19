# https://github.com/Gordonei/pyconza-october-2018
# https://github.com/Gordonei/pyconza-october-2018/blob/master/code/PyConZA_OpenCL_Talk.ipynb
import pyopencl
import numpy

ocl_platforms = (platform.name
                 for platform in pyopencl.get_platforms())
print("\n".join(ocl_platforms))

nvidia_platform = [platform
                   for platform in pyopencl.get_platforms()
                   if platform.name == "NVIDIA CUDA"][0]
nvidia_devices = nvidia_platform.get_devices()

# build the program

nvidia_context = pyopencl.Context(devices=nvidia_devices)

program_source = """
      kernel void sum(global float *a, 
                      global float *b,
                      global float *c){
        int gid = get_global_id(0);
        c[gid] = a[gid] + b[gid];
      }
    """
nvidia_program_source = pyopencl.Program(nvidia_context, program_source)
nvidia_program = nvidia_program_source.build()

program_kernel_names = nvidia_program.get_info(pyopencl.program_info.KERNEL_NAMES)
print("Kernel Names: {}".format(program_kernel_names))


def run_ocl_kernel(queue, kernel, global_size,
                   input_tuples, output_tuples,
                   local_size=(32,)):
    # copying data onto the device
    for (array, buffer) in input_tuples:
        pyopencl.enqueue_copy(queue, src=array, dest=buffer)

    # running program on the device
    kernel_arguments = [buffer for (_, buffer) in input_tuples]
    kernel_arguments += [buffer for (_, buffer) in output_tuples]

    kernel(queue, global_size, local_size,
           *kernel_arguments)

    # copying data off the device
    for (arr, buffer) in output_tuples:
        pyopencl.enqueue_copy(queue, src=buffer, dest=arr)

    # waiting for everything to finish
    queue.finish()


def check_sum_results(a, b, c):
    c_ref = a + b
    err = numpy.abs(c - c_ref)
    if (err.sum() > 0.0).any():
        print("result does not match")
    else:
        print("result matches!")


# Synthetic data setup
N = int(2 ** 20)
a = numpy.random.rand(N).astype(numpy.float32)
b = numpy.random.rand(N).astype(numpy.float32)
c = numpy.empty_like(a)

# Device Memory setup
a_nvidia_buffer = pyopencl.Buffer(nvidia_context,
                                  flags=pyopencl.mem_flags.READ_ONLY,
                                  size=a.nbytes)
b_nvidia_buffer = pyopencl.Buffer(nvidia_context,
                                  flags=pyopencl.mem_flags.READ_ONLY,
                                  size=b.nbytes)
c_nvidia_buffer = pyopencl.Buffer(nvidia_context,
                                  flags=pyopencl.mem_flags.WRITE_ONLY,
                                  size=c.nbytes)

nvidia_queue = pyopencl.CommandQueue(nvidia_context)

input_tuples = ((a, a_nvidia_buffer), (b, b_nvidia_buffer),)
output_tuples = ((c, c_nvidia_buffer),)
run_ocl_kernel(nvidia_queue, nvidia_program.sum, (N,), input_tuples, output_tuples)

check_sum_results(a, b, c)
