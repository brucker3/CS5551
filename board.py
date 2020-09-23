
class Board:
	
		
	def initboard(self):

		w, h = 8, 8;
		board = [[0 for x in range(w)] for y in range(h)]  # 8*8 array
	
		y = 0
		while y < 8 :

			x = 0

			while x < 8 :

				if((x + y) % 2) == 0:

					board[x][y] = ''

				else:

					board[x][y] = ''
				x +=1
			y +=1

		a = 0
		while a < 7:
			b = 0
			while b < 7:
				print (board[a][b],end = " ")

				b +=1
			print("\n")
				
			a += 1


board_object = Board()
board_object.initboard()





