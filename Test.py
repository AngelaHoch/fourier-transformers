import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import timeit
import numpy as np

if __name__ == '__main__':
    implementations = ['opencv', 'numpy', 'naive', 'fft']
    sizes = ['image_16', 'image_32', 'image_64', 'image_128', 'image_256', 'image_512']
    colors = {'opencv':'#79abfc', 'numpy':'#a078fc', 'naive':'#fc78d0', 'fft':'#78fcb1', 'fftw':'#c7fc78'}

    times = {}
    for i in implementations:
        times[i] = {}
        for size in sizes:
            setup = 'from TestFourierTransform import ft_{}, {}'.format(i, size)
            times[i][size] = timeit.timeit('ft_{}({})'.format(i, size), setup=setup, number=10)

    with plt.xkcd():

        fig = plt.figure()
        fig.patch.set_facecolor('white')
        ax = fig.add_axes((0.1, 0.2, 0.8, 0.7))
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.set_ylim([0, 1])

        plt.xlabel('image sizes')
        plt.ylabel('run times')
    
        for i in times.keys():
            size = []
            time = []
            for s in sizes:
                size = size + [s]
                time = time + [times[i][s]]
            plt.plot(range(len(time)), time, color = colors[i], label = i)
            plt.xticks(range(len(size)), size)
        
        plt.legend(bbox_to_anchor=(0.4, 0.75), bbox_transform=plt.gcf().transFigure)
        plt.savefig('test.png')
        plt.show()