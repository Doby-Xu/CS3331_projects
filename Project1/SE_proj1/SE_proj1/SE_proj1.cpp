/*
静态管理互助系统 ver1.0

目前只支持将数据存在内存中
暂不支持输入物品数量
*/


#include<iostream>
#include<vector>
#include<string>

using namespace std;

//类：物品
// 
//属性：
//编号	名称	数量	联系方式
//no	name	num		tel
//int	string	int		string
//方法：
//	构造函数Item
//		用法：给出所有属性
//
//	void printItem
//		功能：打印物品信息
//		用法：直接调用

class Item 
{
private:
	int no;
	string name;
	int num;
	string tel;
public:
	Item(int input_no, string input_name, int input_num, string input_tel) 
	{
		no = input_no;
		name = input_name;
		num = input_num;
		tel = input_tel;
	}
	void printItem() {
		cout << "编号No." << no << "\t\t名称：" << name << "\t\t数量：" << num << "\t\t联系方式：" << tel << endl;
	}

	int getNo() {
		return no;
	}
	string getName() {
		return name;
	}
	int getNum() {
		return num;
	}
	string getTel() {
		return tel;
	}
};

void printAll(vector<Item> items)
{
	cout << "\n所有物品：" << endl;
	for (int i = 0; i < items.size(); i++) {
		items[i].printItem();
	}
}

//函数功能：通过编号查找
//参数：物品编号与物品列表，返回：物品在items中所在位置
//备注：在该系统中，编号为物品所特有，物品被删除，则编号也被删除，编号与物品一一对应，但不与物品在items中的位置对应
int searchItemByNo(int no, vector<Item>& items) {
	for (int i = 0; i < items.size(); i++) 
	{
		if (items[i].getNo() == no) return i; 
	}
	return -1;
}

//函数功能：通过输入名称查找物品，打印所有精确匹配项
//参数：物品列表，返回：无
void searchItem(vector<Item> items) {
	string name;
	vector<Item> item_found;

	cout << "\n请输入要搜索物品的名称：\t";
	getline(cin, name);
	for (int i = 0; i < items.size(); i++)
	{
		if (items[i].getName() == name) 
		{
			Item tmp(items[i]);
			item_found.push_back(tmp);
		}
	}
	if (item_found.size()) 
	{
		for (int i = 0; i < item_found.size(); i++)
		{
			item_found[i].printItem();
		}
	}
	else
	{
		cout << "\n没有找到相关物品\n";
	}
}


void addItem(int no, vector<Item>& items) 
{
	string name;
	int num = 1;
	string tel;
	//user input
	cout << "\n请输入所添加物品名称：\t";
	getline(cin, name);
	//cout << "\n请输入物品件数：\t";
	//getchar();
	cout << "\n请输入联系方式：\t";
	getline(cin, tel);

	//add item
	Item new_item(no, name, num, tel);
	items.push_back(new_item);

	new_item.printItem();

	cout << "\n添加成功！\n";
}


bool deleteByNo(int no, vector<Item>& items) 
{
	int i = searchItemByNo(no, items);
	if (i >= 0)
	{
		items.erase(items.begin() + i);
		return 1;
	}
	else return 0;
}

void delItem(vector<Item>& items) 
{
	int no;
	cout << "\n请输入要删除物品的编号：\t";
	cin >> no;
	getchar();
	if (deleteByNo(no, items))cout << "删除成功！" << endl;
	else cout << "未查找到该物品，删除失败" << endl;

}

int main() 
{
	int no = 1;					//初始化物品编号，每个物品将有独一无二的编号
	int op = 0;					//操作
	vector<Item> items;
	while(1)
	{
		op = 0;
		cout << "\n请选择操作：\n1. 搜索物品\n2. 添加物品\n3. 删除物品\n4. 查看所有物品\n";
		cin >> op;
		getchar();
		switch (op)
		{
		case 1:searchItem(items); break;
		case 2:addItem(no, items); no++; break;		//添加物品，编号增加
		case 3:delItem(items); break;
		case 4:printAll(items); break;
		default:
			break;
		}
		system("pause");
	}
	return 0;
}