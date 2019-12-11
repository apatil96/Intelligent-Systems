##..........
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt1
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
import networkx as nx
#..........
import copy
import webbrowser
import timeit
painted = {}
retreat = 0
domain_singleton = 0
heuristic_for_depth_first_search = 0
#.................. create the map
map1 = Basemap(llcrnrlon=-119,llcrnrlat=22,urcrnrlon=-64,urcrnrlat=49,projection='lcc',lat_1=33,lat_2=45,lon_0=-95)
#.................. load the shapefile, use the name 'states'
map1.readshapefile(r'''c:\users\amitp\desktop\st99_d00''', name='states', drawbounds=True)
state_names = []
for shape_dict in map1.states_info:
   state_names.append(shape_dict['NAME'])
ax = plt.gca()


def verify_proof(map):
    for child, after in map.items():
        assert (child not in after)  # Children are not connected to themselves
        for later in after:
            assert (later in map and child in map[later])  #  Connection B to A infers connection A to B


# Depth First Search Only

def next_door_value_get(region, nation, nation_assignment):
    if heuristic_for_depth_first_search == 0:
        return nation[region]
    else:
        if domain_singleton == 0:
            information_added_for_states = [
                (
                    -len({painted[next_neighbor] for next_neighbor in nation[number] if next_neighbor in painted}),
					# prevents the assignment of colors to values with colors
                    -len({next_neighbor for next_neighbor in nation[number] if next_neighbor not in painted}),
                    #Subtracts the value of the node next door if no color is applied to this state
					# Now the neighbor number is calculated
                    number
                ) for number in nation[region] if number not in painted]
        else:
            information_added_for_states = [
                (
                    -len({painted[next_neighbor] for next_neighbor in nation[number] if next_neighbor in painted}),
                    # prevents the assignment of colors to values with colors
                    -len({next_neighbor for next_neighbor in nation[number] if next_neighbor not in painted}),
                    # Subtracts the value of the node next door if no color is applied to this state
                    # Now the neighbor number is calculated
                    len(nation_assignment[number]),
                    number
                ) for number in nation[region] if number not in painted]

        print(information_added_for_states, "()()()()()")
        information_added_for_states.sort()
        print(information_added_for_states, "--Sort - ()()()()()")
        if domain_singleton == 0:
            candidates = [number for _, _, number in information_added_for_states]
        else:
            candidates = [number for _, _, _, number in information_added_for_states]
        return candidates


def color_assignment_get(region, nation, nation_assignment):
    if heuristic_for_depth_first_search == 0:
        return nation_assignment[region]
    else:
        array = []
        for state_color in nation_assignment[region]:
            color_totals = 0
            array.append([state_color])
            for next_neighbor in nation[region]:
                if state_color in nation_assignment[next_neighbor]:
                    color_totals = color_totals + len(nation_assignment[next_neighbor]) - 1
                else:
                    color_totals = color_totals + len(nation_assignment[next_neighbor])
            array[array.index([state_color])].append(color_totals)
        array = sorted(array, key=lambda array_sort: array_sort[1], reverse=True)
        array = [array_sort[0] for array_sort in array]
        return array


def DFS_path_calculation(region, nation, nation_assignment):
    color_adder = 0
    warning = 0
    global retreat
    for state_color in color_assignment_get(region, nation, nation_assignment):
        for j in nation[region]:
            if j in painted and painted[j] == state_color:
                color_adder = 1
                break
        if color_adder == 1:
            color_adder = 0
            continue
        painted[region] = state_color
        for k in next_door_value_get(region, nation, nation_assignment):
            if k not in painted:
                if (DFS_path_calculation(k, nation, nation_assignment) == False):
                    painted.pop(region)
                    warning = 1
                    break
        if warning == 0:
            print("Color assignment was successful %s to %s" % (painted[region], region))
            return True
        else:
            warning = 0
            continue
    retreat = retreat + 1
    return False


# Depth First Search with Forward Chaining
def domain_decrease(region, nation, attempt_colors):
    for j in nation[region]:
        if painted[region] in attempt_colors[j]:
            attempt_colors[j].remove(painted[region])


def domain_decrease_for_forward_check(state_color, region, nation, attempt_colors):
    array_copy = copy.deepcopy(attempt_colors)
    for j in nation[region]:
        if state_color in array_copy[j]:
            array_copy[j].remove(state_color)
        if not domain_validation(j, array_copy):
            return False
    return True


def domain_validation(region, attempt_colors):
    if not (attempt_colors[region]):
        return False
    return True


def DFS_path_calculation_forward(region, nation, nation_assignment):
    warning = 0
    duplicate = copy.deepcopy(nation_assignment)
    global retreat
    for state_color in color_assignment_get(region, nation, nation_assignment):
		# Temporary values of the colors of the states are stored and used for retreating to previous node
        array = copy.deepcopy(duplicate)
        if domain_decrease_for_forward_check(state_color, region, nation, array) == False:
            continue
        painted[region] = state_color
        print("Attempting to assign an appropriate color %s to %s" % (state_color, region))
        domain_decrease(region, nation, array)
        array[region] = state_color
        if domain_singleton == 1 and heuristic_for_depth_first_search == 0:
            nation[region] = sorted(nation[region], key=lambda array_sort: len(nation_assignment[array_sort]), reverse=False)
        for next_neighbor in next_door_value_get(region, nation, nation_assignment):
            if next_neighbor not in painted:
                if (DFS_path_calculation_forward(next_neighbor, nation, array)) == False:
                    painted.pop(region)
                    warning = 1
                    break
        if warning == 0:
            print("Color assignment was successful %s to %s" % (painted[region], region))
            return True
        else:
            warning = 0
            continue
    retreat = retreat + 1
    return False


WestAustralia = 'WestAustralia'
NorthTerritory = 'NorthTerritory'
SouthAustralia = 'SouthAustralia'
Queensland = 'Queensland'
NewSouthWales = 'NewSouthWales'
Victoria = 'Victoria'
Tasmania = 'Tasmania'

Commonwealth_of_Australia = {
    Tasmania: {Victoria},
    WestAustralia: {NorthTerritory, SouthAustralia},
    NorthTerritory: {WestAustralia, Queensland, SouthAustralia},
    SouthAustralia: {WestAustralia, NorthTerritory, Queensland, NewSouthWales, Victoria},
    Queensland: {NorthTerritory, SouthAustralia, NewSouthWales},
    NewSouthWales: {Queensland, SouthAustralia, Victoria},
    Victoria: {SouthAustralia, NewSouthWales, Tasmania}
}

colors_australia = {
    Tasmania: ['red', 'green', 'blue'],
    WestAustralia: ['red', 'green', 'blue'],
    NorthTerritory: ['red', 'green', 'blue'],
    SouthAustralia: ['red', 'green', 'blue'],
    Queensland: ['red', 'green', 'blue'],
    NewSouthWales: ['red', 'green', 'blue'],
    Victoria: ['red', 'green', 'blue']
}

Alabama = "Alabama"
Alaska = "Alaska"
Arizona = "Arizona"
Arkansas = "Arkansas"
California = "California"
Colorado = "Colorado"
Connecticut = "Connecticut"
Delaware = "Delaware"
Florida = "Florida"
Georgia = "Georgia"
Hawaii = "Hawaii"
Idaho = "Idaho"
Illinois = "Illinois"
Indiana = "Indiana"
Iowa = "Iowa"
Kansas = "Kansas"
Kentucky = "Kentucky"
Louisiana = "Louisiana"
Maine = "Maine"
Maryland = "Maryland"
Massachusetts = "Massachusetts"
Michigan = "Michigan"
Minnesota = "Minnesota"
Mississippi = "Mississippi"
Missouri = "Missouri"
Montana = "Montana"
Nebraska = "Nebraska"
Nevada = "Nevada"
NewHampshire = "NewHampshire"
NewJersey = "NewJersey"
NewMexico = "NewMexico"
NewYork = "NewYork"
NorthCarolina = "NorthCarolina"
NorthDakota = "NorthDakota"
Ohio = "Ohio"
Oklahoma = "Oklahoma"
Oregon = "Oregon"
Pennsylvania = "Pennsylvania"
RhodeIsland = "RhodeIsland"
SouthCarolina = "SouthCarolina"
SouthDakota = "SouthDakota"
Tennessee = "Tennessee"
Texas = "Texas"
Utah = "Utah"
Virginia = "Virginia"
Vermont = "Vermont"
Washington = "Washington"
WestVirginia = "WestVirginia"
Wisconsin = "Wisconsin"
Wyoming = "Wyoming"

all_state_of_the_US = {
    Alabama: {Georgia, Florida, Tennessee, Mississippi},
    Alaska: {Washington},
    Arizona: {California, Nevada, Utah, Colorado,  NewMexico},
    Arkansas: {Missouri, Oklahoma, Texas, Louisiana, Tennessee, Mississippi},
    California: {Oregon, Nevada, Arizona, Hawaii},
    Colorado: {Wyoming, Nebraska, Kansas, Oklahoma,  NewMexico, Arizona, Utah},
    Connecticut: { NewYork,  RhodeIsland, Massachusetts},
    Delaware: {Maryland, Pennsylvania,  NewJersey},
    Florida: {Alabama, Georgia},
    Georgia: { SouthCarolina,  NorthCarolina, Tennessee, Alabama, Florida},
    Hawaii: {California},
    Idaho: {Washington, Montana, Oregon, Wyoming, Utah, Nevada},
    Illinois: {Wisconsin, Iowa, Missouri, Kentucky, Indiana, Michigan},
    Indiana: {Michigan, Illinois, Kentucky, Ohio},
    Iowa: {Minnesota,  SouthDakota, Nebraska, Missouri, Wisconsin, Illinois},
    Kansas: {Nebraska, Colorado, Oklahoma, Missouri},
    Kentucky: {Indiana, Illinois, Missouri, Tennessee, Ohio,  WestVirginia, Virginia},
    Louisiana: {Arkansas, Texas, Mississippi},
    Maine: { NewHampshire},
    Maryland: {Pennsylvania,  WestVirginia, Virginia, Delaware},
    Massachusetts: { NewYork, Vermont,  NewHampshire, Connecticut,  RhodeIsland},
    Michigan: {Illinois, Wisconsin, Indiana, Ohio},
    Minnesota: { NorthDakota,  SouthDakota, Iowa, Wisconsin},
    Mississippi: {Tennessee, Arkansas, Louisiana, Alabama},
    Missouri: {Iowa, Nebraska, Kansas, Oklahoma, Arkansas, Illinois, Kentucky, Tennessee},
    Montana: {Idaho, Wyoming,  SouthDakota,  NorthDakota},
    Nebraska: { SouthDakota, Colorado, Wyoming, Kansas, Missouri, Iowa},
    Nevada: {Oregon, Idaho, Utah, Arizona, California},
     NewHampshire: {Maine, Vermont, Massachusetts},
     NewJersey: { NewYork, Pennsylvania, Delaware},
     NewMexico: {Arizona, Utah, Colorado, Oklahoma, Texas},
     NewYork: {Pennsylvania,  NewJersey, Connecticut, Massachusetts, Vermont},
     NorthCarolina: {Georgia, Tennessee,  SouthCarolina, Virginia},
     NorthDakota: {Montana,  SouthDakota, Minnesota},
    Ohio: {Michigan, Indiana, Kentucky,  WestVirginia, Pennsylvania},
    Oklahoma: {Kansas, Colorado,  NewMexico, Texas, Arkansas, Missouri},
    Oregon: {Washington, Idaho, Nevada, California},
    Pennsylvania: {Ohio,  WestVirginia, Delaware,  NewJersey,  NewYork, Maryland},
     RhodeIsland: {Connecticut, Massachusetts},
     SouthCarolina: {Georgia,  NorthCarolina},
     SouthDakota: { NorthDakota, Montana, Wyoming, Nebraska, Minnesota, Iowa},
    Tennessee: {Kentucky, Arkansas, Mississippi, Missouri, Alabama, Georgia,  NorthCarolina, Virginia},
    Texas: {Oklahoma,  NewMexico, Arkansas, Louisiana},
    Utah: {Idaho, Nevada, Wyoming, Colorado, Arizona,  NewMexico},
    Vermont: {Massachusetts,  NewYork,  NewHampshire},
    Virginia: { WestVirginia, Kentucky,  NorthCarolina, Tennessee, Maryland},
    Washington: {Oregon, Idaho, Alaska},
     WestVirginia: {Ohio, Virginia, Kentucky, Pennsylvania, Maryland},
    Wisconsin: {Minnesota, Illinois, Michigan, Iowa},
    Wyoming: {Montana,  SouthDakota, Nebraska, Colorado, Utah, Idaho},
}

United_States_final_colors = {
    Alabama: ['red', 'green', 'blue', 'yellow'],
    Alaska: ['red', 'green', 'blue', 'yellow'],
    Arizona: ['red', 'green', 'blue', 'yellow'],
    Arkansas: ['red', 'green', 'blue', 'yellow'],
    California: ['red', 'green', 'blue', 'yellow'],
    Colorado: ['red', 'green', 'blue', 'yellow'],
    Connecticut: ['red', 'green', 'blue', 'yellow'],
    Delaware: ['red', 'green', 'blue', 'yellow'],
    Florida: ['red', 'green', 'blue', 'yellow'],
    Georgia: ['red', 'green', 'blue', 'yellow'],
    Hawaii: ['red', 'green', 'blue', 'yellow'],
    Idaho: ['red', 'green', 'blue', 'yellow'],
    Illinois: ['red', 'green', 'blue', 'yellow'],
    Indiana: ['red', 'green', 'blue', 'yellow'],
    Iowa: ['red', 'green', 'blue', 'yellow'],
    Kansas: ['red', 'green', 'blue', 'yellow'],
    Kentucky: ['red', 'green', 'blue', 'yellow'],
    Louisiana: ['red', 'green', 'blue', 'yellow'],
    Maine: ['red', 'green', 'blue', 'yellow'],
    Maryland: ['red', 'green', 'blue', 'yellow'],
    Massachusetts: ['red', 'green', 'blue', 'yellow'],
    Michigan: ['red', 'green', 'blue', 'yellow'],
    Minnesota: ['red', 'green', 'blue', 'yellow'],
    Mississippi: ['red', 'green', 'blue', 'yellow'],
    Missouri: ['red', 'green', 'blue', 'yellow'],
    Montana: ['red', 'green', 'blue', 'yellow'],
    Nebraska: ['red', 'green', 'blue', 'yellow'],
    Nevada: ['red', 'green', 'blue', 'yellow'],
     NewHampshire: ['red', 'green', 'blue', 'yellow'],
     NewJersey: ['red', 'green', 'blue', 'yellow'],
     NewMexico: ['red', 'green', 'blue', 'yellow'],
     NewYork: ['red', 'green', 'blue', 'yellow'],
     NorthCarolina: ['red', 'green', 'blue', 'yellow'],
     NorthDakota: ['red', 'green', 'blue', 'yellow'],
    Ohio: ['red', 'green', 'blue', 'yellow'],
    Oklahoma: ['red', 'green', 'blue', 'yellow'],
    Oregon: ['red', 'green', 'blue', 'yellow'],
    Pennsylvania: ['red', 'green', 'blue', 'yellow'],
     RhodeIsland: ['red', 'green', 'blue', 'yellow'],
     SouthCarolina: ['red', 'green', 'blue', 'yellow'],
     SouthDakota: ['red', 'green', 'blue', 'yellow'],
    Tennessee: ['red', 'green', 'blue', 'yellow'],
    Texas: ['red', 'green', 'blue', 'yellow'],
    Utah: ['red', 'green', 'blue', 'yellow'],
    Virginia: ['red', 'green', 'blue', 'yellow'],
    Vermont: ['red', 'green', 'blue', 'yellow'],
    Washington: ['red', 'green', 'blue', 'yellow'],
     WestVirginia: ['red', 'green', 'blue', 'yellow'],
    Wisconsin: ['red', 'green', 'blue', 'yellow'],
    Wyoming: ['red', 'green', 'blue', 'yellow'],
}



#children are not deleted from array and were used for debugging 
all_state_of_the_US = {number: next_neighbor for number, next_neighbor in all_state_of_the_US.items() if next_neighbor}

def CreateGraph():
     Gr = nx.Graph()
     for edge in tempList:
         Gr.add_edge(edge[0],edge[1])
     return Gr
def DrawGraph(G,painted):
    pos = nx.spring_layout(G)
#    if G.node==
    val=painted.values()
    nx.draw(G, pos, with_labels = True,node_size= 500, node_color = val, edge_color = 'black' ,width = 1, alpha = .7)  #with_labels=true is to show the node number in the output graph

if __name__ == '__main__':

    print("\n1. Map of America")
    print("2. Map of Australia")
    nation_name = int(input("\nSelect the country in which you want to see the map coloring for:\n "))

    name_of_country = ""
    name_complete = {}
    state_color = {}
    short_name = ""

    if nation_name == 1:
        name_of_country = "United_States_of_America"
        name_complete = all_state_of_the_US
        state_color = United_States_final_colors
        short_name =  NorthCarolina
        flag = 1
    elif nation_name == 2:
        name_of_country = "Australia"
        name_complete = Commonwealth_of_Australia
        state_color = colors_australia
        short_name = NewSouthWales
        flag = 2
    else:
        print("Incorrect value! Please enter a correct value!")
        exit(0)

    verify_proof(all_state_of_the_US)
    print("\n1. Depth First Search Only")
    print("2. Depth First Search with Forward Chaining")
    print("3. Depth First Search with Forward Chaining and Singleton")
    print("4. Depth First Search With Heuristic")
    print("5. Depth First Search with Heuristic and Forward Chaining")
    print("6. Depth First Search with heuristic, Forward Chaining and singleton")
    type_of_algorithm = int(input("\nPlease choose the algorithm you want to see the visualization for:\n"))
    timer_start = timeit.default_timer()
    if type_of_algorithm == 1:
        if (DFS_path_calculation(short_name, name_complete, state_color)):
            print("Adding color values", len(painted.keys()))
            stt=list(painted.keys())
            clr=list(painted.values())
            if flag==1:
                for i in range(len(painted.keys())):
                    seg = map1.states[state_names.index(stt[i])]
                    p= Polygon(seg,facecolor=(clr[i]),edgecolor=clr[i])
                    ax.add_patch(p)
                plt.show()
 #           elif flag==2:
 #               tempList = []

 #               for state, neighbor in Commonwealth_of_Australia.items():
    
 #                   for n in neighbor:
        
 #                       tempList.append([state,n])
 #               E = CreateGraph()
 #               DrawGraph(E, painted)
 #               plt1.show()
 #               print (tempList)	 
    elif type_of_algorithm == 2:
        if (DFS_path_calculation_forward(short_name, name_complete, state_color)):
            print("Adding color values", len(painted.keys()))
            stt=list(painted.keys())
            clr=list(painted.values())
            if flag==1:
                for i in range(len(painted.keys())):
                    seg = map1.states[state_names.index(stt[i])]
                    p= Polygon(seg,facecolor=(clr[i]),edgecolor=clr[i])
                    ax.add_patch(p)
                plt.show()
    elif type_of_algorithm == 3:
        domain_singleton = 1
        if DFS_path_calculation_forward(short_name, name_complete, state_color):
            print("Adding color values", len(painted.keys()))
            stt=list(painted.keys())
            clr=list(painted.values())
            if flag==1:
                for i in range(len(painted.keys())):
                    seg = map1.states[state_names.index(stt[i])]
                    p= Polygon(seg,facecolor=(clr[i]),edgecolor=clr[i])
                    ax.add_patch(p)
                plt.show()
    elif type_of_algorithm == 4:
        heuristic_for_depth_first_search = 1
        if (DFS_path_calculation(short_name, name_complete, state_color)):
            print("Adding color values", len(painted.keys()))
            stt=list(painted.keys())
            clr=list(painted.values())
            if flag==1:
                for i in range(len(painted.keys())):
                    seg = map1.states[state_names.index(stt[i])]
                    p= Polygon(seg,facecolor=(clr[i]),edgecolor=clr[i])
                    ax.add_patch(p)
                plt.show()
    elif type_of_algorithm == 5:
        heuristic_for_depth_first_search = 1
        if (DFS_path_calculation_forward(short_name, name_complete, state_color)):
            print("Adding color values", len(painted.keys()))
            stt=list(painted.keys())
            clr=list(painted.values())
            if flag==1:
                for i in range(len(painted.keys())):
                    seg = map1.states[state_names.index(stt[i])]
                    p= Polygon(seg,facecolor=(clr[i]),edgecolor=clr[i])
                    ax.add_patch(p)
                plt.show()
    elif type_of_algorithm == 6:
        heuristic_for_depth_first_search = 1
        domain_singleton = 1
        if (DFS_path_calculation_forward(short_name, name_complete, state_color)):
            print("Adding color values", len(painted.keys()))
            stt=list(painted.keys())
            clr=list(painted.values())
            if flag==1:
                for i in range(len(painted.keys())):
                    seg = map1.states[state_names.index(stt[i])]
                    p= Polygon(seg,facecolor=(clr[i]),edgecolor=clr[i])
                    ax.add_patch(p)
                plt.show()
    else:
        print("Incorrect value! Please enter a correct value!")
        exit(0)
    timer_stop = timeit.default_timer()
    print('\nTime: ', timer_stop - timer_start)
    print("Number of retreats",retreat)
    painted.clear()
