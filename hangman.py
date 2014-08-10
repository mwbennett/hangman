class Hangman:
	def __init__(self, word):
		self.word = word
		self.progress = '-' * len(word)
		self.guessed = []
		self.attempts = 0
		self.chances = 10
	
	def guess_letter(self, letter):
		"""Guess a letter

		Guess a letter towards the word. Returns True on a good guess, and False
		otherwise
		"""
		
		letter = letter.lower()
		
		if len(letter) != 1:
			raise ValueError("Input must be a single letter")
		
		if letter in self.guessed:
			print "You already guessed the letter \'%s\'" % letter
			return False
		
		else:
			self.guessed.append(letter) #add the letter to the list of guessed letters
			self.guessed.sort()
			self.attempts += 1 #increment the number of attempts made

			if letter in self.word:	
				#with word: "joe", would create [(j, 0), (o, 1), (e, 2)]
				positions = [(l, p) for l, p in zip(self.word, range(len(self.word)))]

				#x cycles through the positions of the letters that match the word
				for x in [p for l, p in positions if l == letter]:
					#add the letter to self.progess
					if x == 0:
						self.progress = letter + self.progress[1:]
					else:
						self.progress = self.progress[:x] + letter + self.progress[x + 1:]

				return True
			
			else:
				self.chances -= 1
				return False
	
	def check_winner(self):
		"""Check for a winner

		Returns True if there is a winner, False otherwise
		"""
		return self.word == self.progress


def main():
	import random
	import sys
	
	try:
		words = open("words.txt", 'r')
		count = 0

		for line in words:
			count += 1

		words.seek(0)
		wordlist = words.readlines()
		word = wordlist[random.randint(1, count)] #fetch a random word from the word file
		word = word[:len(word) - 1] #get rid of space at the end of the word
		
	except IOError, ioe:
		print "Necessary file \"words.txt\" not found."
		sys.exit()
	
	else:
		h = Hangman(word)
		while h.chances  > -1:
			try:
				print "\n\n\t%s" % h.progress
				
				if h.check_winner():
					print "Excellent! You guessed the secret word in %d attempts!" % h.attempts
					sys.exit()

				print "\nGuessed letters", h.guessed
				print "Bad guesses left: ", h.chances
				
				letter = raw_input("\n\tEnter letter to guess: ")
				if h.guess_letter(letter):
					print "\nGood guess!"
					continue
				else:
					print "\nBad guess. Try again."
				
			except ValueError, ve:
				print ve
				continue

		print "\n\nYou ran out of guesses! The word was \"%s\"" % h.word
		sys.exit()
		
if __name__ == "__main__":
	main()
