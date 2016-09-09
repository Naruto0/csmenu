#! /usr/bin/python

def save(string):
    with open("GameMenu.res", 'w') as text_file:
        text_file.write(string)

ip = 'csko.cz'

testing = [('csko.cz  |  Zombie', 27017),
('csko.cz  |  Knife', 27019),
('csko.cz  |  Jump', 27025),
('csko.cz  |  Aim', 27027),
('>---<',0),
('csko.cz  |  He grenades', 27035),
('csko.cz  |  BaseBuilder+XP', 27040),
('csko.cz  |  Jailbreak 2', 27042),
('csko.cz  |  Zombie Apokalypsa', 27057)]

def wrap(value):
    try:
         return '"%d"' % (value)
    except TypeError:
        return '"%s"' % (value)

class menuGen(object):
    def __init__(self):
        pass
    def lbStr(self):
        return 2*'\t'+'"label"'

    def cmdStr(self):
        return 2*'\t'+'"command"'

    def oigStr(self):
        return 2*'\t'+'"OnlyInGame" "1"'

    def nsStr(self):
        return 2*'\t'+'"notsingle" "1"'

    def ccmdStr(self, serv, port):
        return '"engine connect %s:%d"' % (serv, port)

    def header(self):
        return '"GameMenu"\n{\n'

    def defaults(self):
        l = [('""','""',1),
        ('"#GameUI_GameMenu_ResumeGame"','"ResumeGame"',1),
        ('"#GameUI_GameMenu_Disconnect"','"Disconnect"',2),
        ('"#GameUI_GameMenu_PlayerList"','"OpenPlayerListDialog"',2),
        ('""','""',0),
        ('"#GameUI_GameMenu_NewGame"','"OpenCreateMultiplayerGameDialog"',0),
        ('"#GameUI_GameMenu_FindServers"','"OpenServerBrowser"',0),
        ('"#GameUI_GameMenu_Options"','"OpenOptionsDialog"',0),
        ('"#GameUI_GameMenu_Quit"','"Quit"',0)]
        return l

    def generate(self, ls,ip):
        content = self.header()
        i = 0
        while i < len(ls):
            content = content+'\t"%d"\n' % (i+1)
            content = content+'\t{\n'
            # if there's a separator
            if ls[i][0] == ">---<":
                content = content+self.lbStr()+' '+self.defaults()[0][0]+'\n'
                content = content+self.cmdStr()+' '+self.defaults()[0][1]+'\n'
                content = content+'\t}\n'
            else:
                content = content+self.lbStr()+' '+wrap(ls[i][0])+'\n'
                content = content+self.cmdStr()+' '+self.ccmdStr(ip,ls[i][1])+'\n'
                content = content+'\t}\n'
            i += 1
        y = i - len(ls)
        while y < len(self.defaults()):
            content = content+'\t"%d"\n' % (i+1)
            content = content+'\t{\n'
            content = content+self.lbStr()+' '+self.defaults()[y][0]+'\n'
            content = content+self.cmdStr()+' '+self.defaults()[y][1]+'\n'
            if self.defaults()[y][2] == 1:
                content = content+self.oigStr()+'\n'
            elif self.defaults()[y][2] == 2:
                content = content+self.oigStr()+'\n'
                content = content+self.nsStr()+'\n'
            content = content+'\t}\n'
            y += 1
            i += 1

        return content + '}'

def main():
    f = menuGen()
    s = f.generate(testing,ip)
    print(s)

if __name__ == '__main__':
    main()
