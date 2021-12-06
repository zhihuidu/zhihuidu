#!/usr/bin/env python3                                                         

import time, argparse
import random
import string
import numpy as np
import arkouda as ak
import sys

TYPES = ('int64', 'float64', 'bool', 'str')

def time_ak_tri_delaunay_graph(fn:int):
    filename="delaunay_n"+str(fn)
    print("---------Graph Triangle Results For {}----------".format(filename))
    #print("Graph BFS")
    cfg = ak.get_config()
    # print("server Hostname =",cfg["serverHostname"])
    # print("Number of Locales=",cfg["numLocales"])
    # print("number of PUs =",cfg["numPUs"])
    # print("Max Tasks =",cfg["maxTaskPar"])
    # print("Memory =",cfg["physicalMemory"])

    lgNv=8
    Ne_per_v=3
    p=0.03
    directed=0
    weighted=0
    f = open("./data/delaunay/"+filename+"/"+filename+".mtx")
    Line = f.readline()
    while not(Line[1]>='0' and Line[0]<='9'):
         Line = f.readline()
         b = Line.split(" ")
    edges=int(b[2])
    vertices=max(int(b[0]),int(b[1]))


    ''' EXACT TIMINGS
    start = time.time()
    Graph=ak.graph_file_read(edges,vertices,2,directed,"../testingFiles/data/delaunay/"+filename+"/"+filename+".gr")
    end = time.time()
    BuildingTime=end-start
    print("Regular Building ", filename , " takes {:.4f} seconds".format(end-start))
    #print("directed graph  ={}".format(Graph.directed))
    #print("weighted graph  ={}".format(Graph.weighted))
    start = time.time()
    triary = ak.graph_triangle(Graph)
    end = time.time()
    print("----------------------")
    print("triary = ak.graph_triangle(Graph)")
    print(triary)
    print("Triangle Counting  takes {:.4f} seconds".format(end-start)) '''


    ''' STREAMING TIMINGS '''
   
    #Graph=ak.stream_file_read(edges,vertices,2,directed,"../testingFiles/data/delaunay/"+filename+"/"+filename+".gr",4)
    #Graph=ak.stream_tri_cnt(edges,vertices,2,directed,"../testingFiles/data/delaunay/"+filename+"/"+filename+".gr",64)
    #print("Stream Building ", filename , " takes {:.4f} seconds".format(end-start))

    start = time.time()
    Graph=ak.streamHead_tri_cnt(edges,vertices,2,directed,"../testingFiles/data/delaunay/"+filename+"/"+filename+".gr",64)
    end = time.time()
    print("Stream building and Head triangle count of", filename , " takes {:.4f} seconds".format(end-start))
    print("Head triangle count: {}", Graph)

    start = time.time()
    Graph=ak.streamMid_tri_cnt(edges,vertices,2,directed,"../testingFiles/data/delaunay/"+filename+"/"+filename+".gr",64)
    end = time.time()
    print("Stream building and Mid triangle count of", filename , " takes {:.4f} seconds".format(end-start))
    print("Mid triangle count: {}", Graph)

    start = time.time()
    Graph=ak.streamTail_tri_cnt(edges,vertices,2,directed,"../testingFiles/data/delaunay/"+filename+"/"+filename+".gr",64)
    end = time.time()
    print("Stream building and Tail triangle count of", filename , " takes {:.4f} seconds".format(end-start))
    print("Tail triangle count: {}", Graph)

    #print("directed graph  ={}".format(Graph.directed))
    #print("weighted graph  ={}".format(Graph.weighted))
    #start = time.time()
    #triary = ak.graph_triangle(Graph)
    #end = time.time()
    #print("----------------------")
    #print("triary = ak.graph_triangle(Graph)")
    #print(triary)
    #print("Triangle Counting  takes {:.4f} seconds".format(end-start))
    return

def time_ak_tri_graphs(filepath:str, edges:int, vertices:int):
    print("----------Graph Triangle Results For {}----------".format(filepath))
    #print("Graph BFS")
    cfg = ak.get_config()
    # print("server Hostname =",cfg["serverHostname"])
    # print("Number of Locales=",cfg["numLocales"])
    # print("number of PUs =",cfg["numPUs"])
    # print("Max Tasks =",cfg["maxTaskPar"])
    # print("Memory =",cfg["physicalMemory"])

    lgNv=8
    Ne_per_v=3
    p=0.03
    directed=0
    weighted=0

    ''' EXACT TIMINGS
    start = time.time()
    Graph=ak.graph_file_read(edges,vertices,2,directed,filepath)
    end = time.time()
    BuildingTime=end-start
    print("Regular Building ", filepath , " takes {:.4f} seconds".format(BuildingTime))
    #print("directed graph  ={}".format(Graph.directed))
    #print("weighted graph  ={}".format(Graph.weighted))
    start = time.time()
    triary = ak.graph_triangle(Graph)
    end = time.time()
    TriaryTime = end-start
    print("----------------------")
    print("triary = ak.graph_triangle(Graph)")
    print(triary)
    print("Triangle Counting Exact takes {:.4f} seconds".format(TriaryTime))
    '''
    start = time.time()
    Graph=ak.graph_file_read(edges,vertices,2,directed,filepath)
    triary = ak.graph_triangle(Graph)
    #triary=ak.streamPL_tri_cnt(3056,1025,2,directed,"/rhome/zhihui/ArkoudaExtension/arkouda/data/delaunay/delaunay_n10/delaunay_n10.gr",1,0)
    end = time.time()
    print("Exact building and PL triangle count of", filepath , " takes {:.4f} seconds".format(end-start))
    print("Exact triangle count: {}", triary)


    ''' STREAMING TIMINGS
    start = time.time()
    Graph=ak.streamHead_tri_cnt(edges,vertices,2,directed,filepath,64)
    end = time.time()
    print("Stream building and Head triangle count of", filepath , " takes {:.4f} seconds".format(end-start))
    print("Head triangle count: {}", Graph)

    start = time.time()
    Graph=ak.streamMid_tri_cnt(edges,vertices,2,directed,filepath,64)
    end = time.time()
    print("Stream building and Mid triangle count of", filepath , " takes {:.4f} seconds".format(end-start))
    print("Mid triangle count: {}", Graph)

    start = time.time()
    Graph=ak.streamTail_tri_cnt(edges,vertices,2,directed,filepath,64)
    end = time.time()
    print("Stream building and Tail triangle count of", filepath , " takes {:.4f} seconds".format(end-start))
    print("Tail triangle count: {}", Graph) '''
    
    
    #start = time.time()
    #Graph=ak.stream_file_read(edges,vertices,2,directed,filepath,4)
    #Graph=ak.stream_tri_cnt(edges,vertices,2,directed,filepath,64)
    #end = time.time()
    #BuildingTime=end-start
    #print("Stream Building ", filepath , " takes {:.4f} seconds".format(end-start))
    #print("Stream Building and triangle count", filepath , " takes {:.4f} seconds".format(end-start))
    #print("directed graph  ={}".format(Graph.directed))
    #print("weighted graph  ={}".format(Graph.weighted))
    #start = time.time()
    #triary = ak.graph_triangle(Graph)
    #end = time.time()
    #print("----------------------")
    #print("triary = ak.graph_triangle(Graph)")
    #print(triary)
    #print("Triangle Counting Stream takes {:.4f} seconds".format(end-start))
    return


def create_parser():
    parser = argparse.ArgumentParser(description="Measure the performance of suffix array building: C= suffix_array(V)")
    parser.add_argument('hostname', help='Hostname of arkouda server')
    parser.add_argument('port', type=int, help='Port of arkouda server')
    parser.add_argument('-v', '--logvertices', type=int, default=5, help='Problem size: log number of vertices')
    parser.add_argument('-e', '--vedges', type=int, default=2,help='Number of edges per vertex')
    parser.add_argument('-p', '--possibility', type=float, default=0.01,help='Possibility ')
    parser.add_argument('-t', '--trials', type=int, default=6, help='Number of times to run the benchmark')
    parser.add_argument('-f', '--fileNo', type=int, default=17, help='Number of times to run the benchmark')
    parser.add_argument('-m', '--perm', type=int, default=0 , help='if permutation ')
    parser.add_argument('--numpy', default=False, action='store_true', help='Run the same operation in NumPy to compare performance.')
    parser.add_argument('--correctness-only', default=False, action='store_true', help='Only check correctness, not performance.')
    return parser

    
if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()
    ak.verbose = False
    ak.connect(args.hostname, args.port)

    # A = ak.array([4, 1, 1])
    # B = ak.array([6, -3, -8])

    # C = A * B
    # print(C)

    # D = C.sum()

    # print(D)


    '''
    if args.correctness_only:
        check_correctness(args.number, args.size, args.trials, args.dtype)
        print("CORRECT")
        sys.exit(0)
    '''

    '''
    for i in range(10,19):
        time_ak_tri_delaunay_graph(i)
    '''

    '''
    time_ak_tri_graphs("../testingFiles/data/graphs/ground_truth_community_networks/youtube", 2987624, 1134890)   
    time_ak_tri_graphs("../testingFiles/data/graphs/ground_truth_community_networks/lj", 34681189, 3997962)   
    time_ak_tri_graphs("../testingFiles/data/graphs/ground_truth_community_networks/orkut", 117185083, 3072441)
    '''

    '''
    time_ak_tri_graphs("../testingFiles/data/graphs/ca-HepTh.txt", 51971, 9877)
    time_ak_tri_graphs("../testingFiles/data/graphs/ca-CondMat.txt", 186936, 23133)
    time_ak_tri_graphs("../testingFiles/data/graphs/ca-AstroPh.txt", 396160, 18772)
    time_ak_tri_graphs("../testingFiles/data/graphs/email-Enron.txt", 367662, 36692)
    time_ak_tri_graphs("../testingFiles/data/graphs/ca-GrQc.txt", 28980, 5242)
    time_ak_tri_graphs("../testingFiles/data/graphs/ca-HepPh.txt", 237010, 12008)
    time_ak_tri_graphs("../testingFiles/data/graphs/loc-brightkite_edges.txt", 214078, 58228)

    time_ak_tri_graphs("../testingFiles/data/graphs/ground_truth_community_networks/amazon", 925872, 334863)
    time_ak_tri_graphs("../testingFiles/data/graphs/ground_truth_community_networks/dblp", 1049866, 317080)
    '''

    # time_ak_tri_graphs("/rhome/zhihui/ArkoudaExtension/arkouda/data/com-friendster.ungraph.txt", 1806067135, 65608366)
    # print(f"ak.__file__: {ak.__file__}")
    # print(f"sys.path: {sys.path}")
    # Graph1 = ak.graph_file_read(78,34,2,0,"/rhome/oaa9/ArkoudaExtension/testingFiles/data/graphs/soc-karate.mtx")
    # Graph2 = ak.graph_file_read(78,34,2,1,"/rhome/oaa9/ArkoudaExtension/testingFiles/data/graphs/soc-karate.mtx")
    # Graph1 = ak.graph_file_read(13,10,2,0,"/rhome/oaa9/ArkoudaExtension/testingFiles/data/graphs/simple2.txt")
    Graph1 = ak.graph_file_read(4,5,2,0,"/rhome/oaa9/ArkoudaExtension/testingFiles/data/graphs/line2.txt")
    # print(Graph)
    # Graph2 = ak.graph_file_read(13,10,2,1,"/rhome/oaa9/ArkoudaExtension/testingFiles/data/graphs/simple2.txt")
    # print(Graph)
    bc1 = ak.graph_bc(Graph1)
    # bc2 = ak.graph_bc(Graph2)
    print("bc1=", bc1)
    # print("bc2=", bc2)

    # for i in range(21, 25): 
    #     filename="delaunay_n" + str(i)
    #     f = open("/rhome/oaa9/ArkoudaExtension/testingFiles/data/delaunay/"+filename+"/"+filename+".mtx")
    #     Line = f.readline()
    #     while not(Line[1]>='0' and Line[0]<='9'):
    #         Line = f.readline()
    #         b = Line.split(" ")
    #     edges=int(b[2])
    #     vertices=max(int(b[0]),int(b[1]))

    #     Graph = ak.graph_file_read(edges, vertices, 2, 0, "/rhome/oaa9/ArkoudaExtension/testingFiles/data/delaunay/"+filename+"/"+filename+".gr")
    #     bfs = ak.graph_bfs(Graph, 0)
    #     print("BFS for", filename, ":", bfs)
    
    # bfs1 = ak.graph_bfs(Graph1, 0)
    # bfs2 = ak.graph_bfs(Graph2)
    # print("bfs1=", bfs1)
    # print("bfs2=", bfs2)
    
    # ak.shutdown()
