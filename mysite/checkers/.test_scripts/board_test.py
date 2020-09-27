# simpmle test scirpts for loal work



 61 if __name__ == "__main__":
 62     test_board = board( black_space=[], red_space=[], free_space= [],
 63                        board=[])   #[[0 for i in range(8)] for j in range(8)])
 64     test_board.generate_board("standard")
 65     print(test_board.board)
 66     print("--------")
 67     print(test_board.get_spaces("black"))
 68     print(test_board.space_swap( [6, 'b'] , [26, "r"]))
 69


