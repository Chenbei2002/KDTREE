from typing import List
from collections import namedtuple
import time

class Point(namedtuple("Point", "x y")):
    def __repr__(self) -> str:
        return f'Point{tuple(self)!r}'

class Rectangle(namedtuple("Rectangle", "lower upper")):
    def __repr__(self) -> str:
        return f'Rectangle{tuple(self)!r}'

    def is_contains(self, p: Point) -> bool:
        return self.lower.x <= p.x <= self.upper.x and self.lower.y <= p.y <= self.upper.y

class Node(namedtuple("Node", "location left right")):
    """
    location: Point
    left: Node
    right: Node
    """
    def _init_(self, location, left = None, right = None):
        self.location = location
        self.left = left
        self.right = right

    def __repr__(self):
        return f'{tuple(self)!r}'

class KDTree:
    """k-d tree"""

    def __init__(self):
        self._root = None
        self._n = 0  #Indicates the dimension


    def insert(self, p: List[Point]):
        """insert a list of points"""
        depth=0
        self._n=len(p[0])  #Calculate the dimensionality
        
        #Create a recursive function to insert the point
        def insert_points_rec(p,depth):
            if len(p)>0:
                median=len(p)//2  # Find the index of the median

                axis=depth%self._n  #Find the splitting dimension
                
                p_new=sorted(p,key=lambda x:x[axis]) #Arrange the inserted points in ascending orde
                
                #ecursive function
                if depth==0:
                    self._root=Node(p_new[median],insert_points_rec(p_new[:median],depth+1),insert_points_rec(p_new[median+1:],depth+1))
                node=Node(p_new[median],insert_points_rec(p_new[:median],depth+1),insert_points_rec(p_new[median+1:],depth+1))
                return node
        insert_points_rec(p,depth)

    def range(self, rectangle: Rectangle) -> List[Point]:
        """range query"""
        contains_points = []  #Create a list to store the points that meet the requirements

        #Create a recursive function to query sequentially
        def range_query_rec(node,rectangular, depth):  
            axis = depth % self._n   #Find the splitting dimension
            
            if not node:
                return None
             
            if axis == 0:  # x-axis
                if node.location.x < rectangular.lower.x:  
                    range_query_rec(node.right,rectangular,  depth + 1)
                elif node.location.x > rectangular.upper.x:  
                    range_query_rec( node.left,rectangular, depth + 1)
                else:  
                    range_query_rec(node.right, rectangular,  depth + 1)
                    range_query_rec(node.left, rectangular,  depth + 1)
                    if rectangular.is_contains(node.location):  
                        contains_points.append(node.location)  
            
            else:   #y-axis
                if node.location.y < rectangular.lower.y:  
                    range_query_rec(node.right, rectangular,  depth + 1)
                elif node.location.y > rectangular.upper.y:  
                    range_query_rec(node.left,rectangular,  depth + 1)
                else: 
                    range_query_rec(node.right,rectangular,  depth + 1)
                    range_query_rec( node.left,rectangular, depth + 1)
                    if rectangular.is_contains(node.location): 
                        contains_points.append(node.location)  
        range_query_rec(self._root,rectangle,  self._n)  
        return contains_points  # return the point list



    def Nearest_Neighbor(self,p,root=None,axis=0,distance_function=lambda x,y:((x[0]-y[0])**2+(x[1]-y[1])**2)) :
        """Find the nearest neighbor point"""       
        if root is None:
            root=self._root
            self._nearest=None #create a variable to store the nearest distance
       
        #Start at the root node and move down recursively
        if root.left or root.right:
            axis_new = (axis+1) % self._n
            if p[axis]<root.location[axis] and root.left:
                self.Nearest_Neighbor(p,root.left,axis_new)
            elif root.right:
                self.Nearest_Neighbor(p,root.right,axis_new)

        distance=distance_function(root.location,p)

        if self._nearest is None or distance<self._nearest[0]:
            self._nearest=(distance,root.location)
        
        #Solve the recursion and run the following steps for each node that passes through.
        if abs(p[axis]-root.location[axis]) < self._nearest[0]:
            axis_new=(axis+1)%self._n
            if root.left and p[axis]>=root.location[axis]:
                self.Nearest_Neighbor(p,root.left,axis_new)
            elif root.right and p[axis]<root.location[axis]:
                self.Nearest_Neighbor(p,root.right,axis_new)
        return self._nearest

   
def range_test():
    points = [Point(7, 2), Point(5, 4), Point(9, 6), Point(4, 7), Point(8, 1), Point(2, 3)]
    kd = KDTree()
    kd.insert(points)
    result = kd.range(Rectangle(Point(0, 0), Point(6, 6)))
    assert sorted(result) == sorted([Point(2, 3), Point(5, 4)])


def performance_test():
    points = [Point(x, y) for x in range(1000) for y in range(1000)]

    lower = Point(500, 500)
    upper = Point(504, 504)
    rectangle = Rectangle(lower, upper)
    #  naive method
    start = int(round(time.time() * 1000))
    result1 = [p for p in points if rectangle.is_contains(p)]
    end = int(round(time.time() * 1000))
    print(f'Naive method: {end - start}ms')

    kd = KDTree()
    kd.insert(points)
    # k-d tree
    start = int(round(time.time() * 1000))
    result2 = kd.range(rectangle)
    end = int(round(time.time() * 1000))
    print(f'K-D tree: {end - start}ms')

    assert sorted(result1) == sorted(result2)
    

def Nearest_Neighbor_test():
    points = [Point(7, 2), Point(5, 4), Point(9, 6), Point(4, 7), Point(8, 1), Point(2, 3)]
    kd = KDTree()
    kd.insert(points)
    point_test=Point(2.1,4)
    dis,point=kd.Nearest_Neighbor(point_test)
    print('the nearest point is:{},and the distance is {}'.format(point,dis))



if __name__ == '__main__':
    range_test()
    performance_test()
    Nearest_Neighbor_test()

    