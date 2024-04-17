import re



def remove_duplicates(data):
	countdict = {}
	for element in data:
		if element in countdict.keys():
			 
			# increasing the count if the key(or element)
			# is already in the dictionary
			countdict[element] += 1
		else:
			# inserting the element as key  with count = 1
			countdict[element] = 1
	data.clear()
	for key in countdict.keys():
		data.append(key)
	return data

def remove_subtitle_info(content):
	output_list =  []
	for line in content:
		text = line
		for regex_search_term in regex_search_term_list:
			text = re.sub(regex_search_term, "", text)
		output_list.append(text)
	no_duplicates_output = remove_duplicates(output_list)
	return no_duplicates_output
		
regex_search_term_list = [
"<[0-9][0-9]:[0-9][0-9]:[0-9][0-9]\\.[0-9][0-9][0-9]>",
"<c>",
"</c>",
"[0-9][0-9]:[0-9][0-9]:[0-9][0-9]\\.[0-9][0-9][0-9] --> [0-9][0-9]:[0-9][0-9]:[0-9][0-9]\\.[0-9][0-9][0-9]"
" align:start position:0%",
]


def write_cleaned_subtitle(filename,)


	with open(filename) as f:
		content = f.readlines()

	output_list = remove_subtitle_info(content)


	output_str = "".join(output_list)


	new_filename = filename + "_cleaned.txt"

	with open(new_filename,"w") as f:
		f.write(output_str)

	print("saved",new_filename)
