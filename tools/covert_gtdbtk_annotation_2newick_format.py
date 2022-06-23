import io
import sys


def add_to_dict(line,all_species):
	
	line_list = line.split(";")
	line_list[-1] = "s__"+line_list[-1].split("|")[1].strip()
	d = line_list[0].split("__")[1]
	if d not in all_species.keys():
		all_species[d]={}
	p = line_list[1].split("__")[1]
	if p not in all_species[d].keys():
		all_species[d][p]={}
	c = line_list[2].split("__")[1]
	if c not in all_species[d][p].keys():
		all_species[d][p][c]={}
	o = line_list[3].split("__")[1]
	if o not in all_species[d][p][c].keys():
		all_species[d][p][c][o]={}
	f = line_list[4].split("__")[1]
	if f not in all_species[d][p][c][o].keys():
		all_species[d][p][c][o][f]={}
	g = line_list[5].split("__")[1]
	if g not in all_species[d][p][c][o][f].keys():
		all_species[d][p][c][o][f][g] = []
	s = line_list[6].split("__")[1]
	all_species[d][p][c][o][f][g].append(s)


def transfrom_dict_to_VK(all_species):
	line_stack=[]
	for d,p_dict in all_species.items():
		floold_num[d] = len(p_dict.keys())
		now_num[d] = 0
		print(d+"(",end="")
		line_stack.append(d)
		for p,c_dict in p_dict.items():
			now_num[d] += 1
			floold_num[p] = len(c_dict.keys())
			now_num[p] = 0
			print(p+"(",end="")
			line_stack.append(p)
			for c,o_dict in c_dict.items():
				now_num[p]+=1
				floold_num[c] = len(o_dict.keys())
				now_num[c] = 0
				print(c+"(",end="")
				line_stack.append(c)
				for o,f_dict in o_dict.items():
					now_num[c] += 1
					print(o+"(",end="")
					line_stack.append(o)
					floold_num[o] = len(f_dict.keys())
					now_num[o] = 0
					for f,g_dict in f_dict.items():
						now_num[o] += 1
						print(f+"(",end="")
						line_stack.append(f)
						floold_num[f] = len(g_dict.keys())
						now_num[f] = 0
						for g,s in g_dict.items():
							now_num[f] += 1
							print(g+"(",end="")
							line_stack.append(g)
							index = 0
							for specie in s:
								index+=1
								if index != len(s):
									print(specie+",",end="")
								else:
									print(specie,end="")
							if len(line_stack)!= 0 :
								print(")",end="")
								line_stack.pop()
							if(now_num[f] != floold_num[f]):
								print(",",end="")
						if len(line_stack)!=0 :
							print(")",end="")
							line_stack.pop()
						if (now_num[o] != floold_num[o]) :
							print(",",end="")
					if len(line_stack)!= 0 :
						print(")",end="")
						line_stack.pop()
					if(now_num[c]!=floold_num[c]):
						print(",",end="")
				if len(line_stack)!= 0 :
					print(")",end="")
					line_stack.pop()
				if(now_num[p]!=floold_num[p]):
					print(",",end="")
			if len(line_stack) != 0 :
				print(")",end="")
				line_stack.pop()
			if(now_num[d]!=floold_num[d]):
				print(",",end="")
		if len(line_stack) != 0 :
			print(")",end="")
			line_stack.pop()
	if len(line_stack)!= 0:
		print(")",end="")
		line_stack.pop()
	print("\n")							

if __name__=="__main__":

	inputfile = sys.argv[1]
	f1 = open(inputfile,'r')
	all_species = {}
	line_stack = []
	floold_num = {}
	now_num = {}

	for line in f1.readlines():
		add_to_dict(line,all_species)

	transfrom_dict_to_VK(all_species)
