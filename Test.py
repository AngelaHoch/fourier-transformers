import matplotlib
import timeit

if __name__ == '__main__':
    implementations = ['opencv', 'numpy', 'naive']
    sizes = ['image_16', 'image_32', 'image_64', 'image_128', 'image_256', 'image_512']

    times = {}
    for i in implementations:
        times[i] = {}
        for size in sizes:
            setup = 'from TestFourierTransform import ft_{}, {}'.format(i, size)
            times[i][size] = timeit.timeit('ft_{}({})'.format(i, size), setup=setup, number=10)

    print(times)

    # Generate matplotlib line plot for each implementation and size
    
