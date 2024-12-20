import random

plastic_trash = [f'plastic-{i}' for i in range(1,4)]
plastic_bin = "plastic"
aluminium_trash = [f'alu-{i}' for i in range(1,4)]
aluminium_bin = "aluminium"
paper_trash = [f'paper-{i}' for i in range(1,4)]
paper_bin = "paper"
waste_trash = [f'waste-{i}' for i in range(1,4)]
waste_bin = "waste"

class Trash():

    def __init__(self, catergory:str, wait_time:int):
        self.catergory = catergory
        self.sprites = "assets\\" + self.get_sprites() + "\\.png"
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
        self.sprites = "assets\\" + self.get_sprites() + "\\.png"
    
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