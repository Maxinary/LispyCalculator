from functools import reduce


class Parser(object):

    """
    General Notes:

        Why Floats?:
            I'm using floats here because I can remove a '.0'
            but can't add a '.$whatever', after the calculation.


    """

    def __init__(self, given_calc_code):
        self.given_calc_code = given_calc_code

        def operation_model(operation, value_list):

            """
            takes:
                an operator + - * /, etc
                &
                a list or floats

            logic:
                $operation's up the entire list

            returns:
                floats

            """

            return reduce(
                lambda x, y: eval('{x} {operation} {y}'.format(
                    x=x,
                    operation=operation,
                    y=y
                )),
                value_list
            )

        self.OPERATION = {
            '+': lambda lst: operation_model('+', lst),
            '-': lambda lst: operation_model('-', lst),
            '*': lambda lst: operation_model('*', lst),
            '/': lambda lst: operation_model('/', lst),
        }

    def parse_node(self, node):
        """
        takes:
            a lisp expression like (* 2 2) or (/ 2 2)

        returns:
            values suitable for the eval_node method such as
            ['*', '2', '2'] and ['/', '2', '2']
        """
        return [
            symbol for symbol in node
                if symbol not in ['(', ')', ' ']
        ]

    def eval_node(self, node):
        """
        takes:
            a lisp expression like (* 2 2) or (/ 2 2)

        logic:
            runs the expression through parse_node,
            convert all strings(that represent floats) to floats
            and then pass the list to the OPERATION map

        Note:
            the key value takes a lambda which is why we are able
            to do this '[]()' !
        """

        parsed_node = self.parse_node(node=node)

        return self.OPERATION[parsed_node[0]](
            [float(i) for i in parsed_node[1:]]
        )


if __name__ == '__main__':

    # parse_node test
    assert Parser('').parse_node('(+ 2 2)') == ['+', '2', '2']
    assert Parser('').parse_node('(- 2 2)') == ['-', '2', '2']
    assert Parser('').parse_node('(* 2 2)') == ['*', '2', '2']
    assert Parser('').parse_node('(/ 2 2)') == ['/', '2', '2']

    # eval_node test
    assert Parser('').eval_node('(+ 2 2)') == 4.0
    assert Parser('').eval_node('(- 2 2)') == 0.0
    assert Parser('').eval_node('(* 2 2)') == 4.0
    assert Parser('').eval_node('(/ 2 2)') == 1.0

    eq = '(+ (+ 1 1) (+ 2 1))'

    # Gets [[3, '('], [9, ')'], [11, '('], [17, ')']] from code
    parens = [
        [i, v]
        for i, v in enumerate(eq) if v in '()'
    ]

    # Gets a a list of tuples for each node where said
    # tuple has a a list with an index position and symbol
    # like [([3, '('], [9, ')']), ([11, '('], [17, ')'])]
    non_nested_nodes = [
        (parens[i], parens[i+1])
        for i in range(len(parens))
            if i < len(parens)
            and parens[i][1] == '('
            and parens[i+1][1] == ')'
    ]

    print(parens)
    print(non_nested_nodes)

    for i in non_nested_nodes:
        print(''.join(
            i for i in eq
        ))
        print(Parser('').eval_node(eq[i[0][0]: i[1][0]]))

        # I just need to be able to put the evaled non nested nodes into the orginal eqaution

    """
    nnn = non_nested_nodes

    for i in range(len(non_nested_nodes)):

        # gets olny one (+ 1 1) atm
        # get sets of nodes and sub strings
        if i % 2 == 0:
            start = nnn
            end = nnn[i+1][0]
            print(
                eq[[i][0]: -[i+1][0]]
            )
    """