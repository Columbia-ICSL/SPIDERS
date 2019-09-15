def find_vector(imgP, imgI, row, col, MBSIZE, P, rowSize, colSize):

    import numpy as np

    def costFuncMAD (currentBlk, refBlk, MBSIZE):
        cost = int(0)
        delta = int(0)
        for i in range(MBSIZE):
            for j in range(MBSIZE):
                delta = int(int(currentBlk[i,j]) - int(refBlk[i,j])) # Calulating MAD
                if delta < 0:
                    delta = int(delta * -1)
                cost = int(cost + delta)
        return cost

    def minCost(costs, P):
        (row, col) = costs.shape
        min = costs[P, P]
        dx = dy = P
        # Finding minimum from all mbSize*mbSize MAD values
        for i in range(row):
            for j in range(col):
                if costs[i, j] < min:
                    min = costs[i, j]
                    dx = j
                    dy = i
        return dx, dy

    costs = np.ones((2 * P + 1, 2 * P + 1)) * float('inf')
    for m in range(-P, P):
        for n in range(-P, P):
            refBlkVer = row + m   # row/Vert co-ordinate for ref block
            refBlkHor = col + n   # col/Horizontal co-ordinate
            if ( refBlkVer < 0 or refBlkVer+MBSIZE >= rowSize \
                    or refBlkHor < 0 or refBlkHor+MBSIZE >= colSize):
                continue

            cost = costFuncMAD(imgP[row : row + MBSIZE, col : col + MBSIZE], \
                 imgI[refBlkVer : refBlkVer + MBSIZE, refBlkHor : refBlkHor + MBSIZE], MBSIZE)
            costs[m + P, n + P] = cost

    dx, dy = minCost(costs, P)
    dx = dx - P - 1
    dy = dy - P - 1
    return dx, dy
