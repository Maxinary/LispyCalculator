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