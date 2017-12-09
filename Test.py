import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import timeit

if __name__ == '__main__':
    implementations = ['numpy', 'naive', 'fft']
    sizes = ['image_16', 'image_32', 'image_64', 'image_128', 'image_256', 'image_512']
    colors = {'opencv':'#79abfc', 'numpy':'#a078fc', 'naive':'#fc78d0', 'fft':'#78fcb1', 'fftw':'#c7fc78'}

    times = {}
    for i in implementations:
        times[i] = {}
        for size in sizes:
            setup = 'from TestFourierTransform import ft_{}, {}'.format(i, size)
            times[i][size] = timeit.timeit('ft_{}({})'.format(i, size), setup=setup, number=10)
    
    fig = plt.figure()
    fig.patch.set_facecolor('white')

    ax = fig.add_subplot(111)
    ax.tick_params(axis='x', pad = 10)

    font = FontProperties()
    font.set_family('monospace')
    font.set_size(12)

    plt.xlabel('Image Size', fontproperties = font)
    plt.ylabel('Run Time', fontproperties = font)

    for i in times.keys():
        size = []
        time = []
        for s in sizes:
            size = size + [s]
            time = time + [times[i][s]]
        plt.plot(range(len(time)), time, color = colors[i], label = i)
        plt.xticks(range(len(size)), size, fontproperties = font)

    for tick in ax.get_yticklabels():
        tick.set_fontproperties(font)
    
    plt.legend(bbox_to_anchor=(0.4, 0.75), bbox_transform=plt.gcf().transFigure, prop = font)
    plt.savefig('test.png', transparent = True)
    plt.show()
