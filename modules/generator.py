#! /usr/bin/python
import json, re

regulars = {
    r'csko\.cz\s{1,3}\|\s{1,3}': '',
    r'aim\s?' : 'aim',
    r'awp' : 'aw',
    r'b(?:ase)?\s?b(?:uilder)[+]XP\s?': 'bb',
    r'bh(?:op)\s?' : 'bh',
    r'cod:mw\s?' : 'cod',
    r'(?:\.\s-\s1\s)?itemy?\s?': '',
    r'\s?,\s?fymaps' : 'fy',
    r'capture\s?the\s?flag\s?' : 'ctf',
    r'classic' : 'cc',
    r'd(?:eath)?\s?m(?:atch)?\s?' : 'dm',
    r'free' : 'fr',
    r'ffa?\s?' : 'ff',
    r'death\s?run\s?' : 'dr',
    r'fun' : 'fn',
    r'furien\s?' : 'fu',
    r'fy\s?' : 'fy',
    r'g(?:un)?\s?g(?:ame)?\s?' : 'gg',
    r'(?:he)?\s?grenades?' : 'he',
    r'c21' : '',
    r'hide\s?&?\s?seek\s?' : 'hns',
    r'jail\s?break\s?' : 'jb',
    r'mini' : '',
    r'jump' : 'jm',
    r'training' : 't',
    r'Mega\s?pub(?:lic)?\s?' : 'mg',
    r'old\s?school' : 'os',
    r'paint\s?ball\s?' : 'pb',
    r'rc.....': 'rc',
    r'rats?\s?(?:maps)?' : 'rm',
    r'schovka' : 'sch',
    r'scoutz?\s?knive[zs]\s?' : 'sc',
    r'snow\s?ball\s?(?:war)?' : 'sb',
    r'soccer\s?jam' : 'sj',
    r'super\s?hero\s?' : 'sh',
    r'\(40 lvl\)' : '',
    r'surf\s?kill\s?' : 'sk',
    r'surf\s?speed' : 'ss',
    r'knife\s?' : 'kn',
    r'100hp dm' : 'dm',
    r'super\s?jump' : 'sj',
    r'u(?:nreal)?\s?t(?:ournament)' : 'ut',
    r'vanocni\s?server' : 'vs',
    r'war3\s?' : 'war',
    r'ft\s?' : 'f',
    r'ultimate\s?' : 'u',
    r'zombie\s?' : 'zm',
    r'revolution\s?' : 'r',
    r'apokalypsa\s?' : 'a',
    r'escape' : 'es',
    r'dust_?2\s' : 'd2',
    r'inf(?:erno)?\s?' : 'inf',
    r'only\s?' : '',
}

def save_res(string):
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


def process(data):

    for server in data:
        name = server[0]
        for expression in regulars:
            name = re.sub(expression, regulars[expression], name, flags=re.IGNORECASE)
        server[0] = name
    return data


def wrap(value):
    try:
         return '"%d"' % (value)
    except TypeError:
        return '"%s"' % (value)


class menu_gen(object):
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


    def generate(self, ls, ip):
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


def save_data(data):
    """another helper function"""
    print(data)
    with open('names.txt', 'w') as outfile:
        json.dump(data, outfile)


def read_data():
    """helper function"""
    with open('../names.txt', 'r') as infile:
        data = json.load(infile)
        return data

def make_cfg(data, server):
    """make a config out of fetched data"""
    data = process(data)
    cfg_string = ''
    for entry in data:
        cfg_string += '"alias" "{abbr}" "connect {ip}:{port}"\n'.format(abbr=entry[0],\
                                                            ip=server,
                                                            port=entry[1])
    
    print(cfg_string)
    ## with open('aliases.cfg', 'w') as file:
    ##    file.write(cfg_string)

def main():
    f = menu_gen()
    s = f.generate(*read_data())
    print(s)

    make_cfg(*read_data())

if __name__ == '__main__':
    main()
