from redis_wrap import *
setup_system(name='other', host='125.218.212.151', port=6379 ,password="27622223")

bears = get_list('bears')
print bears
bears.append('3')