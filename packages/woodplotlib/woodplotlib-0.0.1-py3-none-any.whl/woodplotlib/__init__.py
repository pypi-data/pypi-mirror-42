import numpy as _np

name = "woodplotlib"
version = '0.0'

class Board(object):
    """A board that may also have a location."""
    _all_boards = []

    def __init__(self, **kwargs):
        self.thickness = 0.75
        self.width = 1.75
        self.length = 12
        self.origin = _np.array([0, 0, 0.])
        self._far = _np.array([0, 0, 1.])
        self._left = _np.array([0, 1., 0])
        self._front = _np.array([1., 0, 0])
        self.color = 'C' + str(len(Board._all_boards) % 10)
        if 'dim' in kwargs:
            if kwargs['dim'] == '1x2':
                self.width = 1.75
            elif kwargs['dim'] == '1x3':
                self.width = 2.75
            elif kwargs['dim'] == '1x4':
                self.width = 3.75
        if 'feet' in kwargs:
            self.length = 12*kwargs['feet']
        if 'length' in kwargs:
            self.length = kwargs['length']
        if 'color' in kwargs:
            self.color = kwargs['color']
        Board._all_boards.append(self)
    def _corners(self):
        import numpy as np
        points = np.zeros((3,8))
        points[:,0] = self.origin
        points[:,1] = self.origin + self.width*self._left
        points[:,2] = points[:,1] + self.length*self._far
        points[:,3] = points[:,2] - self.width*self._left
        for i in range(4):
            points[:,4+i] = points[:,i] + self.thickness*self._front
        return points
    def join(self, board, relationship='far-left-edge-to-far-left-edge'):
        if relationship == 'end-to-far-left-edge':
            self.origin = board.origin + board._left*board.width + board._far*board.length
            self._far = 1.0*board._left
            self._left = -1.0*board._far
            self._front = 1.0*board._front
        elif relationship == 'left-edge-to-far-end':
            self.origin = board.origin + board._left*board.width
            self._far = 1.0*board._left
            self._left = -1.0*board._far
            self._front = 1.0*board._front
        elif relationship == 'end-to-far-front':
            self.origin = board.origin + board._front*board.thickness + board._far*board.length
            self._far = 1.0*board._front
            self._front = -1.0*board._far
            self._left = 1.0*board._left
        elif relationship == 'end-to-near-front':
            self.origin = board.origin + board._front*board.thickness
            self._far = 1.0*board._front
            self._front = 1.0*board._far
            self._left = 1.0*board._left
        elif relationship == 'end-to-far-back':
            self.origin = board.origin + board._far*board.length - board._far*self.thickness
            self._far = -board._front
            self._front = board._far
            self._left = 1.0*board._left
        elif relationship == 'end-to-near-back':
            self.origin = board.origin + board._far*self.thickness
            self._far = -board._front
            self._front = -board._far
            self._left = 1.0*board._left
        elif relationship == 'edge-to-left-edge':
            self.origin = board.origin + board._left*board.width
            self._far = 1.0*board._far
            self._left = 1.0*board._left
            self._front = 1.0*board._front
        else:
            raise ValueError('Unrecognized relationship: '+ relationship)

def show3d():
    import matplotlib.pyplot as plt
    import numpy as np
    from mpl_toolkits.mplot3d import Axes3D

    fig = plt.figure('3d')
    ax = fig.gca(projection='3d')
    bottom = np.array([0,1,2,3,0])
    top = bottom + 4
    maxdist = 0
    mindist = 0
    for b in Board._all_boards:
        corners = b._corners()

        plt.figure('3d')
        ax.plot(corners[0,bottom], corners[1,bottom], corners[2,bottom], color=b.color)
        ax.plot(corners[0,top], corners[1,top], corners[2,top], color=b.color)
        for i in range(4):
            ax.plot(corners[0,i::4], corners[1,i::4], corners[2,i::4], color=b.color)
        plt.plot(corners[0,top[::2]], corners[1,top[::2]], corners[2,top[::2]], color=b.color)
        plt.plot(corners[0,top[1::2]], corners[1,top[1::2]],  corners[2,top[1::2]], color=b.color)
        if corners.max() > maxdist:
            maxdist = corners.max()
        if corners.min() < mindist:
            mindist = corners.min()

        plt.figure('xy')
        plt.plot(corners[0,bottom], corners[1,bottom], color=b.color)
        plt.plot(corners[0,top], corners[1,top], color=b.color)
        for i in range(4):
            plt.plot(corners[0,i::4], corners[1,i::4], color=b.color)

        plt.figure('xz')
        plt.plot(corners[0,bottom], corners[2,bottom], color=b.color)
        plt.plot(corners[0,top], corners[2,top], color=b.color)
        for i in range(4):
            plt.plot(corners[0,i::4], corners[2,i::4], color=b.color)

        plt.figure('yz')
        plt.plot(corners[1,bottom], corners[2,bottom], color=b.color)
        plt.plot(corners[1,top], corners[2,top], color=b.color)
        for i in range(4):
            plt.plot(corners[1,i::4], corners[2,i::4], color=b.color)

    plt.figure('3d')
    plt.scatter([mindist,maxdist],[mindist,maxdist],[mindist,maxdist])

    plt.figure('xy')
    plt.axes().set_aspect('equal')
    plt.xlabel('x')
    plt.ylabel('y')

    plt.figure('xz')
    plt.axes().set_aspect('equal')
    plt.xlabel('x')
    plt.ylabel('z')

    plt.figure('yz')
    plt.axes().set_aspect('equal')
    plt.xlabel('y')
    plt.ylabel('z')

    plt.show()
