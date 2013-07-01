#coding:utf-8
import Tkinter as tk

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.createWidgets()
    def createWidgets(self):
        for i in range(NUMS):
            for j in range(NUMS):
                invars[(i,j)]=tk.StringVar()
                invars[(i,j)].set(' ')
                buttons[(i,j)]=tk.Button(self, textvariable=invars[(i,j)],
                    command=Press(i,j),width=4,height=2,borderwidth=1,background='#ffffff')
                buttons[(i,j)].grid(row=i,column=j)
                buttons[(i,j)].taken=''
        Application.label_values = tk.StringVar()
        Application.label_values.set('start')
        w = tk.Label(self, textvariable=Application.label_values)
        w.grid(row=NUMS+1,column=2)
        Press(NUMS/2,NUMS/2).sitedown('computer')
class Press:
    def __init__(self,row,column):
        self.row,self.column=row,column
    def sitedown(self,color):
        buttons[(self.row,self.column)].taken=color
        buttons[(self.row,self.column)].config(state=tk.DISABLED,background=colors[color])
        check_over()
    def __call__(self,next=True):
        self.sitedown('person')
        if next:
            self.row,self.column = compute()
            self.sitedown('computer')
        buttons[Press.last_position].config(background=colors['computer'])
        Press.last_position=(self.row,self.column)
        buttons[Press.last_position].config(background='#667788')
nearpos=((1,0),(1,1),(0,1),(-1,1))
def compute():
    bsites=[p for p,b in buttons.iteritems() if b.taken == '']
    bsites_values=[]
    for bpos in bsites:
        for step_pos in nearpos:
            value=0
            #buttons[npos].taken == 'computer'
            _space = 0
            for i in range(1,5):
                npos = _add(bpos,_mul(step_pos,i))
                if npos is None:
                    break
                if buttons[npos].taken == 'person':
                    break
                else:
                    _space += 1
            for i in range(1,5):
                npos = _add(bpos,_mul(step_pos,i*-1))
                if npos is None:
                    break
                if buttons[npos].taken == 'person':
                    break
                else:
                    _space += 1
            if _space < 4: #没有连续5个空位置 本纬度pass掉
                break
            #怎么量化可能性呢
            max_step = 1
            for i in (-4,-3,-2,-1,0):
                _t = 1
                npos = _add(bpos,_mul(step_pos,i))
                if npos is None:
                    continue
                for i in range(0,5):
                    npos = _add(npos,step_pos)
                    if npos is None:
                        break
                    if buttons[npos].taken == 'computer':
                        _t += 1
                if _t > max_step:
                    max_step = _t
            value = 10**(max_step-1)
            npos = _add(bpos,step_pos)
            if npos is not None :
                if buttons[npos].taken == 'computer':
                    value += 1
            npos = _add(bpos,_mul(step_pos,-1))
            if npos is not None :
                if buttons[npos].taken == 'computer':
                    value += 1 
                
            if value > 1:
                bsites_values.append((bpos,value))
    _maxvalue,_maxp=0,None
    for p,v in bsites_values:
        if v > _maxvalue:
            _maxvalue,_maxp = v,p
    assert not _maxp is None
    #debug
    for p,v in invars.iteritems():
        v.set('')
    for p,v in bsites_values:
        invars[p].set(str(v))
    return _maxp
def _mul(pos1,n):
    return (pos1[0]*n,pos1[1]*n)
def _add (pos1,pos2):
    npos = (pos1[0]+pos2[0],pos1[1]+pos2[1] )
    if npos[0] >= NUMS or npos[1] >= NUMS or npos[0] <0 or npos[1] <0:
        return None
    return npos
def check_over():
    #横线
    for rows in range(NUMS):
        step_compute,step_person=0,0
        for cols in range(NUMS):
            npos=(rows,cols)
            if buttons[npos].taken == 'computer':
                step_compute += 1
                step_person = 0
                invars[npos].set('c%d'%step_compute)
                if step_compute >= 5:
                    Application.label_values.set('c win')
            elif buttons[npos].taken == 'person':
                step_compute =0
                step_person += 1
                invars[npos].set('p%d'%step_person)
                if step_person >= 5:
                    Application.label_values.set('p win')
            else:
                step_compute,step_person=0,0
    #竖线
    for cols in range(NUMS):
        step_compute,step_person=0,0
        for rows in range(NUMS):
            npos=(rows,cols)
            if buttons[npos].taken == 'computer':
                step_compute += 1
                step_person = 0
                invars[npos].set('c%d'%step_compute)
                if step_compute >= 5:
                    Application.label_values.set('c win')
            elif buttons[npos].taken == 'person':
                step_compute =0
                step_person += 1
                invars[npos].set('p%d'%step_person)
                if step_person >= 5:
                    Application.label_values.set('p win')
            else:
                step_compute,step_person=0,0
    #上斜线
    for pos in [(row,0) for row in range(NUMS)] + [(NUMS-1,col) for col in range(NUMS)]:
        _step = (-1,1)
        n=0
        step_compute,step_person=0,0
        while 1:
            npos = _add(pos,_mul(_step,n))
            if npos is None :
                break
            if buttons[npos].taken == 'computer':
                step_compute += 1
                step_person = 0
                invars[npos].set('c%d'%step_compute)
                if step_compute >= 5:
                    Application.label_values.set('c win')
            elif buttons[npos].taken == 'person':
                step_compute =0
                step_person += 1
                invars[npos].set('p%d'%step_person)
                if step_person >= 5:
                    Application.label_values.set('p win')
            else:
                step_compute,step_person=0,0
            n += 1
    #下斜线
    for pos in [(row,0) for row in range(NUMS)] + [(0,col) for col in range(NUMS)]:
        _step = (1,1)
        n=0
        step_compute,step_person=0,0
        while 1:
            npos = _add(pos,_mul(_step,n))
            if npos is None :
                break
            if buttons[npos].taken == 'computer':
                step_compute += 1
                step_person = 0
                invars[npos].set('c%d'%step_compute)
                if step_compute >= 5:
                    Application.label_values.set('c win')
            elif buttons[npos].taken == 'person':
                step_compute =0
                step_person += 1
                invars[npos].set('p%d'%step_person)
                if step_person >= 5:
                    Application.label_values.set('p win')
            else:
                step_compute,step_person=0,0
            n += 1
NUMS=11    
buttons={}
invars={}

colors={'person':'#dddddd','computer':'#000000'}
Press.last_color = colors['person']
Press.last_position=(NUMS/2,NUMS/2)

if __name__ == '__main__': 
    app = Application()
    app.master.title('five step cheep')
    app.mainloop()
