from bridges.data_src_dependent import data_source
from bridges.bridges import Bridges
import os
#from heapq import heappush, heappop
import queue as Q
    
def getClosest(gr, lat, lon):
    closest = -1
    dist = float('inf')

    for k in gr.vertices:
        theosmvertex = gr.get_vertex(k).get_value()
        vlat = theosmvertex.latitude
        vlon = theosmvertex.longitude
        vdist = (vlat-lat)*(vlat-lat)+(vlon-lon)*(vlon-lon)
        if (vdist < dist):
            dist = vdist
            closest = k
        
    return closest

def style_root(gr, root) :
    elvis = gr.get_visualizer(root)
    elvis.set_color(0,0,0)

def dijkstra (gr, root) :
    distance = {}
    parent = {}
    
    for v in gr.vertices:
        distance[v] = float('inf')

    distance[root] = 0

    qu = Q.PriorityQueue()
    qu.put((distance[root], root))
    

    while not qu.empty():
        (d,v) = qu.get()
#        print (str(d)+" "+str(v))
        if d > distance[v]:
            continue

        nei_link = gr.get_adjacency_list(v)
        while (nei_link != None):
            nei=nei_link.get_value().get_vertex()
            edge_length=nei_link.get_value().get_weight()

#            print ("  "+str(nei)+" "+str(edge_length))

            if distance[v]+edge_length < distance[nei]:
                distance[nei] = distance[v]+edge_length
                qu.put((distance[nei], nei))
                parent[nei] = v
                
            nei_link=nei_link.get_next()
            
    return (distance, parent)
    

def style_distance(gr, distance):
    maxd = 0
    for v in gr.vertices:
        if distance[v] != float('inf') and distance[v] > maxd:
            maxd = distance[v]

    for v in gr.vertices:
        if distance[v] != float('inf'):
            grays = (maxd-distance[v])/maxd*255
            gr.get_visualizer(v).set_color(grays, grays, grays)


def style_parent(gr, parent, dest):
    # style out all vertices
    for v in gr.vertices:
        gr.get_visualizer(v).set_color(0, 0, 0, 0.2)

    # style out all edges
    for v in gr.vertices:
        nei_link = gr.get_adjacency_list(v)

        while (nei_link != None):
            nei=nei_link.get_value().get_vertex()
            gr.get_link_visualizer(v, nei).set_color(0, 0, 0, 0.2)
            
            nei_link=nei_link.get_next()

    # Style the path between parent and dest
    prev = dest
    cur = dest
    while cur != None:
        #style node
        gr.get_visualizer(cur).set_color(0, 0, 0, 1)

        #style edge along the path
        if prev != cur:
            gr.get_link_visualizer(cur, prev).set_color(0, 0, 0, 1) 
            gr.get_link_visualizer(prev, cur).set_color(0, 0, 0, 1) #some of these back edges should not exist but bridges gives me whatever I ask
        
        prev = cur
        cur = parent.get(cur)
    
    return
            
def main():
    user = os.environ.get("BRIDGES_USER_NAME")
    key = os.environ.get("BRIDGES_API_KEY")
    bridges = Bridges(100, user, key)
    bridges.connector.set_server("clone")
    
    osm_data = data_source.get_osm_data("uncc_campus")
    
    print(osm_data.longitude_range)
    print(osm_data.latitude_range)
    
    gr = osm_data.get_graph()
    
    root = getClosest(gr,
                         (osm_data.latitude_range[0]+osm_data.latitude_range[1])/2,
                         (osm_data.longitude_range[0]+osm_data.longitude_range[1])/2)

    print (root)

    style_root(gr, root)

    (distance,parent) = dijkstra(gr,root)

    style_distance(gr, distance)
    
    bridges.set_data_structure(gr)
    bridges.visualize()

    dest = getClosest(gr,
                      (osm_data.latitude_range[0]+(osm_data.latitude_range[1]-osm_data.latitude_range[0])/4),
                      (osm_data.longitude_range[0]+(osm_data.longitude_range[1]-osm_data.longitude_range[0])/4))

    style_parent(gr,parent, dest)

    bridges.set_data_structure(gr)
    bridges.set_visualize_JSON(True)
    bridges.visualize()


if __name__ == "__main__":
    main()
