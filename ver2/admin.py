# -*- coding: utf-8 -*-
"""
管理员和用户

@author: Doby Xu
"""
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import numpy as np

#解决弹出两个消息框的bug
root = tk.Tk()
root.withdraw()
#代价是不能点xx来退出窗口，需要ctrl C

#import obj#由于pickle的原因，该导包出现较多问题，故将obj.py代码放入此文件中


#用户类
#属性：用户名和密码
#方法：
#   主页
#   浏览该类所有物品
#   搜索该类中的物品
#   为该类添加物品
class User:
    user_name = "unnamed"
    pw = "123456"
    
    def main_page_user(self, win = None):
        if win:
            win.destroy()
        win = tk.Tk()
        self.win_u = win
        win.geometry('450x300')
        win.resizable()
        win.title('你帮我助——用户界面')
        
        def flush_and_show(event):
            for i in range(len(g_list)):
                g_list[i].destroy()
                
            #查看全部物品
            b_explore = tk.Button(self.win_u, text="查看全部物品", width=15, 
                               command = lambda:self.explore(cbox.current()))
            b_explore.grid(row = 2)
            g_list.append(b_explore)
            
            #搜索物品
            b_search = tk.Button(self.win_u, text="搜索并申领物品", width=15, 
                               command = lambda:self.search(cbox.current()))
            b_search.grid(row = 3)
            g_list.append(b_search)
            
            #添加物品
            b_add = tk.Button(self.win_u, text="添加物品", width=15, 
                               command = lambda:self.add(cbox.current()))
            b_add.grid(row = 4)
            g_list.append(b_add)
            
        #控件
        labe1 = tk.Label(self.win_u,text="请选择一个物品类型：")
        labe1.grid(row = 1, column = 0)
        #显示所有类型，作为下拉菜单出现
        # 创建下拉菜单
        cbox = ttk.Combobox(self.win_u)
        cbox.grid(row = 1, column = 1)
        # 设置下拉菜单中的值
        print(classes.get_class_name())
        cbox['value'] = tuple(classes.get_class_name())
        
        #控件列表
        g_list = []
        
        cbox.bind("<<ComboboxSelected>>", flush_and_show)
        
        
        #tk.Button(win, text="选择类型", width=10, command=self.add_cls).grid(row=0, column=0, sticky="w", padx=10, pady=5)
        #tk.Button(admin_main_win, text="修改类型", width=10, command=self.modify_cls).grid(row=0, column=1, sticky="w", padx=10, pady=5)
        win.mainloop()
        
    def explore(self, idx):
        #print("显示所有商品")
        c = classes.classes[idx]
        print(c.name+str(len(c.items)))
        self.win_u.destroy()
        win = tk.Tk()
        self.win_u = win
        win.geometry('450x300')
        win.resizable()
        win.title('你帮我助——'+c.name+'类的全部物品')
        
        # 创建滚动条
        s = tk.Scrollbar(win)
        # 设置垂直滚动条显示的位置，使得滚动条，靠右侧；通过 fill 沿着 Y 轴填充
        s.pack(side = tk.RIGHT,fill = tk.Y)
        # 创建列表选项
        listbox1 =tk.Listbox(self.win_u, yscrollcommand = s.set)
        listbox1.pack()
        s.config(command = listbox1.yview)
        # i表示索引值
        for i in range(len(c.items)):
            listbox1.insert(i, c.items[i].name)
            print(c.items[i].name)
            
        def show(event):
            #print(listbox1.curselection())#提取点中选项的下标
            #print(listbox1.get(listbox1.curselection()))#提前点中选项下标的值
            item_idx = listbox1.curselection()[0]
            print(c.items[item_idx].name)
            #c = self
            self.show_item(c.items[item_idx], c)
        listbox1.bind("<Double-Button-1>",show)
        #返回按钮    
        b = tk.Button(self.win_u, text="返回", width=5, 
                               command = lambda:self.main_page_user(win))
        
        b.pack(side = tk.BOTTOM)
        self.win_u.mainloop()
        
    def search(self, idx):
        print("搜索并申领商品")
        c = classes.classes[idx]
        
        def click_search():
            item_list = c.search(e.get())
            
            #创建新窗口展示物品
            win1 = tk.Tk()
            win1.geometry('450x300')
            win1.resizable()
            win1.title('搜索到'+str(len(item_list))+'件物品')
            # 创建滚动条
            s = tk.Scrollbar(win1)
            # 设置垂直滚动条显示的位置，使得滚动条，靠右侧；通过 fill 沿着 Y 轴填充
            s.pack(side = tk.RIGHT,fill = tk.Y)
            # 创建列表选项
            listbox1 =tk.Listbox(win1, yscrollcommand = s.set)
            listbox1.pack()
            s.config(command = listbox1.yview)
            # i表示索引值
            for i in range(len(item_list)):
                listbox1.insert(i, item_list[i].name)
                print(item_list[i].name)
            
            def show(event):
                #print(listbox1.curselection())#提取点中选项的下标
                #print(listbox1.get(listbox1.curselection()))#提前点中选项下标的值
                item_name = listbox1.get(listbox1.curselection())
                item_idx = 0
                for i in range(len(c.items)):
                    if c.items[i].name == item_name:
                        item_idx = i
                        break
                #c = self
                self.show_item(c.items[item_idx], c)
            listbox1.bind("<Double-Button-1>",show)
            win.mainloop()
            
            
        
        self.win_u.destroy()
        win = tk.Tk()
        self.win_u = win
        win.geometry('450x300')
        win.resizable()
        win.title('你帮我助——搜索'+c.name+'类物品')
        l = tk.Label(self.win_u, text="请输入关键词：")
        l.grid(row = 0, column = 0)
        e = tk.Entry(self.win_u)    
        e.grid(row = 0, column = 1)
        
        b = tk.Button(self.win_u, text="搜索", width=5, 
                               command = lambda:click_search())
        b.grid(row = 0, column = 2)
        
        b_back = tk.Button(self.win_u, text="返回", width=5, 
                               command = lambda:self.main_page_user(win))
        
        b_back.grid(row = len(c.class_attributes)+5, column = 1)
        self.win_u.mainloop()
        
    def add(self, idx):
        print("添加物品")
        c = classes.classes[idx]
        
        def create_item():
            #输入检查
            if e_name.get()=="" or e_addr.get()=="":
                messagebox.showinfo(title=':(', message='请正确填写品名和地址')
                return
            if e_num.get()=="" or e_unit.get()=="":
                messagebox.showinfo(title=':(', message='请正确填写数量和单位')
                return
            #获取属性
            attributes=[]
            for i in range(len(c.class_attributes)):
                attributes.append(e_att[i].get())
                print(attributes[i])
                
            #创建物品
            
            item = Item(e_name.get(), e_addr.get(), attributes, e_num.get(), e_unit.get(),e_info.get(),e_tel.get() )
            res = c.add_item(item)
            #注意在调用Class的方法后要更新数据库！！！
            classes.update()
            
            if res:
                item = c.items[len(c.items)-1]
                messagebox.showinfo(title='恭喜', message='添加成功\n'
                                    +item.name+" "+str(item.num)+item.unit)
                self.main_page_user(self.win_u)
            else:
                messagebox.showinfo(title=':(', message='添加失败')
                
                
        
        
        print(c.name+str(len(c.items)))
        self.win_u.destroy()
        win = tk.Tk()
        self.win_u = win
        win.geometry('450x300')
        win.resizable()
        win.title('你帮我助——添加'+c.name+'类物品')
        
        l_name = tk.Label(self.win_u, text="物品名：")
        l_name.grid(row = 0, column = 0)
        
        e_name = tk.Entry(self.win_u)    
        e_name.grid(row = 0, column = 1)
        
        l_addr = tk.Label(self.win_u, text="物品地址：")
        l_addr.grid(row = 1, column = 0)
        e_addr = tk.Entry(self.win_u)    
        e_addr.grid(row = 1, column = 1)
        
        l_num = tk.Label(self.win_u, text="物品数量：")
        l_num.grid(row = 2, column = 0)
        e_num = tk.Entry(self.win_u)   
        e_num.insert(0, "1")
        e_num.grid(row = 2, column = 1)
        
        l_unit = tk.Label(self.win_u, text="单位：")
        l_unit.grid(row = 2, column = 2)
        e_unit = tk.Entry(self.win_u)  
        e_unit.insert(0, "个")
        e_unit.grid(row = 2, column = 3)
        
        l_info = tk.Label(self.win_u, text="物品说明（选填）：")
        l_info.grid(row = 3, column = 0)
        e_info = tk.Entry(self.win_u, width=20)  
        #e_info.insert(0, "个")
        e_info.grid(row = 3, column = 1)
        
        l_tel = tk.Label(self.win_u, text="联系方式（选填）：")
        l_tel.grid(row = 4, column = 0)
        e_tel = tk.Entry(self.win_u, width=20)  
        #e_info.insert(0, "个")
        e_tel.grid(row = 4, column = 1)
        
        
        
        e_att = []
        
        for i in range(len(c.class_attributes)):
            l_att = tk.Label(self.win_u, text=c.class_attributes[i])
            l_att.grid(row = 5+i, column = 0)
            e = tk.Entry(self.win_u)    
            e.grid(row = 5+i, column = 1)
            e_att.append(e)
            
        b_add = tk.Button(self.win_u, text="添加", width=5, 
                               command = lambda:create_item())
        b_add.grid(row = len(c.class_attributes)+5, column = 0)
        
        b_back = tk.Button(self.win_u, text="返回", width=5, 
                               command = lambda:self.main_page_user(win))
        
        b_back.grid(row = len(c.class_attributes)+5, column = 1)
        self.win_u.mainloop()
    
    #展示物品页面
    #并且有申请领取按钮
    #给入物品和类型
    def show_item(self, item, c):
        win = tk.Tk()
        win.geometry('450x300')
        win.resizable()
        win.title('你帮我助——'+item.name+'详细信息')
        
        def get_item():
            print(c.items[item.no])
            if c.remove_item(item.no):
                classes.update()
                messagebox.showinfo(title='恭喜', message='申领 '+item.name+' 成功\n'
                                    +item.name+" "+str(item.num)+item.unit)
                #或许可以添加一些人性化的界面，而不是粗暴退出
                win.destroy()
                self.main_page_user(self.win_u)
        
        l_name = tk.Label(win, text="物品名："+item.name)
        l_name.grid(row = 0, column = 0)

        l_addr = tk.Label(win, text="物品地址："+item.addr)
        l_addr.grid(row = 1, column = 0)

        
        l_num = tk.Label(win, text="物品数量："+str(item.num)+item.unit)
        l_num.grid(row = 2, column = 0)
        
        if item.info:
            l_info = tk.Label(win, text="物品说明："+item.info)
            l_info.grid(row = 3, column = 0)
        else:
            l_info = tk.Label(win, text="物品说明：无")
            l_info.grid(row = 3, column = 0)
        if item.tel:
            l_tel = tk.Label(win, text="物主联系方式："+item.tel)
            l_tel.grid(row = 4, column = 0)
        
        
        for i in range(len(c.class_attributes)):
            if item.attributes[i] == None or item.attributes[i]=='' :
                l = tk.Label(win, text = c.class_attributes[i] + ':无')
            else:
                l = tk.Label(win, text = c.class_attributes[i] +':\t'+ item.attributes[i])
            l.grid(row = 5+i, column = 0)

        b_get = tk.Button(win, text="申请领取", width=10, 
                               command = lambda:get_item())
        b_get.grid(row = 5+len(c.class_attributes))
        win.mainloop()
        
#管理员
#方法：
#   修改类
#   创建新类
#   User的所有方法，即切换到用户类的主页
class Admin(User):
    #管理员主页
    #给入需要销毁的页
    def main_page_admin(self, win=None):
        if win:
            win.destroy()
            #elf.win.destroy()
        
        admin_main_win = tk.Tk()
        self.win_a = admin_main_win
        #设置窗口样式
        admin_main_win.geometry('450x300')
        admin_main_win.resizable()
        admin_main_win.title('你帮我助——管理员界面')
        #待美化↑
        
        #设置窗口 控件
        tk.Button(admin_main_win, text="添加类型", width=10, command=self.add_cls).grid(row=0, column=0, sticky="w", padx=10, pady=5)
        tk.Button(admin_main_win, text="修改类型", width=10, command=self.modify_cls).grid(row=0, column=1, sticky="w", padx=10, pady=5)
        tk.Button(admin_main_win, text="打开用户页面", width=10, command=self.main_page_user).grid(row=1, column=0, sticky="w", padx=10, pady=5)
        tk.Button(admin_main_win, text="审核注册账户", width=10, command=self.check_user).grid(row=1, column=1, sticky="w", padx=10, pady=5)
        
        admin_main_win.mainloop()
    
    #添加类型
    #只允许主窗口调用
    def add_cls(self):
        #helper
        def write_in_att(num, entry_att):
            #classes = np.load('./database/class.npy', allow_pickle=True)
            atts = []
            for i in range(num):
                atts.append(entry_att[i].get())
                
            name =str( entry1.get())
            classes.add_cls(name, atts)
            #classes.append(new_class)
            #np.save('./database/class.npy',classes)
            #classes = np.load('./database/class.npy', allow_pickle=True)
            #for i in range(len(classes)):
            #    print(classes[i].name)
            classes.add_cls(name, atts)
            messagebox.showinfo(title='消息', message='“'+name+'”类已成功添加')
            self.main_page_admin(self.win_a)
            
        def entry_att():
            b1.destroy()
            if cbox.get()=='':
                return
            num = int(cbox.get())
            print(num)
            entry_att = []
            for i in range(num):
                e = tk.Entry(self.win_a)
                e.grid(row = i+3, column = 1)
                entry_att.append(e)
            tk.Button(self.win_a, text="确定", width=5, command=lambda:write_in_att(num, entry_att)).grid(row=num+3, column=2, sticky="w", padx=5, pady=5)
                
        new_win = tk.Tk()
        
        self.win_a.destroy()
        
        self.win_a = new_win
        self.win_a.geometry('450x300')
        self.win_a.resizable()
        self.win_a.title('你帮我助——管理员界面-添加类型')
        
        labe1 = tk.Label(self.win_a,text="添加类型的名称：")
        #更换为下拉选择菜单
        labe2 = tk.Label(self.win_a,text="类型属性个数:" )
        labe1.grid(row=1)
        labe2.grid(row=2)
        
        
        
        entry1 = tk.Entry(self.win_a)
        #entry2 = tk.Entry(self.win_a)
        entry1.grid(row=1, column=1)
        #entry2.grid(row=2, column=1)
        cbox = ttk.Combobox(self.win_a)
        cbox.grid(row=2, column=1)
        cbox['value'] = ('1','2','3','4','5')
        cbox.current(3)

        b1 = tk.Button(self.win_a, text="确定", width=5, command=lambda:entry_att())
        b1.grid(row=2, column=2, sticky="w", padx=5, pady=5)
        b2 = tk.Button(self.win_a, text="返回", width=5, command=lambda:self.return_to_main()())
        b2.grid(row=2, column=3, sticky="w", padx=5, pady=5)
        self.win_a.mainloop()

        #classes = np.load('./database/class.npy', allow_pickle=True)
    
    
    #修改类型
    #只允许主窗口调用
    def modify_cls(self):
        #窗口调度
        new_win = tk.Tk()
        self.win_a.destroy()
        self.win_a = new_win
        self.win_a.geometry('500x300')
        self.win_a.resizable()
        self.win_a.title('你帮我助——管理员界面-修改类型')
        
        def change_name(idx, new_name):
            if classes.change_name_by_idx(idx, new_name):
                cbox['value'] = tuple(classes.get_class_name())
                messagebox.showinfo(title='消息', message='修改成功')
                flush_and_show("")#该行代码正确性有待考究
            else:
                messagebox.showinfo(title=':(', message='修改失败')
                
        def modify_att(c, idx, new_name):
            print(idx)
            if c.class_attributes[idx]==new_name:
                return
            if c.modify_att(idx, new_name):
                messagebox.showinfo(title='消息', message='修改成功')
                classes.update()
                flush_and_show("")#该行代码正确性有待考究
            else:
                messagebox.showinfo(title=':(', message='修改失败')
                
        def delete_att(c, idx):
            res = messagebox.askokcancel('请确认：', '真的要删除“'+c.class_attributes[idx]+'”吗？')
            if res:
                name = c.class_attributes[idx]
                if c.remove_att(name):
                    classes.update()
                    messagebox.showinfo(title='消息', message='删除成功')
                    flush_and_show("")#该行代码正确性有待考究
                else:
                    messagebox.showinfo(title=':(', message='已删除，请刷新')
        def add_att(c, name):
            if name == "在此输入新增类型名" or name == "":
                return
            if len(c.class_attributes)>=5:
                messagebox.showinfo(title='经过', message='该物品类型的属性数量已达上限')
            else:
                res = messagebox.askokcancel('请确认：', '为'+c.name+'添加“'+name+'”？')
                if res:
                    if c.add_att(name):
                        classes.update()
                        messagebox.showinfo(title='消息', message='添加成功')
                    else: 
                        messagebox.showinfo(title='添加失败', message='已有该属性，添加失败')
                    flush_and_show("")#该行代码正确性有待考究
        
        #函数flush_and_show
        #通过按钮调用
        #清空当前页面上的控件，并展示新的控件
        def flush_and_show(event):   
            #清空当前控件
            for i in range(len(g_list)):
                g_list[i].destroy()
            #显示修改项
            # 将俩个标签分别布置在第一行、第二行
            l1 = tk.Label(self.win_a, text="类型名：")
            l2 = tk.Label(self.win_a, text="类型属性列表：")
            l1.grid(row=2, column = 1)
            l2.grid(row=3, column = 1)
            g_list.append(l1)
            g_list.append(l2)
            
            #读取输入
            idx = cbox.current()
            print(idx)
            c = classes.classes[idx]
            
            #名称修改框
            e_name = tk.Entry(self.win_a)
            e_name.insert(0,c.name)
            e_name.grid(row = 2, column = 2)
            g_list.append(e_name)
            #名称修改按钮
            b_name = tk.Button(self.win_a, text="修改类型名", width=10, 
                               command = lambda:change_name(idx = idx, new_name = e_name.get()))
            b_name.grid(row = 2, column = 3)
            g_list.append(b_name)
            
            #属性修改项
            #无用的代码设计，待删除
            
            '''
            for i in range(len(c.class_attributes)):
                #输入框控件
                #已有属性的输入框
                e = tk.Entry(self.win_a)
                e.insert(0, c.class_attributes[i])
                e.grid(row = 3+i, column = 2)
                e_att.append(e)
                g_list.append(e)
                
                #按钮控件
                #修改按钮
                b1 = tk.Button(self.win_a, text="修改属性名", width=10, 
                               command = lambda:modify_att(c, idx = i, new_name = e.get()))
                b1.grid(row = 3+i, column = 3)
                b_att.append(b1)
                g_list.append(b1)
                #删除按钮
                b_del = tk.Button(self.win_a, text="删除", width=5, 
                               command = lambda:delete_att(c, idx = i))
                b_del.grid(row = 3+i, column = 4)
                g_list.append(b_del)
            '''
            def flush_att(event):
                print(cbox_att.current())
                e_att.delete(0, len(e_att.get()))
                e_att.insert(0, c.class_attributes[cbox_att.current()])
                
            cbox_att = ttk.Combobox(self.win_a)
            cbox_att.grid(row=3, column=2)
            cbox_att['value'] = tuple(c.class_attributes)
            cbox_att.current(0)
            cbox_att.bind("<<ComboboxSelected>>", flush_att)
            
            g_list.append(cbox_att)
            
            l_att = tk.Label(self.win_a, text="编辑该属性：")
            l_att.grid(row=4, column = 1)
            e_att = tk.Entry(self.win_a)
            e_att.insert(0, c.class_attributes[cbox_att.current()])
            e_att.grid(row = 4, column = 2)

            g_list.append(e_att)
                
            #按钮控件
            #修改按钮
            b_att = tk.Button(self.win_a, text="修改属性名", width=10, 
                           command = lambda:modify_att(c, idx = cbox_att.current(), new_name = e_att.get()))
            b_att.grid(row = 4, column = 3)

            g_list.append(b_att)
            #删除按钮
            b_del = tk.Button(self.win_a, text="删除", width=5, 
                              command = lambda:delete_att(c, idx = cbox_att.current()))
            b_del.grid(row = 4, column = 4)
            g_list.append(b_del)
        
        
        
            #新属性的输入框
            e_add = tk.Entry(self.win_a)
            e_add.insert(0, "在此输入新增类型名")
            e_add.grid(row = 4+len(c.class_attributes), column = 2)
            g_list.append(e_add)
            #新增按钮
            b_add = tk.Button(self.win_a, text="新增", width=5, 
                               command = lambda:add_att(c, name = e_add.get()))
            b_add.grid(row = 4+len(c.class_attributes), column = 3)
            g_list.append(b_add)    
                
        #窗口设计
        labe1 = tk.Label(self.win_a,text="选择要修改的类型：")
        labe1.grid(row = 1, column = 1)
        #显示所有类型，作为下拉菜单出现
        # 创建下拉菜单
        cbox = ttk.Combobox(self.win_a)
        cbox.grid(row = 1, column = 2)
        # 设置下拉菜单中的值
        print(classes.get_class_name())
        cbox['value'] = tuple(classes.get_class_name())
        
        #控件列表
        g_list = []
        
        cbox.bind("<<ComboboxSelected>>", flush_and_show)
        
        #退出按键
        b_cancel = tk.Button(self.win_a, text="退出", width=5, 
                               command = self.return_to_main)
        b_cancel.grid(row = 10)
        
        self.win_a.mainloop()
    
    #审核用户
    #只允许主窗口调用    
    def check_user(self):
        ud.signup
        
        new_win = tk.Tk()
        self.win_a.destroy()
        self.win_a = new_win
        self.win_a.geometry('500x300')
        self.win_a.resizable()
        self.win_a.title('你帮我助——管理员界面-修改类型')
        
        g_list = []
        def approve(user):
            ud.approve(user.no)
            
            if len(ud.get_signup_name())==0:
                messagebox.showinfo(title='', message='审核列表空')
                self.return_to_main()
            cbox.current(0)
            cbox['value'] = tuple(ud.get_signup_name())
            flush_and_show(None)
            messagebox.showinfo(title='', message='审核成功')
            
        def reject(user):
            ud.reject(user.no)
            if len(ud.get_signup_name())==0:
                messagebox.showinfo(title='', message='审核列表空')
                self.return_to_main()
            cbox.current(0)
            cbox['value'] = tuple(ud.get_signup_name())
            flush_and_show(None)
            messagebox.showinfo(title='', message='审核成功')
        def flush_and_show(event):   
            #清空当前控件
            idx = cbox.current()
            print(idx)
            user = ud.signup[idx]
            
            for i in range(len(g_list)):
                g_list[i].destroy()
            l1 = tk.Label(self.win_a, text="用户名："+user.user_name)
            l2 = tk.Label(self.win_a, text="密码："+user.password)
            l3 = tk.Label(self.win_a, text="业主真实姓名："+user.real_name)
            l4 = tk.Label(self.win_a, text="业主地址："+user.real_name)
            l1.grid(row=2, column = 1)
            l2.grid(row=3, column = 1)
            l3.grid(row=4, column = 1)
            l4.grid(row=5, column = 1)
            g_list.append(l1)
            g_list.append(l2)
            g_list.append(l3)
            g_list.append(l4)
            
            b_app = tk.Button(self.win_a, text="通过", width=5, 
                               command = lambda: approve(user))
            b_app.grid(row=6, column = 1)
            
            b_rej = tk.Button(self.win_a, text="拒绝", width=5, 
                               command = lambda: reject(user))
            b_rej.grid(row=6, column = 2)
                
        #窗口设计
        if len(ud.get_signup_name())==0:
            messagebox.showinfo(title='', message='审核列表空')
            self.return_to_main()
        labe0 = tk.Label(self.win_a,text="请仔细检查业主真实姓名以及对应住址：")
        labe0.grid(row = 0, column = 1)
        labe1 = tk.Label(self.win_a,text="选择：")
        labe1.grid(row = 1, column = 1)
        #显示所有类型，作为下拉菜单出现
        # 创建下拉菜单
        cbox = ttk.Combobox(self.win_a)
        cbox.grid(row = 1, column = 2)
        # 设置下拉菜单中的值
        #print(classes.get_class_name())
        cbox['value'] = tuple(ud.get_signup_name())
        
        #控件列表
        g_list = []
        
        cbox.bind("<<ComboboxSelected>>", flush_and_show)
        b_cancel = tk.Button(self.win_a, text="退出", width=5, 
                               command = self.return_to_main)
        b_cancel.grid(row = 10)
        self.win_a.mainloop()
        
    def return_to_main(self):
        self.main_page_admin(self.win_a)
    


        

if __name__ == '__main__':
    #测试代码，直接运行该py即可测试
    admin = Admin()
    admin.main_page_admin()
    #user = User()
    #user.main_page_user()
    s = SignIn()
    #s.main_page()