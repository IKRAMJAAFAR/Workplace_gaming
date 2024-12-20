import random

plastic_trash = []
plastic_bin = ""
aluminium_trash = []
aluminium_bin = ""
paper_trash = []
paper_bin = ""
waste_trash = []
waste_bin = ""

class Trash():

    def __init__(self, catergory:str, wait_time:int):
        self.catergory = catergory
        self.sprites = self.get_sprites()
        self.wait_time = wait_time

    def get_sprites(self):
        if self.catergory == "Plastic":
            return random.choice(plastic_trash)
        elif self.catergory == "Aluminium":
            return random.choice(aluminium_trash)
        elif self.catergory == "Paper":
            return random.choice(paper_trash)
        else:
            return random.choice(waste_trash)


class Bin():

    def __init__(self, catergory:str):
        self.catergory = catergory
        self.sprites = self.get_sprites()
    
    def get_sprites(self):
        if self.catergory == "Plastic":
            return plastic_bin
        elif self.catergory == "Aluminium":
            return aluminium_bin
        elif self.catergory == "Paper":
            return paper_bin
        else:
            return waste_bin

    def check_trash(self,trash: Trash):
        return trash.catergory == self.catergory