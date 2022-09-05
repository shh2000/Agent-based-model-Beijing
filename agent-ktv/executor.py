from map import Map
from person import Person
import random

if __name__ == '__main__':
    random.seed(17373507)

    width = 600  # grid in Beijing
    height = 360  # grid in Beijing
    # for COVID-19,each grid maybe 20m*20m,area of Beijing is 16k km2,
    # so there are 50*50*16k=40M grid, here are only 2M
    hours = 50 * 24
    population = 30000  # population/family in Beijing, maybe 20M or 6M, here are only 0.3M
    # T=O(width*height*popu),
    # so in Beijing, 24 hour need 20*20=400 more time than now
    mobility = 18

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
               'DR_ratio': 0.03,
               'virus_delay': 72  # hour
               }
    mymap = Map(width, height)
    ## simulate KTV
    for i in range(200, 220):
        for j in range(200, 220):
            mymap.set_env(i, j, False)
    for i in range(203, 217):
        for j in range(203, 217):
            mymap.set_env(i, j, True)
    for i in range(200, 203):
        for j in range(208, 212):
            mymap.set_env(i, j, True)

    people = []
    ## normal people
    for i in range(population):
        x, y = random.randint(1, width - 1), random.randint(1, height - 1)
        while not mymap.map[x][y]['accessible']:
            x, y = random.randint(1, width - 1), random.randint(1, height - 1)
        people.append(Person(x, y, mobility=mobility))

    people.append(Person(210, 210, 'Exposed', mobility=mobility))  # import case in KTV

    for i in range(hours):
        # print(i)
        for person in people:
            for step in range(person.mobility):
                person.move(mymap)
                person.release_virus(mymap, epidata)
            person.state_upd_hour(mymap, epidata)
        mymap.state_upd_hour()
        if i % 24 == 0:
            print('Day ' + str(int(i / 24)) + ':')
            state2number = {}
            for person in people:
                if person.state not in state2number.keys():
                    state2number[person.state] = 0
                state2number[person.state] += 1
            for state in ['Susceptible', 'Exposed', 'Unconfirmed', 'Confirmed', 'Recovered', 'Death']:
                number = 0
                if state in state2number.keys():
                    number = state2number[state]
                print(state + ' : ' + str(number), end='; ')
            print('')
        if i % 6 == 0:
            img = mymap.visual_people_img(people)
            img.save(open('pics/' + str(int(i / 6 + 0.01)) + '.jpg', 'w'))
