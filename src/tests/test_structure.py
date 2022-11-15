from structure import Board, Location
SIZE = 5

def test_board():
    board = Board(SIZE)
    assert len(board.rows) == SIZE
    assert board.size == SIZE
    board = Board(-1)
    assert len(board.rows) == 1
    assert board.size == 1
    
    try:
        print(Board(SIZE))
        assert True
    except:
        assert False

def test_location():
    x1 = 0
    y1 = 2
    loc1 = Location(x1, y1)
    assert loc1.x is x1
    assert loc1.y is y1
    assert loc1.validate(1) is False
    assert loc1.validate(3) is True   
    
def run_structure_tests():
    test_board()
    test_location()

if __name__ == "__main__":
    run_structure_tests()