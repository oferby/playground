def func_main(func_int):
    def func_first():
        result = func_int()
        print(result)

    return func_first


def f_int():
    return {'this_k': 'this_v',
            'that_k': 'that_v'}


f = func_main(f_int)
f()


f = lambda: print('hello lambda')

f()
