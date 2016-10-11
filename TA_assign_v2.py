from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
from tkinter import messagebox


class Time:
    def __init__(self, hour = 0, minute = 0):
        self.time = (hour, minute)
    def __le__(self, x):
        return self.time[0] < x.time[0] or self.time[0] == x.time[0] and self.time[1] <= x.time[1]
    def __ge__(self, x):
        return self.time[0] > x.time[0] or self.time[0] == x.time[0] and self.time[1] >= x.time[1]
    def __repr__(self):
        if self.time[1] >= 10:
            return str(self.time[0]) + ':' +str(self.time[1])
        else:
            return str(self.time[0]) + ':0' +str(self.time[1])
    def dis(self, y):  #this method measures the distance between self and another time y.
        return 60*(self.time[0] - y.time[0]) + self.time[1] - y.time[1]

    
class Course:
    def __init__(self, cid, num, ctype = 'LEC', ccap = '0 OF 0'):
        self.cid = cid  # this is course id (type str)
        self.num = num  # this is course number (type int)
        self.ctype = ctype # this is course type, either 'LEC' or 'LAB'
        self.ccap = ccap  # this is course capacity
        self.ctime = tuple([list() for i in range(5)])  #this is course time, with five lists correspond to Monday to Friday respectively.
    def __repr__(self):
        days = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday')
        res = self.cid +' '+ self.ctype + '   ' + self.ccap + '\n'
        for i in range(5):
            if self.ctime[i]:
                temp = days[i] + ': ' + ', '.join(['%s - %s' % t for t in self.ctime[i]]) + '\n'
                res += temp
        return res
    '''The function update() add the lecture time in each weekday.
        The argument 'day' should be an integer in range(5) and 
        argument 'bt' should be a tuple of the form (starttime, endtime)'''    
    def update(self, day, bt):
        self.ctime[day].append(bt)


            
class Student:
    def __init__(self, name, sid, level = 'UnderGrad'):
        self.name = name  #this is student's name (type str)
        self.sid = int(sid)   #this is student's id number (type int)
        self.stime = tuple([list() for i in range(5)])  #this tuple records the time when the student is not available. The five lists correspond to Monday to Friday.
        self.course = []  #this list records the course id which the student will take.
        self.level = level  #this records whether the student is 'UnderGrad' or 'Grad'.
        self.ta = []  #this list records all the courses for which this student can be a TA.
    def __repr__(self):
        days = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday')
        res = self.name + ' (ID:' + str(self.sid) + ') ' + self.level + '\nHe/she can be TA for the following courses\n' + '\n'.join(self.ta) + '\nHe/She has class at:\n'
        for i in range(5):
            if self.stime[i]:
                temp = days[i] + ': ' + ', '.join(['%s - %s' % t for t in self.stime[i]]) + '\n'
                res += temp
        return res
    '''The function update() add the busy time in each weekday.
    The argument 'day' should be an integer in range(5) and 
    argument 'bt' should be a tuple of the form (starttime, endtime)'''
    def update(self, day, bt):
        self.stime[day].append(bt)

class Grad(Student):
    def __init__(self, name, sid):
        Student.__init__(self, name, sid, level = 'Grad')
        self.cou = dict()  #this dictionary records all the courses the student took, with the three digit course number as key and the grade as value. The course number maps to the grade.
        self.lan = '(Native speaker)'
        self.pl = set()  #this set records all the language this student is familiar with.
        self.note = ''  #this string records all the additional notes about this student.
    def __repr__(self):
        res = self.name + ' (ID:' + str(self.sid) + ') ' + self.level + ' ' + self.lan + '\n'
        if self.cou:
            for (n, g) in self.cou.items():
                res = res + str(n) + ' ' + g + ', '
            res = res + '\n'
        if self.pl:
            for l in self.pl:
                res = res + l + ', '
            res = res + '\n'
        res = res + self.note + '\nHe/she can be TA for the following courses\n' + '\n'.join(self.ta) + '\nHe/She has class at:\n'
        days = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday')
        for i in range(5):
            if self.stime[i]:
                temp = days[i] + ': ' + ', '.join(['%s - %s' % t for t in self.stime[i]]) + '\n'
                res += temp
        return res
        
        
        

dd = {'M' : 0, 'T' : 1, 'W' : 2, 'R': 3, 'F' : 4}
id_c = {} # course id maps to course instance
id_s6 = {} # student id number(string) of those who took CISC106 maps to student instance
id_s8 = {} # student id number(string) of those who took CISC108 maps to student instance
id_g = {} # graduate student id number(string) maps to grad instance
cid_s = {} # course id maps to the list of TA's id
sid_c = {} # student id maps to the list of courses' id which he/she can be a TA for
cr = {} # course number maps to a tuple of two frozensets, 
        # with the first set containing the three digit number of required courses
        # and the second set containing the reqired languages
        # the program will only assign TAs to the courses whose course number is a key in this dictionary.
        # so even if a course has no requirement, its course number should still be added to this dictionary.
        

# the following code is the initialization of the requirement dictionary 'cr'.
def f(v = []):
    return frozenset([i for i in v])
cr[101] = (f(), f())
cr[103] = (f(), f())
cr[105] = (f(), f())
cr[106] = (f(), f())
cr[108] = (f([108, 280, 481, 681]), f())
cr[181] = (f(), f())
cr[220] = (f(), f())
cr[250] = (f([450, 650]), f())
cr[260] = (f([662]), f())
cr[275] = (f([675]), f())
cr[280] = (f([681]), f())
cr[303] = (f([601]), f())
cr[304] = (f([604]), f())
cr[320] = (f([621]), f())
cr[355] = (f(), f())
cr[360] = (f([662]), f())
cr[361] = (f([663]), f())
cr[364] = (f([364, 464, 664, 864]), f())
cr[370] = (f(), f(['java']))
cr[372] = (f(), f(['mpi']))
cr[401] = (f([601]), f())
cr[601] = (f([601]), f())
cr[403] = (f([603]), f())
cr[603] = (f([603]), f())
cr[409] = (f([601]), f())
cr[414] = (f([614]), f())
cr[614] = (f([614]), f())
cr[429] = (f([621]), f())
cr[436] = (f([636, 841]), f())
cr[636] = (f([636, 841]), f())
cr[437] = (f([637]), f(['mysql']))
cr[637] = (f([637]), f(['mysql']))
cr[440] = (f([640]), f())
cr[640] = (f([640]), f())
cr[450] = (f([650]), f())
cr[451] = (f([451, 651]), f())
cr[651] = (f([451, 651]), f())
cr[459] = (f([659]), f())
cr[659] = (f([659]), f())
cr[471] = (f([672]), f())
cr[474] = (f(), f(['java', 'apache']))
cr[475] = (f([675]), f())
cr[675] = (f([675]), f())
cr[481] = (f([681]), f())
cr[681] = (f([681]), f())
cr[483] = (f([683]), f())
cr[683] = (f([683]), f())
cr[484] = (f([684]), f())
cr[684] = (f([684]), f())
cr[404] = (f([604]), f())
cr[604] = (f([604]), f())
cr[611] = (f([475, 675]), f())
cr[612] = (f([475, 675]), f())
cr[613] = (f([475, 675]), f())
cr[615] = (f([475, 675, 672]), f())
cr[621] = (f([621]), f())
cr[650] = (f([650]), f())
cr[662] = (f([662]), f())
cr[663] = (f([663]), f())
cr[672] = (f([672]), f())
cr[673] = (f([673, 872]), f())


'''
the following function convert a string denoting time to a tuple of two integers
for example, it will convert '1:23AM' to (1, 23) and '1:23PM' to (13, 23)
'''
def strtime(s):
    if s.index(':') == 1:
        if s[-2:].upper() == 'PM':
            return (int(s[0]) + 12, int(s[2:4]))
        else:
            return (int(s[0]), int(s[2:4]))
    if s.index(':') == 2:
        if int(s[:2]) == 12:
            if s[-2:].upper() == 'AM':
                return (0, int(s[3:5]))
            else:
                return (12, int(s[3:5]))
        elif s[-2:].upper() == 'PM':
            return (int(s[:2]) + 12, int(s[3:5]))
        else:
            return (int(s[:2]), int(s[3:5]))

#the following function returns the first index in string s which is a digit.
def indig(s):
    c = 0
    for i in s:
        if not i.isdigit():
            c += 1
        else:
            return c

#the following function returns the first index in string s which is an alphabet.
def inalp(s):
    c = 0
    for i in s:
        if not i.isalpha():
            c += 1
        else:
            return c



'''
The following function scans the courses information from text file. The result is the dictionary 'id_c' is populated.
the first argument 'addr' should be the address of the text file which contains the course information.
'''
def coursescan(addr, id_c, keys = cr.keys()):
    def ccap(p): # this function parses the capacity of the course from string 'p'. If no capacity info is detected, the program consider the course being cancelled.
        for s in p:
            if 'OF' in s and s.split()[0].isdigit():
                return s
        return ''
    def strins(p): # the string 'p' contains the full information of ONE course in the text file, and the function returns a tuple: (course id, course instance).
        dic = {}
        dic['cid'] = p[0].split()[0]
        dic['num'] = int(dic['cid'][4:7])
        if 'LAB' in p[0].upper():
            dic['ctype'] = 'LAB'
        dic['ccap'] = ccap(p)
        ins = Course(**dic)
        day = []
        time = []
        z = ['M', 'T', 'W', 'R', 'F', ' ']
        for s in p:
            if not s == '' and all(i in z for i in s):
                day.append(list(s.replace(' ', '')))
            if ':' in s and '-' in s:
                ss = s.replace(' ', '')
                j = ss.index(':')
                if ss[j-1].isdigit() and ss[j+1:j+3].isdigit():
                    m = ss.index('-')
                    l = indig(ss)
                    r = ss.upper().index('M', m)
                    st = Time(*strtime(ss[l:m]))
                    et = Time(*strtime(ss[m+1:r+1]))
                    time.append((st, et))
        lmin = min(len(time), len(day))
        for i in range(lmin):
            for d in day[i]:
                ins.update(dd[d], time[i])
        return (dic['cid'], ins)
    fset = frozenset(keys)
    patch = []
    boo = False # whether we are scaning a course which needs TA
    for line in (i.strip().split('\t') for i in open(addr)):
        if not boo and (len(line[0]) < 7 or line[0][:4] != 'CISC' or int(line[0][4:7]) not in fset):
            continue
        elif not boo: # if we found a new valid course
            boo = True
            patch = line[:]
        else: # if boo is True
            if len(line[0]) < 7 or line[0][:4] != 'CISC':  # if we have not met a new course
                patch.extend(line)
            else: # if we find a new course, which means 'patch' now contains full information of the previous course
                if ccap(patch): # whether the course is canceled
                    temp = strins(patch)
                    id_c[temp[0]] = temp[1]
                if int(line[0][4:7]) not in fset: # whether the new course needs TA
                    boo = False
                    patch = []
                else:
                    boo = True
                    patch = line[:]
    if patch and ccap(patch):
        temp = strins(patch)
        id_c[temp[0]] = temp[1]





'''
the following function scans the text file which contains the student's schedule. 
The result is the dictionary 'id_s6' or 'id_s8' or 'id_g' is populated.
the first argument 'addr' should be the address of the text file which contains the schedule of the students.
the second argument 'id_s' should be one of 'id_s6', 'id_s8' or 'id_g', depending on which type of students you are scanning.
if you are scanning graduate students, the third argument 'level' should be Grad, since graduate students are represented by class Grad.
'''
def studentscan(addr, id_s, level = Student):
    def strins(p, level):
        dic = {}
        dic['name'] = p[0]
        dic['sid'] = p[1]
        ins = level(**dic)
        z = ['M', 'T', 'W', 'R', 'F', ' ']
        day = []
        time = []
        for s in p:
            if len(s) > 7 and s[4:8].isdigit() and s[:4].isupper():
                ins.course.append(s)
                lmin = min(len(time), len(day))
                for i in range(lmin):
                    for d in day[i]:
                        ins.update(dd[d], time[i])
                day = []
                time = []
            if not s == '' and all(i in z for i in s):
                day.append(list(s.replace(' ', '')))
            if ':' in s and '-' in s:
                ss = s.replace(' ', '')
                j = ss.index(':')
                if ss[j-1].isdigit() and ss[j+1:j+3].isdigit():
                    m = ss.index('-')
                    l = indig(ss)
                    r = ss.upper().index('M', m)
                    st = Time(*strtime(ss[l:m]))
                    et = Time(*strtime(ss[m+1:r+1]))
                    time.append((st, et))
        lmin = min(len(time), len(day))
        for i in range(lmin):
            for d in day[i]:
                ins.update(dd[d], time[i])
        return (dic['sid'], ins)
    patch = []
    boo = False
    for line in (i.strip().split('\t') for i in open(addr)):
        t = ' '.join(line)
        if '(' in t and ')' in t:
            r = t.index(')')
            l = t.index('(')
            if r - l > 7 and t[l+1:r].isdigit():
                if boo:
                    temp = strins(patch, level)
                    id_s[temp[0]] = temp[1]
                patch = [t[:l].strip()]
                patch.append(t[l+1:r])
                boo = True
        else:
            patch.extend(line)
    if boo and patch:
        temp = strins(patch, level)
        id_s[temp[0]] = temp[1]



'''
the following function updates the background information of graduate students.
the first argument 'addr' should be the address of the text file which contains the background info of graduate students.
'''
def infoscan(addr, id_g = id_g):
    def strins(p):
        h = p[0]
        i = inalp(h)
        ids = h[:i].strip()
        if ids not in id_g.keys():           
            if '(' in h and ')' in h:
                j = h.index('(', i)
                k = h.index(')', j)
                temp = Grad(h[i:j], ids)
                temp.lan = h[j:k+1]
            else:
                temp = Grad(h[i:], ids)
        else:
            temp = id_g[ids]
            if '(' in h and ')' in h:
                j = h.index('(', i)
                k = h.index(')', j)
                temp.lan = h[j:k+1]
        if len(p) > 1 and p[1][:3].isdigit():
            dic = {}
            lis = p[1].split(',')
            for s in (t.strip() for t in lis):
                if s[:3].isdigit():
                    dic[int(s[:3])] = s[3:].lstrip()
            temp.cou = dic
        if len(p) > 2 and p[2][:4].upper() != 'NONE': # if no programming language for this student, the line should start with 'None'.
            lis = p[2].split(',')
            temp.pl = set(t.strip().lower() for t in lis)
        if len(p) > 3:
            temp.note = ' '.join(p[3:])
        return (ids, temp)
    patch = []
    boo = False
    c = 0
    for line in (i.strip() for i in open(addr)):
        if len(line) > 7 and line[:8].isdigit(): # ID number and name should be in a single line
            if boo:
                t = strins(patch)
                id_g[t[0]] = t[1]
                c += 1
            patch = [line, '']
            boo = True
        elif line[:3].isdigit() and len(patch) == 2: # Course grade can occupy multiple lines. Each line should start with course number.
            patch[1] = patch[1] + line + ','
        elif line:
            patch.append(line) # Programming languages should be in a single line. Notes can be multiple lines.
    if boo and patch:
        t = strins(patch)
        id_g[t[0]] = t[1]
        c += 1
    return c
            


'''
the following function check whether the time of course 'c' is in conflict with the schedule of student 's'.
the second argument 'offset' denotes the minimum number of minutes the course time should be apart from the student's unavailable time, the default value is 14 minutes.
'''
def nonconflict(c, s, offset = 14):
    for i in range(5):
        for ct in c.ctime[i]:
            for st in s.stime[i]:
                if ct[0].dis(st[1]) <= offset and st[0].dis(ct[1]) <= offset:
                    return False
    return True





class Datascan(Frame):
    def __init__(self, parent = None, typestr = None, title = ''):
        Frame.__init__(self, parent)
        self.address = ''
        self.l0 = Label(self, text = 'Choose the text file which contains\n' + typestr)
        self.l0.pack(pady = 70, side = TOP)
        self.l0.config(font = ('courier', 13, 'bold roman'))
        self.b0 = Button(self, text = 'Browse', font = ('helvetica', 15), bd = 7, relief = RAISED, height = 2, width = 9, command = self.browse)
        self.b0.pack()
        self.title = title
        
    def browse(self):
        self.address = askopenfilename(filetypes=[("Text files","*.txt")])
        if self.address != '':
            result = messagebox.askyesno(title = self.title, message = 'The selected file is\n' + self.address + '\n Is that correct?')
            if result:
                self.l0.destroy()
                self.b0.destroy()
                coursescan(self.address, id_c)
                l1 = Label(self, text = str(len(id_c.keys())) + ' courses have been scanned', font = ('courier', 15, 'bold roman'))
                l1.pack(side = TOP, pady = 80)
                b1 = Button(self, text = 'OK', font = ('helvetica', 15), bd = 7, relief = RAISED,  height = 2, width = 7, command = self.des)
                b1.pack()

    def des(self):
        main(self.master)
        self.destroy()

def main(p):
    tt = Frame(p)
    tt.pack(expand = YES, fill = BOTH)
    Button(tt, text = 'Undergraduate 106', command = lambda: under(p, '106'), bd = 7, relief = RAISED, font = ('helvetica', 15, 'bold')).pack(side = TOP, expand = YES, fill = BOTH)
    Button(tt, text = 'Undergraduate 108', command = lambda: under(p, '108'), bd = 7, relief = RAISED, font = ('helvetica', 15, 'bold')).pack(side = TOP, expand = YES, fill = BOTH)
    Button(tt, text = 'Graduate TA', command = lambda: grad0(p), bd = 7, relief = RAISED, font = ('helvetica', 15, 'bold')).pack(side = TOP, expand = YES, fill = BOTH)
    Button(tt, text = 'Student Search', command = lambda: search(p), bd = 7, relief = RAISED, font = ('helvetica', 15, 'bold')).pack(side = TOP, expand = YES, fill = BOTH)

def under(p = None, t = ''):
    u = Toplevel(p)
    u.geometry('700x400+300-300')
    u.resizable(False, False)
    u.title('UnderGrad '+ t)
    u.grab_set()
    fr = Frame(u)
    fr.pack(expand = YES, fill = BOTH)
    l0 = Label(fr, text = 'Choose the text file which contains the schedule of\nundergraudate who have taken CISC' + t)
    l0.pack(pady = 80, side = TOP)
    l0.config(font = ('courier', 13, 'bold roman'))
    b0 = Button(fr, text = 'Browse', font = ('helvetica', 15), bd = 7, relief = RAISED, height = 2, width = 9, command = lambda: under1(t, fr, u))
    b0.pack()
    
def under1(title = '', fr = None, parent = None):
    address = ''
    address = askopenfilename(parent = parent, filetypes = [("Text files","*.txt")])
    if address != '':
        result = messagebox.askyesno(parent = parent, title = 'UnderGrad' + title, message = 'The selected file is\n' + address + '\n Is that correct?')
        if result:            
            fr.destroy()
            if title == '106':
                id_sx = id_s6
            else:
                id_sx = id_s8
            studentscan(address, id_sx)
            fr1 = Frame(parent)
            fr1.pack(expand = YES, fill = BOTH)
            l1 = Label(fr1, text = str(len(id_sx.keys())) + ' students have been scanned.\nPlease save the assignment result.', font = ('courier', 15, 'bold roman'))
            l1.pack(side = TOP, pady = 80)
            b1 = Button(fr1, text = 'Save', font = ('helvetica', 15), bd = 7, relief = RAISED,  height = 2, width = 7, command = lambda: sav(res, parent))
            b1.pack()         
            ctemp = list()
            for key in sorted(id_c.keys()):
                if key[4:7] == title:
                    ctemp.append(key)
                    temp = list() # record the TA candidate
                    for hey in id_sx.keys():
                        if nonconflict(id_c[key], id_sx[hey]):
                            temp.append(hey)
                            id_sx[hey].ta.append(key)
                    cid_s[(key, title)] = temp
            res = 'The TA assignment for undergraduate who have taken CISC' + title + ':\n\n'
            for key in ctemp:
                res = res + '\n' + key + '\n'
                if (key, title) in cid_s.keys():
                    for i in cid_s[(key, title)]:
                        res = res + i + '  ' + id_sx[i].name + '\n'
            
def sav(res, parent = None):
    addr = ''
    addr = asksaveasfilename(defaultextension = '.txt',  filetypes = [('Text files','*.txt')])
    if addr:
        ff = open(addr, 'w')
        ff.write(res)
        ff.close()
        parent.destroy()

def grad0(p = None):
    u = Toplevel(p)
    u.geometry('700x400+300-300')
    u.resizable(False, False)
    u.title('Graduate Student')
    u.grab_set()
    fr = Frame(u)
    fr.pack(expand = YES, fill = BOTH)
    l0 = Label(fr, text = 'Choose the text file which contains\nthe schedule of graduate TAs')
    l0.pack(pady = 80, side = TOP)
    l0.config(font = ('courier', 13, 'bold roman'))
    b0 = Button(fr, text = 'Browse', font = ('helvetica', 15), bd = 7, relief = RAISED, height = 2, width = 9, command = lambda: gradsche(fr, u))
    b0.pack()

def gradsche(fr, parent = None):
    address = ''
    address = askopenfilename(parent = parent, filetypes = [("Text files","*.txt")])
    if address != '':
        result = messagebox.askyesno(parent = parent, title = "Graduate TAs' schedule", message = 'The selected file is\n' + address + '\n Is that correct?')
        if result:
            fr.destroy()
            studentscan(address, id_g, level = Grad)
            fr1 = Frame(parent)
            fr1.pack(expand = YES, fill = BOTH)
            l1 = Label(fr1, text = str(len(id_g.keys())) + ' graduate TAs have been scanned', font = ('courier', 15, 'bold roman'))
            l1.pack(side = TOP, pady = 80)
            b1 = Button(fr1, text = 'Next', font = ('helvetica', 15), bd = 7, relief = RAISED,  height = 2, width = 8, command = lambda: grad1(fr1, parent) )
            b1.pack()

def grad1(fr, parent = None):
    fr.destroy()
    fr2 = Frame(parent)
    fr2.pack(expand = YES, fill = BOTH)
    l2 = Label(fr2, text = 'Choose the text file which contains\nthe background information of graduate TAs')
    l2.pack(pady = 80, side = TOP)
    l2.config(font = ('courier', 13, 'bold roman'))
    b2 = Button(fr2, text = 'Browse', font = ('helvetica', 15), bd = 7, relief = RAISED, height = 2, width = 9, command = lambda: gradinfo(fr2, parent))
    b2.pack()

def gradinfo(fr, parent = None):
    address = ''
    address = askopenfilename(parent = parent, filetypes = [("Text files","*.txt")])
    if address != '':
        result = messagebox.askyesno(parent = parent, title = "Graduate TAs' background", message = 'The selected file is\n' + address + '\n Is that correct?')
        if result:
            fr.destroy()
            c = infoscan(address, id_g)
            for key in sorted(id_c.keys()):
                num = int(key[4:7])
                (cc, ll) = cr[num]
                if not cc and not ll:  #if this course has no requirement
                    temp = list()
                    for hey in id_g.keys():
                        sins = id_g[hey]
                        if nonconflict(id_c[key], sins):
                            temp.append((hey, ''))
                            sins.ta.append(key)
                else:  #if the course has requirement
                    temp = list()
                    for hey in id_g.keys():
                        sins = id_g[hey]             
                        if cc.intersection(sins.cou.keys()) or ll.intersection(sins.pl):
                            if nonconflict(id_c[key], sins):
                                com = ', '.join([str(c) + ' ' + sins.cou[c] for c in cc.intersection(sins.cou.keys())]) + ', ' + ', '.join([l for l in ll.intersection(sins.pl)])
                                temp.append((hey, com))
                                sins.ta.append(key)
                cid_s[key] = temp
            res = 'The TA assignment for graduate students:\n\n'
            for key in sorted(id_c.keys()):
                res = res + key + '\n'
                if key in cid_s.keys():
                    for i in cid_s[key]:
                        res = res + i[0] + ' ' + id_g[i[0]].name + ' ' + id_g[i[0]].lan + ' ' + i[1] + ' (' + str(len(id_g[i[0]].ta)) + ')' + '\n'
                res = res + '\n'
            fr3 = Frame(parent)
            fr3.pack(expand = YES, fill = BOTH)
            l3 = Label(fr3, text = str(c) + ' graduate TAs have been updated.\nPlease save the assignment result.', font = ('courier', 15, 'bold roman'))
            l3.pack(side = TOP, pady = 80)
            b3 = Button(fr3, text = 'Save', font = ('helvetica', 15), bd = 7, relief = RAISED,  height = 2, width = 7, command = lambda: sav(res, parent))
            b3.pack()    

class ScrolledText(Frame):
    def __init__(self, parent = None, text = ''):
        Frame.__init__(self, parent)
        self.pack(expand = YES, fill = BOTH)
        self.makewidget()
        self.settext(text)
    def makewidget(self):
        sbar = Scrollbar(self)
        text = Text(self, relief=SUNKEN, bg = 'light grey')
        sbar.config(command=text.yview) 
        text.config(yscrollcommand=sbar.set)
        sbar.pack(side=RIGHT, fill=Y) 
        text.pack(side=LEFT, expand=YES, fill=BOTH) 
        self.text = text
    def settext(self, text):
        self.text.config(state = NORMAL)
        self.text.delete('1.0', END) 
        self.text.insert('1.0', text)
        self.text.config(state = DISABLED)
        

def search(parent = None):
    u = Toplevel(parent)
    u.geometry('800x500+100-100')
    u.minsize(800, 500)
    u.title('Search')
    l0 = Label(u, text = 'Input the Student ID Number')
    l0.config(font = ('courier', 13, 'bold roman'))
    l0.pack(fill = X, pady = 5)
    fr = Frame(u)
    fr.pack(fill = BOTH)
    ent = Entry(fr, font = ('helvetica', 15))
    b0 = Button(fr, text = 'Search', font = ('helvetica', 9), bd = 3, relief = RAISED, width = 7, command = lambda: info(ent.get(), ss))
    b0.pack(side = RIGHT, padx = (5, 220), pady = 15)
    ent.bind('<Return>', lambda event: info(ent.get(), ss))
    ent.pack(padx = (220, 5), pady = 15)
    ent.focus()
    ss = ScrolledText(u)
    
def info(s, ss):
    res = 'Student can not be found.'
    s = s.strip()
    if s.isdigit():
        if s in id_g.keys():
            res = str(id_g[s])
        elif s in id_s6.keys():
            res = str(id_s6[s])
        elif s in id_s8.keys():
            res = str(id_s8[s])
    ss.settext(res)

root = Tk()
root.title('TA Assignment')
root.geometry('700x400+300-300')
root.resizable(False, False)
a = Datascan(root, title = 'Course Scan', typestr ='the courses to which TAs are to be assigned')
a.pack(expand = YES, fill = BOTH)

root.mainloop()