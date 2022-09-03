from map import Map
from person import Person

if __name__ == '__main__':
    widht = 1024  # grid in Beijing
    height = 768  # grid in Beijing
    # for COVID-19,each grid maybe 20m*20m,area of Beijing is 16k km2,
    # so there are 50*50*16k=40M grid, here are only 0.8M
    hours = 20 * 24
    population = 50000  # population/family in Beijing, maybe 20M or 6M, here are only 50k
    # 24 hour need about 1second,T=O(width*height*popu),
    # so in Beijing, 24 hour need 500*100s=12h in R7-5800H/16G

    epidata = {'infect_rate': 0.9,
               # hourly/mainly determined by mask and vaccine, have no relationship with mobility/policy
               'Teu_lower': 48,
               'Teu_upper': 96,
               # mean is 3.0(day)
               'Tui_lower': 12,
               'Tui_upper': 96,
               # mean is 1.89(beijing tiantang bar),3.89(beijing 2022.05)(day)
               'Tir_lower': 72,
               'Tir_upper': 120,
               'DR_ratio': 0.1,
               'virus_delay': 72  # hour
               }

    people = []
    for i in range(population):
        people.append(Person(widht, height))
    people.append(Person(10, 10, 'Exposed'))

    mymap = Map(widht, height)

    for i in range(hours):
        for person in people:
            person.move(mymap.map)
            person.release_virus(mymap.map, epidata)
            person.state_upd_hour(mymap.map, epidata)
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
