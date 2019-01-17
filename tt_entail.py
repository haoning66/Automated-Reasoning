from copy import deepcopy
result = []
ce_set = set()
ext_symbols=[]


class LogicalExpression(object):
    def __init__(self, tree_value, parent=None):
        super(LogicalExpression, self).__init__()
        self.tree_value = tree_value
        if tree_value in ['ifof', 'and', 'or', 'equal', 'ent', 'not', 'if']:
            self.symbol = None
            self.connective = tree_value
        else:
            self.symbol = tree_value
            self.connective = None
        self.parent = parent
        self.children = []

    def add_child(self, tree_value, child=None):
        if child and not isinstance(child, LogicalExpression):
            raise ValueError('LogicalExpression only add another LogicalExpression object as child')
        if child is None:
            child = LogicalExpression(tree_value)
        child.parent = self
        self.children.append(child)
        return child


def extract_symbols(le=LogicalExpression(None)):
    get_symbols = []
    if le.symbol is not None:
        ext_symbols.append(le.symbol)
    else:
        for child in le.children:
            ext_symbols.append(extract_symbols(child)[0])
    for item in ext_symbols:
        if item not in get_symbols:
            get_symbols.append(item)
    return get_symbols


def pl_true(le=LogicalExpression(None),model={}):
    if le.symbol is not None:
        return model[le.symbol]
    elif le.connective == 'and':
        for child in le.children:
            if (pl_true(child,model)) is False:
                return False
        return True
    elif le.connective == 'or':
        for child in le.children:
            if (pl_true(child,model)) is True:
                return True
        return False
    elif le.connective == 'if':
        left = le.children[0]
        right = le.children[1]
        if pl_true(left, model) is True:
            if pl_true(right, model) is False:
                return False
            else:
                return True
        else:
            return True
    elif le.connective == 'ifof':
        left = le.children[0]
        right = le.children[1]
        if pl_true(left,model) == pl_true(right,model):
            return True
        else:
            return False
    elif le.connective == 'not':
        child=le.children[0]
        if pl_true(child,model) is True:
            return False
        else:
            return True
    elif le.connective == 'ent':
        left = le.children[0]
        right = le.children[1]
        if pl_true(left,model) is True:
            if pl_true(right,model) is True:
                return True


def tt_entails(kb=LogicalExpression(None), alpha=LogicalExpression(None)):
    symbols = []
    for i in (extract_symbols(kb) + extract_symbols(alpha)):
        if i not in symbols:
            symbols.append(i)
    tt_check_all(kb, alpha, symbols, {})
    #print result
    if False in result:
        return False
    else:
        return True


def extend(symbol, value, model):
    model[symbol] = value
    return model


def copy_symbols(symbols=[]):
    new_symbols = deepcopy(symbols)
    return new_symbols


def copy_model(model={}):
    new_model=deepcopy(model)
    return new_model


def tt_check_all(kb=LogicalExpression(None), alpha=LogicalExpression(None), symbols=[], model={}):
    #print model
    if len(symbols) == 0:
        if pl_true(kb, model):
            result.append(pl_true(alpha,model))
            return pl_true(alpha,model)
        else:
            result.append(True)
            return True
    else:
        p = symbols[0]
        rest = symbols
        rest.remove(symbols[0])
        return tt_check_all(kb, alpha, copy_symbols(symbols), extend(p, True, copy_model(model))) & tt_check_all(kb, alpha, copy_symbols(symbols), extend(p, False, copy_model(model)))


if __name__ == '__main__':

    kb1=LogicalExpression('and')     #kb for question 1
    kb11=kb1.add_child('p')
    kb12=kb1.add_child('if')
    kb12.add_child('p')
    kb12.add_child('q')
    alpha1=LogicalExpression('q')

    kb2=LogicalExpression('and')      #kb for question 2
    kb21=kb2.add_child('not')
    kb211=kb21.add_child('p11')
    kb22=kb2.add_child('ifof')
    kb221=kb22.add_child('b11')
    kb222=kb22.add_child('or')
    kb222.add_child('p12')
    kb222.add_child('p21')
    kb23=kb2.add_child('ifof')
    kb23.add_child('b21')
    kb232=kb23.add_child('or')
    kb232.add_child('p11')
    kb232.add_child('p22')
    kb232.add_child('p31')
    kb24=kb2.add_child('not')
    kb24.add_child('b11')
    kb2.add_child('b21')
    alpha2=LogicalExpression('p12')

    kb3=LogicalExpression('and')    #kb for question3
    kb31 = kb3.add_child('if')
    kb31.add_child('myt')
    kb31.add_child('imm')
    kb32 = kb3.add_child('if')
    kb321=kb32.add_child('not')
    kb321.add_child('myt')
    kb32.add_child('mor')
    kb33=kb3.add_child('if')
    kb331=kb33.add_child('or')
    kb331.add_child('imm')
    kb331.add_child('mor')
    kb33.add_child('hor')
    kb34 = kb3.add_child('if')
    kb34.add_child('hor')
    kb34.add_child('mag')
    alpha31 = LogicalExpression('myt')
    alpha32 = LogicalExpression('mag')
    alpha33 = LogicalExpression('hor')

    kb4 = LogicalExpression('and')    #knowledge base for question 4(a)
    kb41=kb4.add_child('or')
    kb411=kb41.add_child('not')
    kb411.add_child('a')
    kb41.add_child('a')
    kb42 = kb4.add_child('or')
    kb421 = kb42.add_child('not')
    kb421.add_child('a')
    kb42.add_child('c')
    kb43 = kb4.add_child('or')
    kb43.add_child('a')
    kb432=kb43.add_child('not')
    kb432.add_child('a')
    kb43.add_child('c')
    kb44 = kb4.add_child('or')
    kb441=kb44.add_child('not')
    kb441.add_child('b')
    kb442 = kb44.add_child('not')
    kb442.add_child('c')
    kb45=kb4.add_child('or')
    kb45.add_child('b')
    kb45.add_child('c')
    kb46=kb4.add_child('or')
    kb461=kb46.add_child('not')
    kb461.add_child('c')
    kb46.add_child('b')
    kb463 = kb46.add_child('not')
    kb463.add_child('a')
    kb47 = kb4.add_child('or')
    kb47.add_child('c')
    kb472=kb47.add_child('not')
    kb472.add_child('b')
    kb48=kb4.add_child('or')
    kb48.add_child('a')
    kb48.add_child('c')

    kb5 = LogicalExpression('and') #kb for question 4(b)
    kb51 = kb5.add_child('or')
    kb511=kb51.add_child('not')
    kb511.add_child('a')
    kb512=kb51.add_child('not')
    kb512.add_child('c')
    kb52=kb5.add_child('or')
    kb52.add_child('a')
    kb52.add_child('c')
    kb53=kb5.add_child('or')
    kb531=kb53.add_child('not')
    kb531.add_child('b')
    kb53.add_child('a')
    kb54=kb5.add_child('or')
    kb541=kb54.add_child('not')
    kb541.add_child('b')
    kb54.add_child('c')
    kb55=kb5.add_child('or')
    kb55.add_child('b')
    kb552=kb55.add_child('not')
    kb552.add_child('a')
    kb553=kb55.add_child('not')
    kb553.add_child('c')
    kb56=kb5.add_child('or')
    kb561=kb56.add_child('not')
    kb561.add_child('c')
    kb56.add_child('b')
    kb57=kb5.add_child('or')
    kb57.add_child('c')
    kb571=kb57.add_child('not')
    kb571.add_child('b')
    alpha41 = LogicalExpression('a')
    alpha42 = LogicalExpression('b')
    alpha43 = LogicalExpression('c')

    kb6=LogicalExpression('and')      #kb for question 5
    kb61 = kb6.add_child('or')
    kb611=kb61.add_child('not')
    kb611.add_child('a')
    kb61.add_child('h')
    kb62=kb6.add_child('or')
    kb621=kb62.add_child('not')
    kb621.add_child('a')
    kb62.add_child('i')
    kb63=kb6.add_child('or')
    kb63.add_child('a')
    kb632=kb63.add_child('not')
    kb632.add_child('h')
    kb633=kb63.add_child('not')
    kb633.add_child('i')
    kb64=kb6.add_child('or')
    kb641=kb64.add_child('not')
    kb641.add_child('b')
    kb64.add_child('a')
    kb65=kb6.add_child('or')
    kb651=kb65.add_child('not')
    kb651.add_child('b')
    kb65.add_child('l')
    kb66 = kb6.add_child('or')
    kb66.add_child('b')
    kb662=kb66.add_child('not')
    kb662.add_child('a')
    kb663=kb66.add_child('not')
    kb663.add_child('l')
    kb67=kb6.add_child('or')
    kb671=kb67.add_child('not')
    kb671.add_child('c')
    kb67.add_child('b')
    kb68=kb6.add_child('or')
    kb681 = kb68.add_child('not')
    kb681.add_child('c')
    kb68.add_child('g')
    kb69=kb6.add_child('or')
    kb69.add_child('c')
    kb692=kb69.add_child('not')
    kb692.add_child('b')
    kb693=kb69.add_child('not')
    kb693.add_child('g')
    kb6a=kb6.add_child('or')
    kb6a1=kb6a.add_child('not')
    kb6a1.add_child('d')
    kb6a.add_child('e')
    kb6b=kb6.add_child('or')
    kb6b1=kb6b.add_child('not')
    kb6b1.add_child('d')
    kb6b.add_child('l')
    kb6c=kb6.add_child('or')
    kb6c.add_child('d')
    kb6c2=kb6c.add_child('not')
    kb6c2.add_child('e')
    kb6c3=kb6c.add_child('not')
    kb6c3.add_child('l')
    kb6d=kb6.add_child('or')
    kb6d1=kb6d.add_child('not')
    kb6d1.add_child('e')
    kb6d.add_child('c')
    kb6e=kb6.add_child('or')
    kb6e1=kb6e.add_child('not')
    kb6e1.add_child('e')
    kb6e.add_child('h')
    kb6f=kb6.add_child('or')
    kb6f.add_child('e')
    kb6f2=kb6f.add_child('not')
    kb6f2.add_child('c')
    kb6f3=kb6f.add_child('not')
    kb6f3.add_child('h')
    kb6g=kb6.add_child('or')
    kb6g1=kb6g.add_child('not')
    kb6g1.add_child('f')
    kb6g.add_child('d')
    kb6h=kb6.add_child('or')
    kb6h1=kb6h.add_child('not')
    kb6h1.add_child('f')
    kb6h.add_child('i')
    kb6i=kb6.add_child('or')
    kb6i.add_child('f')
    kb6i2=kb6i.add_child('not')
    kb6i2.add_child('d')
    kb6i3=kb6i.add_child('not')
    kb6i3.add_child('i')
    kb6j=kb6.add_child('or')
    kb6j1=kb6j.add_child('not')
    kb6j1.add_child('g')
    kb6j2=kb6j.add_child('not')
    kb6j2.add_child('e')
    kb6k=kb6.add_child('or')
    kb6k1=kb6k.add_child('not')
    kb6k1.add_child('g')
    kb6k2=kb6k.add_child('not')
    kb6k2.add_child('j')
    kb6l=kb6.add_child('or')
    kb6l.add_child('g')
    kb6l.add_child('e')
    kb6l.add_child('j')
    kb6m=kb6.add_child('or')
    kb6m1=kb6m.add_child('not')
    kb6m1.add_child('h')
    kb6m2=kb6m.add_child('not')
    kb6m2.add_child('f')
    kb6n=kb6.add_child('or')
    kb6n1=kb6n.add_child('not')
    kb6n1.add_child('h')
    kb6n2=kb6n.add_child('not')
    kb6n2.add_child('k')
    kb6o=kb6.add_child('or')
    kb6o.add_child('h')
    kb6o.add_child('f')
    kb6o.add_child('k')
    kb6p=kb6.add_child('or')
    kb6p1=kb6p.add_child('not')
    kb6p1.add_child('i')
    kb6p2=kb6p.add_child('not')
    kb6p2.add_child('g')
    kb6q=kb6.add_child('or')
    kb6q1=kb6q.add_child('not')
    kb6q1.add_child('i')
    kb6q2=kb6q.add_child('not')
    kb6q2.add_child('k')
    kb6r=kb6.add_child('or')
    kb6r.add_child('i')
    kb6r.add_child('g')
    kb6r.add_child('k')
    kb6s=kb6.add_child('or')
    kb6s1=kb6s.add_child('not')
    kb6s1.add_child('j')
    kb6s2=kb6s.add_child('not')
    kb6s2.add_child('a')
    kb6t=kb6.add_child('or')
    kb6t1=kb6t.add_child('not')
    kb6t1.add_child('j')
    kb6t2=kb6t.add_child('not')
    kb6t2.add_child('c')
    kb6u=kb6.add_child('or')
    kb6u.add_child('j')
    kb6u.add_child('a')
    kb6u.add_child('c')
    kb6v=kb6.add_child('or')
    kb6v1=kb6v.add_child('not')
    kb6v1.add_child('k')
    kb6v2=kb6v.add_child('not')
    kb6v2.add_child('d')
    kb6w=kb6.add_child('or')
    kb6w1=kb6w.add_child('not')
    kb6w1.add_child('k')
    kb6w2=kb6w.add_child('not')
    kb6w2.add_child('f')
    kb6x=kb6.add_child('or')
    kb6x.add_child('k')
    kb6x.add_child('d')
    kb6x.add_child('f')
    kb6y=kb6.add_child('or')
    kb6y1=kb6y.add_child('not')
    kb6y1.add_child('l')
    kb6y2=kb6y.add_child('not')
    kb6y2.add_child('b')
    kb6z=kb6.add_child('or')
    kb6z1=kb6z.add_child('not')
    kb6z1.add_child('l')
    kb6z2=kb6z.add_child('not')
    kb6z2.add_child('j')
    kb6zz=kb6.add_child('or')
    kb6zz.add_child('l')
    kb6zz.add_child('b')
    kb6zz.add_child('j')
    alpha51 = LogicalExpression('a')
    alpha52 = LogicalExpression('b')
    alpha53 = LogicalExpression('c')
    alpha54 = LogicalExpression('d')
    alpha55 = LogicalExpression('e')
    alpha56 = LogicalExpression('f')
    alpha57 = LogicalExpression('g')
    alpha58 = LogicalExpression('h')
    alpha59 = LogicalExpression('i')
    alpha510 = LogicalExpression('j')
    alpha511 = LogicalExpression('k')
    alpha512 = LogicalExpression('l')

    kb7=LogicalExpression('and')         #knowledge base for problem5(a)
    kb71=kb7.add_child('or')
    kb711=kb71.add_child('not')
    kb711.add_child('a')
    kb71.add_child('x')
    kb72=kb7.add_child('or')
    kb72.add_child('a')
    kb722=kb72.add_child('not')
    kb722.add_child('x')
    kb73=kb7.add_child('or')
    kb731=kb73.add_child('not')
    kb731.add_child('b')
    kb73.add_child('y')
    kb73.add_child('z')
    kb74=kb7.add_child('or')
    kb74.add_child('b')
    kb742=kb74.add_child('not')
    kb742.add_child('y')
    kb75=kb7.add_child('or')
    kb75.add_child('b')
    kb752=kb75.add_child('not')
    kb752.add_child('z')
    kb76=kb7.add_child('or')
    kb761=kb76.add_child('not')
    kb761.add_child('c')
    kb76.add_child('a')
    kb77=kb7.add_child('or')
    kb771=kb77.add_child('not')
    kb771.add_child('c')
    kb77.add_child('b')
    kb78=kb7.add_child('or')
    kb78.add_child('c')
    kb782=kb78.add_child('not')
    kb782.add_child('a')
    kb783=kb78.add_child('not')
    kb783.add_child('b')
    kb79=kb7.add_child('or')
    kb791=kb79.add_child('not')
    kb791.add_child('d')
    kb79.add_child('x')
    kb7a=kb7.add_child('or')
    kb7a1=kb7a.add_child('not')
    kb7a1.add_child('d')
    kb7a.add_child('y')
    kb7b=kb7.add_child('or')
    kb7b.add_child('d')
    kb7b2=kb7b.add_child('not')
    kb7b2.add_child('x')
    kb7b3=kb7b.add_child('not')
    kb7b3.add_child('y')
    kb7c=kb7.add_child('or')
    kb7c1=kb7c.add_child('not')
    kb7c1.add_child('e')
    kb7c.add_child('x')
    kb7d=kb7.add_child('or')
    kb7d1=kb7d.add_child('not')
    kb7d1.add_child('e')
    kb7d.add_child('z')
    kb7e=kb7.add_child('or')
    kb7e.add_child('e')
    kb7e2=kb7e.add_child('not')
    kb7e2.add_child('x')
    kb7e3=kb7e.add_child('not')
    kb7e3.add_child('z')
    kb7f=kb7.add_child('or')
    kb7f1=kb7f.add_child('not')
    kb7f1.add_child('f')
    kb7f.add_child('d')
    kb7f.add_child('e')
    kb7g=kb7.add_child('or')
    kb7g.add_child('f')
    kb7g2=kb7g.add_child('not')
    kb7g2.add_child('d')
    kb7h=kb7.add_child('or')
    kb7h.add_child('f')
    kb7h2=kb7h.add_child('not')
    kb7h2.add_child('e')
    kb7i=kb7.add_child('or')
    kb7i1=kb7i.add_child('not')
    kb7i1.add_child('g')
    kb7i2=kb7i.add_child('not')
    kb7i2.add_child('c')
    kb7i.add_child('f')
    kb7j=kb7.add_child('or')
    kb7j.add_child('g')
    kb7j.add_child('c')
    kb7k=kb7.add_child('or')
    kb7k.add_child('g')
    kb7k2=kb7k.add_child('not')
    kb7k2.add_child('f')
    kb7l=kb7.add_child('or')
    kb7l1=kb7l.add_child('not')
    kb7l1.add_child('h')
    kb7l2=kb7l.add_child('not')
    kb7l2.add_child('g')
    kb7l.add_child('a')
    kb7m=kb7.add_child('or')
    kb7m.add_child('h')
    kb7m.add_child('g')
    kb7.add_child('h')
    kb7n=kb7.add_child('or')
    kb7n.add_child('h')
    kb7n2=kb7n.add_child('not')
    kb7n2.add_child('a')
    kb7o=kb7.add_child('or')
    kb7o.add_child('x')
    kb7o.add_child('y')
    kb7o.add_child('z')
    kb7o.add_child('w')

    kb8=LogicalExpression('and')
    kb81=kb8.add_child('or')
    kb811=kb81.add_child('not')
    kb811.add_child('a')
    kb81.add_child('x')
    kb82=kb8.add_child('or')
    kb82.add_child('a')
    kb822=kb82.add_child('not')
    kb822.add_child('x')
    kb83=kb8.add_child('or')
    kb831=kb83.add_child('not')
    kb831.add_child('c')
    kb83.add_child('a')
    kb84=kb8.add_child('or')
    kb84.add_child('c')
    kb842=kb84.add_child('not')
    kb842.add_child('a')
    kb843=kb84.add_child('not')
    kb843.add_child('b')
    kb85=kb8.add_child('or')
    kb85.add_child('c')
    kb852=kb85.add_child('not')
    kb852.add_child('a')
    kb853=kb85.add_child('not')
    kb853.add_child('d')
    kb86=kb8.add_child('or')
    kb86.add_child('c')
    kb862=kb86.add_child('not')
    kb862.add_child('a')
    kb863=kb86.add_child('not')
    kb863.add_child('e')
    kb87=kb8.add_child('or')
    kb87.add_child('c')
    kb872=kb87.add_child('not')
    kb872.add_child('a')
    kb873=kb87.add_child('not')
    kb873.add_child('f')
    kb88=kb8.add_child('or')
    kb88.add_child('c')
    kb882=kb88.add_child('not')
    kb882.add_child('a')
    kb883=kb88.add_child('not')
    kb883.add_child('g')
    kb89=kb8.add_child('or')
    kb89.add_child('c')
    kb892=kb89.add_child('not')
    kb892.add_child('a')
    kb893=kb89.add_child('not')
    kb893.add_child('h')
    kb8a=kb8.add_child('or')
    kb8a.add_child('c')
    kb8a2=kb8a.add_child('not')
    kb8a2.add_child('a')
    kb8a3=kb8a.add_child('not')
    kb8a3.add_child('h')
    kb8b=kb8.add_child('or')
    kb8b1=kb8b.add_child('not')
    kb8b1.add_child('h')
    kb8b2=kb8b.add_child('not')
    kb8b2.add_child('g')
    kb8b.add_child('a')
    kb8c=kb8.add_child('or')
    kb8c.add_child('h')
    kb8c.add_child('g')
    kb8.add_child('h')
    kb8d=kb8.add_child('or')
    kb8d.add_child('h')
    kb8d2=kb8d.add_child('not')
    kb8d2.add_child('a')
    kb8e=kb8.add_child('or')
    kb8e.add_child('g')
    kb8e.add_child('c')
    kb8f=kb8.add_child('or')
    kb8f.add_child('x')
    kb8f.add_child('y')
    kb8f.add_child('z')
    kb8f.add_child('w')

    alpha71=LogicalExpression('x')
    alpha72 = LogicalExpression('y')
    alpha73 = LogicalExpression('z')
    alpha74 = LogicalExpression('w')

while(True):
    choose = input('Please choose problem')
    if choose == 1:
        print 'Result for {P,P=>Q}|=Q is ' + str(tt_entails(kb1, alpha1))
        result = []
    elif choose == 2:
        print 'P12 is ' + str(tt_entails(kb2, alpha2))
        result = []
    elif choose == 3:
        print '(a) is ' + str(tt_entails(kb3, alpha31))
        result = []
        print '(b) is ' + str(tt_entails(kb3, alpha32))
        result = []
        print '(c) is ' + str(tt_entails(kb3, alpha33))
        result = []
    elif choose == 4:
        print '(a)'
        print 'Amy is ' + str(tt_entails(kb4, alpha41))
        result = []
        print 'Bob is ' + str(tt_entails(kb4, alpha42))
        result = []
        print 'Cal is ' + str(tt_entails(kb4, alpha43))
        result = []
        print '(b)'
        print 'Amy is ' + str(tt_entails(kb5, alpha41))
        result = []
        print 'Bob is ' + str(tt_entails(kb5, alpha42))
        result = []
        print 'Cal is ' + str(tt_entails(kb5, alpha43))
        result = []
    elif choose==5:
        print 'Amy is ' + str(tt_entails(kb6,alpha51))
        result=[]
        print 'Bob is ' + str(tt_entails(kb6, alpha52))
        result = []
        print 'Cal is ' + str(tt_entails(kb6, alpha53))
        result = []
        print 'Dee is ' + str(tt_entails(kb6, alpha54))
        result = []
        print 'Eli is ' + str(tt_entails(kb6, alpha55))
        result = []
        print 'Fay is ' + str(tt_entails(kb6, alpha56))
        result = []
        print 'Gil is ' + str(tt_entails(kb6, alpha57))
        result = []
        print 'Hal is ' + str(tt_entails(kb6, alpha58))
        result = []
        print 'Ida is ' + str(tt_entails(kb6, alpha59))
        result = []
        print 'Jay is ' + str(tt_entails(kb6, alpha510))
        result = []
        print 'Kay is ' + str(tt_entails(kb6, alpha511))
        result = []
        print 'Lee is ' + str(tt_entails(kb6, alpha512))
        result = []
    elif choose == 6:
        print '(a)'
        print 'x is ' + str(tt_entails(kb7,alpha71))
        result = []
        print 'y is ' + str(tt_entails(kb7, alpha72))
        result = []
        print 'z is ' + str(tt_entails(kb7, alpha73))
        result = []
        print 'w is ' + str(tt_entails(kb7, alpha74))
        result = []
        print 'so, he should choose door x'
        print '(b)'
        print 'x is ' + str(tt_entails(kb8, alpha71))
        result = []
        print 'y is ' + str(tt_entails(kb8, alpha72))
        result = []
        print 'z is ' + str(tt_entails(kb8, alpha73))
        result = []
        print 'w is ' + str(tt_entails(kb8, alpha74))
        result = []
        print 'so, he have heard enough to choose door x'