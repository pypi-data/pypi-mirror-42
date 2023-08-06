"""This is the standard way to include a multiple-line comment in your code"""
def print_lol(the_list):
	"""这个函数可以对列表的每一个元素进行输出"""
	for each_item in the_list:
		if isinstance(each_item,list):
			print_lol(each_item)
		else: 
			print(each_item)