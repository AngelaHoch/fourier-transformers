import matplotlib.pyplot as plt
import timeit

if __name__ == '__main__':
    implementations = ['opencv', 'numpy', 'naive']
    sizes = ['image_16', 'image_32', 'image_64', 'image_128', 'image_256', 'image_512']
    #colors = ['c', 'm', 'y', 'k', 'burlywood']

    times = {}
    for i in implementations:
        times[i] = {}
        for size in sizes:
            setup = 'from TestFourierTransform import ft_{}, {}'.format(i, size)
            times[i][size] = timeit.timeit('ft_{}({})'.format(i, size), setup=setup, number=10)

    for i in times.keys():
        size = []
        time = []
        for s in sizes:
            size = size + [s]
            time = time + [times[i][s]]
        plt.plot(range(len(time)), time, label = i)
        plt.xticks(range(len(size)), size)
    
    plt.legend(bbox_to_anchor=(0.4, 0.75), bbox_transform=plt.gcf().transFigure)
    plt.show()