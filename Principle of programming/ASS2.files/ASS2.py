class FriezeError(Exception):
    def __init__(self, err="Incorrect input."):
        Exception.__init__(self, err)


class Frieze:
    def __init__(self, file_name):
        self.file_name = file_name
        with open(self.file_name) as files:
            lines = files.readlines()
            lines = [line.strip() for line in lines]
            lis = []
            lis_test = []
            for k in lines:
                if k != '':
                    lis_test.append([x for x in k.split()])
            for v in lis_test:
                for j in v:
                    if j not in [str(x) for x in range(16)]:
                        raise FriezeError('Incorrect input.')

            for i in lines:
                if i != '':
                    lis.append([int(x) for x in i.split()])
            self.lis = lis

            if len(lis) < 3 or len(lis) > 17:
                raise FriezeError('Incorrect input.')

            length = len(lis[0])
            for i in lis:
                if len(i) < 5 or len(i) > 51:
                    raise FriezeError('Incorrect input.')
                elif i[-1] not in [0, 1]:
                    raise FriezeError('Input does not represent a frieze.')
                elif len(i) != length:
                    raise FriezeError('Incorrect input.')
                for v in i:
                    if v not in range(16):
                        raise FriezeError('Incorrect input.')
            length1 = len(lis[0])
            for j in lis[0][:length1 - 1]:
                if j not in [4, 12]:
                    raise FriezeError('Input does not represent a frieze.')
            for k in lis[-1][:length1 - 2]:
                if k in range(8, 16):
                    raise FriezeError('Input does not represent a frieze.')
            if lis[0][-1] != 0:
                raise FriezeError('Input does not represent a frieze.')

            for x in range(1, len(lis) - 1):
                for y in range(len(lis[0])):
                    if lis[x][y] in [i for i in range(8, 16)] and lis[x + 1][y] in [2, 3, 6, 7, 10, 11, 14, 15]:
                        raise FriezeError('Input does not represent a frieze.')
            for i in lis:
                if i[0] in [1, 3, 5, 7, 9, 11, 13, 15] and i[-1] != 1:
                    raise FriezeError('Input does not represent a frieze.')
                elif i[0] in [0, 2, 4, 6, 8, 10, 12, 14] and i[-1] != 0:
                    raise FriezeError('Input does not represent a frieze.')
            # 找到period 先反转矩形 然后看有没有相同数列
            def convert_grid_90(new_grid):
                new_grid.reverse()
                new_grid = [[j[i] for j in new_grid] for i in range(len(new_grid[0]))]
                return new_grid

            lis.reverse()
            new_lis = convert_grid_90(lis)
            period = []
            for i in range(1, len(new_lis)):
                if new_lis[0] == new_lis[i]:
                    period.append(i)
            # 把找到的priod带入验证遍历全部矩阵如果发现所带入的period只要有一个不相同则这个period并不是真正的period只有全部都满足相等
            # 才会return true
            def find_period(v):
                for k in range(v, len(new_lis) - 1, v):
                    if new_lis[k:k + v] != new_lis[:v]:
                        return False
                return True

            lis_period = []
            for i in period:
                if find_period(i):
                    lis_period.append(i)
            self.lis_period = lis_period

            if len(lis_period) == 0 or lis_period[0] == 1:
                raise FriezeError('Input does not represent a frieze.')

    def analyse(self):
        lis_period = self.lis_period
        lis = self.lis
        period = lis_period[0]

        def Dec2Bin(dec):
            if dec == 0:
                return '0000'
            temp = []
            result = ''
            while dec:
                quo = dec % 2
                dec = dec // 2
                temp.append(quo)
            while temp:
                result += str(temp.pop())
            if len(list(result)) == 1:
                result = '000' + result
            elif len(list(result)) == 2:
                result = '00' + result
            elif len(list(result)) == 3:
                result = '0' + result
            return result

        def isVR(lis):

            def check_VR(period1):
                for i in range(len(period1)):
                    a = len(period1[0])
                    for j in range(a // 2):
                        a -= 1
                        if period1[i][j][1:2] != period1[i][a][1:2]:
                            return False
                        if i < len(period1) - 1 and period1[i][j][:1] != period1[i + 1][a][2:3]:
                            return False
                        if period1[i][j + 1][3:4] != period1[i][a][3:4]:
                            return False
                return True

            period1 = []
            period2 = []
            lis1 = []
            lis2 = []
            for k in lis:
                for j in k:
                    lis1.append(Dec2Bin(j))
                lis2.append(lis1)
                lis1 = []
            for i in lis2:
                period2.append(i[:period * 2])
            m = 0
            n = period
            lis_check = []
            for v in range(period + 1):
                m += 1
                n += 1
                for k in period2:
                    period1.append(k[m - 1:n + 2])
                lis_check.append(period1)
                period1 = []
            count = 0
            for x in lis_check:
                if check_VR(x):
                    count += 1
            if count > 0:
                return True
            else:

                return False

        def isRT(lis):
            def check_RT(period1):
                lis_len = len(period1)
                for i in range(lis_len):
                    # print(len(period1))
                    a = len(period1[0])
                    # print('a',a)
                    for j in range(a // 2 + 1):
                        a -= 1
                        if period1[i][j][1:2] != period1[lis_len - i - 1][a][1:2]:
                            return False
                        # 判断竖线是非相等
                        if i > 0 and j > 0 and period1[i][j][3:4] != period1[lis_len - i][a + 1][3:4]:
                            return False
                        # 判断斜上线是否相等
                        if i > 0 and period1[i][j][2:3] != period1[lis_len - i][a][2:3]:
                            return False
                        # 判断斜下线是否相等
                        if i > 0 and period1[i][j][:1] != period1[lis_len - i - 2][a][:1]:
                            return False
                return True

            period1 = []
            period2 = []
            lis1 = []
            lis2 = []
            for k in lis:
                for j in k:
                    lis1.append(Dec2Bin(j))
                lis2.append(lis1)
                lis1 = []
            for i in lis2:
                period2.append(i[:period * 2])

            m = 0
            n = period
            lis_check = []
            for v in range(period + 1):
                m += 1
                n += 1
                for i in range(1, 2):
                    for k in period2:
                        period1.append(k[m - 1:n + 2])
                    lis_check.append(period1)
                    period1 = []
            count = 0
            for x in lis_check:
                if check_RT(x):
                    count += 1
            if count > 0:
                return True
            else:

                return False

        def isGHR(lis):
            period1 = []
            period2 = []
            period3 = []
            lis1 = []
            lis2 = []
            for k in lis:
                for j in k:
                    lis1.append(j)
                lis2.append(lis1)
                lis1 = []
            for i in lis2:
                period3.append(i[:period * 2])
            for i in lis2:
                period1.append(i[:period])
            for j in lis2:
                period2.append(j[int(period / 2):period + int(period / 2)])
            lis_GHR = period1 + period2
            if isHR(lis_GHR):
                return True
            else:
                return False

        def isHR(lis):
            def check_HR(period1):
                lis_len = len(period1)
                if lis_len % 2 == 0:
                    k = 0
                else:
                    k = 1
                for i in range(lis_len // 2 + k):
                    a = len(period1[0])
                    for j in range(a // 2 + 2):
                        # 判断横线是否相等
                        if period1[i][j][1:2] != period1[lis_len - i - 1][j][1:2]:
                            return False
                        # 判断斜线是否相等
                        if period1[i][j][:1] != period1[lis_len - i - 1][j][2:3]:
                            return False
                        # 判断竖线是否相等
                        if period1[i + 1][j][3:4] != period1[lis_len - i - 1][j][3:4]:
                            return False
                return True

            lis1 = []
            lis2 = []
            period1 = []
            for k in lis:
                for j in k:
                    lis1.append(Dec2Bin(j))
                lis2.append(lis1)
                lis1 = []
            for i in lis2:
                period1.append(i[:period * 2])
            if check_HR(period1):
                return True
            else:
                return False

        isVR = isVR(lis)
        isGHR = isGHR(lis)
        isHR = isHR(lis)
        isRT = isRT(lis)

        if not isVR and not isGHR and not isHR and not isRT:
            print(f'Pattern is a frieze of period {lis_period[0]} that is invariant under translation only.')

        elif isVR and not isGHR and not isHR and not isRT:
            print(
                f'Pattern is a frieze of period {lis_period[0]} that is invariant under translation\n        and vertical reflection only.')

        elif not isVR and not isGHR and isHR and not isRT:
            print(
                f'Pattern is a frieze of period {lis_period[0]} that is invariant under translation\n        and horizontal reflection only.')

        elif not isVR and isGHR and not isHR and not isRT:
            print(
                f'Pattern is a frieze of period {lis_period[0]} that is invariant under translation\n        and glided horizontal reflection only.')

        elif not isVR and not isGHR and not isHR and isRT:
            print(
                f'Pattern is a frieze of period {lis_period[0]} that is invariant under translation\n        and rotation only.')

        elif isVR and isGHR and not isHR and isRT:
            print(
                f'Pattern is a frieze of period {lis_period[0]} that is invariant under translation,\n        glided horizontal and vertical reflections, and rotation only.')

        elif isVR and not isGHR and isHR and isRT:
            print(
                f'Pattern is a frieze of period {lis_period[0]} that is invariant under translation,\n        horizontal and vertical reflections, and rotation only.')

    def display(self):
        lis = self.lis

        def Dec2Bin(dec):
            if dec == 0:
                return '0000'
            temp = []
            result = ''
            while dec:
                quo = dec % 2
                dec = dec // 2
                temp.append(quo)
            while temp:
                result += str(temp.pop())
            if len(list(result)) == 1:
                result = '000' + result
            elif len(list(result)) == 2:
                result = '00' + result
            elif len(list(result)) == 3:
                result = '0' + result
            return result

        lis1 = []
        lis2 = []
        for k in lis:
            for j in k:
                lis1.append(Dec2Bin(j))
            lis2.append(lis1)
            lis1 = []

        lis_heng = []
        lis_heng1 = []

        for i in lis2:
            for j in i:
                a = list(j)
                if a[1:2] == ['1']:
                    lis_heng1.append(1)
                else:
                    lis_heng1.append(0)
            lis_heng.append(lis_heng1)
            lis_heng1 = []

        lis_vertical = []
        lis_vertical1 = []

        for i in lis2:
            for j in i:
                a = list(j)
                if a[3:4] == ['1']:
                    lis_vertical1.append(1)
                else:
                    lis_vertical1.append(0)
            lis_vertical.append(lis_vertical1)
            lis_vertical1 = []
        lis_diaup = []
        lis_diaup1 = []

        for i in lis2:
            for j in i:
                a = list(j)
                if a[2:3] == ['1']:
                    lis_diaup1.append(1)
                else:
                    lis_diaup1.append(0)
            lis_diaup.append(lis_diaup1)
            lis_diaup1 = []

        lis_diadown = []
        lis_diadown1 = []

        for i in lis2:
            for j in i:
                a = list(j)
                if a[0:1] == ['1']:
                    lis_diadown1.append(1)
                else:
                    lis_diadown1.append(0)
            lis_diadown.append(lis_diadown1)
            lis_diadown1 = []

        def find_NS_point(grid):
            xy_pos = []
            for x in range(len(grid)):
                for y in range(len(grid[0])):
                    if grid[x][y] == 1:
                        xy_pos.append((y, x))
            if xy_pos == []:
                return
            point = sorted(xy_pos)
            first_num = point[0][0]
            loc = [point[0]]
            count = 0

            for i in range(1, len(point)):
                count += 1
                if point[i][0] == first_num and point[i][1] - 1 == point[i - 1][1]:
                    continue
                else:
                    loc.append(point[i])
                    loc.append(point[count - 1])
                    first_num = point[i][0]
            loc.append(point[-1])
            loc = sorted(loc)
            start_point = [(k[0], k[1] - 1) for k in loc[::2]]
            end_point = [(k[0], k[1]) for k in loc[1::2]]
            path = list(map(lambda x, y: [x, y], start_point, end_point))
            return path

        def find_WE_point(grid):
            xy_pos = []
            for x in range(len(grid)):
                for y in range(len(grid[0])):
                    if grid[x][y] == 1:
                        xy_pos.append((y, x))
            if xy_pos == []:
                return
            point = sorted(xy_pos, key=lambda x: x[1])
            first_num = point[0][1]
            loc = [point[0]]
            count = 0
            for i in range(1, len(point) - 1):
                count += 1
                # 如果第一个（x，y）中x等于first_num and 当前一个数减1等于前一个数则继续执行
                if point[i][1] == first_num and point[i][0] - 1 == point[i - 1][0]:
                    continue
                else:
                    loc.append(point[count - 1])
                    loc.append(point[i])
                    first_num = point[i][1]
            loc.append(point[-1])
            loc = sorted(loc, key=lambda x: x[1])
            start_point = [(k[0], k[1]) for k in loc[::2]]
            end_point = [(k[0] + 1, k[1]) for k in loc[1::2]]
            path = list(map(lambda x, y: [x, y], start_point, end_point))
            return path

        def find_NW_SE_point(grid):
            xy_pos = []

            for x in range(len(grid)):
                for y in range(len(grid[0])):
                    if grid[x][y] == 1:
                        xy_pos.append((y, x))
            if xy_pos == []:
                return
            point = sorted(xy_pos, key=lambda x: (x[1], x[0]))
            loc1 = []

            for i in range(0, len(point)):
                if (point[i][0] + 1, point[i][1] + 1) in point:
                    continue
                else:
                    loc1.append((point[i][0] + 1, point[i][1] + 1))
            loc2 = []
            point = sorted(xy_pos, key=lambda x: (x[0], x[1]))
            for i in range(0, len(point)):
                if (point[i][0] - 1, point[i][1] - 1) in point:
                    continue
                else:
                    loc2.append((point[i][0], point[i][1]))
            loc3 = []
            for k in loc1:
                for v in loc2:
                    if k[0] - v[0] == k[1] - v[1] and k[0] > v[0] and k[1] > v[1] and v not in [x[0] for x in loc3]:
                        loc3.append([v, k])
            path = sorted(loc3, key=lambda x: (x[0][1], x[0]))
            return path

        def find_SW_NE_point(grid):
            xy_pos = []

            for x in range(len(grid)):
                for y in range(len(grid[0])):
                    if grid[x][y] == 1:
                        xy_pos.append((y, x))
            if xy_pos == []:
                return
            point = sorted(xy_pos, key=lambda x: (x[1], x[0]))
            loc1 = []

            for i in range(0, len(point)):
                if (point[i][0] - 1, point[i][1] + 1) in point:
                    continue
                else:
                    loc1.append((point[i][0], point[i][1]))
            loc2 = []
            point = sorted(xy_pos, key=lambda x: (x[0], x[1]))
            for i in range(0, len(point)):
                if (point[i][0] + 1, point[i][1] - 1) in point:
                    continue
                else:
                    loc2.append((point[i][0] + 1, point[i][1] - 1))
            loc3 = []
            for k in loc1:
                for v in loc2:
                    if v[0] - k[0] == k[1] - v[1] and k[0] < v[0] and k[1] > v[1] and k not in [x[0] for x in loc3]:
                        loc3.append([k, v])
            path = sorted(loc3, key=lambda x: (x[0][1], x[0]))
            return path

        filename = self.file_name
        if '.' in filename:
            filename_head = filename[0: filename.index('.')]
        else:
            filename_head = filename

        with open(filename_head + '.tex', 'w', encoding='utf-8') as latex_file:
            print('\\documentclass[10pt]{article}\n'
                  '\\usepackage{tikz}\n'
                  '\\usepackage[margin=0cm]{geometry}\n'
                  '\\pagestyle{empty}\n'
                  '\n'
                  '\\begin{document}\n'
                  '\n'
                  '\\vspace*{\\fill}\n'
                  '\\begin{center}\n'
                  '\\begin{tikzpicture}[x=0.2cm, y=-0.2cm, thick, purple]', file=latex_file
                  )
            print('% North to South lines', file=latex_file)
            if find_NS_point(lis_vertical):
                for i in find_NS_point(lis_vertical):
                    print(f'    \draw ({i[0][0]},{i[0][1]}) -- ({i[1][0]},{i[1][1]});', file=latex_file)

            print('% North-West to South-East lines', file=latex_file)
            if find_NW_SE_point(lis_diadown):
                for i in find_NW_SE_point(lis_diadown):
                    print(f'    \draw ({i[0][0]},{i[0][1]}) -- ({i[1][0]},{i[1][1]});', file=latex_file)

            print('% West to East lines', file=latex_file)
            if find_WE_point(lis_heng):
                for i in find_WE_point(lis_heng):
                    print(f'    \draw ({i[0][0]},{i[0][1]}) -- ({i[1][0]},{i[1][1]});', file=latex_file)

            print('% South-West to North-East lines', file=latex_file)
            if find_SW_NE_point(lis_diaup):
                for i in find_SW_NE_point(lis_diaup):
                    print(f'    \draw ({i[0][0]},{i[0][1]}) -- ({i[1][0]},{i[1][1]});', file=latex_file)

            print('\\end{tikzpicture}\n'
                  '\\end{center}\n'
                  '\\vspace*{\\fill}\n'
                  '\n'
                  '\\end{document}', file=latex_file
                  )
