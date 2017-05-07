import BitVector
import os
import sys

class SimpleHash() :
	def __init__(self,capability,seed) :
		self.capability = capability
		self.seed = seed

	def hash(self,value) :
		ret = 0
		for i in range(len(value)) :
			ret += self.seed*ret + ord(value[i])
		return (self.capability - 1) & ret

class BloomFilter() :
	def __init__(self,BIT_SIZE = 1<<25) :
		self.BIT_SIZE = BIT_SIZE
		self.seeds = [5,7,11,13,31,37,61]
		self.bitset = BitVector.BitVector(size = self.BIT_SIZE)
		self.hashFunc = []
		for i in range(len(self.seeds)) :
			self.hashFunc.append(SimpleHash(self.BIT_SIZE,self.seeds[i]))

	def insert(self,value) :
		for f in self.hashFunc :
			loc = f.hash(value)
			self.bitset[loc] = 1

	def is_exit(self,value) :
		if value == None :
			return False
		ret = True
		for f in self.hashFunc :
			loc = f.hash(value)
			ret = ret & self.bitset[loc]
			if ret == False :
				return ret

		return ret


if __name__ == '__main__' :
	b = BloomFilter()
	b.insert('aa')
	b.insert('cc')

	print(b.is_exit('aa'))
	print(b.is_exit('bb'))