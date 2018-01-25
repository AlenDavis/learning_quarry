import csv
import random
import tournament_selection as s
import matplotlib.pyplot as plt
from drawnow import *


names=[]
pref=[]
genes = []
size_of_pop = 20
#generations = 2000
cxpb = 0.8
mpb = 0.3

fitness_plot = []
gen = []

class individuals:

    def __init__(self, total_guests,table_size):

        self.formation = init_individuals(total_guests,table_size)
        self.fitness = -1

def init_individuals(total_guests,table_size):

    formation = []
    total_seats = [a for a in range(1,total_guests+1)]

    if(total_guests%table_size>0):
        for _ in range(0,table_size - total_guests%table_size):
            total_seats.append(' ')
        rem = 1

    for _ in range(0,len(total_seats)):
        i = random.choice(total_seats)
        formation.append(i)
        total_seats.remove(i)

    return formation


def get_inp_file():

    inp_file = open("preferences.csv")
    inp_size = open("ip_test.txt")
    rows = csv.reader(inp_file,delimiter = ',')
    total_guests = int(inp_size.readline())
    table_size = int(inp_size.readline())
    inp_size.close()

    next(rows)

    for row in rows:
        names.append(row[0])
        pref.append(row[1:])
    return total_guests,table_size

def init_pop(size_of_pop,total_guests,table_size):

    return [individuals(total_guests,table_size) for _ in xrange(size_of_pop)]

def fitness(population,table_size,total_guests):
    x = 0

    for individual in population:
        fitness = 0
        for i in individual.formation:
            if i == ' ':
                continue

            pos = individual.formation.index(i) + 1
            table_no = pos/table_size


            if pos%table_size:
                table_no += 1

            table_members = individual.formation[(table_no-1 )*table_size:table_no*table_size]
            for j in range(0,total_guests):
                if i-1 == j:
                    continue

                preference = int(pref [i-1][j])
                pos_diff = abs(pos-individual.formation.index(j+1))

                value = get_postion(table_members,i,j,table_size)


                if preference == 1:

                    if value == 1:
                        fitness += 15

                    elif value == 2:
                        fitness += 10

                elif preference == 2:

                    if value == 1:
                        fitness += 15

                elif preference == 4:

                    if value != 2:
                        fitness +=15

                elif preference == 5:

                    if value != 1:
                        fitness += 20

        individual.fitness=fitness
    return population


def get_postion(table_members,i,j,table_size):

    if (j+1 not in table_members):
        return 0    # not in the same table
    elif(abs(table_members.index(i)-table_members.index(j+1))) == 1:
        return 1    # next
    elif(table_size-abs(table_members.index(i)-table_members.index(j+1))) == 1:
        return 1    #next
    else:
        return 2    # on same table


def cross(parent1,parent2,x,y):
    child=[]
    l =len(parent1) + 1
    for i in xrange(len(parent1)):
        child.append('')

        if parent1[i] == ' ':
            parent1[i] = l
            l = l+1

    l = len(parent1) + 1
    for i in xrange(len(parent1)):
        if parent2[i] == ' ':
            parent2[i] = l
            l = l + 1

    child[x:y] = parent1[x:y]
    #for i in range (x,y)
    for  i in range(x,y):
        if parent2[i] in parent1[x:y]:
            continue
        else:
            pos = parent2.index(parent1[i])
            while (pos >= x and pos < y ):
                j = pos
                pos = parent2.index(parent1[j])

            child[pos] = parent2[i]


    for i in range (len(parent2)):

        if child[i] == '':
            child[i] = parent2[i]


    for i in range (len(parent2)):
        if child[i] > len(parent1):
            child[i] = ' '
        if parent1[i] > len(parent1):
            parent1[i] = ' '
        if parent2[i] > len(parent1):
            parent2[i] = ' '

    return child

def crossover(parents,population,cxpb,total_guests,table_size):

    offspring = []

    for i in xrange(len(parents)):
        x=random.choice(parents)

        y=random.choice(parents)
        while (x==y):

            y=random.choice(parents)

        parent1 = population[x].formation
        parent2 = population[y].formation
        split1 = random.randint(0,len(parent1)-1)
        split2 = random.randint(0,len(parent2)-1)



        if split1 > split2:
            split1+=split2
            split2=split1-split2
            split1=split1-split2
        split2 = split2 + 1

        child1 = individuals(total_guests,table_size)
        child2 = individuals(total_guests,table_size)




        if random.uniform(0.00,1.0) < cxpb:
            child1.formation = cross(parent1,parent2,split1,split2)
            child2.formation = cross(parent2,parent1,split1,split2)
            offspring.append(child1)
            offspring.append(child2)



    #population.extend(offspring)
    return offspring

def mutation(offspring):
    #a = []
    for individual in offspring:
        #a =  individual.formation
        for i in xrange(len(individual.formation)):

            if random.uniform(0.00,1) < mpb :
                x = random.randint(0,len(individual.formation)-1)
                if individual.formation[x] != individual.formation[i]:
                    tmp = individual.formation[x]
                    individual.formation[x]=individual.formation[i]
                    individual.formation[i]=tmp

    return offspring

def select_offspring(population,offspring):
    selected_offspring = []
    fit = [individual.fitness for individual in population]
    formation = [individual.formation for individual in population]
    for i in offspring:
        if i.formation not in formation and i.fitness < max(fit):
#        if i.formation not in formation:
            selected_offspring.append(i)
    return selected_offspring


def plot():
    plt.xlabel("Fitness")
    plt.ylabel("Generation")
    plt.plot(gen,fitness_plot)

def write_output(output,table_size):
    with open('output.csv','w') as o:
        #thewriter = csv.Dictwriter(o)
        fieldnames = ['Names','Table No','Seat No']
        thewriter.writerow(fielnames)

        table = 0
        seat = 0

        for i in xrange(len(names)):
            table = output.index(i)/table_size + 1
            seat = output.index(i)%table_size
            if seat == 0:
                seat = table_size
            thewriter.writerow([names(i),table,seat])


def main():

    total_guests,table_size=get_inp_file()
    population = init_pop(size_of_pop,total_guests,table_size)


    population = fitness(population,table_size,total_guests)

    for individual in population:
        print individual.formation,individual.fitness

    #for generation in xrange(generations):
    generation = 0


    plt.ion()

    while(True):
        population = sorted(population, key=lambda individual: individual.fitness, reverse=False)
        fit = [individual.fitness for individual in population]
        parents =  s.selection(fit)
        formations = [individual.formation for individual in population]
        offspring = crossover(parents,population,cxpb,total_guests,table_size)

        offspring = mutation(offspring)
        offspring = fitness(offspring,table_size,total_guests)

        offspring = select_offspring(population,offspring)
        #offspring = population + offspring
        #offspring = sorted(offspring, key=lambda individual: individual.fitness, reverse=False)
        population[len(population)-len(offspring):]=offspring
        #population.extend(offspring)

        generation +=1

        print 'generation:',generation
        population = sorted(population, key=lambda individual: individual.fitness, reverse=False)
        for individual in population:
            print individual.formation,individual.fitness

        fitness_plot.append(population[0].fitness)
        gen.append(generation)
        drawnow(plot)
        plt.pause(0.0000001)



        if (any(individual.fitness == 0 for individual in population)):
            print "Threshold readched"
            break



        #if population[0].fitness == population[len(population)-1].fitness:
        #    print "Less Diversity"
        #    exit(0)
    write_output(population[0].formation,table_size)

main()
