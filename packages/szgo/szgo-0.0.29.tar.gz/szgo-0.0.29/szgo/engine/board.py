import random,copy

import datetime
       

# https://thepythonguru.com/python-regular-expression/
import re
from pprint import pprint



class Board:
    def __init__(self, boardlist=[]):

        # 如果沒有給定任何預設的盤面，那就是盤上沒有任何子
        if not boardlist:
            boardlist = []
            for y in range(0, 361):
                boardlist.append(0)

        self.boardlist = boardlist
        self.BOARDSIZE = 19
        self.BlackGrp = []
        self.WhiteGrp = []
        self.counter = 0  # current, after first move it will be 1
        self.next = 1  # Black, 2:White
        self.captured = []  # captured[1]:Black captured White

        self.captured.append(0)
        self.captured.append(0)
        self.captured.append(0)
        self.moveList = []
        self.removedList = []
        self.passcnt =0

        self.isKo = False  # KO
        self.hotpoint = None  # KO

        # self.next = 'B'

        self.show1()

        self.cmd()


    # get x, y from pi
    def xy(self,i):
        y = i // self.BOARDSIZE
        x = i - self.BOARDSIZE*y
        return x, y       

    # get pi from x,y
    def pi(self,x, y):
        return x + 19*y      

    #
    # input: 0-360 in list
    #
    def t19grp(self,grp):
        temp =''
        for p in grp:
            temp += self.t19(p)+"-"
        return temp[:-1]

    def getStoneList(self,color):
        stonelist =[]
        for p in range(361):
            if self.boardlist[p] == color:
                stonelist.append(p)
        return stonelist

    def isInListList(self,p,ll):
        for k1 in ll:
            if p in k1:
                return True
        return False

    def updateGrp(self):
        print("All Black Groups")
        print(self.getAllGrpList(1))
        print("\nAll White Groups")
        print(self.getAllGrpList(2))


    def getAllGrpList(self,color):
        bstonelist = self.getStoneList(color)
        bgrp = []
        blib = []
        for p in bstonelist:
            # print(p)
            if self.isInListList(p,bgrp):
                # print ("got you", p)
                continue
            grp = self.getGrpList(p)
            lib = self.getLibList(grp)
            # print(grp)
            bgrp.append(grp)
            blib.append(lib)
            # print("where went wrong? ",bgrp,blib)
        return bgrp,blib

        




        # grp = self.getGrpList(21)
        # print(self.t19grp(grp))
        # lib = self.getLibList(grp)
        # print(self.t19grp(lib))
        # https://stackoverflow.com/questions/8528178/list-of-zeros-in-python
        # bboard = [0]*361

        # https://docs.python.org/3.6/library/copy.html#copy.deepcopy
        # bboard = copy.deepcopy(self.boardlist)
        # wboard = copy.deepcopy(self.boardlist)

        
        # print("B:")
        # for p in range(361):
        #     if bboard[p] == 1:
        #         print (p,self.t19(p) )
        #         grp =self.getGrpList(p)
        #         print(grp)
        
        #         for done in grp:
        #             bboard[done] == -1 
            
        # print("\nW:")
        # for p in range(361):
        #     if wboard[p] == 2:
        #         print (p,self.t19(p) )
            
            
            

    # for any given pi
    # get Group List 
    # if can be any color
    # including empty
    def getGrpList(self,pi): # for 0,1,2
        grp = [pi]
        color = self.boardlist[pi] 

        # 這段比傳統的寫法要好，因為新加入的成員，待會立即可以用來擴展
        for pi in grp:
            x,y = self.xy(pi)
            if x+1 <=18 and self.stone(x+1,y) == color and not self.pi(x+1,y) in grp:
                grp.append(self.pi(x+1,y))
                
            if y+1 <=18 and self.stone(x,y+1) == color and not self.pi(x,y+1) in grp:
                grp.append(self.pi(x,y+1))
            
            if x-1 >= 0 and self.stone(x-1,y) == color and not self.pi(x-1,y) in grp:
                grp.append(self.pi(x-1,y))
            
            if y-1 >= 0 and self.stone(x,y-1) == color and not self.pi(x,y-1) in grp:
                grp.append(self.pi(x,y-1))
        return grp
        




    # for stone grp only    
    def getLibList(self,grp):
        lib = set()
        
        def isEmpty(x, y):

            if x < 0 or x > 18 or y < 0 or y > 18:
                return False  # out of board
            if self.boardlist[x+19*y] == 0:
                return True
            return False
        
        for pi in grp:
            x,y = self.xy(pi)
            if isEmpty(x+1, y):
                lib.add(self.pi(x+1,y))
            if isEmpty(x-1, y):
                lib.add(self.pi(x-1,y))
            if isEmpty(x, y+1):
                lib.add(self.pi(x,y+1))
            if isEmpty(x, y-1):
                lib.add(self.pi(x,y-1))
        return list(lib)   

    # for empty grp only
    # surrounding list
    def getSurList(self,grp):
        lib = set()
        
        def isStone(x, y):

            if x < 0 or x > 18 or y < 0 or y > 18:
                return False  # out of board
            if self.boardlist[x+19*y] > 0:
                return True
            return False
        
        for pi in grp:
            x,y = self.xy(pi)
            if isStone(x+1, y):
                lib.add(self.pi(x+1,y))
            if isStone(x-1, y):
                lib.add(self.pi(x-1,y))
            if isStone(x, y+1):
                lib.add(self.pi(x,y+1))
            if isStone(x, y-1):
                lib.add(self.pi(x,y-1))
        return list(lib)   




    # TODO 已經放到 getGrpList
    def xxxgetGrpListCore(self,grp,color): # for 0,1,2
        for pi in grp:
            x,y = self.xy(pi)
            if x+1 <=18 and self.stone(x+1,y) == color and not self.pi(x+1,y) in grp:
                grp.append(self.pi(x+1,y))
                
            if y+1 <=18 and self.stone(x,y+1) == color and not self.pi(x,y+1) in grp:
                grp.append(self.pi(x,y+1))
             
            if x-1 >= 0 and self.stone(x-1,y) == color and not self.pi(x-1,y) in grp:
                grp.append(self.pi(x-1,y))
             
            if y-1 >= 0 and self.stone(x,y-1) == color and not self.pi(x,y-1) in grp:
              grp.append(self.pi(x,y-1))
             

        
        return grp


    def xxxgetGrpSet(self,seed):
        set2 =copy.deepcopy(seed)
        localSeed = seed
        pi = seed.pop()
        color = self.boardlist[pi] # 0,1,2

        isExpanding = True
        while isExpanding:
            # pi
            x,y = self.xy(pi)

            isNoExpand = True
            if x+1 <=18 and self.stone(x+1,y) == color:
                set2.add(self.pi(x+1,y))
                isNoExpand = False
                
            if y+1 <=18 and self.stone(x,y+1) == color:
                set2.add(self.pi(x,y+1))
                isNoExpand = False
            
            if x-1 >= 0 and self.stone(x-1,y) == color:
                set2.add(self.pi(x-1,y))
                isNoExpand = False
            
            if y-1 >= 0 and self.stone(x-1,y) == color:
                set2.add(self.pi(x-1,y))
                isNoExpand = False
            
        print(set2)
        # if (len(grp) > 1):
        #     self.getSubGrpSet(grp,color)
        # print(len(grp))
    


      
    def xxxgetSubGrpSet(self,grp,color):
        for pi in grp:
            x,y = self.xy(pi)
            if x+1 <=18 and self.stone(x+1,y) == color:
                grp.append(self.pi(x+1,y))
            if y+1 <=18 and self.stone(x,y+1) == color:
                grp.append(self.pi(x,y+1))
            if x-1 >= 0 and self.stone(x-1,y) == color:
                grp.append(self.pi(x-1,y))
            if y-1 >= 0 and self.stone(x-1,y) == color:
                grp.append(self.pi(x-1,y))
                
    


    def changePlayer(self):
        if self.next == 1:
            self.next = 2
        else:
            self.next = 1
        return

    def showWarning(self, str):
       
        return
        print()
        print("  xxx Warning! xxx ", str)
        print()
        # self.sho

    def debug(self, obj):
        

        print("--- debug ---")
        print( obj)
        # print("--- debug ---")
        # self.sho

    
    
    # self contain logic 
    def playOneMove(self, pi):  # pi 0-360

        # Board range check, out of 19*19
        # 棋盤範圍
        if pi < 0 or pi > 360:
            return False

        # Hello World!
        # Never put your stone on your one eye
        # Doing
        if self.isPlayerOneEye(pi):
            self.showWarning('不可自填單空眼位！！！')
            return False
        
        # 禁著
        # 1) 有子是明顯可以判斷可不可以下。

        # self.debug ("suicide ...")

        if self.boardlist[pi] > 0:
            self.showWarning('有子禁著！')
            return False

        # 先下當前的顏色的子



        def putOneStone( pi):
            # print("putOneStone ", pi, self.t19(pi))
                # 劫的熱點不能下

            #

            #
            #  真正下一顆子
            self.boardlist[pi] = self.next

            # 確定對方的顏色 是黑或是白
            oppo = self.opponentColor()

            # 讀取對方每塊棋的氣數
            # grps
            # libs
            # 在 grps 的序列，映對 libs
            # grps, libs = self.getGrpV2(oppo)
            grps, libs = self.getAllGrpList(oppo)
            # print(grps)
            # print(libs)




            # print (grps, libs)
            # grps =[]
            # libs =[]
            x,y = self.xy(pi)
            
            # 只看落子時對上下左右四塊棋的影響

            # if x+1 <=18 and self.boardlist[self.pi(x+1,y)]== oppo:
            #     grps.append(self.getGrpList(self.pi(x+1,y)))
            # if y+1 <=18 and self.boardlist[self.pi(x,y+1)]== oppo:
            #     grps.append(self.getGrpList(self.pi(x,y+1)))
            # if x-1 >=0 and self.boardlist[self.pi(x-1,y)]== oppo:
            #     grps.append(self.getGrpList(self.pi(x-1,y)))
            # if y-1 >=0 and self.boardlist[self.pi(x,y-1)]== oppo:
            #     grps.append(self.getGrpList(self.pi(x,y-1)))
                
            # if grps:
            #     self.show1()
            #     print(grps)
            #     print("capturing is not complete!")
            #     # exit()影響到的對方的棋
            # # if  grps:
            # if  False:
            #     self.show1()
            #     print(self.getT19ByPiList(grps))
            #     print("可能殺到對方。。。")
            #     input ("anykey to continue...")
            
            # 如上記住當前處理的序列
            k = 0
            # 這手棋的提子數
            removedSum = 0
            removedList =[]

        
            for lib in libs:
                # 當某塊棋的外氣為 0 時
                if len(lib) == 0:
                    # self.show1()
                    # print ("是否沒有氣了？",grps[k])
                    # 提子，提的是這塊棋
                    for p in grps[k]:

                        # 處理提子的動作，一顆一顆
                        # dead = p[0]+19*p[1]
                
                        # print("removed is ",self.t19(p))
                        self.boardlist[p] = 0
                        removedList.append({1+self.counter:p})
                        removedSum = 1 + removedSum
                k = 1 + k

            if removedSum:
                self.captured[self.next] = self.captured[self.next] + removedSum
                # print("current move is ",self.t19(pi))
                # print("removedSum=",removedSum)
                # print(" self.captured[self.next]", self.captured[self.next])
                # print("removedList=",removedList)
                
  
                # 只要有吃子，不必考慮是否自殺
                # print("This move capturing ", removedSum)

                # 只吃子一子時，對方不能立即下在這裡，稱之為hot
                if removedSum == 1:

                    if self.isKo and move == self.hotpoint:
                        self.showWarning("劫，不能在這手下。")
                        # print ("要rollback")
                        self.boardlist[move] = 0
                        self.boardlist[self.hotpoint] = self.opponentColor
                        return False

                    # TODO 剛下的單子提子後的氣為1，就是劫，
                    self.isKo = True  # 不是嚴格定義，但是夠用，

                    self.hotpoint = pi
                    # return True

            else:

                # 2）自殺禁著
                # 沒有吃子，要檢查是否自殺棋
                #
                # 雖然一開始在左上角單眼測試對方不能投入，但自動對局裡出理有兩子的 suicide
                #

                # TODO 要有一個功能針對某一子，查其 grp and lib
                #      目前先套用全局的

                # grps, libs = self.getGrpV2(self.next)
                grps, libs = self.getAllGrpList(self.next)
                

                for lib in libs:

                    # 沒有吃子，但是自己緊氣氣絕
                    if len(lib) == 0:
                        self.showWarning("出現自殺棋 ")

                        # 棋盤要還原，當做沒下過
                        self.boardlist[pi] = 0
                        return False

            # 只要一手過後，劫就消失
            # TODO：要查看2，3，4 劫的規定
            #
            self.isKo = False
            self.counter = self.counter + 1
            
            # TODO to find a bug
            if removedList:
                self.removedList.append({self.counter:removedList})
            
            self.changePlayer()
            self.moveList.append(pi)
            # if removedSum > 0:
                # self.show1()
                # input ("有吃子，。。。。")

            # 只要有走棋，
            self.passcnt = 0
            return True





        if putOneStone(pi):
            return True

        return False


   
    def isValidMove(self, cmd):
        XSTR = 'ABCDEFGHJKLMNOPQRST'
        # 接受盤 A1  to T19, not including I1-I19
        if len(cmd) > 3:
            return False

        #
        x = cmd[0].upper()
        x2 = XSTR.find(x)
        if x2 == -1:
            msg = x+' is not in '+XSTR
            # self.showWarning(msg)
            return False

        y = cmd[1:]
        try:
            y2 = int(y)
        except:
            msg = y2 + " must be 1 to 19. It's not number."
            self.showWarning(msg)
            return False

        if y2 < 1 or y2 > 19:
            msg = " Move must be 1 to 19. It's not in range."
            self.showWarning(msg)
            return False
        y2 = 19 - y2

        pi = x2 + 19*y2  # position index
        # print( x2, y2,pi)

        # 禁著
        # 1) 有子
        if self.boardlist[pi] > 0:
            self.showWarning('有子禁著！')
            return False
        # 2) 自殺

        # if self.play(pi):
     
        if self.playOneMove(pi):
            
            pass

        else:
            # need to roll back to previous status
            pass
            return False

        return True

    def opponentColor(self):
        if self.next == 1:
            return 2
        return 1

  
    def xxxplay(self, move):

            # 劫的熱點不能下

        #

        #
        #
        self.boardlist[move] = self.next
        # self.isKo = False

        # 吃子數為何？如果沒有吃子，要考慮有沒有自殺
        # print("who's playing?", self.next)
        oppo = self.opponentColor()
        # print("who's opponent?", oppo)

        grps, libs = self.getGrpV2(oppo)
        # print('xxxxx',grps,libs)

        k = 0
        removedSum = 0
        pi = None
        for lib in libs:
            # print("氣",lib,len(lib))
            if len(lib) == 0:
                # print ("going to remove ", grps[k])
                for p in grps[k]:
                    # print ("what is p now?",p)
                    pi = p[0]+19*p[1]
                    self.boardlist[pi] = 0
                    removedSum = 1 + removedSum
            k = 1 + k
        if removedSum:
            # 只要有吃子，不必考慮是否自殺
            # print("This move capturing ", removedSum)

            # 只吃子一子時，對方不能立即下在這裡，稱之為hot
            if removedSum == 1:

                if self.isKo and move == self.hotpoint:
                    self.showWarning("劫，不能在這手下。")
                    # print ("要rollback")
                    self.boardlist[move] = 0
                    self.boardlist[self.hotpoint] = self.opponentColor
                    return False

                # TODO 剛下的單子提子後的氣為1，就是劫，
                self.isKo = True  # 不是嚴格定義，但是夠用，

                self.hotpoint = pi
                return True

        else:

            # 只要有吃子，不必考慮是否自殺
            grps, libs = self.getGrpV2(self.next)
        # print('xxxxx',grps,libs)

            # k = 0
            # k = 0
            # suicideSum = 0
            for lib in libs:
                # print("氣",lib,len(lib))
                if len(lib) == 0:
                    self.showWarning("出現自殺棋 ")
                    # 當做沒下過
                    self.boardlist[move] = 0
                    return False

        # grps1, libs1 = self.getGrpV2(1)
        # grps2, libs2 = self.getGrpV2(2)

        self.isKo = False
        return True


    # https://en.wikibooks.org/wiki/Computer_Go/Tromp-Taylor_Rules

    # 一開始先以任意的點去下
    # 為了要解決結局
    # 要判斷出所有的點都試過
    # 任一方無法落子時 Pass
    # 另一方繼續下
    # 一直到雙方都 Pass
    # 這時盤面上都只有多處的單眼
    # ***或是兩塊不完全相連的雙眼
    # 採中國式的盤面計點法決定勝負
    #
    def autoX(self, AUTO_NUM):
        cnt = 0

        # TODO
  
        # random.seed(999)
        random.seed(1001)
        
        while True:
            pi = random.randint(0, 360)
           
            # 有效落子才算一手
            if self.playOneMove(pi):
                cnt = 1 + cnt
                # 有效的落子，顯示盤面
                self.show1()
                if cnt >= AUTO_NUM:
                    break
                
            # 要設計另一個沒有地方下的出口
            else:
                if self.counter > 300: # TODO 先以300
                    print("TODO ... 要開始有計畫逐點檢查")
                    emptylist = self.getEmptyList()
                    possible = len(emptylist)
                    # print("possible:",len(emptylist),emptylist)
                    # https://www.tutorialspoint.com/python3/list_remove.htm
                    working = False
                    while possible >0:
                        print(possible, end = ' ')
                        # https://docs.python.org/3/library/random.html
                        rnd = random.randint(0, possible-1) # randing(0,3): {0,1,2}
                        # print("rnd:",rnd)
                        
                        p2 = emptylist[rnd]
                        # print(p2)
                        # print(p2.items())
                        # https://stackoverflow.com/questions/17322668/typeerror-dict-keys-object-does-not-support-indexing
                        key = list(p2.keys())[0]
                        # print(key)
                        # input (" have a look on items and key")
                        if self.playOneMove(key):
                            cnt = 1 + cnt
                             # 有效的落子，顯示盤面
                            self.show1()
                            working = True
                            break
                        else:
                            # print (p2 , "不能下，拿掉")
                            emptylist.remove(p2)
                            possible = len(emptylist)
                            # print("possible:",len(emptylist),emptylist)
                            # exit()
                            
                    if working:        
                        pass # 繼續
                    else:
                        self.passcnt += 1 # PASS
                        self.changePlayer()
                        self.moveList.append(-1)
                        self.counter += 1
                        self.show1()
                        if self.passcnt == 2:
                            # self.show1()
                            print (end ='  ')
                            print("----------")
                            print (end ='  ')
                            print("Game Over!")
                            print (end ='  ')
                            print("----------")
                            data = self.endGameCount()
                            print (end ='  ')
                            print("B: "+ str(data['bstone']), end=' + ')
                            print(str(data['beye']), end=' = ')
                            print(str(data['bsum']))
                            print (end ='  ')
                            print("W: "+ str(data['wstone']), end=' + ')
                            print(str(data['weye']), end=' = ')
                            print(data['wsum'])
                            print ('\n',end ='  ')
                            if data['result'] > 0:
                                print ("BLACK WON ", end ='' )
                            else:
                                print ("WHITE WON ", end ='' )
                                
                            print(abs(data['result']))
                            print()
                            
                            return

    def endGameCount(self):

        def getOwner(p):
            x,y = self.xy(p)
            if x + 1 <= 18:
                return self.boardlist[self.pi( x+1, y)]
            if x - 1 >= 0:
                return self.boardlist[self.pi( x-1, y)]
            if y + 1 <= 18:
                return self.boardlist[self.pi( x, y+1)]
            if y - 1 >= 0:
                return self.boardlist[self.pi( x, y-1)]
                


        bstone = 0
        beye = 0
        wstone = 0
        weye = 0
        i = 0
        for p in self.boardlist:
            if p == 1:
                bstone += 1
            if p == 2:
                wstone += 1
            if p == 0:
                if getOwner(i) == 1:
                    beye += 1
                if getOwner(i) == 2:
                    weye += 1
            i += 1
        bsum = bstone+beye
        wsum = wstone+weye
        result = bsum - wsum 
        return {'bstone':bstone,'beye':beye,'bsum':bsum,'wstone':wstone,'weye':weye,'wsum':wsum,'result':result}
             

            


    
    def getEmptyList(self):
        list1 = []
        for p in range(361):
            if self.boardlist[p] == 0:
                list1.append({p:0})
        return list1

    def import1(self):
        # https://www.w3schools.com/python/python_file_open.asp
        filename = "output/test1.sgf"
        # f = open(filename, "r")
        # print(f.read())

        # 
        seq = []
        with open(filename) as f:
            collection = sgf.parse(f.read())
        
        

            # https://github.com/twoutlook/sgf
            print('collection len',len(collection))
            for x in collection[0]:
                # print(x)
                k =0
                # for attr, value in vars(x).items():
                #     k += 1
                #     print(k," ", attr, '=', value)
                    # print(attr.parent)
           
                # print("===============")
                # pprint(vars(x))  #https://stackoverflow.com/questions/192109/is-there-a-built-in-function-to-print-all-the-current-properties-and-values-of-a
                
                # print("...")
                # pprint(x)
                # pprint(vars(x)['properties'])
                prop = vars(x)['properties']
                # print(prop)
                # b = prop['B']
                # pprint(type(prop))
               
                for z in prop:
                    # print(z, end=':')
                    # print(prop[z])
                    if z in ['B','W']:
                        for z2 in prop[z]:
                            # print(z,z2)
                            seq.append(z2)
        print(seq)
        strSS='abcdefghijklmnopqrs'
        # https://stackoverflow.com/questions/2294493/how-to-get-the-position-of-a-character-in-python/2294502
        def p(x,y):
            return x+19*y
           
        for ss in seq:
            # print(ss)
            x=strSS.find(ss[0])
            y=strSS.find(ss[1])
            # print(x,y)
            self.playOneMove(p(x,y))
            self.show1()
            # input("... presss any key to continue")

        # https://stackoverflow.com/questions/25150955/python-iterating-through-object-attributes
        # for attr, value in collection.__dict__.items():
        #     print("attr",attr)
        #     print("value", value)

  



    def cmd(self):
        while True:
            if self.next == 1:
                next = 'B'
            else:
                next = 'W'

            cmd = input("  go("+next+")? ")
            cmdxxx ="xxx"+str(cmd)+"xxx"
            if cmdxxx == 'xxxxxx':
                # print("xxxxxx???")
                continue
                    
            
            if cmd in {'exit', 'quit', 'done'}:
                exit()

        
            if True:
                cmd = str(cmd)
                cmd = cmd.lower()
                if cmd == 'status':
                    self.status()
                
                    continue
                if cmd == 'grp1':
                    self.updateGrp()
                    continue
                if cmd == 'test':
                    grp = self.getGrpList(0)
                    

                    lib = self.getLibList(grp)
                    print(len(grp))
                    self.showGrpT19(grp)
                    self.showGrpT19(lib)

                    continue

                if cmd == 'import1':
                    
                    self.import1()
                    continue

                if cmd == 'test2':
                    def p(x,y):
                        return x+19*y
                    self.playOneMove(p(1,0))
                    self.playOneMove(p(2,0))
                    self.playOneMove(p(1,1))
                    self.playOneMove(p(2,1))
                    self.playOneMove(p(0,1))
                    self.playOneMove(p(0,2))
                    self.show1()
                    continue

                if cmd == 'test3':
                    def p(x,y):
                        return x+19*y
                    self.playOneMove(p(1,0))
                    self.playOneMove(p(2,0))
                    self.playOneMove(p(1,1))
                    self.playOneMove(p(2,1))
                    self.playOneMove(p(0,1))
                    self.playOneMove(p(0,2))
                    self.show1()
                    print("suicide not detected!")
                    continue

                if cmd == 'show':
                    self.show1()
                    continue

                if cmd == 'bgrp':
                    grps, libs = self.getGrpV2(1)
                    print("--- Black's groups and libs ---")
                    print(grps, libs)
                    continue
                if cmd == 'wgrp':
                    grps, libs = self.getGrpV2(2)
                    print("--- Write's groups and libs ---")
                    print(grps, libs)
                    continue

               

                if cmd == 'output':
                    # print("--- going to output sgf file ---")
                    self.output()
                    continue

                if cmd == 'auto':
                    # print("TODO ...going to auto play ")
                    self.autoX(426)
                    continue
                if cmd == '1':
                    # print("TODO ...going to auto play ")
                    self.autoX(1)
                    continue
                if cmd == '10':
                    # print("TODO ...going to auto play ")
                    self.autoX(10)
                    continue
            
            
            if self.isValidMove(cmd):
                # self.changePlayer()
                self.show1()
                if self.isKo:
                    print("possible KO alert")
            else:    
                print("  go >>> Move is not valid. Please try again!\n  ")
    #  print("  go >>> Move is not valid. Please try again!\n    (Hint: A1 to T19, not including I1 to I19)")

    def output(self):
        ss = 'abcdefghijklmnopqrs'
        # sgf = "(;GM[1]FF[4]CA[UTF-8]AP[kunshanGo]ST[1]SZ[19]HA[0]KM[0]PW[ksGO]WR[30k]PB[ksGO]BR[30k]DT[2019-02-22]PC[KunshanGo]"
        sgf = "(;GM[1]FF[4]CA[UTF-8]AP[kunshanGo]ST[1]SZ[19]HA[0]KM[0]PW[ksGO]WR[30k]PB[ksGO]BR[30k]DT[2019-02-22]PC[KunshanGo]"
        sgf.replace("DT[2019-02-22]", datetime.datetime.now().isoformat())
        
        print(self.moveList)
        cnt = 0
        stone = 'B'
        for move in self.moveList:
            cnt = cnt + 1


            if move == -1: # PASS
                str1 = ';'+stone+'[]'
                str2 ='C['+str(cnt)+' PASS]'
           
            else:
                if cnt % 2 == 1:
                    stone = 'B'
                else:
                    stone = 'W'
                x = move % 19
                y = move // 19
                ssx = ss[x]
                ssy = ss[y]
                str1 = ';'+stone+'['+ssx+ssy+']'
                
                # https://www.red-bean.com/sgf/user_guide/index.html#move_vs_place
                # show game info here
                if cnt == 1:
                    str2 ='C['+str(cnt)+"  KunshanGo autoplay,"+datetime.datetime.now().isoformat()+"]"
                else:
                    str2 ='C['+str(cnt)+']'
            sgf += str1+str2
        sgf += ')'
        # print(sgf)
        filename = "output.sgf"
        text_file = open(filename, "w")
        text_file.write(sgf)
        text_file.close()
        print("Please check file:", filename)
        # print(cnt,stone,ssx,ssy,move, x, y)

    def show(self, style):
        if style == 0:
            return self.show0()
        if style == 1:
            return self.show1()

    def show0(self):
        # print('doing show0')
        # print(len(self.boardlist))

        for y in self.boardlist:
            print(y, end='')
        print()

    # def xy(self, x, y):
    #     return self.boardlist[x + 19*y]

    def status(self):
        print(self.getGrpV2(1))
        print(self.getGrpV2(2))
        print(self.removedList)
        print()

    def playSgfStyle(self, move):

        dict = {
            'a': 1,
            'b': 2,
            'c': 3,
            'd': 4,
            'e': 5,
            'f': 6,
            'g': 7,
            'h': 8,
            'i': 9,
            'j': 10,
            'k': 11,
            'l': 12,
            'm': 13,
            'n': 14,
            'o': 15,
            'p': 16,
            'q': 17,
            'r': 18,
            's': 19,
        }
        color = move[0]
        x = dict[move[2]]
        y = dict[move[3]]

        if color == 'B':
            self.boardlist[(x-1)+(y-1)*self.BOARDSIZE] = 1
        if color == 'W':
            self.boardlist[(x-1)+(y-1)*self.BOARDSIZE] = 2

    # 在有子的部份，先確認完全連接的，準備算氣

    def getT19ByPiList(self, grps):
        ruler = 'ABCDEFGHJKLMNOPQRST'
        res = " "
        for grp in grps:
            for pi in grp:
                x,y = self.xy(pi)
                res += ruler[x]+str(1+y)+""
            res += ","
        return res

    
    def showGrpT19(self, grp):
        ruler = 'ABCDEFGHJKLMNOPQRST'
        res =""
        for pi in grp:
            x,y = self.xy(pi)
            res += ruler[x]+str(18-y)+"-"
        res = res[:-1]
        res ={ res:len(grp)}
        print (res)

    
    def getT19String(self, grp):
        ruler = 'ABCDEFGHJKLMNOPQRST'
        res = "'"
        for x in grp:
            res += ruler[x[0]]+str(19-x[1])+"-"
        # res += "'"
        return res[:-1]+ "'"

    # set , pop
    def getT19StringForSet(self, grp):
        ruler = 'ABCDEFGHJKLMNOPQRST'
        res = "'"
        # for x in grp:
        while True:
            x = grp.pop()
            if not x:
                break
            print("debug x is ", x)
            # res += ruler[x[0]]+str(18-x[1])+""
        
        return res[:-1]+ "'"



    def t19(self, pi):
        if (pi == -1):
            return 'PASS'
        x,y = self.xy(pi)
        ruler = 'ABCDEFGHJKLMNOPQRST'
        temp = ruler[x]+str(19-y)
        
        return temp


    def isPlayerOneEye(self, pi):
        # print("when to check isPlayerOneEye",self.counter)
        def isConnected(p1, p2):
            if abs(p1[0]-p2[0])+abs(p1[1]-p2[1]) == 1:
                return True
            return False

        def getXY(i):
            y = i // self.BOARDSIZE
            x = i - self.BOARDSIZE*y
            return x, y        # Empty

        def getPi(x, y):
            return x + 19*y      

        # given is not an empty point
        if self.boardlist[pi] > 0:
            return []

        color = 0

        x, y = getXY(pi)
        # print(" isPlayerOneEye (x,y)=","(", x,",", y,")",)
        # 如果上下左右還有一個空，

        def isRightEmpty(x, y):
            x = x + 1
            if x > 18:
                return False
            if self.boardlist[getPi(x, y)] == 0:
                return True
            return False

        def isDownEmpty(x, y):
            y = y + 1
            if y > 18:
                return False
            if self.boardlist[getPi(x, y)] == 0:
                return True
            return False

        def isLeftEmpty(x, y):
            x = x - 1
            if x < 0:
                return False
            if self.boardlist[getPi(x, y)] == 0:
                return True
            return False

        def isUpEmpty(x, y):
            y = y - 1
            if y < 0:
                return False
            if self.boardlist[getPi(x, y)] == 0:
                return True
            return False

        if isRightEmpty(x, y):
            return False  # 表示往右有空
        if isDownEmpty(x, y):
            return False  # 表示往下有空
        if isLeftEmpty(x, y):
            return False  # 表示往左有空
        if isUpEmpty(x, y):
            return False  # 表示往上有空

        # print("... TODO 看看包圍住的是幾塊棋")
        # print(" isPlayerOneEye (x,y)=", "(", x, ",", y, ")",)
        # self.show1()
        # input(" checking 看看包圍住的是幾塊棋")

        s4 = []  # surounding 4 directions
        s4Color = set()
        if x + 1 <= 18:
            s4.append([x+1, y])
            temp = getPi(x + 1,y)
            s4Color.add(self.boardlist[temp])
        if y + 1 <= 18:
            s4.append([x, y+1])
            temp = getPi(x,y+1)
            s4Color.add(self.boardlist[temp])
        if x - 1 >= 0:
            s4.append([x-1, y])
            temp = getPi(x-1,y)
            s4Color.add(self.boardlist[temp])
        if y - 1 >= 0:
            s4.append([x, y-1])
            temp = getPi(x,y-1)
            s4Color.add(self.boardlist[temp])
        
        # print (" color kinds is " , len(s4Color))
        
        if len(s4Color) == 2:
            return False   # 黑白交界共氣

        # print(" isPlayerOneEye (x,y)=", "(", x, ",", y, ")",)
        # input(" TODO ... is player's color?")
        scolor = s4Color.pop()   # set , no index, just use pop
        if self.next == scolor:

            # print("...TODO 是自己一方的, 周邊的算不算同一塊棋？")
            # input(" ...TODO ...")
            # print(s4, scolor)
            # print(" isPlayerOneEye (x,y)=", "(", x, ",", y, ")",)

            temp = []
            if x+1 <=18:
                temp.append(set(self.getGrpList(self.pi(x+1,y))))
            if y+1 <=18:
                temp.append(set(self.getGrpList(self.pi(x,y+1))))

            if x-1 >=0:
                temp.append(set(self.getGrpList(self.pi(x-1,y))))
            if y-1 >=0:
                temp.append(set(self.getGrpList(self.pi(x,y-1))))
            
            # self.debug(temp)

            
            for m in range(len(temp)):
                # print("m",m)
                for n in range(1+m,len(temp)):
                    # print("n",n)
                    if temp[m]!= temp[n]:
                        return False
            # self.showWarning("不可自填單空眼位")
            return True
                
        return False

    def xxxgetGrpV2(self, color):
        grp = []
        for y in range(0, 19):
            for x in range(0, 19):
                # print('(%d,%d)'%(x,y), end=',')
                # if self.xy(x,y)==1: # Black
                if self.stone(x, y) == color:  # Black :1 => for White:2 as well

                    grp.append([x, y])
                    # break

        # print("由左而右，由上而下，先找到所有 color is ", color)

        # if color == 1:
        #     stoneColor='Black'
        # if color == 2:
        #     stoneColor='White'

        # print("\n   ", stoneColor)

        bgrp = []

        def isConnected(p1, p2):
            if abs(p1[0]-p2[0])+abs(p1[1]-p2[1]) == 1:
                return True
            return False

        def getXY(i):
            y = i // self.BOARDSIZE
            x = i - self.BOARDSIZE*y
            return [x, y]

        def tryToLink(k):
            # print("try to link here",k)
            if len(bgrp) == 0:
                return False
            for knownGrp in bgrp:
                for point in knownGrp:
                    if isConnected(point, k):
                        knownGrp.append(k)
                        return True

            return False

        # print(grp)
        for k in grp:
            # print(k)
            # 有沒有和現在的GRP連接
            if tryToLink(k):
                # 有連接
                # print (bgrp)

                pass
            else:
                # 建新的GRP
                bgrp.append([k])
                # print (bgrp)

        def isEmpty(x, y):

            if x < 0 or x > 18 or y < 0 or y > 18:
                return False  # out of board
            if self.boardlist[x+19*y] == 0:
                return True
            return False
        # def checkRight(p)
        #     if isEmpty(p[0]+1,p[1]):

        # print(bgrp)
        grplib = []
        for grp in bgrp:
            # print(grp)
            liberity = set()
            for p in grp:
                if isEmpty(p[0]+1, p[1]):
                    liberity.add(p[0]+1+self.BOARDSIZE*p[1])
                if isEmpty(p[0]-1, p[1]):
                    liberity.add(p[0]-1+self.BOARDSIZE*p[1])

                if isEmpty(p[0], p[1]+1):
                    liberity.add(p[0]+self.BOARDSIZE*(1+p[1]))
                if isEmpty(p[0], p[1]-1):
                    liberity.add(p[0]+self.BOARDSIZE*(-1+p[1]))

            # print("{", self.getT19String(grp), ":",len(liberity)+"}")
            # print(end='      {')
            # print(self.getT19String(grp),end=':')
            # print(len(liberity),end='}\n')
            grplib.append(liberity)
            print('棋塊',self.getT19String(grp), end=' 內外氣')
            # print('外圍',self.getT19StringForSet(liberity))
            print(liberity)
        return bgrp, grplib

    def getGrp(self, color):
        grp = []
        for y in range(0, 19):
            for x in range(0, 19):
                # print('(%d,%d)'%(x,y), end=',')
                # if self.xy(x,y)==1: # Black
                if self.stone(x, y) == color:  # Black => for White as well

                    grp.append([x, y])
                    # break

        # print("由左而右，由上而下，先找到所有 color is ", color)
        if color == 1:
            stoneColor = 'Black'
        if color == 2:
            stoneColor = 'White'

        print("\n   ", stoneColor)

        bgrp = []

        def isConnected(p1, p2):
            if abs(p1[0]-p2[0])+abs(p1[1]-p2[1]) == 1:
                return True
            return False

        def getXY(i):
            y = i // self.BOARDSIZE
            x = i - self.BOARDSIZE*y
            return [x, y]

        def tryToLink(k):
            if len(bgrp) == 0:
                return False
            for knownGrp in bgrp:
                for point in knownGrp:
                    if isConnected(point, k):
                        knownGrp.append(k)
                        return True

            return False

        # print(grp)
        for k in grp:
            # print(k)
            # 有沒有和現在的GRP連接
            if tryToLink(k):
                # 有連接
                # print (bgrp)

                pass
            else:
                # 建新的GRP
                bgrp.append([k])
                # print (bgrp)

        def isEmpty(x, y):

            if x < 0 or x > 18 or y < 0 or y > 18:
                return False  # out of board
            if self.boardlist[x+19*y] == 0:
                return True
            return False
        # def checkRight(p)
        #     if isEmpty(p[0]+1,p[1]):

        for grp in bgrp:
            # print(grp)
            liberity = set()
            for p in grp:
                if isEmpty(p[0]+1, p[1]):
                    liberity.add(p[0]+1+self.BOARDSIZE*p[1])
                if isEmpty(p[0]-1, p[1]):
                    liberity.add(p[0]-1+self.BOARDSIZE*p[1])

                if isEmpty(p[0], p[1]+1):
                    liberity.add(p[0]+self.BOARDSIZE*(1+p[1]))
                if isEmpty(p[0], p[1]-1):
                    liberity.add(p[0]+self.BOARDSIZE*(-1+p[1]))

            # print("{", self.getT19String(grp), ":",len(liberity)+"}")
            print(end='      {')
            print(self.getT19String(grp), end=':')
            print(len(liberity), end='}\n')
    
    def stone(self,x,y):
        return self.boardlist[x+19*y]

    def show1(self):
        print()
        print('   A B C D E F G H J K L M N O P Q R S T')
        for y in range(0, 19):
            yp = 19-y
            if yp < 10:
                print(end=' ')
                print(yp, end='')
            else:
                print(yp, end='')

            for x in range(0, 19):
                if self.stone(x, y) == 1:
                    print(' X', end='')
                elif self.stone(x, y)  == 2:
                    print(' O', end='')
                else:
                    if x in [3, 9, 15] and y in [3, 9, 15]:

                        print(' *', end='')
                    else:
                        print(' .', end='')

            print(' ', end='')
            if yp < 10:
                print(yp, end='')
                print(end=' ')
            else:
                print(yp, end=' ')

            print()
        print('   A B C D E F G H J K L M N O P Q R S T')
        print(' -----------------------------------------')
       
        print('  Move:', self.counter,end= ' ')
        if self.counter > 0:
            print(self.t19(self.moveList[self.counter-1]))
        # else:
        #     print()
        print()
        print('  B captured:', self.captured[1])
        print('  W captured:', self.captured[2])
        if self.passcnt > 0:
            print('  pass cnt:', self.passcnt)

        print()
        # print(self.boardlist)
