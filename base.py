class Game:
    pass

class Tab:
    def __init__(self):
        self.tab = {str(i): list(8*" ") for i in range(8, 0, -1)}

    def show(self):
        for i in self.tab.values():
            print(i)

    def get_tile(self, line, column):
        return self.tab[line][column]

    def set_tile(self, line, column, key):
        self.tab[line][column] = key

class Key:
    def __init__(self, tab: Tab, color, line, column):
        self.position = [line, column]
        self.tab = tab
        self.tab.set_tile(*self.position, self)
        self.color = color
    
    def move(self, line, column):
        pass

    def attack(self, line, column):
        pass

class Pawn(Key):
    def __init__(self, *kwargs):
        super().__init__(*kwargs)
    
    def move(self, line, column):
        is_empty = self.tab.get_tile(*self.position) == ' '
        is_in_front = self.position[1] == column and line
        if :
            self.tab.set_tile(*self.position, ' ')
            self.position = [line, column]
            self.tab.set_tile(*self.position, self)
        return super().move(line, column)


class Knight(Key):
    pass

class King(Key):
    pass

class Queen(Key):
    pass

class Bishop(Key):
    pass

class Rook(Key):
    pass


Tab().show()