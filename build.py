from o3a2 import *

@command()
@step()
def task_a():
    print("task_a")
    run(["bash", "-c", "bla"])


@command()
@step(task_a)
@foreach([1,2,3])
def task_b(num):
    print("task_b %d" % num)


@command()
@step(task_a, task_b)
def task_c():
    print("task_c")


if __name__ == "__main__":
    o3a2()