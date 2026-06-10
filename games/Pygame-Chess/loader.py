from pathlib import Path
import pygame

class Loader:
    def __init__(self):
        self.black_pieces={}
        self.white_pieces={}
        self.board_pieces={}
    def get_file_extension(self,filename):
        return filename.split('.')[-1]
    def load_pieces(self):
        #loads the black and white pixels and stores it in the attribute
        pixel = Path('./assets/board_pixels')
        for file in pixel.iterdir():
            if file.is_file() and file.name!=".DS_Store":
                if file.name.startswith("black"):
                    image=pygame.image.load(file).convert_alpha()
                    self.board_pieces['black']=image
                else:
                    image=pygame.image.load(file)
                    self.board_pieces['white']=image
        #loads the black chess pieces and stores in black_pieces attribute
        black_pieces=Path("./assets/pieces/black")
        for file in black_pieces.iterdir():
            if file.is_file() and file.name!=".DS_Store":
                image=pygame.image.load(file).convert_alpha()
                extension=self.get_file_extension(file.name)
                self.black_pieces[file.name.removesuffix(f".{extension}")]=image
        #loads the white chess pieces and stores in white_pieces attribute
        black_pieces=Path("./assets/pieces/white")
        for file in black_pieces.iterdir():
            if file.is_file() and file.name!=".DS_Store":
                image=pygame.image.load(file).convert_alpha()
                extension=self.get_file_extension(file.name)
                self.white_pieces[file.name.removesuffix(f".{extension}")]=image
    def convert(self):
        for i in self.white_pieces:
                print(i)
        pixel_width=(90,90)
        piece_width=(72,72)
        #resize black pieces
        for i in self.black_pieces:
            image=self.black_pieces[i]
            resized_image=pygame.transform.scale(image,piece_width)
            self.black_pieces[i]=resized_image
        #resize white pieces
        for i in self.white_pieces:
            image=self.white_pieces[i]
            resized_image=pygame.transform.scale(image,piece_width)
            self.white_pieces[i]=resized_image
        #resize the board pixels
        for i in self.board_pieces:
            image=self.board_pieces[i]
            resized_image=pygame.transform.scale(image,pixel_width)
            self.board_pieces[i]=resized_image
   
