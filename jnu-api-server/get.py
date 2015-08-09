from jwckit.func import *
s=login('2006107','006107')
zhuangye,zhengjianleibie,zhengjianhao,chushengriqi,guoji,xingbie,niandu=get_person_teacher(s)
print zhuangye,zhengjianleibie,zhengjianhao,chushengriqi,guoji,xingbie,niandu
import codecs
f = codecs.open("pru_uni.html", "w", "utf-8")


html=get_socre_teacher(s)
f.write(html)
f.close()