import random
from map import Map

states = {'Susceptible': 0,
          'Exposed': 1,
          'Unconfirmed': 2,
          'Confirmed': 3,
          'Recovered': 4,
          'Death': 5}


class Person(object):
    def __init__(self, width, height, state='Susceptible', mobility=1):
        self.state = state
        self.cnt = 0
        self.loc = [width, height]
        self.mobility = int(mobility / random.randint(1, mobility) + 0.01)

    def move(self, mymap):
        if self.state == 'Confirmed' or self.state == 'Death':
            return
        direct = [[1, 0], [-1, 0], [0, 1], [0, -1]]
        seq = [0, 1, 2, 3]
        random.shuffle(seq)
        for i in seq:
            width = self.loc[0] + direct[i][0]
            height = self.loc[1] + direct[i][1]
            if 0 < width < mymap.width and 0 < height < mymap.height:
                if mymap.map[width][height]['accessible']:
                    self.loc = [width, height]
                    return

    def release_virus(self, mymap, epidata):
        if self.state == 'Unconfirmed':
            direct = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [1, -1], [-1, 1], [-1, -1], [2, 0], [0, 2], [-2, 0],
                      [0, -2]]
            for item in direct:
                width = self.loc[0] + item[0]
                height = self.loc[1] + item[1]
                if 0 < width < mymap.width and 0 < height < mymap.height:
                    if mymap.map[width][height]['accessible']:
                        mymap.map[width][height]['virus'] = epidata['virus_delay']

    def state_upd_hour(self, mymap, epidata):
        if self.state == 'Susceptible':
            if mymap.map[self.loc[0]][self.loc[1]]['virus'] > 0:
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
    epidata = {'infect_rate': 0.9,
               # hourly/mainly determined by mask and vaccine, have no relationship with mobility/policy
               'Teu_lower': 48,
               'Teu_upper': 96,
               # mean is 3.0(day)
               'Tui_lower': 12,
               'Tui_upper': 96,
               # mean is 1.89(beijing tiantang bar),3.89(beijing 2022.05)(day)
               'Tir_lower': 48,
               'Tir_upper': 120,
               'DR_ratio': 0.01,
               'virus_delay': 72  # hour
               }
    person = Person(220, 220, state='Exposed', mobility=18)
    mymap = Map(500, 500)
    for i in range(200, 240):
        for j in range(200, 240):
            mymap.set_env(i, j, False)
    for i in range(203, 237):
        for j in range(203, 237):
            mymap.set_env(i, j, True)
    for i in range(200, 203):
        for j in range(215, 225):
            mymap.set_env(i, j, True)
    for i in range(48):
        for step in range(person.mobility):
            person.move(mymap)
            person.release_virus(mymap, epidata)
        person.state_upd_hour(mymap, epidata)
        print(person.state, person.loc)
