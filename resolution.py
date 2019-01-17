from copy import deepcopy
ce_set = set()


class ClauseExpression(object):
    def __init__(self,clause):
        self.clause = clause
        self.clause_list = clause.split()

    def ce_set(self):
        str_clause = ''
        for item in self.clause_list:
            str_clause = str_clause + ' ' + item
        str_clause = str_clause.lstrip()
        ce_set.add(str_clause)
'''
def contradict(clauses, not_alpha):
    not_alpha_list = not_alpha.split()
    for item in clauses:
        clauses_list = item.split()
        clauses_list_2 = deepcopy(clauses_list)
        not_alpha_list_2 = deepcopy(not_alpha_list)
        for item1 in clauses_list:
            if item1.startswith('not'):
                x = item1.replace('not','')
                for item2 in not_alpha_list:
                    if x == item2:
                        clauses_list_2.remove(item1)
                        not_alpha_list_2.remove(item2)
            else:
                for item2 in not_alpha_list:

                    if item2.startswith('not'):
                        y = item2.replace('not','')
                        if item1 == y:
                            clauses_list_2.remove(item1)
                            not_alpha_list_2.remove(item2)
        if len(clauses_list_2) == 0 and len(not_alpha_list_2) == 0:
            return True
            break
    return False
'''

def pl_resolution(kb_list, alpha):
    resolvent_str = ''
    resolvents_set = set()
    new = set()
    for itemx in kb_list:
        itemx.ce_set()
    alpha.ce_set()
    clauses = deepcopy(ce_set)
    while(True):
        for item1 in clauses:
            for item2 in clauses:
                if item1 != item2:
                    resolvent_str = pl_resolve(item1,item2)
                    if resolvent_str == '':
                        #print clauses
                        return True
                        break
                    elif resolvent_str != 'alwaystrue' and resolvent_str!='F':
                        resolvents_set.add(resolvent_str)
                        new = new | resolvents_set

        if new.issubset(clauses):
            return False
            break
        clauses = clauses | new


def pl_resolve(ci,cj):
    ci_list = ci.split()
    cj_list = cj.split()
    len_ci=len(ci_list)
    len_cj=len(cj_list)
    resolvents=''
    count = 0
    for item7 in ci_list:
        for item8 in cj_list:
            if item7 == item8:
                if len(ci_list)==1 or len(cj_list)==1:
                    return 'alwaystrue'
                    break
                elif len_ci!=2 and len_cj!=2:
                    return 'F'
                    break
    for item1 in ci_list:
        if item1.startswith('not'):
            x=item1.replace('not', '')
            for item2 in cj_list:
                if x == item2:
                    count+=1
                    ci_list.remove(item1)
                    cj_list.remove(item2)

        else:
            for item2 in cj_list:
                if item2.startswith('not'):
                    y = item2.replace('not','')
                    if y == item1:
                        count+=1
                        ci_list.remove(item1)
                        cj_list.remove(item2)
    if count == 0:
        return 'F'
    if count>1:
        return  'alwaystrue'
    for item3 in ci_list:
        if item3.startswith('not'):
            z = item3.replace('not', '')
            for item4 in cj_list:
                if z == item4:
                    return 'alwaystrue'
                    break
        else:
            for item4 in cj_list:
                if item4.startswith('not'):
                    h = item4.replace('not','')
                    if h == item3:
                        return 'alwaystrue'
                        break
    for item9 in ci_list:
        for item10 in cj_list:
            if item9 == item10:
                ci_cj_list=[]
                ci_list.extend(cj_list)
                ci_cj_list = ci_list
                ci_list=[]
                cj_list=[]
                for item11 in ci_cj_list:
                    if item11 not in ci_list:
                        ci_list.append(item11)
    if (len_ci>=2) and (len_cj>=2) and (len(ci_list)+len(cj_list))>=2:
        return 'F'
    for item5 in ci_list:
        resolvents = resolvents + ' ' + item5
        resolvents = resolvents.lstrip()
    for item6 in cj_list:
        resolvents = resolvents + ' ' + item6
        resolvents = resolvents.lstrip()
    return resolvents


if __name__ == '__main__':
    #print pl_resolve('d notb', 'd b')



    kb_list1=[]                 #knowledge base for question 1
    kb11=ClauseExpression('p')
    kb_list1.append(kb11)
    kb12=ClauseExpression('notp q')
    kb_list1.append(kb12)
    a11=ClauseExpression('notq')

    kb_list2=[]                 #knowledge base for question 2
    kb21=ClauseExpression('notp11')
    kb_list2.append(kb21)
    kb22=ClauseExpression('notb11 p12 p21')
    kb_list2.append(kb22)
    kb23 = ClauseExpression('notp12 b11')
    kb_list2.append(kb23)
    kb24 = ClauseExpression('notp21 b11')
    kb_list2.append(kb24)
    kb25 = ClauseExpression('notb21 p11 p22 p31')
    kb_list2.append(kb25)
    kb26 = ClauseExpression('b21 notp11')
    kb_list2.append(kb26)
    kb27 = ClauseExpression('b21 notp22')
    kb_list2.append(kb27)
    kb28 = ClauseExpression('b21 notp31')
    kb_list2.append(kb28)
    kb29 = ClauseExpression('notb11')
    kb_list2.append(kb29)
    kb30 = ClauseExpression('b21')
    kb_list2.append(kb30)
    a21 = ClauseExpression('notp12')

    kb_list3=[]                 #knowledge base for question 3
    kb31 = ClauseExpression('notmyt imm')
    kb_list3.append(kb31)
    kb32 = ClauseExpression('myt mor')
    kb_list3.append(kb32)
    kb33 = ClauseExpression('notimm hor')
    kb_list3.append(kb33)
    kb34 = ClauseExpression('notmor hor')
    kb_list3.append(kb34)
    kb35 = ClauseExpression('nothor mag')
    kb_list3.append(kb35)
    a31=ClauseExpression('notmyt')
    a32=ClauseExpression('notmag')
    a33=ClauseExpression('nothor')

    kb_list4=[]                 #knowledge base for question 4(a)
    kb41 = ClauseExpression('nota a')
    kb_list4.append(kb41)
    kb42 = ClauseExpression('nota c')
    kb_list4.append(kb42)
    kb43 = ClauseExpression('a nota c')
    kb_list4.append(kb43)
    kb44 = ClauseExpression('notb notc')
    kb_list4.append(kb44)
    kb45 = ClauseExpression('b c')
    kb_list4.append(kb45)
    kb46 = ClauseExpression('notc b nota')
    kb_list4.append(kb46)
    kb47 = ClauseExpression('c notb')
    kb_list4.append(kb47)
    kb48 = ClauseExpression('c a')
    kb_list4.append(kb48)

    kb_list42=[]                 #knowledge base for question 4(b)
    kb421 = ClauseExpression('nota notc')
    kb_list42.append(kb421)
    kb422 = ClauseExpression('a c')
    kb_list42.append(kb422)
    kb423 = ClauseExpression('notb a')
    kb_list42.append(kb423)
    kb424 = ClauseExpression('notb c')
    kb_list42.append(kb424)
    kb425 = ClauseExpression('b nota notc')
    kb_list42.append(kb425)
    kb426 = ClauseExpression('notc b')
    kb_list42.append(kb426)
    kb427 = ClauseExpression('c notb')
    kb_list42.append(kb427)
    a41=ClauseExpression('nota')
    a42 = ClauseExpression('notb')
    a43 = ClauseExpression('notc')

    kb_list5=[]
    kb51 = ClauseExpression('nota h')
    kb_list5.append(kb51)
    kb52 = ClauseExpression('nota i')
    kb_list5.append(kb52)
    kb53 = ClauseExpression('a noth noti')
    kb_list5.append(kb53)
    kb54 = ClauseExpression('notb a')
    kb_list5.append(kb54)
    kb55 = ClauseExpression('notb l')
    kb_list5.append(kb55)
    kb56 = ClauseExpression('b nota notl')
    kb_list5.append(kb56)
    kb57 = ClauseExpression('notc b')
    kb_list5.append(kb57)
    kb58 = ClauseExpression('notc g')
    kb_list5.append(kb58)
    kb59 = ClauseExpression('c notb notg')
    kb_list5.append(kb59)
    kb510 = ClauseExpression('notd e')
    kb_list5.append(kb510)
    kb511 = ClauseExpression('notd l')
    kb_list5.append(kb511)
    kb512 = ClauseExpression('d note notl')
    kb_list5.append(kb512)
    kb513 = ClauseExpression('note c')
    kb_list5.append(kb513)
    kb514 = ClauseExpression('note h')
    kb_list5.append(kb514)
    kb515 = ClauseExpression('e notc noth')
    kb_list5.append(kb515)
    kb516 = ClauseExpression('notf d')
    kb_list5.append(kb516)
    kb517 = ClauseExpression('notf i')
    kb_list5.append(kb517)
    kb518 = ClauseExpression('f notd noti')
    kb_list5.append(kb518)
    kb519 = ClauseExpression('notg note')
    kb_list5.append(kb519)
    kb520 = ClauseExpression('notg notj')
    kb_list5.append(kb520)
    kb521 = ClauseExpression('g e j')
    kb_list5.append(kb521)
    kb522 = ClauseExpression('noth notf')
    kb_list5.append(kb522)
    kb523 = ClauseExpression('noth notk')
    kb_list5.append(kb523)
    kb524 = ClauseExpression('h f k')
    kb_list5.append(kb524)
    kb525 = ClauseExpression('noti notg')
    kb_list5.append(kb525)
    kb526 = ClauseExpression('noti notk')
    kb_list5.append(kb526)
    kb527 = ClauseExpression('i g k')
    kb_list5.append(kb527)
    kb528 = ClauseExpression('notj nota')
    kb_list5.append(kb528)
    kb529 = ClauseExpression('notj notc')
    kb_list5.append(kb529)
    kb530 = ClauseExpression('j a c')
    kb_list5.append(kb530)
    kb531 = ClauseExpression('notk notd')
    kb_list5.append(kb531)
    kb532 = ClauseExpression('notk notf')
    kb_list5.append(kb532)
    kb533 = ClauseExpression('k d f')
    kb_list5.append(kb533)
    kb534 = ClauseExpression('notl notb')
    kb_list5.append(kb534)
    kb535 = ClauseExpression('notl notj')
    kb_list5.append(kb535)
    kb536 = ClauseExpression('l b j')
    kb_list5.append(kb536)
    a51 = ClauseExpression('nota')
    a52 = ClauseExpression('notb')
    a53 = ClauseExpression('notc')
    a54 = ClauseExpression('notd')
    a55 = ClauseExpression('note')
    a56 = ClauseExpression('notf')
    a57 = ClauseExpression('notg')
    a58 = ClauseExpression('noth')
    a59 = ClauseExpression('noti')
    a510 = ClauseExpression('notj')
    a511 = ClauseExpression('notk')
    a512 = ClauseExpression('notl')

    kb_list6=[]
    kb61 = ClauseExpression('nota x')
    kb_list6.append(kb61)
    kb62 = ClauseExpression('a notx')
    kb_list6.append(kb62)
    kb63 = ClauseExpression('notc a')
    kb_list6.append(kb63)
    kb64 = ClauseExpression('notc b c d e f g h')
    kb_list6.append(kb64)
    kb65 = ClauseExpression('c nota notb')
    kb_list6.append(kb65)
    kb66 = ClauseExpression('c nota notc')
    kb_list6.append(kb66)
    kb67 = ClauseExpression('c nota notd')
    kb_list6.append(kb67)
    kb68 = ClauseExpression('c nota note')
    kb_list6.append(kb68)
    kb69 = ClauseExpression('c nota notf')
    kb_list6.append(kb69)
    kb610 = ClauseExpression('c nota notg')
    kb_list6.append(kb610)
    kb611 = ClauseExpression('c nota noth')
    kb_list6.append(kb611)
    kb612 = ClauseExpression('noth notg a')
    kb_list6.append(kb612)
    kb613 = ClauseExpression('h g')
    kb_list6.append(kb613)
    kb614 = ClauseExpression('h')
    kb_list6.append(kb614)
    kb615 = ClauseExpression('h nota')
    kb_list6.append(kb615)
    kb616 = ClauseExpression('g c')
    kb_list6.append(kb616)
    kb617 = ClauseExpression('x y z w')
    kb_list6.append(kb617)

    kb_list62=[]
    kb618 = ClauseExpression('nota x')
    kb_list62.append(kb618)
    kb619 = ClauseExpression('a notx')
    kb_list62.append(kb619)
    kb620 = ClauseExpression('notb y z')
    kb_list62.append(kb620)
    kb621 = ClauseExpression('b noty')
    kb_list62.append(kb621)
    kb622 = ClauseExpression('b notz')
    kb_list62.append(kb622)
    kb623 = ClauseExpression('notc a')
    kb_list62.append(kb623)
    kb624 = ClauseExpression('notc b')
    kb_list62.append(kb624)
    kb625 = ClauseExpression('c nota notb')
    kb_list62.append(kb625)
    kb626 = ClauseExpression('notd x')
    kb_list62.append(kb626)
    kb627 = ClauseExpression('notd y')
    kb_list62.append(kb627)
    kb628 = ClauseExpression('d notx noty')
    kb_list62.append(kb628)
    kb629 = ClauseExpression('note x')
    kb_list62.append(kb629)
    kb630 = ClauseExpression('note z')
    kb_list62.append(kb630)
    kb631 = ClauseExpression('e notx notz')
    kb_list62.append(kb631)
    kb632 = ClauseExpression('notf d e')
    kb_list62.append(kb632)
    kb633 = ClauseExpression('f notd')
    kb_list62.append(kb633)
    kb634 = ClauseExpression('f note')
    kb_list62.append(kb634)
    kb635 = ClauseExpression('notg notc f')
    kb_list62.append(kb635)
    kb636 = ClauseExpression('g c')
    kb_list62.append(kb636)
    kb637 = ClauseExpression('g notf')
    kb_list62.append(kb637)
    kb638 = ClauseExpression('noth notg a')
    kb_list62.append(kb638)
    kb639 = ClauseExpression('h g')
    kb_list62.append(kb639)
    kb640 = ClauseExpression('h')
    kb_list62.append(kb640)
    kb641 = ClauseExpression('h nota')
    kb_list62.append(kb641)
    kb642 = ClauseExpression('x y z w')
    kb_list62.append(kb642)

    a61 = ClauseExpression('notx')
    a62 = ClauseExpression('noty')
    a63 = ClauseExpression('notz')
    a64 = ClauseExpression('notw')

    while(True):
        choose = input('please choose question')
        if choose == 1:
            print 'Result for {P,P=>Q}|=Q is ' + str(pl_resolution(kb_list1, a11))
            ce_set=set()
        elif choose == 2:
            print 'P12 is '+str(pl_resolution(kb_list2, a21))
            ce_set = set()
        elif choose == 3:
            print '(a) is ' + str(pl_resolution(kb_list3, a31))
            ce_set = set()
            print '(b) is ' + str(pl_resolution(kb_list3, a32))
            ce_set = set()
            print '(c) is ' + str(pl_resolution(kb_list3, a33))
            ce_set = set()
        elif choose == 4:
            print '(a)'
            print 'Amy is ' + str(pl_resolution(kb_list4, a41))
            ce_set = set()
            print 'Bob is ' + str(pl_resolution(kb_list4, a42))
            ce_set = set()
            print 'Cal is ' + str(pl_resolution(kb_list4, a43))
            ce_set = set()
            print '(b)'
            print 'Amy is ' + str(pl_resolution(kb_list42, a41))
            ce_set = set()
            print 'Bob is ' + str(pl_resolution(kb_list42, a42))
            ce_set = set()
            print 'Cal is ' + str(pl_resolution(kb_list42, a43))
            ce_set = set()
        elif choose==5:
            print 'Amy is ' + str(pl_resolution(kb_list5, a51))
            ce_set = set()
            print 'Bob is ' + str(pl_resolution(kb_list5, a52))
            ce_set = set()
            print 'Cal is ' + str(pl_resolution(kb_list5, a53))
            ce_set = set()
            print 'Dee is ' + str(pl_resolution(kb_list5, a54))
            ce_set = set()
            print 'Eli is ' + str(pl_resolution(kb_list5, a55))
            ce_set = set()
            print 'Fay is ' + str(pl_resolution(kb_list5, a56))
            ce_set = set()
            print 'Gil is ' + str(pl_resolution(kb_list5, a57))
            ce_set = set()
            print 'Hal is ' + str(pl_resolution(kb_list5, a58))
            ce_set = set()
            print 'Ida is ' + str(pl_resolution(kb_list5, a59))
            ce_set = set()
            print 'Jay is ' + str(pl_resolution(kb_list5, a510))
            ce_set = set()
            print 'Kay is ' + str(pl_resolution(kb_list5, a511))
            ce_set = set()
            print 'Lee is ' + str(pl_resolution(kb_list5, a512))
            ce_set = set()
        elif choose==6:
            print '(a)'
            print 'x is' + str(pl_resolution(kb_list62, a61))
            ce_set = set()
            print 'y is' + str(pl_resolution(kb_list62, a62))
            ce_set = set()
            print 'z is' + str(pl_resolution(kb_list62, a63))
            ce_set = set()
            print 'w is' + str(pl_resolution(kb_list62, a64))
            ce_set = set()
            print 'so he should choose door x'

            print '(b)'
            print 'x is' + str(pl_resolution(kb_list6, a61))
            ce_set = set()
            print 'y is' + str(pl_resolution(kb_list6, a62))
            ce_set = set()
            print 'z is' + str(pl_resolution(kb_list6, a63))
            ce_set = set()
            print 'w is' + str(pl_resolution(kb_list6, a64))
            ce_set = set()
            print 'so he have heard enough to choose door x'



