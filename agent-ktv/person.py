import random

states = {'Susceptible': 0,
          'Exposed': 1,
          'Unconfirmed': 2,
          'Confirmed': 3,
          'Recovered': 4,
          'Death': 5}


class Person(object):
    def __init__(self, width, height, state='Susceptible'):
        self.state = state
        self.cnt = 0
        self.loc = [random.randint(1, width - 1), random.randint(1, height - 1)]
        self.age = 20
        self.scale = [width, height]

    def move(self, mymap):
        if self.state == 'Confirmed' or self.state == 'Death':
            return
        direct = [[1, 0], [-1, 0], [0, 1], [0, -1]]
        seq = [0, 1, 2, 3]
        random.shuffle(seq)
        for i in seq:
            width = self.loc[0] + direct[i][0]
            height = self.loc[1] + direct[i][1]
            if 0 < width < self.scale[0] and 0 < height < self.scale[1]:
                if mymap[width][height]['accessible']:
                    self.loc = [width, height]
                    return

    def release_virus(self, mymap, epidata):
        if self.state == 'Unconfirmed':
            direct = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [1, -1], [-1, 1], [-1, -1], [2, 0], [0, 2], [-2, 0],
                      [0, -2]]
            for item in direct:
                width = self.loc[0] + item[0]
                height = self.loc[1] + item[1]
                if 0 < width < self.scale[0] and 0 < height < self.scale[1]:
                    if mymap[width][height]['accessible']:
                        mymap[width][height]['virus'] = epidata['virus_delay']

    def state_upd_hour(self, mymap, epidata):
        if self.state == 'Susceptible':
            if mymap[self.loc[0]][self.loc[1]]['virus'] > 0:
                p = random.random()
                if p < epidata['infect_rate']:
                    self.state = 'Exposed'
                    self.cnt = random.randint(epidata['Teu_lower'], epidata['Teu_upper'])
            return
        if self.state == 'Exposed':
            self.cnt -= 1
            if self.cnt < 0:
                self.state = 'Unconfirmed'
                self.cnt = random.randint(epidata['Tui_lower'], epidata['Tui_upper'])
            return
        if self.state == 'Unconfirmed':
            self.cnt -= 1
            if self.cnt < 0:
                self.state = 'Confirmed'
                self.cnt = random.randint(epidata['Tir_lower'], epidata['Tir_upper'])
            return
        if self.state == 'Confirmed':
            self.cnt -= 1
            if self.cnt < 0:
                p = random.random()
                if p < epidata['DR_ratio']:
                    self.state = 'Death'
                else:
                    self.state = 'Recovered'
            return


if __name__ == '__main__':
    person = Person(10, 10)
    mymap = []
    for i in range(1280):
        mymap.append([])
        for j in range(720):
            mymap[i].append({'accessible': True, 'virus': 0})
    for i in range(48):
        person.move(mymap)
        print(person.loc)
