import sys
import numpy as np
import copy


class Log:
    def __init__(self):
        self.route_log = []
        self.route_log_tmp = []
        self.episode = 0


class Data:

    def __init__(self, lines):
        tmp_mtx = []
        self.step = lines[0]
        self.row = lines[1].split()[0]
        self.col = lines[1].split()[1]
        for lp in range(int(self.row)):
            tmp_mtx.append(list(lines[2 + lp]))
        self.mtx = tmp_mtx
        self.a_coo, self.b_coo = self.a_b_coo_read()

    def a_b_coo_read(self):  # A,Bの座標を求める
        a_coo = -1
        b_coo = -1
        for row, arr in enumerate(self.mtx):
            try:
                a_coo = (row, arr.index("A"))
            except ValueError:
                pass
            try:
                b_coo = (row, arr.index("B"))
            except ValueError:
                pass
        return a_coo, b_coo


class Agent:

    def __init__(self, data, depth, ct, mtx, log):
        self.y = data.a_coo[0]
        self.x = data.a_coo[1]
        self.ct = ct
        self.depth = depth
        self.mtx = mtx
        self.bool = False
        self.data = data

    def add_log(self, data, a_coo, depth, ct, mtx, log):
        string = str(a_coo[0]) + "-" + str(a_coo[1])
        setattr(self, string, Agent(data, depth, ct, copy.deepcopy(mtx), log))
        getattr(self, string).depth = depth
        getattr(self, string).y = a_coo[0]
        getattr(self, string).x = a_coo[1]
        if getattr(self, string).move(log):
            log.route_log_tmp.pop()
            return True

    def state(self):
        return self.y, self.x

    def move(self, log):
        actions = np.array([[0, -1], [-1, 0], [0, 1], [1, 0]])
        coo = np.array(self.state())
        if self.state() == self.data.b_coo:
            self.bool = True
            log.route_log.append(copy.deepcopy(log.route_log_tmp))
            return True
        for n, ac in enumerate(actions):
            self.mtx[coo[0]][coo[1]] = '#'
            if self.can_move(coo + ac):
                log.route_log_tmp.append(coo)
                self.add_log(self.data, list(coo + ac), self.depth + 1, self.ct + 1, self.mtx, log)
        try:
            log.route_log_tmp.pop()
        except IndexError:
            pass

    def can_move(self, coo):
        try:
            if 0 > coo[0] or coo[0] >= int(self.data.row):
                return False
            elif 0 > coo[1] or coo[1] >= int(self.data.col):
                return False
            elif self.mtx[coo[0]][coo[1]] == '.' or self.mtx[coo[0]][coo[1]] == 'B':
                return True
            else:
                return False
        except IndexError:
            pass


def road(data):
    log = Log()
    ash = Agent(data, 0, 0, data.mtx, log)
    ash.move(log)
    mini = 1000
    for rt in log.route_log:
        if mini > len(rt):
            mini = len(rt)

    route = []
    for rt in log.route_log:
        if mini == len(rt):
            route.append(list(rt))
    print(mini, encount(route, data))


def encount(route, data):
    enemy = []
    player = 0
    ct = 0
    max_ct = 0

    for row in range(int(data.row)):
        for col in range(int(data.col)):
            if data.mtx[row][col] in ['W', 'N', 'E', 'S']:
                player += 1
            try:
                if data.mtx[row][col] == 'W':
                    for lp in reversed(range(0, col)):
                        if data.mtx[row][lp] != '.':
                            break
                        else:
                            enemy.append([row, lp, player])
                if data.mtx[row][col] == 'N':
                    for lp in reversed(range(0, row)):
                        if data.mtx[lp][col] != '.':
                            break
                        else:
                            enemy.append([lp, col, player])
                if data.mtx[row][col] == 'E':
                    for lp in range(col + 1, int(data.col)):
                        if data.mtx[row][lp] != '.':
                            break
                        else:
                            enemy.append([row, lp, player])
                if data.mtx[row][col] == 'S':
                    for lp in range(row + 1, int(data.row)):
                        if data.mtx[lp][col] != '.':
                            break
                        else:
                            enemy.append([lp, col, player])
            except IndexError:
                pass
    pass

    passcard = []
    for pl, rt in enumerate(route):
        for rt_el in rt:
            for en in enemy:
                if en[2] in passcard:
                    continue
                if list(rt_el) == en[0:2]:
                    passcard.append(en[2])
                    ct += 1
                    if max_ct < ct:
                        max_ct = ct
        ct = 0
        passcard.clear()

    return max_ct


def main(lines):

    data = Data(lines)
    road(data)


if __name__ == '__main__':
    lines = []
    for l in sys.stdin:
        lines.append(l.rstrip('\r\n'))
    main(lines)
