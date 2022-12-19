# -*- coding: utf-8 -*-
"""
这里定义着物品、物品类型以及其属性、数据库类

@author: Doby Xu
"""
import numpy as np



#物品的类别    
class Class:
    name = 'none'
    class_attributes = []
    #每个类别都管理一个物品列表
    items = []
    
    def __init__(self, name, attributes):
        self.name = name
        self.class_attributes = attributes   
        self.items = []
        
    #删除该类型
    #待测试    
    def remove_self(self):
        classes = np.load('./database/class.npy', allow_pickle=True)
        for i in range(len(classes)):
            if self.name == classes[i].name:
                classes.pop(i)
                while (i<len(classes)):
                    classes[i].no-=1
                    i+=1
                np.save('./database/class.npy', classes)
                return 1
        return 0
    
    def update_database(self):
        classes = np.load('./database/class.npy', allow_pickle=True)
        for i in range(len(classes)):
            if self.name == classes[i].name:
                classes[i] = self
                np.save('./database/class.npy', classes)
                return 1
        return 0
    
    #添加物品
    #参数：物品本品
    #返回：是否成功
    def add_item(self, item):
        #为该item分配编号
        item.no = len(self.items)
        item.class_name = self.name
        self.items.append(item)
        return self.update_database()
    
    #删除物品
    #参数：物品编号
    #返回：是否成功
    def remove_item(self, no):
        #no = item.no
        #no -=1
        #self.items.pop(no)
        del self.items[no]
        while (no<len(self.items)):
            self.items[no].no-=1
            no+=1
        return self.update_database()
        
                
    def modify_name(self, name):
        classes = np.load('./database/class.npy', allow_pickle=True)
        for i in range(len(classes)):
            if self.name == classes[i].name:
                classes[i].name = name
                self.name = name
                np.save('./database/class.npy', classes)
                return 1
        return 0

    #添加属性
    #直接调用，通过属性名添加属性,若有该属性返回0
    def add_att(self, name_att):
        #已有该属性则返回0
        if name_att in self.class_attributes:
            return 0
        self.class_attributes.append(name_att)
        
        #为所有Items增加该属性
        for i in range(len(self.items)):
            self.items[i].attributes.append("None")
        
        
        return self.update_database()
    
    def modify_att(self, idx, new_name):
        
        self.class_attributes[idx] = new_name
        return self.update_database()
        
    
    #删除属性
    #直接调用，通过属性名删除属性，若无该属性，返回0
    def remove_att(self, name_att):
        if name_att in self.class_attributes:
            idx = self.class_attributes.index(name_att)
            #self.class_attributes.remove(name_att)
            self.class_attributes.pop(idx)
            
            #为所有Items删除该属性           
            for i in range(len(self.items)):
                self.items[i].attributes.pop(idx)
            return self.update_database()
        else:
            return 0
        
    #搜索物品名
    #关键字搜索，返回物品列表
    def search_name(self, key):
        result = []
        for i in range(len(self.items)):
            if self.items[i].name.find(key)!=-1:
                result.append(self.items[i])
        return result
    
    #搜索物品说明
    #关键字搜索，返回info中含有该关键字，name中无该关键字的物品列表
    def search_info(self, key):
        result = []
        for i in range(len(self.items)):
            if self.items[i].info:
                if self.items[i].name.find(key)==-1 and self.items[i].info.find(key)!=-1:
                    result.append(self.items[i])
        return result
    #关键字搜索，返回物品列表：
    def search(self, key):
        return self.search_name(key)+self.search_info(key)
    
    
#数据库类
#存放着所有类别，每个类别中存放着所有该类别的物品
#方法：
#   增删改物品类型及其属性
#没有的方法：
#   增删改物品，可获取索引后调用classes[idx]的方法来修改其中的物品
#不必初始化，默认读取'./database/class.npy'数据库
class Classes:    
    
    def __init__(self):
        self.classes = np.load('./database/class.npy', allow_pickle=True)
        print("当前数据库：")
        for i in range(len(self.classes)):
            print(self.classes[i].name)
    
    #更新数据库
    #外部调用，在修改物品后调用，或在任何直接外部调用某*类型*的方法后调用
    def update(self):
        self.classes = np.load('./database/class.npy', allow_pickle=True)
           
    #添加类型
    #参数：添加类型名，属性列表
    def add_cls(self, name, att):
        new_class = Class(name,att)
        for i in range(len(self.classes)):
            #如果已有该类，则添加失败
            if name == self.classes[i].name:
                return
        #为新class分配编号
        new_class.cls_no = len(self.classes)
        
        self.classes = np.append(self.classes, new_class)
        np.save('./database/class.npy', self.classes)
        

    #获取类型名列表
    def get_class_name(self):
        res = []
        for i in range(len(self.classes)):
            res.append(self.classes[i].name)
        return res
    
    #通过名称获得类型的索引
    def get_index_by_name(self, name):
        for i in range(len(self.classes)):
            if name == self.classes[i].name:
                return i
        return -1
    
    #通过名称修改类型名称
    def change_name_by_name(self, old_name, new_name):
        idx = self.get_index_by_name(old_name)
        if idx == -1:
            return 0
        else:
            return self.change_name_by_idx(idx, new_name)
    def change_name_by_idx(self, idx, new_name):
        res = self.classes[idx].modify_name(new_name)
        self.classes = np.load('./database/class.npy', allow_pickle=True) #维护：class的modify_name中更新了数据库，这里要重新加载
        return res
    
    #通过名称增加类型属性
    def add_att_by_name(self, name, att):
        idx = self.get_index_by_name(name)
        if idx == -1:
            return 0
        else:
            return self.add_att_by_idx(idx, att)
    def add_att_by_idx(self, idx, att):
        res = self.classes[idx].add_att(att)
        self.classes = np.load('./database/class.npy', allow_pickle=True)
        return res
    
    #通过名称删除类型属性
    def remove_att_by_name(self, name, att):
        idx = self.get_index_by_name(name)
        if idx == -1:
            return 0
        else:
            return self.remove_att_by_idx(idx, att)
    def remove_att_by_idx(self, idx, att):
        res = self.classes[idx].remove_att(att)
        self.classes = np.load('./database/class.npy', allow_pickle=True)
        return res
    

#物品本品类
class Item:
    def __init__(self, 
                 name: str,
                 addr: str,
                 #c: Class,
                 attributes,
                 num = 1,
                 unit = "个",
                 info = None,
                 tel = None,
                 wx = None
                 ):
        """
        参数：
        name：物品名
        addr：地址
        attributes：属性，是属性的具体值，*给入时应该保证与c的属性名称一一对应*
        数量和单位、物品介绍、电话和微信号
        """
        self.name = name
        self.addr = addr
        self.attributes = attributes
        self.num = num
        self.unit = unit
        self.info = info
        self.tel = tel
        self.wx = wx
        #class_name：类型名，该属性在物品创建时给予
        
        
    
        
        
    

#helpers

    
    
#classes = np.load('./database/class.npy', allow_pickle=True)


if __name__ == '__main__':
    #测试脚本，直接运行该py即可测试
    #注意：测试代码会刷新数据库，投入使用后不可再运行该脚本
    #类测试
    print("hello world")
    np.save('./database/class.npy',[])
    classes = Classes()


    classes.add_cls('书籍', ["作者","出版社"])
    classes.add_cls('食品',["保质期"])
    cs1 = classes.classes
    print(cs1[1].name)
    #先根据类型对应的att，生成物品
    coke = Item("可口", "X01", ["2020.01.01"])
    coke1 = Item("可口可乐","X02",["11.1"], info = "可口可乐，畅享美味")
    coke2 = Item("百事","X02",["11.1"], info = "可口可乐的完美替代，也能畅享美味")
    #再将物品加入类型
    cs1[1].add_item(coke)
    cs1[1].add_item(coke1)
    cs1[1].add_item(coke2)
    
    cs1[1].remove_item(2)
    
    classes.update()
    cs1 = classes.classes
    
    print(cs1[1].__dict__)
    for i in range(len(cs1[1].items)):
        print("物品："+cs1[1].items[i].name)
    print("*****")
    print(cs1[0].__dict__)
    for i in range(len(cs1[0].items)):
        print("物品："+cs1[0].items[i].name)
   
    
