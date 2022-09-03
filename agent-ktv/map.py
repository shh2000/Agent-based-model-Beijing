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

    def visual_virus(self):
        for i in range(self.width):
            for j in range(self.height):
                print(self.map[i][j]['virus'], end=' ')
            print('')

    def visual_people(self, people):
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


if __name__ == '__main__':
    mymap = Map(20, 20)
    mymap.visual_virus()
