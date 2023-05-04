from typing import Any


class CF:
    """
    Class for all the constant and calculation related to certainty factor(CF)
    """
    TRUE = 1.0
    FALSE = -1.0
    UNKNOWN = 0.0
    CUTOFF = 0.2

    @staticmethod
    def cf_or(a: float, b: float):
        """
        :param a:
        :param b:
        :return: return the result of or(cf_a, cf_b)
        """
        if a > 0 and b > 0:
            return a + b - a * b
        if a < 0 and b < 0:
            return a + b + a * b
        return (a + b) / (1 - min(abs(a), abs(b)))

    @staticmethod
    def cf_and(a: float, b: float):
        """
        :param a:
        :param b:
        :return: return the result of and(cf_a, cf_b)
        """
        return min(a, b)

    @staticmethod
    def cf_valid(x: float):
        """
        :param x:
        :return: return if the certainty factor is valid
        """
        return CF.FALSE <= x <= CF.TRUE

    @staticmethod
    def cf_true(x):
        """
        :param x:
        :return: return if the certainty factor is recognized as true
        """
        return CF.cf_valid(x) and x > CF.CUTOFF

    @staticmethod
    def cf_false(x):
        """
        :param x:
        :return: return if the certainty factor is recognized as false
        """
        return CF.cf_valid(x) and x < (CF.CUTOFF - 1)


class Context:
    """
    Context
    """
    cnt = 0
    contexts = {}

    def __init__(self, name: str, initial_data: list[str] = [], goals: list[str] = []):
        if name in Context.contexts:
            raise ValueError(f'redundant context {name}')
        Context.contexts[name] = self
        self.id = Context.cnt
        Context.cnt += 1
        self.name = name
        self.initial_data = initial_data
        self.goals = goals

    def __str__(self):
        return f'Context {self.name}'

    @staticmethod
    def get_context_by_name(name):
        """
        find context by name
        :param name:
        """
        if name not in Context.contexts:
            raise ValueError(f'Context {name} not found.')
        return Context.contexts[name]


class Parameter:
    """
    Parameter is the property of a context. It is used as a type which does not contain
    any value
    """
    cnt = 0
    parameters = {}

    def __init__(self, name: str, ctx_name: str, ask_first: bool = False, param_type: type = None,
                 allowed_values: list = None):
        if name in Parameter.parameters:
            raise ValueError(f'redundant parameter with name {name}')
        Parameter.parameters[name] = self
        self.id = Parameter.cnt
        Parameter.cnt += 1
        self.name = name
        self.ask_first = ask_first
        self.ctx = Context.get_context_by_name(ctx_name)
        self.param_type = param_type
        self.allowed_values = allowed_values

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return f'{self.name}'

    @staticmethod
    def get_parameter_by_name(name):
        """
        find parameter by name
        :param name:
        """
        if name not in Parameter.parameters:
            raise ValueError(f'Parameter {name} not found.')
        return Parameter.parameters[name]

    def get_value(self, val: Any):
        """
        :param val:
        :return: val of the same type of parameter or val that is within the allowed
        values
        """
        if self.param_type:
            return self.param_type(val)
        if val in self.allowed_values:
            return val
        raise ValueError('val must be one of %s for the parameter %s' %
                         (', '.join(list(self.enum)), self.name))


class Statement:
    """
    Statement: a statement can either be a condition or conclusion
    since they are in the same format (param, ctx, op, val)
    """
    cnt = 0

    def __init__(self, param_name: str, ctx_name: str, op_str: str, val: Any):
        self.param = Parameter.get_parameter_by_name(param_name)
        self.val = val
        self.context = Context.get_context_by_name(ctx_name)
        self.op_str = op_str
        if op_str == '>=':
            self.op = lambda x, y: x >= y
        elif op_str == '>':
            self.op = lambda x, y: x > y
        elif op_str == '<=':
            self.op = lambda x, y: x <= y
        elif op_str == '<':
            self.op = lambda x, y: x < y
        elif op_str == '=':
            self.op = lambda x, y: x == y
        else:
            raise ValueError(f'op_str for Condition can only be one of the following: <=, <, >=, >, =')

    def meet(self, real_val: Any):
        """
        :param real_val:
        :return: check if the statement meets
        it is only used for condition since conclusion does not need to be evaluated
        """
        val = self.param.get_value(self.val)
        real_val = self.param.get_value(real_val)
        return self.op(real_val, val)

    def __str__(self):
        return f'{self.param} {self.context.name} {self.op_str} {self.val}'


class Store:
    """
    Store: a global key/value store
    store_dict: (ctx, param) => {val: cf, ...}
    """
    store_dict = dict()

    @staticmethod
    def get_vals(ctx: Context, param: Parameter):
        """
        :param ctx:
        :param param:
        :return: val
        return the val dict according to ctx, param
        """
        if (ctx, param) not in Store.store_dict:
            Store.store_dict[(ctx, param)] = {}
        return Store.store_dict[(ctx, param)]

    @staticmethod
    def update_cf(ctx: Context, param: Parameter, val: Any, cf: float):
        """
        :param ctx:
        :param param:
        :param val:
        :param cf:
        update the stored cf
        """
        d = Store.get_vals(ctx, param)
        if val not in d:
            d[val] = CF.UNKNOWN
        cur_cf = d[val]
        Store.store_dict[(ctx, param)][val] = CF.cf_or(cur_cf, cf)


class Rule:
    """
    Rule: each Rule contains multiple conditions and conclusions, and an associated cf
    """
    rules = {}
    cnt = 0

    def __init__(self, conditions: list[tuple], conclusions: list[tuple], cf: float):
        self.id = Rule.cnt
        Rule.cnt += 1
        self.conditions = []
        for param_name, ctx_name, op, val in conditions:
            self.conditions.append(Statement(param_name, ctx_name, op, val))
        self.conclusions = []
        for param_name, ctx_name, op, val in conclusions:
            self.conclusions.append(Statement(param_name, ctx_name, op, val))
        self.cf = cf
        self._map_param_to_rules()

    def _map_param_to_rules(self):
        for condition in self.conclusions:
            if condition.param not in Rule.rules:
                Rule.rules[condition.param] = []
            Rule.rules[condition.param].append(self)

    def __str__(self):
        conditions = ' AND\n\t'.join([str(condition) for condition in self.conditions])
        conclusions = ' AND\n\t'.join(str(conclusion) for conclusion in self.conclusions)
        return f'RULE {self.id}: IF {conditions} THEN\n ({self.cf})\n {conclusions}\n'

    def applicable(self):
        """
        :return: cf related to the rule
        """
        for condition in self.conditions:
            cf = self.eval_condition(condition)
            if CF.cf_false(cf):
                return CF.FALSE

        total_cf = CF.TRUE
        for condition in self.conditions:
            Executor.find_out(condition.context.name, condition.param.name)
            cf = self.eval_condition(condition)
            total_cf = CF.cf_and(total_cf, cf)
            if not CF.cf_true(total_cf):
                return CF.FALSE
        return total_cf

    def apply(self):
        """
        :return: if the rule applied
        """
        Executor.set_current_rule(self)

        cf = self.cf * self.applicable()
        if not CF.cf_true(cf):
            return False

        for conclusion in self.conclusions:
            Store.update_cf(conclusion.context, conclusion.param, conclusion.val, cf)

        return True

    @staticmethod
    def use_rules(rules):
        """
        :param rules:
        :return: if the rules applied
        """
        applied = False
        for rule in rules:
            if rule.apply():
                applied = True
        return applied

    @staticmethod
    def eval_condition(condition):
        """
        :param condition:
        :return: the cf of all the conditions that meet
        """
        values = Store.get_vals(condition.context, condition.param)
        return sum(cf for known_val, cf in values.items() if condition.meet(known_val))


class Executor:
    """
    Executor: the executor of the whole program, it contains several local variable that will be used during the run time
    """
    known = set()
    asked = set()
    current_rule = None

    HELP = """Type one of the following:
     ?     - to see possible answers for this parameter
     rule  - to show the current rule
     why   - to see why this question is asked
     help  - to see this list
     xxx   - (for some specific xxx) if there is a definite answer
     (xxx .5 yyy .4) - If there are several answers with different certainty factors.
     """

    @staticmethod
    def ask(ctx: Context, param: Parameter):
        """
        Ask the user to provide the corresponding parameter
        return immediately if the parameter of the ctx is asked
        :param ctx:
        :param param:
        :return: the user's reply: str
        """

        def parse_user_input(param: Parameter, reply: str):
            """
            take in the user's input and parse it to [(val, CF.TRUE)]
            or [(val1, cf1), ...] if there are multiple answers
            :param param:
            :param reply:
            :return: list[tuple(Any, float)]
            """
            if reply.find(',') < 0:
                return [(param.get_value(reply), CF.TRUE)]
            vals = []
            for pair in reply.split(','):
                val, cf = pair.strip().split(' ')
                vals.append((param.get_value(val), float(cf)))
            return vals

        if (ctx, param) in Executor.asked:
            return
        Executor.asked.add((ctx, param))
        while True:
            resp = input(f'What is the {param.name} of {ctx.name}? ')
            if not resp:
                continue
            elif resp == 'unknown':
                return False
            elif resp == 'help':
                print(Executor.HELP)
            elif resp == 'why':
                Executor.explain(param)
            elif resp == 'rule':
                print(Executor.current_rule)
            elif resp == '?':
                if param.param_type:
                    print(f'{param.name} must be of type {param.param_type})')
                else:
                    print(f'the allowed values of {param.name} are {param.allowed_values}')
            else:
                try:
                    for val, cf in parse_user_input(param, resp):
                        Store.update_cf(ctx, param, val, cf)
                    return True
                except:
                    print('Invalid response. Type ? to see legal ones.')

    @staticmethod
    def explain(param):
        """
        print all the current known parameters and the rule being applied
        :param param:
        :return: None
        """
        print(f'Why is the value of {param.name} being asked for?')
        if Executor.current_rule in ('initial', 'goal'):
            print(f'{param.name} is one of the {Executor.current_rule} parameters.')
            return
        known, unknown = [], []
        for condition in Executor.current_rule.conditions:
            if CF.cf_true(Rule.eval_condition(condition)):
                known.append(condition)
            else:
                unknown.append(condition)

        if known:
            print('It is known that:')
            for condition in known:
                print(condition)
            print(f'Therefore, \n{Executor.current_rule}')

    @staticmethod
    def set_current_rule(rule):
        """
        Set the current rule of Executor class
        :param rule:
        """
        Executor.current_rule = rule

    @staticmethod
    def find_out(ctx_name: str, param_name: str):
        """
        find out the parameter indicated by the param_name
        :param ctx_name:
        :param param_name:
        :return: if the parameter is asked successfully: Bool
        """
        param = Parameter.get_parameter_by_name(param_name)
        ctx = Context.get_context_by_name(ctx_name)
        if (ctx, param) in Executor.known:
            return True

        success = False
        if param.ask_first:
            success = Executor.ask(ctx, param)

        if not success:
            if param in Rule.rules:
                success = Rule.use_rules(Rule.rules[param])
            if not success and not param.ask_first:
                success = Executor.ask(ctx, param)

        if success:
            Executor.known.add((ctx, param))
        return success

    @staticmethod
    def execute(context_names: list[str]):
        """
        entry point of the program
        :param context_names:
        :return: results
        """
        print(f'Executing begins, type HELP for help')
        results = {}
        for ctx_name in context_names:
            ctx = Context.get_context_by_name(ctx_name)

            Executor.set_current_rule('initial')
            for param_name in ctx.initial_data:
                Executor.find_out(ctx_name, param_name)

            Executor.set_current_rule('goal')
            for param_name in ctx.goals:
                Executor.find_out(ctx_name, param_name)

            if ctx.goals:
                result = {}
                for param_name in ctx.goals:
                    pram = Parameter.get_parameter_by_name(param_name)
                    result[param_name] = Store.get_vals(ctx, pram)
                results[ctx] = result
        Executor.output_result(results)
        return results

    @staticmethod
    def output_result(result):
        """
        output the findings of the program
        :param result:
        """
        for ctx, result in result.items():
            print(f'Findings for {ctx.name}:')
            for param_name, value_dict in result.items():
                possibilities = [f'{val[0]} {val[1]}' for val in value_dict.items()]
                possibilities.sort(key=lambda key: float(-float(key.split(' ')[-1])))
                possibilities_str = ', '.join(possibilities)
                print(f'{param_name}: {possibilities_str}')
