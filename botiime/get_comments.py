import re


def check_if_ruiping(in_str):
    if re.findall('ime (rp|ruiping|锐评|瑞平|瑞萍)|(rp|ruiping|锐评|瑞平|瑞萍) ', in_str):
        lst = re.match(r'(ime\s(rp|ruiping|锐评|瑞平|瑞萍)|(rp|ruiping|锐评|瑞平|瑞萍)\s)\s*(\S+)\s(.+)', in_str, re.I)
        print(lst.group(1))
        print(lst.group(4))
        print(lst.group(5))
        return str(lst)
