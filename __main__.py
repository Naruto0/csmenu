#! /usr/bin/python3

from modules.filter import src_query
from modules.generator import menu_gen, save_res, make_cfg

import tkinter as tk
import tkinter.messagebox as messagebox

def switch(ls,idx,ost):
    ls[idx], ls[idx+ost] = ls[idx+ost], ls[idx]
    return ls

def isInt(s):
    try:
        i = int(s)
        return i
    except ValueError:
        return s

# Entry with label sub-widget class
class LabEntry(tk.Frame):
    '''Entry with label sub-widget class. Takes parent, string as label and default value string'''
    def __init__(self, parent, label, default):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.label = tk.Label(self, text=label)
        self.label.pack(side="left")
        self.entry = tk.Entry(self, width=10)
        self.entry.pack(side="left")
        self.entry.insert(0, default)

# Status bar class
class StatBar(tk.Frame):
    '''Status bar with small status entry'''
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.status = tk.Label(self, bd=1, relief="sunken", anchor="w")
        self.status.pack(fill="x")

    def set(self, format, *args):
        '''Set status method'''
        self.status.config(text=format % args)
        self.status.update_idletasks()

    def clear(self):
        '''Clear status method'''
        self.status.config(text="")
        self.label.update_idletasks

#Listbox wrapped with scrollbar
class scrollBox(tk.Frame):
    '''Listbox wrapped in Frame with attached scrollbar'''
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.config(width="800",height="640")
        self.scrollbar = tk.Scrollbar(self, orient="vertical")
        self.box = tk.Listbox(self, selectmode="single")
        self.scrollbar.config(command=self.box.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.box.pack(side="left", fill="both", expand="yes")

    #if you want to update
    def update(self, data):
        '''update Listbox with given data'''
        for server in data:
            self.box.insert("end", server[0])

    def clear(self):
        '''Clear list box'''
        self.box.delete(0, "end")

    def get_index(self):
        '''gets index number of selected items'''
        item = self.box.curselection()
        return isInt(item[0])

    def get_list(self):
        return self.box.get(0,'end')

class MainWindow(tk.Frame):
    '''Draws and handles application main window'''
    def __init__(self,parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        parent.title("CS Favorites Generator")

        # desired servers list
        self.desired = []

        # Menu
        self.mainMenu = tk.Menu(parent)
        self.FileMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.FileMenu.add_command(label="Quit", command=parent.destroy)
        self.mainMenu.add_cascade(label="File", menu=self.FileMenu)
        parent.winfo_toplevel().config(menu=self.mainMenu)
        self.workMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.workMenu.add_command(label="Fetch", command=self.fetch)
        self.workMenu.add_command(label="Generate", command=self.generate)
        self.workMenu.add_separator()
        self.workMenu.add_command(label="Make aliases", command=self.aliases)
        self.mainMenu.add_cascade(label="Do", menu=self.workMenu)

        # header bar
        self.hBar = tk.Frame(parent)
        self.hBar.pack(side="top", fill="x")
        self.server = LabEntry(self.hBar, "Server:", "csko.cz")
        self.server.pack(side="left")
        self.mod = LabEntry(self.hBar, "Mod:", "cstrike")
        self.mod.pack(side="left")
        self.pFrom = LabEntry(self.hBar, "Port range from:", 27030)
        self.pFrom.pack(side="left")
        self.pTo = LabEntry(self.hBar, "to:", 27040)
        self.pTo.pack(side="left")
        self.getButton = tk.Button(self.hBar, text="Fetch games", command=self.fetch)
        self.getButton.pack(side="left")


        # boxes with slider + add button
        self.box_frame = tk.Frame(parent)
        self.box_frame.pack(side="top", fill="both", expand="yes")
        self.box = scrollBox(self.box_frame)
        self.box.pack(side="left", fill="both", expand="yes")
        self.btnFrame = tk.Frame(self.box_frame)
        self.btnFrame.pack(side="left", fill="both")
        self.addButton = tk.Button(self.btnFrame, text="->", command=self.add_game)
        self.addButton.pack(side="top", fill="x")
        self.popButton = tk.Button(self.btnFrame, text="<-", command=self.pop_game)
        self.popButton.pack(side="top", fill="x")
        self.moveUp = tk.Button(self.btnFrame, text="Up", command=lambda:self.move("up"))
        self.moveUp.pack(side="top", fill="x")
        self.moveDown = tk.Button(self.btnFrame, text="Down", command=lambda:self.move("dwn"))
        self.moveDown.pack(side="top", fill="x")
        self.sepLab = tk.Label(self.btnFrame, text="separator:")
        self.sepLab.pack(side="top", fill="x")
        self.addSeparator = tk.Button(self.btnFrame, text=">---<", command=self.addSep)
        self.addSeparator.pack(side="top", fill="x")
        self.result_box = scrollBox(self.box_frame)
        self.result_box.pack(side="right", fill="both", expand="yes")

        # make config file button frame
        self.btmFrame = tk.Frame(parent)
        self.btmFrame.pack(side="top", anchor="e")
        self.hint = tk.Label(self.btmFrame, text="Select desired servers and click here to generate menu config ->")
        self.hint.pack(side="left", anchor="w")
        self.makeButton = tk.Button(self.btmFrame,text="Generate Hl config", command=self.generate)
        self.makeButton.pack(side="right", anchor="e")

        # status initialization frame
        self.stat = StatBar(parent)
        self.stat.pack(side="bottom", fill="x")
        self.stat.set("idle")

    def aliases(self):
        for item in self.box.get_list():
            print(item)
        make_cfg(self.q, self.host)


    def fetch(self):
        '''Fetch basic data. Return list'''
        self.desired = []
        self.box.clear()
        self.result_box.clear()
        self.stat.set("Finding games on server IP... this'll take some time")
        # call the ip and port ranged server query, return tuple of three items
        # ([list of ports aviable], [list of encountered minor errors], "host alias translated to ip number")
        self.query = src_query(self.server.entry.get(),\
                                self.mod.entry.get(),\
                                int(self.pFrom.entry.get()),\
                                int(self.pTo.entry.get()))
        # assign each tuple variable to readable and usable form
        self.q = sorted(self.query[0])
        self.err = (self.query[1])
        self.host = (self.query[2])

        if self.q:
            self.box.update(self.q)
            self.stat.set("Server list generated succsefully")
        else:
            self.box.clear()
            self.stat.set("No desired games found on ip of this server.")
            self.warning("No Games","No games of this mod found at all on this server.")

        # show user fails and errors from pFilter
        if self.err:
            self.warning("Fetch issues",self.err)
            print(self.err)

        self.ip = self.server.entry.get()

    def warning(self, title, info):
        '''Raises warning defined with ("Title","message string" or [list of messages]).'''
        if type(info) == list:
            result = "\n".join(info)
        else:
            result = info
        warnWind = messagebox.showinfo(title, result)

    def generate(self):
        '''Generate GameMenu from result_box'''
        if self.desired and self.host:
            f = menu_gen()
            s = f.generate(self.desired,self.host)
            save_res(s)
            self.stat.set("Hl config generated! Check for GameMenu.res")
        else:
            self.stat.set("You have to select servers and have valid ip!")
            pass

    def add_game(self):
        try:
            if self.q[self.box.get_index()] not in self.desired:
                self.desired.append(self.q[self.box.get_index()])
                # debug --> print self.desired
                self.stat.set("Game %s added to bottom of your list!" % self.desired[-1][0])
                self.result_box.clear()
                self.result_box.update(self.desired)
            else:
                self.stat.set("You shouldn't have one game twice in the menu!")
                pass
        except (AttributeError, IndexError) as e:
            self.stat.set("There's no game selected to add!")


    def addSep(self):
        self.desired.append(('>---<',0))
        self.result_box.clear()
        self.result_box.update(self.desired)

    def pop_game(self):
        try:
            self.desired.pop(self.result_box.get_index())
            self.result_box.clear()
            self.result_box.update(self.desired)
        except IndexError:
            self.stat.set("You have to select a game to pop out!")
            pass

    def move(self, direction):
        if direction == "up":
            self.offset = -1
        elif direction == "dwn":
            self.offset = 1
        else:
            pass
        try:
            if self.offset:
                switch(self.desired, self.result_box.get_index(), self.offset)
                self.result_box.clear()
                self.result_box.update(self.desired)
            else:
                pass
        except IndexError:
            self.stat.set("You have to select an item to move!")
            pass

def main():
    '''Main method to run window'''
    root = tk.Tk()
    MainWindow(root)
    root.mainloop()

if __name__ == '__main__':
    main()
