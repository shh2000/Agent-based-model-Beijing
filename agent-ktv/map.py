from PIL import Image
import numpy as np


class Map(object):
    def __init__(self, width, height):
        self.map = []
        self.width = width
        self.height = height
        for i in range(width):
            self.map.append([])
            for j in range(height):
                self.map[i].append({'accessible': True, 'virus': 0})
                # use accessible to simulate policy
                # use virus to simulate virus at the grid

    def state_upd_hour(self):
        for i in range(self.width):
            for j in range(self.height):
                if self.map[i][j]['virus'] > 0:
                    self.map[i][j]['virus'] -= 1

    def set_env(self, x, y, access):
        self.map[x][y]['accessible'] = access

    def visual_virus(self):
        for i in range(self.width):
            for j in range(self.height):
                print(self.map[i][j]['virus'], end=' ')
            print('')

    def visual_people_stdout(self, people):
        for i in range(self.width):
            for j in range(self.height):
                no_person = True
                for person in people:
                    if person.loc[0] == i and person.loc[1] == j:
                        print(person.state[0] + str(person.cnt), end=' ')
                        no_person = False
                if no_person:
                    print('0', end=' ')
            print('')

    def visual_people_img(self, people):
        img = Image.new('RGB', (self.width, self.height), (0, 0, 0))

        for person in people:
            i = person.loc[0]
            j = person.loc[1]

            if person.state == 'Susceptible':
                img.putpixel((i, j), (30, 144, 255))  # blue
            elif person.state == 'Exposed':
                img.putpixel((i, j), (255, 185, 15))  # orange
            elif person.state == 'Unconfirmed':
                img.putpixel((i, j), (255, 255, 0))  # yellow
            elif person.state == 'Confirmed':
                img.putpixel((i, j), (255, 0, 0))  # red
            elif person.state == 'Recovered':
                img.putpixel((i, j), (0, 255, 0))  # green
            else:
                img.putpixel((i, j), (255, 187, 255))  # pink
        for i in range(self.width):
            for j in range(self.height):
                if not self.map[i][j]['accessible']:
                    img.putpixel((i, j), (255, 255, 255))  # white
        return img


if __name__ == '__main__':
    mymap = Map(20, 20)
    mymap.visual_virus()
