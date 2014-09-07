#coding:utf-8
import random

sample_line_nums = random.sample(range(12912),200)
sample_line_nums.sort()


with open('raw_test_data.txt') as f:
    test_lines = f.readlines()

with open('tmp_result3') as f:
    result_lines = f.readlines()

with open('sample_data.txt','w') as f:
    for line_num in sample_line_nums:
        line = '%s\t%s' % (line_num+1,test_lines[line_num])
        f.write(line)

with open('sample_results.txt','w') as f:
    for line_num in sample_line_nums:
        line = '%s\t%s' % (line_num+1,result_lines[line_num])
        f.write(line)
    
