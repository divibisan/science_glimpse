import os
import pandas as pd
import re
import textract

all_files = os.walk('.')
all_files = list(all_files)[1:]

student_data = {}

for block_list in all_files:
	dir = block_list[0]
	glimpse_num = re.search('glimpse ?([0-9])_', dir).group(1)
	files = block_list[2]
	if glimpse_num not in student_data.keys():
		student_data[glimpse_num] = {}
	for file in files:
		if not file.startswith('.DS'):
			print(file)
			student_name = file.split(' -')[0]
			text = textract.process(os.path.join(dir,file), encoding = 'utf_8')
			try:
				cite = re.search(b'Science News article here:([\s\S]*?)(Use )?Google Scholar', text).group(1)
				cite = cite.decode('UTF-8')
				cite = cite.strip(' \n\t')
				cite = cite.replace('\n', ' ')
				print(cite)
			except AttributeError:
				print('ERROR: Cannot find article info in text')
				print(text)
			student_data[glimpse_num][student_name] = cite

data_frame = pd.DataFrame.from_dict(student_data)
data_frame.to_csv('science_news_glimpse.csv')