import subprocess
from util import FileHandlers
from Bio.Phylo.TreeConstruction import DistanceCalculator
from Bio import AlignIO

file_handlers = FileHandlers()
file_paths = file_handlers.search_directory()
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


fasta_files = file_handlers.find_files(file_paths, 'fasta')
for path in fasta_files:
	file_name = file_handlers.get_file_name(path)
	name_list = file_name.split('.')
	derep_out_file = ''.join(name_list[0] + '_uniques.fasta')
	dm_out_file = ''.join(name_list[0] + '_dm.txt')
	cmd = ['usearch -derep_fulllength ' + path + ' -fastaout ' + derep_out_file]
	subprocess.call(cmd, shell=True)
	
	#new_file = open('/Users/andrea/repositories/AMPHORA2/muscle_alignments/' + out_file, 'w')
	#aln = AlignIO.read(path, 'fasta')
	#calculator = DistanceCalculator('identity') # identity is the name of the model(scoring matrix) to calculate the distance. The identity model is the default one and can be used both for DNA and protein sequence.
	#dm = calculator.get_distance(aln)
	#new_file.write(dm)





#aln = AlignIO.read('/Users/andrea/repositories/AMPHORA2/muscle_alignments/uniques.fasta', 'fasta')
#calculator = DistanceCalculator('identity') # identity is the name of the model(scoring matrix) to calculate the distance. The identity model is the default one and can be used both for DNA and protein sequence.
#dm = calculator.get_distance(aln)
#print dm







