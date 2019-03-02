import sys
import ast
sys.path.append("..")


class Run:
    def __init__(self, input_amount_list=0):
        self.final = 0
        super(Run, self).__init__()

        from .data import data
        data.Data()

        from .fuzzification import fuzzification
        fuzzified = []

        for i in range(len(data.data_list[0])):
            fuz = fuzzification.Fuzzy(input_amount_list[i])
            fuzzified.append([])
            for j in range(len(data.data_list[0][i][2])):
                mf_points = data.data_list[0][i][2][j][2]
                mf_points = mf_points[1:len(mf_points) - 1]  # to delete '[', ']' from list
                mf_points = mf_points.split()
                a = float(mf_points[0])
                b = float(mf_points[1])
                c = float(mf_points[2])
                d = float(mf_points[3])

                fuz_amount = fuz.fuzzification('Trapezoid', a, b, c, d)
                fuzzified[i].append(fuz_amount)


        from .rules import rules
        rule = rules.Rules(data.data_list[2], data.data_list[0], fuzzified)
        rule.separate()
        rule.each_membership()
        for i in range(1, 19):
            rule.assign_to_input()
        rule.reverse_ready_to_min()
        rule.minimizer()
        rule.output_ready_to_assign()
        rule.assign_to_output()
        rule.processRule()
        # print(rule.maximized)

        from .defuzzification import defuzzification
        alpha_cut_list = rule.maximized
        de = defuzzification.Defuzzy(data.data_list[1], alpha_cut_list)
        self.final = de.x_cog_total
