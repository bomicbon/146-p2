from math import sqrtfrom heapq import heappush, heappopdef find_path (source_point, destination_point, mesh):    """    Searches for a path from source_point to destination_point through the mesh    Args:        source_point: starting point of the pathfinder        destination_point: the ultimate goal the pathfinder must reach        mesh: pathway constraints the path adheres to
    Returns:        A path (list of points) from source_point to destination_point if exists        A list of boxes explored by the algorithm    """    path = [] # list that holds all boxes passed through    boxes = {} # dict that maps boxes to all adjacent / explored boxes    box_w_entry = {} # dict that maps box with entry (x,y) pair - from hw doc    queue = [] # heap that contains boxes to explore    dist = {} # dict that maps boxes to path cost    for first_box in mesh['boxes']: #first_box not actually first box        #if source_point[0] >= first_box[0] and source_point[1] >= first_box[2] and source_point[0] <= first_box[1] and source_point[1] <= first_box[3]:        if is_in_box(source_point, first_box): #function that checks if pt in box            current_box = first_box # Selects 1st Box            boxes[current_box] = None #came_from[start] = None            dist[current_box] = 0 # Sets distance of 1st Box    heappush(queue, (0, current_box))    current_point = source_point    while len(queue) is not 0:        box_pair = heappop(queue)        current_box = box_pair[1]        #current_box = heappop(queue)[1] OG        #if current box contains destination point        if is_in_box(destination_point, current_box):            new_cost = dist[current_box] + distance(current_point, destination_point)            current_point = destination_point        if current_point == destination_point:            entry_points = []            entry_points.append(source_point)            entry_points.extend(list(box_w_entry.values()))            for i, item in enumerate(entry_points):                if i+1 < len(entry_points):                    tup1 = entry_points[i]                    tup2 = entry_points[i+1]                    p_tup = (tup1, tup2)                    path.append(p_tup)            break        #boxes[current_box] = [] OG        # Searches all adjacent boxes        # Assigns path to adjacent boxes        for next_box in mesh['adj'][current_box]:            adjacent = adj_edge(current_box, next_box)            temp_point = shortest_to_adj(current_point, adjacent[0], adjacent[1])            new_cost = dist[current_box] + distance(current_point, temp_point)            #boxes[current_box].append(next_box) OG            #boxes[current_box] = next_box            if next_box not in dist or new_cost < dist[next_box]:                dist[next_box] = new_cost                priority = new_cost + distance(temp_point, destination_point) #euc_dist from curr to final                heappush(queue, (priority, next_box)) #Left off here                #path.append(current_box)                #path should have point a to point b, not current_box                #pathline = (current_point, temp_point)                #path.append(pathline) #path is a list of points not boxes                current_point = temp_point                boxes[next_box] = current_box                box_w_entry[next_box] = temp_point                #boxes[current_box].append(next_box)                #boxes[current_box] = next_box    # current should be at destination here    if current_point != destination_point:        raise ValueError('Destination was not reached!')        #return path, boxes.keys() OG        # In Python 3, dict.keys() returns a view, rather than a list.        # Therefore wrap call to dict.values() in a call to list    return path, list(boxes.keys())'''def adj_edge(b1, b2):    """    Args:        b1: origin box        b2: other box    Returns:        A list of two tuples, each with two values.  The two tuples represent two endpoints        of an adjacent edge between the two boxes    """    edge = None    xBorder = [max(b1[0], b2[0]), min(b1[2], b2[2])]    yBorder = [max(b1[1], b2[1]), min(b1[3], b2[3])]    if xBorder[0] == 0 and xBorder[1] == 0:        if b1[1] == b2[3]: # b1 is below b2            edge = [(xBorder[0], b1[1]), (xBorder[1], b1[1])]        else: # b1 is above b2            edge = [(xBorder[0], b1[3]), (xBorder[1], b1[3])]    else:        if b1[0] == b2[2]: # b1 is right of b2            edge = [(b1[0], yBorder[0]), (b1[0], yBorder[1])]        else: # b1 is left of b2            edge = [(b1[2], yBorder[0]), (b1[2], yBorder[1])]    return edge'''def adj_edge(b1, b2):    '''    Args:        b1 = (x1, x2, y1, y2)        b2 = (x1, x2, y1, y2)                         (x1, y1)------------|                            |                |                            |                |                            |                |        (x1, y1)------------|                |        |                   |------------(x2, y2)        |                   |        |                   |        |---------------(x2, y2)                   (x1, y1)------------------|                       |                     |             (x1, y1)--|---------|------(x2, y2)                 |               |                 |               |                 |               |                 |------------(x2, y2)    Return:        edge = [ (x1, y1), (x2, y2) ]    '''    edge = None    x_rng = [max(b1[0], b2[0]), min(b1[1], b2[1])] # [x1, x2]    y_rng = [max(b1[2], b2[2]), min(b1[3], b2[3])] # [y1, y2]    if y_rng[1] - y_rng[0] == 0: # Above/Below        if b1[3] == b2[2]: # Box 1 is ABOVE Box 2        #y2 (b1) == y1 (b2)        #    (b1x1, b1y1)------|        #        |   BOX 1     |         #(b2x1, b2y1)----(b1x2, b1y2)--|        #    |                          |        #    |        BOX 2             |        #    |--------------------(b2x2, b2y2)        #Then: Box 1 is ABOVE Box 2 !!!            edge = [(x_rng[0], b1[3]), (x_rng[1], b2[2])]            return edge        elif b1[2] == b2[3]: # Box 1 is BELOW Box 2        #   y1 (b1) == y2 (b2)        #(b2x1, b2y1)------------------|        #|           BOX 2          |        #|                          |        #|---(b1x1, b1y1)------(b2x2, b2y2)        #        |        |        #        |  BOX 1 |        #        |-----(b1x2, b1y2)        #        Then: Box 1 is BELOW Box 2 !!!            edge = [(x_rng[0], b1[2]), (x_rng[1], b2[3])]            return edge        else: # Bad Cases            return None    elif x_rng[1] - x_rng[0] == 0: # Left/Right        if b1[0] == b2[1]:        # x1 (b1) == x2 (b2)        #                           (b1x1, b1y1)------|        #                               |             |         #(b2x1, b2y1)------------------|             |        #    |                          |   BOX 1     |        #    |         BOX 2            |             |        #    |---------------------(b2x2, b2y2)       |        #                               |             |        #                               |------(b1x2, b1y2)##        Then: Box 1 on Box 2's RIGHT !!!#        '''            edge = [(b1[0], y_rng[0]), (b2[1], y_rng[1])]            return edge        elif b1[1] == b2[0]:#        ''' x1 (b1) == x2 (b2)#         (b1x1, b1y1)--|#            |          |#            |     (b2x1, b2y1)------------------|#            |  BOX 1   |                        |#            |-----(b1x2, b1y2)   BOX 2          |#                       |---------------------(b2x2, b2y2)#        Then: Box 1 on Box 2's LEFT !!!#        '''            edge = [(b1[1], y_rng[0]), (b2[0], y_rng[1])]            return edge        else: # Bad Cases            return None    else: # Worst Corner Cases Ever        return None'''    # Box 1's Y2 == Box 2's Y1    if b1[3] == b2[2]:        edge = [(x_rng[0], b1[3]), (x_rng[1], b2[2])]        # [ (left_most_x, b1y2), (right_most_x, b2y1)]        return edge    # Box 1's Y1 == Box 2's Y2    elif b1[2] == b2[3]:        edge = [(x_rng[0], b1[2]), (x_rng[1], b2[3])]        # [ (left_most_x, b1y2), (right_most_x, b2y1)]        return edge    # Box 1's X1 == Box 2's X2    elif b1[0] == b2[1]:        edge = [(b1[0], y_rng[0]), (b2[1], y_rng[1])]        # [ (B1x1, top_y), (b2x2, b2y1)]        return edge    # Box 1's X2 == Box 2's X1    elif b1[1] == b2[0]:        edge = [(b1[1], y_rng[0]), (b2[0], y_rng[1])]        # [ (B1x1, top_y), (b2x2, b2y1)]        return edge    else:        return edge        '''def shortest_to_adj(point, l1, l2):    """    Args:        point: starting point        l1: first endpoint of the edge        l2: second endpoint of the edge    Returns:        A tuple that represents a point on the line that has the smallest        euclidean distance between itself and the starting point    """    line = distance(l1, l2)    if line == 0:        return distance(point, l1)    dot_product = ((point[0] - l1[0]) * (l2[0] - l1[0]) + (point[1] - l1[1]) * (l2[1] - l1[1])) / line    dp = max(0, min(1, dot_product))    p1 = l1[0] + dp * (l2[0] - l1[0])    p2 = l1[1] + dp * (l2[1] - l1[1])    return (p1, p2)def distance(p1, p2):    """    Args:        p1: Starting point tuple        p2: Destination point tuple    Returns:        Euclidean distance between p1 and p2    """    '''    a = p1[0]    b = p1[1]    c = p2[0]    d = p2[1]'''    L = []    for i, item in enumerate(p1):        L.append(p1[i])    for j, item in enumerate(p2):        L.append(p2[i])    a = float(L[0])    b = float(L[1])    c = float(L[2])    d = float(L[3])    #x = p2[0] - p1[0] # c - a    #y = p2[1] - p1[1] # d - b    return sqrt(((c-a)**2) + ((d-b)**2))def is_in_box(pt, box):    '''    Args:        pt = point (x,y)        box = box (x1, x2, y1, y2)    Returns:        True: if point is inside box        False: if point is not inside box        '''    if pt[0] >= box[0] and pt[0] <= box[1] and pt[1] >= box[2] and pt[1] <= box[3]:        #since Y increases as you go down        return True    else:        return False