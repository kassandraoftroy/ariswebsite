# -*- coding: utf-8 -*-
from operator import itemgetter
import random
from gensim import models
import numpy as np
import os
import pickle

characters = "1 2 3 4 5 6 7 8 9 0 * & ^ ) ( } { | ] [ ' < > @ . ! ? # $ % , ~ ≈ ç √ ∫ µ ∂ ß ˚ å ø - ∂ ¨ ƒ ¥ © ˙ ∑ œ π : ; – º _ ª • § ¶ ∞ ¢ £ ™ ¡ ª – ≠ “ ‘ « “ π ø ˆ ¨ ¥ † ∑ ® œ ¡ ™ £ ÷ ≥ ç √ ≤ ∫ µ Ω ˜ ∆ ƒ ˙ © ƒ ¥ ¨ å"
stop_char = characters.split()
stop_char.append('"')
model = models.KeyedVectors.load_word2vec_format("/Users/Earth/Desktop/17kVec.txt", binary=False)

class Copy_Cat:

	def __init__(self, pickled_file):
		with open(pickled_file, "rb") as f:
			self.sentences = pickle.load(f)

	def response(self, paragraph_input):
		formatted_input_sentence = None
		words_input = paragraph_input.split()
		####clean sentences
		A_sentence = []
		B_sentence = []
		for word in words_input:
			A_sentence.append(word.lower())
		for word in A_sentence:
			for character in word:
				if character in stop_char:
					word = word.replace(character, "")
			B_sentence.append(word)
		good_words = []
		for word in B_sentence:
			try:
				model[word]
				good_words.append(word)
			except:
				pass
		if good_words!=[]:
			formatted_input_sentence = " ".join(good_words)
		if formatted_input_sentence == None or formatted_input_sentence == " ":
			return "sorry I don't understand any of '%s'" %(paragraph_input)

		Q = formatted_input_sentence
		print Q
		Q_avg = np.sum(np.array([model[word] for word in Q.split()]), axis=0)/np.linalg.norm(np.sum(np.array([model[word] for word in Q.split()]), axis=0))
		similarity = []
		for X in self.sentences:
			R = []
			for w in X[0].split():
				try:
					ppp = model[w]
					if w != " " and w != "":
						R.append(w)
				except:
					pass
			if R != []:
				try:
					R_avg = np.sum(np.array([model[word] for word in R]), axis=0)/np.linalg.norm(np.sum(np.array([model[word] for word in R]), axis=0))
					similarity.append((X[1], np.dot(Q_avg, R_avg)))
				except:
					pass
		return sorted(similarity, key=itemgetter(1), reverse=True)[0][0]