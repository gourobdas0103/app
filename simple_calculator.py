from tkinter import *
from operator import add, sub, mul, truediv

OPFUNC = {'+': add, '-': sub, '*': mul, '/': truediv}


class ParseErr(Exception):
    pass


screen = Tk()

calc = StringVar(screen)
calc.set("")


def lexer(s):
    in_int = False
    current = []
    tokens = []
    for cur in s:
        if in_int:
            if cur.isdigit():
                current.append(cur)
                continue
            else:
                tokens.append(int("".join(current)))
                in_int = False
                current = []
        if cur.isdigit():
            current.append(cur)
            in_int = True
        elif cur in ('+', '-', '*', '/'):
            tokens.append(cur)
        elif not cur.isspace():
            return f"Unexpected char `{cur}`"
    if in_int:
        tokens.append(int("".join(current)))
    return tokens


def parser(tokens):
    stack = []
    op_stack = []
    for tok in tokens:
        if isinstance(tok, int):
            stack.append(tok)
        else:
            while op_stack and not (tok in ('*', '/') and op_stack[-1] in ('+', '-')):
                right = stack.pop()
                stack.append(OPFUNC[op_stack.pop()](stack.pop(), right))
            op_stack.append(tok)
    for op in op_stack[::-1]:
        right = stack.pop()
        stack.append(OPFUNC[op](stack.pop(), right))
    return stack[0]


show = Frame(screen)

entry = Entry(show, textvariable=calc, width="19", state="disable")
entry.grid(column=0, row=0)

ac = Button(show, text='AC', width=4, height=2, command=lambda: calc.set(""))
ac.grid(column=1, row=0)

show.pack()

buttons = Frame(screen)

tab = ["789/","456*","123+","0.=-"]

for i, line in enumerate(tab):
    for j, case in enumerate(line):
        if case == "=":
            a = lambda x=case: calc.set(parser(lexer(calc.get().strip())))
        else:
            a = lambda x=case: calc.set(calc.get() + x)
        Button(buttons, text=case, width=4, height=2, command=a).grid(column=j, row=i)

buttons.pack()

screen.mainloop()