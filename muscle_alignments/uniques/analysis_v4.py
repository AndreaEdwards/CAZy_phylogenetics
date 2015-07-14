import subprocess
from util import FileHandlers
from Bio.Phylo.TreeConstruction import DistanceCalculator
from Bio import AlignIO


#fasta_files = file_handlers.find_files(file_paths, 'faa')

#for path in fasta_files:
#	cmd = ['perl ./Scripts/MarkerScanner.pl -Bacteria ' + path]
#	subprocess.call(cmd, shell=True)


#file_paths = file_handlers.search_directory()
#pep_files = file_handlers.find_files(file_paths, 'pep')
#
#for path in pep_files:
#	file_name = file_handlers.get_file_name(path)
#	name_list = file_name.split('.')
#	out_file = ''.join([name_list[0] + '_out.' + name_list[1]])
#	cmd = ['muscle -in ' + path + ' -out ' + out_file]
#	subprocess.call(cmd, shell=True)

def run_muscle(path):
	file_name = file_handlers.get_file_name(path)
	name_list = file_name.split('.')
	out_file = ''.join(name_list[0] + '_out.' + name_list[1])
	cmd = ['muscle -in ' + path + ' -out ' + out_file]
	subprocess.call(cmd, shell=True)

def multiprocess_muscle(file_paths, nprocesses):
	def worker(file_paths, out_queue):
		"""The worked function, invoked in a process. The results
		are placed in a dictionary that's pushed to a queue.
	
		Parameters
		----------
		file_paths : list 
			a list of file_paths
		"""
		outdict = {}
		for path in file_paths:
			outdict[n] = run_muscle(path)
		out_queue.put(outdict)

	# Each process will get 'chunksize' paths and a queue to put its output dictionary into
	out_queue = Queue()
	chunksize = int(math.ceil(len(file_paths) / float(nprocesses)))
	processes = []
	#outs = [{} for i in range(threads)]

	for i in range(nprocesses):
		p = multiprocessing.Process(
			target = worker,
			args = (file_paths[chunksize * i:chunksize * (i + 1)], out_queue))
		processes.append(p)
		p.start()

	# Collrect all results into a single result dict. We know how many dicts with results to expect.
	result_dict = {}
	for i in range(nprocesses):
		result_dict.update(out_queue.get())

	# Wait for all worker processes to finish
	for p in processes:
		p.join()

	return resultdict


def find_indices(path):
	file_handlers = FileHandlers()
	#for path in fasta_files:
	indices = []
	open_file = open(path, 'rU')
	file_list = open_file.readlines()
	for line in file_list:
		if '>' in line:
			indices.append(file_list.index(line))
	interval = indices[1] - indices[0]
	file_name = file_handlers.get_file_name(path)
	return file_name, file_list, interval

def write_fasta_new_names(path, file_name, file_list, interval):
	#for path in fasta_files:
	name_list = file_name.split('.')
	out_file = ''.join([name_list[0] + '_new_names.' + name_list[1]])
	new_file = open(out_file, 'w')
	temp_dict = {}
	i = 0
	while i < len(file_list):
		if file_list[i] in temp_dict:
			i += interval
		else:
			temp_dict[file_list[i]] = file_list[i + 1 : i + (interval - 1)]
			new_file.write(file_list[i])
			for item in temp_dict[file_list[i]]:
				new_file.write(item)
			i += interval

def main():
	file_handlers = FileHandlers()
	file_paths = file_handlers.search_directory()
	fasta_files = file_handlers.find_files(file_paths, 'fasta')
	for path in fasta_files:
		file_name, file_list, interval = find_indices(path)
		write_fasta_new_names(path, file_name, file_list, interval)

main()

#fasta_files = file_handlers.find_files(file_paths, 'fasta')
#for path in fasta_files:
#	file_name = file_handlers.get_file_name(path)
#	print 'processing ' + file_name
#	name_list = file_name.split('.')
#	#derep_out_file = ''.join(name_list[0] + '_uniques.fasta')
#	dm_out_file = ''.join(name_list[0] + '_dm.txt')
#	#cmd = ['usearch -derep_fulllength ' + path + ' -fastaout ' + derep_out_file]
#	#subprocess.call(cmd, shell=True)
#	
#	new_file = open('/Users/andrea/repositories/AMPHORA2/muscle_alignments/' + dm_out_file, 'w')
#	aln = AlignIO.read(path, 'fasta')
#	calculator = DistanceCalculator('identity') # identity is the name of the model(scoring matrix) to calculate the distance. The identity model is the default one and can be used both for DNA and protein sequence.
#	dm = calculator.get_distance(aln)
#	new_file.write(dm)
#	new_file.close()








