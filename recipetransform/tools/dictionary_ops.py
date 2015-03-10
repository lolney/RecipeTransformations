def setDict(keys, dict, value):

	for key in keys:
		if key not in dict:
			dict[key] = {}

	return dict

def addDict(key, dict, value):

	if key in dict:
		dict[key] = dict[key] + value
	else:
		dict[key] = value

	return dict

def addItemToDict(key, dict, value):

	if key in dict:
		dict[key].append(value)
	else:
		dict[key] = [value]
	return dict

def addListToDict(key, dict, value):

	if key in dict:
		pass
	else:
		dict[key] = value
	return dict