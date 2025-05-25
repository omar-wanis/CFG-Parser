import re
from copy import deepcopy, copy
from prettytable import PrettyTable
from collections import deque, defaultdict

class DerivationNode:
    def __init__(self, value, parent=None):
        self.value = value
        self.parent = parent


def strings_contain_each_other(first_str, second_str):
    """
    Checks if two strings contain each other.

    Returns (the bool value that says if they are containing each other,
            the string that includes,
            the string that is included)
    """
    first_count = second_str.count(first_str)
    second_count = first_str.count(second_str)

    are_containing = bool(first_count + second_count)

    if not bool(second_count) and are_containing:
        first_str, second_str = second_str, first_str

    return are_containing, first_str, second_str


def string_contains_space(string):
    """
    Returns true if string contains space, false otherwise.

    """
    for char in string:
        if char.isspace():
            return True

    return False


def re_escaped(it):
    for i in it:
        yield re.escape(i)

class RuleNode():
        def __init__(self,
                     NodeName=None,
                     NodeVars=None,
                     NodeString=None,
                     CanBeNull=False,
                     CanRepeat=False,  ):
            self.NodeName = NodeName
            self.NodeVars = NodeVars
            self.NodeString = NodeString
            self.CanBeNull = CanBeNull
            self.CanRepeat = CanRepeat
            self.index = 0

class CFG(object):
    """
    Context free grammar (CFG) class

    """
    
            
    
    def __init__(self,
                 variables=None,
                 terminals=None,
                 rules=None,
                 start_variable='S',
                 null_character='λ'
                 ):
        
        """
        Initialize method

        Parameters
            variables (optional): grammar's variables set.
            terminals: grammar's terminals set
            rules:  grammar's rules
            start_variable (optional, defaults to 'S'): grammar's start variable
            null_character (optional, defaults to 'λ'): grammar's null character
        """

        if variables is None:
            variables = set()
        elif hasattr(variables, '__iter__'):
            variables = {*variables}
        else:
            raise TypeError(
                "CFG variables must be a iterable, not {}".format(type(variables).__name__)
            )

        if isinstance(rules, dict):
            variables |= {*rules}
            rules = {
                (var, var_rule)
                for var, var_rules in rules.items()
                for var_rule in var_rules
            }
        elif hasattr(rules, '__iter__'):
            rules = {*rules}
        else:
            raise TypeError(
                "CFG rules must be a collection or a dict, not {}".format(type(rules).__name__)
            )

        if isinstance(terminals, set):
            terminals = terminals
        elif hasattr(terminals, '__iter__'):
            terminals = {*terminals}
        else:
            raise TypeError(
                "CFG variables must be a iterable, not {}".format(type(variables).__name__)
            )

        self.variables = variables
        self.terminals = terminals
        self.start_variable = start_variable
        self.null_character = null_character
        self.accepts_null = None
        self._rules = rules
        self._is_chamsky = None
        self._cnf = None
        self.rulesNodes = {}
        self.index=0
        self.stack=[]
        self.table = PrettyTable(["Input String", "Stack","Action"])
        

    @property
    def variables(self):
        """
        Grammar's variables set property getter
        """
        return self._variables

    @variables.setter
    def variables(self, new_variables):
        """
        Grammar's variables set property setter
        """
        if type(new_variables) is not set:
            raise TypeError("CFG variables must be a set, not '{}'".format(type(new_variables).__name__))

        for variable in new_variables:
            if type(variable) is not str:
                raise TypeError("CFG variables must be strings, not '{}'".format(type(variable).__name__))

        for variable in new_variables:
            if string_contains_space(variable):
                raise ValueError("Variables cannot contain white spaces : '{}'".format(variable))

        new_variables_list = list(new_variables)
        for i in range(len(new_variables_list) - 1):
            for j in range(i + 1, len(new_variables_list)):
                contain_each_other, first_str, second_str = strings_contain_each_other(new_variables_list[i],
                                                                                       new_variables_list[j])
                if contain_each_other:
                    raise ValueError("Variables cannot contain each other, '{}' contains '{}'"
                                     .format(first_str, second_str))

        self._variables = frozenset(new_variables)
        self._is_chamsky = None
        self._cnf = None
        self.accepts_null = None

    @property
    def terminals(self):
        """
        Grammar's terminals set property getter
        """
        return self._terminals

    @terminals.setter
    def terminals(self, new_terminals):
        """
        Grammar's terminals set property setter
        """
        if type(new_terminals) is not set:
            raise TypeError("CFG terminals must be a set, not '{}'".format(type(new_terminals).__name__))

        for terminal in new_terminals:
            if type(terminal) is not str:
                raise TypeError("CFG terminals must be strings, not '{}'".format(type(terminal).__name__))

        for terminal in new_terminals:
            if string_contains_space(terminal):
                raise ValueError("Variables cannot contain white spaces : '{}'".format(terminal))

        new_terminals_list = list(new_terminals)
        for i in range(len(new_terminals_list) - 1):
            for j in range(i + 1, len(new_terminals_list)):
                contain_each_other, first_str, second_str = strings_contain_each_other(new_terminals_list[i],
                                                                                       new_terminals_list[j])
                if contain_each_other:
                    raise ValueError("Terminals cannot contain each other, '{}' contains '{}'"
                                     .format(first_str, second_str))

        self._terminals = frozenset(new_terminals)
        self._is_chamsky = None
        self._cnf = None
        self.accepts_null = None

    
    def rulesNodePrep(self):
        for rule in self._rules:
            #print(rule)
            if rule[0] not in list(self.rulesNodes.keys()):
                v = RuleNode(NodeName=rule[0])
                string = []
                Variables = []
                for s in rule[1]:
                    string.append(s)
                    if s in self.variables:
                        Variables.append(s)
                    elif s == self.null_character:
                        v.CanBeNull = True
                    elif s == rule[0]:
                        v.CanRepeat = True
                v.NodeString=[]
                v.NodeVars=[]
                v.NodeString.append(string)
                v.NodeVars.append(Variables)
                self.rulesNodes[rule[0]] = v
            else:
                v = self.rulesNodes[rule[0]]
                string = []
                Variables = []
                for s in rule[1]:
                    string.append(s)
                    if s in self.variables and s not in v.NodeVars:
                        Variables.append(s)
                    elif s == self.null_character:
                        v.CanBeNull = True
                    elif s == rule[0]:
                        v.CanRepeat = True
                v.NodeString.append(string)
                v.NodeVars.append(Variables)
                self.rulesNodes[rule[0]] = v
                # print(f"Node name :  {self.rulesNodes[rule[0]].NodeName}")
                # print(f"Node String :  {self.rulesNodes[rule[0]].NodeString}")
                # print(f"Node Vars : {self.rulesNodes[rule[0]].NodeVars}")
    
    def rules(self,str):
        """
        Grammar's rules property setter

        """
        # if type(new_rules) is not set:
        #     raise TypeError("CFG rules must be a set, not '{}'".format(type(new_rules).__name__))

        # for rule in new_rules:
        #     if type(rule) is not tuple:
        #         raise TypeError("CFG rules must be 2-tuples, not '{}'".format(type(rule).__name__))
        #     if len(rule) != 2:
        #         raise TypeError("CFG rules must be 2-tuples")
        #     if type(rule[0]) is not str or type(rule[1]) is not str:
        #         raise TypeError("CFG rules must contain strings")
        #     if string_contains_space(rule[0]) or string_contains_space(rule[1]):
        #         raise ValueError("Rule cannot contain white spaces : '{} -> {}'".format(*rule))

        # pattern = re.compile('({})+'.format('|'.join(re_escaped(self.variables | self.terminals))))
        # print(f"the rule pattern : {pattern}")
        # print(f"rule : {rule}")
        # for rule in new_rules:
        #     if rule[0] not in self.variables:
        #         raise ValueError("Unknown Variable '{p0}' in '{p0} -> {p1}'".format(
        #             p0=rule[0],
        #             p1=rule[1]
        #         ))
        #     if not pattern.fullmatch(rule[1]):
        #         raise ValueError("Rule must contain combination of variables and terminals : '{} -> {}'".format(*rule))
        #     if rule[1].count(self.null_character) and rule[1] != self.null_character:
        #         raise ValueError("Rule cannot combine null character with variables and terminals : '{} -> {}'".format(
        #             *rule))
        # print(f"new rules: {new_rules}")
        self.rulesNodePrep()
        self.rulesNodes = dict(reversed(list(self.rulesNodes.items())))
                    
        self._is_chamsky = None
        self._cnf = None
        self.accepts_null = None
        if (self.start_variable, self.null_character) in self._rules:
            self.accepts_null = True
    def addrule(self,left,right):
        compact = {left : right}
        self._rules.add(compact)
    @property
    def start_variable(self):
        """
        Grammar's start_variable property getter
        """
        return self._start_variable

    @start_variable.setter
    def start_variable(self, new_start_variable):
        """
        Grammar's start_variable property setter
        """
        if type(new_start_variable) is not str:
            raise TypeError("CFG start variable must be string, not '{}'".format(type(new_start_variable).__name__))

        if new_start_variable not in self.variables:
            raise ValueError("Start variable must be in variables set")

        self._start_variable = new_start_variable
        self._is_chamsky = None
        self._cnf = None
        self.accepts_null = None

    @property
    def null_character(self):
        """
        Grammar's null_character property getter
        """
        return self._null_character

    @null_character.setter
    def null_character(self, new_null_character):
        """
        Grammar's null_character property setter
        """
        if type(new_null_character) is not str:
            raise TypeError("CFG null character must be string, not '{}'".format(type(new_null_character).__name__))

        if new_null_character not in self.terminals:
            raise ValueError("Null character must be in terminals set")

        self._null_character = new_null_character
        self._is_chamsky = None
        self._cnf = None
        self.accepts_null = None
    
    def DFS(self,input_string,node,nodestr):
        node = DerivationNode(nodestr,node)
        current = nodestr
        if current == input_string:
            return True, node
        if len(current) > len(input_string)+1:
            return False,None
        for i, char in enumerate(current):
            if char in self.variables:
                for production in self.rulesNodes[char].NodeString:
                    if len(production) == 1 and production[0] in {'λ', 'ε'}:
                        new_string = current[:i] + current[i + 1:]
                    else:
                        new_string = current[:i] + ''.join(production) + current[i + 1:]
                    print(f"new string : {new_string} & we are at i : {i} & current : {current}")
                    isTrue,_ = self.DFS(input_string,node,new_string)
                    if isTrue:
                        return True,_
                break
        return False,None
        # string_index = 0
        # self.stack = []
        # self.stack.append("$")
        # self.stack.append("S")
        # print(self.stack)
        # while True:
        #     # print(f"current stack = {self.stack}")
        #     if self.stack[-1] == "$" and string == len(string) * string[0] :
        #         return True
        #     c = string[string_index]
        #     if c == self.stack[-1]:
        #         self.stack.pop()
        #         string_list = list(string)
        #         string_list[string_index] = "_"
        #         string = "".join(string_list)
        #         string_index+=1
        #         self.table.add_row([string,"".join(self.stack[::-1]),f"popped {c}"])
        #         # print(f"|{string}   |    {self.stack}    |    popped {c}|")
        #     else:
        #         if self.stack[-1] in self._variables:
        #             if c in self.stack[:-1] and self.rulesNodes[self.stack[-1]].CanBeNull and string.count(c) == self.stack.count(c):
        #                 last_char = self.stack.pop()
        #                 self.table.add_row([string,"".join(self.stack[::-1]),f"{last_char} became epsilon"])
        #                 continue
        #             x,cond = self.recDfs(c,self.rulesNodes[self.stack[-1]])
        #             print(f"x = {x}")
        #             if cond:
        #                 v = self.rulesNodes[self.stack[-1]]
        #                 self.stack.pop()
        #                 i = len(v.NodeString[x])
        #                 while i>0:
        #                     self.stack.append(v.NodeString[x][i-1])
        #                     self.table.add_row([{string},"".join(self.stack[::-1]),f"appended {self.stack[-1]}"])
        #                     # print(f"|{string}   |    {self.stack}    |    appended {self.stack[-1]}|")
        #                     i-=1
        #             else:
        #                 return False
        #         elif self.stack == "λ":
        #             continue
        #         else:
        #             return False

    def BFS(self, input_string):
        if type(input_string) is not str:
            raise TypeError("Input must be a string")
        queue = deque()
        queue.append(DerivationNode(self.start_variable))
        while queue:
            node = queue.popleft()
            current = node.value

            if current == input_string:
                return True, node
            if len(current) > len(input_string)+2:
                continue
            
            for i, char in enumerate(current):
                if char in self.variables:
                    for production in self.rulesNodes[char].NodeString:
                        if len(production) == 1 and production[0] in {'λ', 'ε'}:
                            new_string = current[:i] + current[i + 1:]
                        else:
                            new_string = current[:i] + ''.join(production) + current[i + 1:]

                        queue.append(DerivationNode(new_string, node))
                    break

        return False, None

    def Derivation_Path(self, leaf):
        path = []
        while leaf:
            path.append(leaf.value)
            leaf = leaf.parent

        lines = []
        for state in reversed(path):
            lines.append("  |- " + state)
        return '\n'.join(lines)

    def str_rules(self, *, return_list=False, prepend='', line_splitter='\n'):
        """
        Returns a human-readable string representation of grammar's rules
        """
        rules_var = {}
        vars = set()
        for rule in self._rules:
            if not rules_var.get(rule[0], None):
                rules_var[rule[0]] = []

            rules_var[rule[0]].append(rule[1])
            if rule[0] != self.start_variable:
                vars.add(rule[0])

        for rules in rules_var.values():
            rules.sort()

        vars = sorted(vars)
        vars.insert(0, self.start_variable)

        if self.accepts_null:
            if self.null_character not in rules_var[self.start_variable]:
                rules_var[self.start_variable].append(self.null_character)

        str_lines = [prepend + '{} -> {}'.format(var, ' | '.join(rules_var[var])) for var in vars]
        if return_list:
            return str_lines

        return line_splitter.join(str_lines)
    
    def __str__(self):
        print_lines = []
        print_lines.append("Variables (V): {}".format(set(self.variables)))
        print_lines.append("Terminals (Σ): {}".format(set(self.terminals)))
        print_lines.append("Null character: {}".format(self.null_character))
        print_lines.append("Start variable (S): {}".format(self.start_variable))
        print_lines.append("Rules (R):")
        print_lines.extend(self.str_rules(return_list=True, prepend='\t'))
        for i in self.rulesNodes.keys():
            print("//////////////////////////////")
            print(f"Node name :  {self.rulesNodes[i].NodeName}")
            print(f"Node String :  {self.rulesNodes[i].NodeString}")
            print(f"Node Vars : {self.rulesNodes[i].NodeVars}")

        return "\n".join(print_lines)
    
g = CFG(terminals={'0', '1','λ'},
        rules={'S': ['0S','1S','0','1']}
        )
g.rules(None)
print(g.__str__())
# test_string = input("Enter your string: ")
# result, node = g.BFS(test_string)
# print(f"\nString '{test_string}' is accepted by the grammar? {result}")
# if result:
#     print("\nLeftmost derivation path:")
#     print(g.Derivation_Path(node))
def DARV(node):
    print("\nLeftmost derivation path:")
    print(g.Derivation_Path(node))
def parse_StringBFS():
    test_string = input("Enter your string: ")
    result, node = g.BFS(test_string)
    print(f"\nString '{test_string}' is accepted by the grammar? {result}")
    # if result:
    #     DARV(node)
def parse_StringDFS():
    test_string = input("Enter your string: ")
    result, node = g.DFS(test_string,None,"S")
    print(f"\nString '{test_string}' is accepted by the grammar? {result}")
    # if result:
    #     DARV(node)

# parse_StringBFS()
# parse_StringDFS()
