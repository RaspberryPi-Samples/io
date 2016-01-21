import pingo
from button import PushButton

def test_pushbutton():
    board = pingo.detect.get_board()  # pingo.ghost.ghost.GhostBoard
    print(board)
    but_pin = board.pins[13]
    print(but_pin)
    but = PushButton(but_pin)
    but.press()  # just for tests
    assert but.pressed
    but.release()  # just for tests
    assert but.released
