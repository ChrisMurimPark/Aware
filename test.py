import re

pattern = '[0-9]{4}/[0-9]{2}/[0-9]{2}'
re.compile(pattern)
match = re.match(pattern, '2016/01/01')
if match:
	print match.group(0)
