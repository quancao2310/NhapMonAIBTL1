class TestCase:
    def __init__(self,filename):
        self.filename = filename
        self.cusor = 0

    def isNotEmpty(self):
        with open(self.filename,'r',encoding='utf-8') as f:
            f.seek(self.cusor)
            buf = f.readline().strip()
            return buf!=""
        
    def getTestCase(self):
        with open(self.filename,'r',encoding='utf-8') as f:
            f.seek(self.cusor)
            board = ""
            cubePosition =""
            buf = f.readline().strip()
            self.cusor +=len(buf)+2
            while (buf!=""): 
                buf = f.readline().strip()
                self.cusor +=len(buf)+2
                buf = f.readline().strip()
                self.cusor +=len(buf)+2
                while buf != "Cube Position":
                    board += buf
                    buf = f.readline().strip()
                    self.cusor +=len(buf)+2
                buf = f.readline().strip()
                self.cusor +=len(buf)+2
                cubePosition = buf
                break
            lst = board.split(';')
            board = {}
            for i in lst:
                board[eval(i.split(':')[0])] = int(i.split(':')[1])
            lst = cubePosition.split(';')
            cubePosition = [eval(lst[0]),eval(lst[1])]
            return [board,cubePosition]
