import pandas as pd
import math

class Filter:

	def __init__(self, filename):
		data = pd.read_csv(filename)
		self.df = pd.DataFrame(data, columns = ['spam', 'ham'], index = list(data['Unnamed: 0']))
		self.df['spam'] = list(data['spam'])
		self.df['ham'] = list(data['ham'])

	def clean_text(self, text):
		for c in text:
			if c in ['.', '!', '?', '\n', '\t', '-', '¿', '¡', ':', ';']:
				text = text.replace(c, ' ')
			if ord(c) in range(ord('a'), ord('z') + 1) or ord(c) in range(ord('A'), ord('Z') + 1) or c in [' ', 'á', 'é', 'í', 'ó', 'ú', 'Á', 'É', 'Í', 'Ó', 'Ú']:
				pass
			else:
				text = text.replace(c, '')
		return text

	def clean_list(self, w_list):
		aux = list()
		for l in w_list:
			l.replace(' ', '')
			if l != '':
				aux.append(l)
		return aux

	def gen_words(self, text):
		text = self.clean_text(text)
		w_list = text.split(' ')
		w_list = self.clean_list(w_list)
		return w_list

	def classificator(self, text, k):
		w_list, sums = self.gen_words(text), list(self.df.sum())
		probspam = math.log(self.df['spam'].gt(0).sum() + k) - math.log(len(list(self.df.index)) + k*2)
		probham = math.log(self.df['ham'].gt(0).sum() + k) - math.log(len(list(self.df.index)) + k*2)
		for w in w_list:
			if w in list(self.df.index):
				probspam += math.log(list(self.df.loc[w])[0] + k) - math.log(sums[0] + k*len(list(self.df.index)))
				probham += math.log(list(self.df.loc[w])[1] + k) - math.log(sums[1] + k*len(list(self.df.index)))
		if probham >= probspam:
			return True
		else:
			return False