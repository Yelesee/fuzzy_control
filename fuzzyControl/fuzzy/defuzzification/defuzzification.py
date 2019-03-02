class Defuzzy:

    def __init__(self, output_mf, alpha_cut_list):
        self.alpha_cut = alpha_cut_list
        self.output_mf = output_mf
        self.x_cog_total = 0
        cut_points_list_full = []
        mf_points_full = []

        for i in range(len(self.output_mf)):  # num of outputs -> points
            for j in range(len(self.output_mf[i][2])):
                mf_points, cut_points_list = self.outputmf(self.output_mf[i][2][j][1], j, self.output_mf[i][2][j][2],
                                                           self.alpha_cut[i][j])
                cut_points_list_full.append(cut_points_list)
                mf_points_full.append(mf_points)

        mf_points_full = [mf_points_full]
        cut_points_list_full = [cut_points_list_full]

        intersection_list_full = self.intersection(mf_points_full)
        cog_points, new_trapezoid = self.area(self.alpha_cut, cut_points_list_full, intersection_list_full)
        self.centeeofgravity(cog_points, new_trapezoid)

    def outputmf(self, functype, mf_num, mf_points, alpha_cut):  # this func get Property of output membershipfunc to
        # create line equation of them and alpha_cut to produce area points
        mf_points = mf_points[1:len(mf_points) - 1]  # to delete '[', ']' from list
        mf_points = mf_points.split()
        a = int(mf_points[0])
        b = int(mf_points[1])
        c = int(mf_points[2])
        d = int(mf_points[3])
        # this part get the enf og range and convert to int
        # --------------------------------------------------------------------------------------------------
        end = ''
        if self.output_mf[0][1][0] == '[' and self.output_mf[0][1][2] == ' ':
            j = 3
            while self.output_mf[0][1][j] != ']':
                end = end + self.output_mf[0][1][j]
                j = j + 1
        else:
            print("ERROR")

        end = int(end)
        # --------------------------------------------------------------------------------------------------

        cut_points_list = []
        if functype == 'Trapezoid':  # line equation : x=float((y:alpha_cut + m:(1/b-a)*x0:a - y0:0)*1/m:(b-a))

            if mf_num == 0:  # at this state y(a) = 0  -> for find the first mf
                x1 = float((-1 * alpha_cut) * (d - c) + d)
                cut_points_list.append([0, 0])
                cut_points_list.append([0, alpha_cut])
                cut_points_list.append([x1, alpha_cut])
                cut_points_list.append([d, 0])

            else:
                if alpha_cut == 1 and alpha_cut == 0:
                    cut_points_list.append([a, 0])
                    cut_points_list.append([b, alpha_cut])
                    cut_points_list.append([c, alpha_cut])
                    cut_points_list.append([d, 0])

                else:
                    x1 = (b - a) * alpha_cut + a
                    x2 = (c - d) * alpha_cut + d
                    cut_points_list.append([a, 0])
                    cut_points_list.append([x1, alpha_cut])
                    cut_points_list.append([x2, alpha_cut])  # B U G  -->>  x2
                    cut_points_list.append([d, 0])

        return mf_points, cut_points_list

    def intersection(self, mf_points_full):
        # print(mf_points_full)
        intersection_list = []
        for i in range(len(mf_points_full)):  # select each output
            intersection_list.append([])
            for j in range(len(mf_points_full[i])):  # select each MF
                # Find the intersection of two lines in programming python
                if j != len(mf_points_full[i][j]) - 1:
                    Xc = int(mf_points_full[i][j][2])
                    Yc = 1
                    Xd = int(mf_points_full[i][j][3])
                    Yd = 0

                    Xa = int(mf_points_full[i][j + 1][0])
                    Ya = 0
                    Xb = int(mf_points_full[i][j + 1][1])
                    Yb = 1

                    x_of_intersection = (Xd * (Xa * (Ya - Yb + Yc - Yd) + Xb * (Yd - Yc)) + Xc * (Xa * (Yb - Ya)) + (
                            Xb - Xa) * (Ya - Yd)) / ((Yd - Yc) * (Xb - Xa) - (Xd - Xc) * (Yb - Ya))

                    y_of_intersection = ((Yd - Yc) / (Xd - Xc)) * (x_of_intersection - Xd) + Yd

                    intersection_list[i].append([x_of_intersection, y_of_intersection])

        return intersection_list

    def area(self, alpha_cut , points, intersection_points):

        upper_trapezoid_full = []
        for i in range(len(points)):  # select each output
            # print(points[i])
            for j in range(len(points[i])):  # select each MF
                # Find the intersection of two lines in programming python
                if j < len(points[i]) - 1:

                    if alpha_cut[i][j] < alpha_cut[i][j + 1]:  # @_1 < @_2

                        if alpha_cut[i][j] > intersection_points[i][j][1]:  # first higher than y_of_intersection
                            print("@_1 < @_2", ", triangle")
                            upper_trapezoid = ([0, 0, 0, 0, alpha_cut[i][j]])

                            if j == 0:  # check that is first or not
                                print('FIRST')
                                upper_trapezoid[2] = points[i][j][2][0]  # Xc = XC +
                                upper_trapezoid[3] = intersection_points[i][j][0]  # Xd = XM +

                            else:
                                print('ELSE')
                                upper_trapezoid[0] = intersection_points[i][j - 1][0]  # Xd = XM ghabli +
                                upper_trapezoid[1] = points[i][j][1][0]  # Xb = Xb +
                                upper_trapezoid[2] = points[i][j][2][0]  # Xc = XC +
                                upper_trapezoid[3] = intersection_points[i][j][0]  # Xd = XM +

                            upper_trapezoid_full.append(upper_trapezoid)

                            points[i][j][2][0] = intersection_points[i][j][0]  # Xc = Xm +
                            points[i][j][3][0] = points[i][j + 1][0][0]  # Xd = Xa +
                            points[i][j][2][1] = intersection_points[i][j][1]  # update @_1 with y_of_intersection +
                            points[i][j][1][1] = intersection_points[i][j][1]  # update @_1 with y_of_intersection +

                        else:  # first lower than y_of_intersection
                            print("@_1 < @_2", ", trapezoid")
                            points[i][j][3][0] = points[i][j + 1][0][0]  # Xd = Xa
                            points[i][j][2][0] = (points[i][j][2][1] - points[i][j + 1][0][1]) * (
                                    points[i][j + 1][1][0] - points[i][j + 1][0][0]) / (
                                                         points[i][j + 1][1][1] - points[i][j + 1][0][1]) + \
                                                 points[i][j + 1][0][0]

                    elif alpha_cut[i][j + 1] < alpha_cut[i][j]:  # @_2 < @_1
                        if alpha_cut[i][j + 1] > intersection_points[i][j][1]:  # 2nd higher than y_of_intersection
                            print("@_2 < @_1", ", triangle")
                            upper_trapezoid = ([intersection_points[i][j][0], points[i][j + 1][1][0], points[i][j + 1][2][0],
                                                intersection_points[i][j][0], points[i][j + 1][2][1]])

                            if j == len(points[i][j]) - 1:
                                print('LAST')
                                upper_trapezoid[3] = points[i][j][3][0]  # Xd = Xd +


                            else:
                                print('ELSE')
                                upper_trapezoid[3] = intersection_points[i][j + 1][0]  # Xd = XM badi +

                            upper_trapezoid_full.append(upper_trapezoid)

                            points[i][j + 1][0][0] = points[i][j][3][0]  # Xa = Xd +
                            points[i][j + 1][1][0] = intersection_points[i][j][0]  # Xb = Xm +
                            points[i][j + 1][2][0] = intersection_points[i][j + 1][0]  # Xb = Xm badi +
                            points[i][j + 1][1][1] = intersection_points[i][j][1]  # update @_1 with y_of_intersection +
                            points[i][j + 1][2][1] = intersection_points[i][j][1]  # update @_1 with y_of_intersection +


                        else:  # second lower than y_of_intersection
                            print("@_2 < @_1", ", trapezoid")
                            points[i][j + 1][0][0] = points[i][j][3][0]  # Xa = Xd
                            points[i][j + 1][1][0] = (points[i][j + 1][2][1] - points[i][j][3][1]) * (
                                    points[i][j][3][0] - points[i][j][2][0]) / (
                                                             points[i][j][3][1] - points[i][j][2][1]) + points[i][j][3][
                                                         0]

                    else:  # @_1 = @_2
                        if alpha_cut[i][j] > intersection_points[i][j][1]:
                            print("@_1 = @_2", ", triangle")
                            upper_trapezoid = ([intersection_points[i][j][0], points[i][j + 1][1][0],
                                                points[i][j + 1][2][0], points[i][j + 1][3][0], points[i][j + 1][2][1]])

                            if j == 0:
                                print('FIRST')
                                upper_trapezoid[0] = intersection_points[i][j][0]  # Xa = XM +
                                upper_trapezoid[1] = points[i][j + 1][1][0]  # Xb = Xb +
                                upper_trapezoid[2] = points[i][j + 1][2][0]  # Xc = Xc +
                                upper_trapezoid[3] = intersection_points[i][j + 1][0]  # Xd = XM +

                            elif j == len(points[i]) - 2:
                                print('ELIF')
                                # upper_trapezoid[0] = intersection_points[i][j][0]  # Xa = XM
                                # upper_trapezoid[1] = points[i][j + 1][1][0]  # Xb = Xb

                                # points[i][j + 1][0][0] = points[i][j][3][0]  # Xa = Xd +
                                # points[i][j + 1][1][0] = intersection_points[i][j][0]  # Xb = XM +
                                # points[i][j + 1][1][1] = intersection_points[i][j][1]  # update @_2 with y_of_intersection +
                                # points[i][j + 1][2][1] = intersection_points[i][j][1]  # update @_2 with y_of_intersection +

                                if alpha_cut[i][j - 1] < intersection_points[i][j][1]:
                                    pass
                                else:
                                    pass

                            else:
                                print('ELSE')
                                upper_trapezoid[0] = intersection_points[i][j][0]  # XA = XM +
                                upper_trapezoid[1] = points[i][j + 1][1][0]  # Xb = Xb +
                                upper_trapezoid[2] = points[i][j + 1][2][0]  # Xc = Xc +
                                upper_trapezoid[3] = intersection_points[i][j + 1][0]  # Xd = XM +
                                points[i][j + 1][2][0] = intersection_points[i][j + 1][0]  # Xc = XM badi +

                            upper_trapezoid_full.append(upper_trapezoid)
                            points[i][j + 1][0][0] = points[i][j][3][0]  # Xa = Xd +
                            points[i][j + 1][1][0] = intersection_points[i][j][0]  # Xb = XM +
                            points[i][j + 1][1][1] = intersection_points[i][j][1]  # update @_2 with y_of_intersection +
                            points[i][j + 1][2][1] = intersection_points[i][j][1]  # update @_2 with y_of_intersection +

                            # if points[i][j - 1][2][1] < points[i][j][2][1]:  # @_0 < @_1
                            #     pass  # do nothing
                            #
                            # elif points[i][j - 1][2][1] < points[i][j][2][1]:  # @_1 < @_0
                            #
                            #
                            #     points[i][j][2][0] = intersection_points[i][j][1]  # Xc = XM
                            #
                            #
                            #     points[i][j][3][0] = points[i][j + 1][0][0]  # Xd = Xa

                        else:
                            print("@_1 = @_2", ", trapezoid")
                            points[i][j][2][0] = points[i][j + 1][1][0]  # Xc = Xb
                            points[i][j][3][0] = points[i][j + 1][0][0]  # Xd = Xa

        # print('................................................')
        # print(points)
        # print(upper_trapezoid_full)
        # print('................................................')
        return points, upper_trapezoid_full

    def centeeofgravity(self, cog_points, new_trapezoid):

        # print('\033[1m' + '\n---------------------------------------------------------' + '\033[0m')
        # print(cog_points)
        # print(new_trapezoid)
        # print('\033[1m' + '---------------------------------------------------------' + '\033[0m')

        cog_list = []
        cog_list_new = []
        denominator = 0
        numerator = 0

        for m in range(len(new_trapezoid)):  # select each MF
            # cog_list_new.append([])
            # for n in range(len(new_trapezoid[m])):  # select each point
            a = new_trapezoid[m][0]
            b = new_trapezoid[m][1]
            c = new_trapezoid[m][2]
            d = new_trapezoid[m][3]
            alpha_cut = new_trapezoid[m][4]
            Xcog_new = (c * c + c * d + d * d - (a * a) - (a * b) - (b * b)) / (3 * (c + d - b - a))
            cog_list_new.append([Xcog_new, alpha_cut])

        for z in range(len(cog_list_new)):  # select each new trapezoid

            # print('\033[96m' + '...............................' + '\033[0m')
            numerator = numerator + cog_list_new[z][0] * cog_list_new[z][1]
            denominator = denominator + cog_list_new[z][1]
            # print('\033[93m' + 'COG : ' + '\033[0m', cog_list_new[z][0])
            # print('\033[93m' + '@ : ' + '\033[0m', cog_list_new[z][1])
            # print('\033[93m' + 'COG * @ : ' + '\033[0m', cog_list_new[z][0] * cog_list_new[z][1])
            # print('\033[96m' + '...............................' + '\033[0m')

        for i in range(len(cog_points)):  # select each output
            cog_list.append([])
            for j in range(len(cog_points[i])):  # select each MF
                a = cog_points[i][j][0][0]
                b = cog_points[i][j][1][0]
                c = cog_points[i][j][2][0]
                d = cog_points[i][j][3][0]

                Xcog = (c * c + c * d + d * d - (a * a) - (a * b) - (b * b)) / (3 * (c + d - b - a))
                # print(cog_list)
                cog_list[i].append([Xcog, cog_points[i][j][2][1]])

            for z in range(len(cog_list[i])):
                # print('\033[91m' + '-------------------------------' + '\033[0m')
                numerator = numerator + cog_list[i][z][0] * cog_list[i][z][1]
                denominator = denominator + cog_list[i][z][1]

                # print('\033[92m' + 'COG : ' + '\033[0m', cog_list[i][z][0])
                # print('\033[92m' + '@ : ' + '\033[0m', cog_list[i][z][1])
                # print('\033[92m' + 'COG * @ : ' + '\033[0m', cog_list[i][z][0] * cog_list[i][z][1])
                # print('\033[91m' + '-------------------------------\n' + '\033[0m')

            self.x_cog_total = numerator / denominator
            # print('\033[94m' + '<><><><><><><><><><><><><>' + '\033[0m')
            # print('\033[94m' + 'FINAL :' + '\033[10m', self.x_cog_total)
            # print('\033[94m' + '<><><><><><><><><><><><><>' + '\033[0m')
