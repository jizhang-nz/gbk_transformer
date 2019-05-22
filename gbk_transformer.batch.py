#!/usr/bin/python3

import argparse
import re
parser = argparse.ArgumentParser()
#parser.add_argument("-i,", "--input", help="the file name of the input GenBank file")
parser.add_argument("-l,", "--list", help="the list of the input GenBank files in a text file")
args = parser.parse_args()
#IN = args.input
LIST = args.list
if LIST:
	with open(LIST, 'r') as list_file:
		inputs = list_file.readlines()
		for IN in inputs:
			IN = IN.rstrip()

			isolate = re.sub(r'\..*', '', IN)
			XLS = isolate + '.xls'
			FNA = isolate + '.fna'
			xls_file = open(XLS, 'w')
			fna_file = open(FNA, 'w')
			counter = -1

			gene_type = ''
			strand = ''
			poz = ''
			locus_tag = ''
			product = ''
			product_extention = ''
			protein_id = ''
			note = ''
			anno_collecting = 'off'
			fna_collecting = 'off'
			contig = 1
			fna = ''

			if IN:
				print ("\nprocessing " + IN + "...")
				with open(IN, 'r') as input_file:
					lines = input_file.readlines()
					line_len = len(lines);
					for line in lines:
						if re.match('//\n', line):
							fna_collecting = 'off'
							head = '>' + isolate + '_' + contig_str + '\n'
							fna = fna + '\n'
							fna_file.write(head)
							fna_file.write(fna)
							fna = ''
							contig += 1
						if re.match('ORIGIN      \n', line):
							fna_collecting = 'on'
						if re.match(' +[0-9]+ ', line) and fna_collecting == 'on':
							seq = line
							seq = re.sub(r'\s', '', seq)
							seq = re.sub(r'\d', '', seq)
							fna = fna + seq
						if re.match('     gene            ', line):
							anno_collecting = 'on'
							counter += 1
							if counter >= 1:
								counter_str = str(counter)
								contig_str = str(contig)
								contig_str = 'contig_' + contig_str
								xls = contig_str + '\t' + counter_str + '\t' + gene_type + '\t' + strand + '\t' + poz + '\t' + locus_tag + '\t' + product + '\t' + protein_id + '\t' + note + '\n'
								xls_file.write(xls)
								xls = ''
								gene_type = ''
								strand = ''
								poz = ''
								locus_tag = ''
								product = ''
								product_extention = ''
								protein_id = ''
								note = ''
							else:
								xls = 'contig\tfeature_sn\ttype\tstrand\tposition\tlocus_tag\tproduct\tprotein_id\tnote\n'
								xls_file.write(xls)
								xls = ''

						if re.match('     CDS             ', line) or re.match('     tRNA            ', line) or re.match('     rRNA            ', line) or re.match('                     ', line):
							if anno_collecting == 'on':
								if re.match('     CDS             complement', line):
									gene_type = 'CDS'
									strand = '-'
									poz = line.replace('     CDS             complement(', '')
									poz = poz.replace(')\n', '')
								elif re.match('     CDS             [0-9]+', line):
									gene_type = 'CDS'
									strand = '+'
									poz = line.replace('     CDS             ', '')
									poz = poz.replace('\n', '')
								elif re.match('     tRNA            complement', line):
									gene_type = 'tRNA'
									strand = '-'
									poz = line.replace('     tRNA            complement(', '')
									poz = poz.replace(')\n', '')
								elif re.match('     tRNA            [0-9]+', line):
									gene_type = 'tRNA'
									strand = '+'
									poz = line.replace('     tRNA            ', '')
									poz = poz.replace('\n', '')
								elif re.match('     rRNA            complement', line):
									gene_type = 'rRNA'
									strand = '-'
									poz = line.replace('     rRNA            complement(', '')
									poz = poz.replace(')\n', '')
								elif re.match('     rRNA            [0-9]+', line):
									gene_type = 'rRNA'
									strand = '+'
									poz = line.replace('     rRNA            ', '')
									poz = poz.replace('\n', '')
								elif re.match('                     /gene=\"', line):
									gene = line.replace('                     /gene=\"', '')
									gene = gene.replace('\"\n', '')
								elif re.match('                     /locus_tag=\"', line):
									locus_tag = line.replace('                     /locus_tag=\"', '')
									locus_tag = locus_tag.replace('\"\n', '')
								elif re.match('                     /product=\"', line):
									product = line.replace('                     /product=\"', '')
									product = product.replace('\"\n', '')
									product = product.replace('\n', '')
								elif re.match('                     [a-z]+', line):
									product_extention = line.replace('                     ', '')
									product_extention = product_extention.replace('\"\n', '')
									product_extention = product_extention.replace('\n', '')
									product = product + " " + product_extention
								elif re.match('                     /pseudogene=\"', line):
									product = 'pseudogene'
								elif re.match('                     /protein_id=\"', line):
									protein_id = line.replace('                     /protein_id=\"', '')
									protein_id = protein_id.replace('\"\n', '')
								elif re.match('                     /note=\"', line):
									note = line.replace('                     /note=\"', '')
									note = note.replace('\"\n', '')
						elif re.match('     gene            ', line):
							anno_collecting = 'on'
						else:
							anno_collecting = 'off'

			else:
				print ("the input file name is missing")

			xls_file.close()
			fna_file.close()
			print (counter_str + " features were extracted from " + IN + " ...")
	list_file.close()
