from graphics import *


def rotate(A, B, C):
    return (B[0] - A[0]) * (C[1] - B[1]) - (B[1] - A[1]) * (C[0] - B[0])


def jarvismarch(A):
    n = len(A)
    P = list(range(n))
    # start point
    for i in range(1, n):
        if A[P[i]][0] < A[P[0]][0]:
            P[i], P[0] = P[0], P[i]
    H = [P[0]]
    del P[0]
    P.append(H[0])
    while True:
        right = 0
        for i in range(1, len(P)):
            if rotate(A[H[-1]], A[P[right]], A[P[i]]) < 0:
                right = i
        if P[right] == H[0]:
            break
        else:
            H.append(P[right])
            del P[right]
    return H


def main():
    a = [
        [1, 2],
        [2, 3],
        [3, 4],
        [4, 6],
        [5, 2],
        [6, 8],
        [7, 4],
        [8, 3],
        [5, 1]
    ]
    b = jarvismarch(a)
    points_objects = list()
    win = GraphWin('Draw a Triangle', 350, 350)
    win.setBackground('yellow')

    for i in range(len(a)):
        points_objects.append(Point(a[i][0] * 20, a[i][1] * 20))
        points_objects[i].draw(win)

    for i in range(len(b) - 1):
        Line(points_objects[b[i]], points_objects[b[i + 1]]).draw(win)
    # Connect last and first points
    Line(points_objects[b[len(b) - 1]], points_objects[b[0]]).draw(win)

    win.getMouse()
    win.close()


main()
