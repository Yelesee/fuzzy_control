# operate is and , or
# inputs are taken for knowing how many each input has membership function


class Rules:
    def __init__(self, all_rules, inputs, fuzzified):
        self.all_rules = all_rules
        self.inputs = inputs
        self.input_rules_separated = []
        self.output_rules_separated = []
        self.eachMembership = []
        self.ready_to_min = []
        self.minimized = []
        self.ready_to_max = []
        self.maximized = []
        self.fuzzified_inputs = fuzzified
        # print("all rules are: ", all_rules)

    # This Function is to separate inputs rules statements from output rules.
    # and they are ready to get their fuzzified inputs.
    # ex: input_rules_separated = [['1', '0', '0', '-1'], ['1', '0', '0', '1']]
    # ex: output_rules_separated = [['2'], ['1'], ['3'], ...]
    def separate(self):
        for key, value in enumerate(self.all_rules):
            input_rules, output_rules = value.split(',')
            output_rules = output_rules.strip(" ")
            self.input_rules_separated.append(input_rules.split(' '))
            self.output_rules_separated.append(output_rules.split(' '))

        # print("input rules separated are: ", self.input_rules_separated)
        # print("output rules separated are: ", self.output_rules_separated)

    # This Function is about how many each input has membership function.
    # ex: eachMembership [['1', '2', '3', '4'], ['1', '2', '3'], ['1', '2', '3'], ['1', '2', '3', '4']]
    def each_membership(self):
        list_mf_input = []

        for i, val in enumerate(self.inputs):
            list_mf_input.append(len(val[2]))
        self.eachMembership = [list(map(str, range(1, x + 1))) for x in list_mf_input]
        # print(self.eachMembership)
        return self.eachMembership

    # This Function will pop each rule from input_rules_separated and it will used just in assign function.
    # ex: [['4'], ['-1'], ['3'], ['3']]
    def get_rule(self):
        list_list_statement = []
        list_statement = self.input_rules_separated.pop()

        for i, val in enumerate(list_statement):
            list_list_statement.append([val])
        return list_list_statement

    # This function will called in the number of rules and assign the fuzzified inputs to its own membership function.
    # this will let us to get the min of fuzzified value of each rule.
    # fuzzified_inputs are the real fuzzified inputs which are ok.
    def assign_to_input(self):
        zipped = zip(self.get_rule(), self.each_membership(), self.fuzzified_inputs)
        zipped = list(zipped)
        temp = []  # temp is like [['4', 0.1], ['0', 1], ['0', 1], ['1', 0.5]]

        for key, value in enumerate(zipped):
            if value[0][0] in value[1]:  # value[0][0] is 1 rule list value[1] is
                for i, val in enumerate(value[1]):
                    if int(val) == int(value[0][0]):
                        temp.append([value[0][0], value[2][int(val) - 1]])
            elif value[0][0][0] == "-":  # not operand
                for i, val in enumerate(value[1]):
                    if int(val) == int(value[0][0][1]):
                        temp.append([value[0][0], 1.0 - value[2][int(val) - 1]])
            else:  # if rule statement is 0 for doing and i put 1 for the value because min not destroyed
                temp.append([value[0][0], 1.0])
        self.ready_to_min.append(temp)
        # print("min bayad is:", self.ready_to_min)

    # Because I use pop for assign amount I will reverse the list.
    # ex: Before ->  [[['4', 0.1], ['0', 1.0], ['0', 1.0], ['1', 0.7]], [['4', 0.1], ['-1', 0.8], ['3', 0.9]]]
    # ex: After -> [[['4', 0.1], ['-1', 0.8], ['3', 0.9]],[['4', 0.1], ['0', 1.0], ['0', 1.0], ['1', 0.7]]]
    def reverse_ready_to_min(self):
        self.ready_to_min.reverse()

    def minimizer(self):
        for i, val in enumerate(self.ready_to_min):
            temp = []
            for j, value in enumerate(val):
                temp.append(value[1])
            self.minimized.append([min(temp)])
        # print(self.minimized)

    # This Function will alter our output_rules_separated to list separated for using in zip
    # ex: Before -> [['2'], ['1'], ['3'], ['4']]
    # ex: After -> [[['2']], [['1']], [['3']], [['4']]]
    def output_ready_to_assign(self):
        self.output_rules_separated = [[[elem] for elem in sub_list] for sub_list in self.output_rules_separated]

    # This Function will assign minimized fuzzified value to each outputs rule statement
    def assign_to_output(self):
        zipped = zip(self.minimized, self.output_rules_separated)
        zipped = list(zipped)
        temp = []
        for i, val in enumerate(zipped):
            temple = []
            for j in range(0, len(val[1])):
                if val[1][j][0][0] == "-":  # not operand
                    temple.append([1 - val[0][0], val[1][j][0]])
                elif val[1][j][0] == "0":  # we take it 0 until our maximization action will not destroy.
                    temple.append([0.0, val[1][j][0]])
                else:
                    temple.append([val[0][0], val[1][j][0]])
            temp.append(temple)
        self.ready_to_max = zipped

    def processRule(self):
        maxed = []
        maxs = []
        # print(self.ready_to_max)
        for i, val in enumerate(self.ready_to_max[0][1]):
            maxed.append([])
        for i, val in enumerate(self.ready_to_max):
            for j in range(0, len(val[1])):
                for i, value in enumerate(val[1][j]):
                    maxed[j].insert(j, abs(int(value)))

        for x, val in enumerate(maxed):
            b = max(val)
            maxs.append(b)
        self.fuzzyVal(maxs)

    def fuzzyVal(self, maxs):
        for i, val in enumerate(maxs):
            zeros = [0 for x in range(val)]
            self.maximized.append(zeros)
            for j in range(0, val):
                self.findMax(j + 1, i)

        # print(self.maximized)

    def findMax(self, out, index):
        # print("outval", out)
        # print("outnum", index)

        for i, val in enumerate(self.ready_to_max):
            if int(val[1][index][0]) < 0:
                if abs(int(val[1][index][0])) == int(out):
                    self.maximized[index][out - 1] = 1.0 - val[0][0]

            elif int(val[1][index][0]) == int(out):

                if float(val[0][0]) > float(self.maximized[index][out - 1]):
                    self.maximized[index][out - 1] = val[0][0]
