import itertools
import re
x=u"①周二 - 3,4节②(1-14)周二 - 1,2节"
x=u"①单周周五 - 1,2节"
x=u"①(2-10)周四 - 3,4节②(2-10)周五 - 3,4节"
x=u"①双周(4-14)周二 - 7,8,9节"
def split_ex(a):
  split_string_set=[u"①",u"②",u";",u"③",u"④",u"⑤",u"⑥",u"⑦",u"⑧",u"⑨",u"⑩"]
  for split_string in split_string_set:
     a=a.replace(split_string,u"分割符")
  cset=a.split(u"分割符")
  cset=[i for i in cset if i!='']#确保无空元素
  return cset


def get_weekday(string):
  
  weekday=dict(zip([u"周一",u"周二",u"周三",u"周四",u"周五",u"周六",u"周日"],range(1,8)))
  for k,v in weekday.items():
     if k in string:
       return v

def single_or_double_week(string):
  if string.find(u"双周")>-1:
       return set([i for i in range(1,17) if i%2==0])
  elif string.find(u"单周")>-1:
       return set([i for i in range(1,17) if i%2==1])
  else:
       return set(range(1,17))

def range_week(s):
      if s.find("(")>-1:
        range_string= s[s.index("(")+1 : s.index(")")]
        begin,end=map(int,range_string.split("-"))
        return set(range(begin,end+1))
      else:
        return set(range(1,17))


def get_class_node(string):
    print string
    s=string.split(" - ")[1][:-1].split(",")
    return s


def process_class_text(x):
    total_list=[]
    x= split_ex(x)
    for s in x:
        print s+"g"
    for s in x:
      try:
        week_set=list ( single_or_double_week(s) & range_week(s) )
        weekday=get_weekday(s)
        class_node= get_class_node(s)
        total_list.append((week_set,weekday,class_node))
      except:
        pass
    #print total_list
    return total_list


def process_class_text2(string,position):
  a= split_ex(position)
  list=process_class_text(string)
  new_list=[]

  """
  ①周一 - 7,8节;周三 - 1,2节
  """
  if len(list)>len(a):
    l=len(list)
    a=a*l
  for (week_set,weekday,class_node),position in zip(list,a):
    in_weeks=lambda x: "1" if x in week_set else "0"
    week_string="".join ( map(in_weeks,range(1,17)) )
    week_string #like 0001010101010100
    node_string=",".join(class_node)
    new_list.append({'week':week_string,'weekday':weekday,'node':node_string,'position':position})
  return new_list

if __name__=='__main__':
    print process_class_text(x)
    print process_class_text2(x)
