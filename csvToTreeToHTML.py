# -*- coding: utf-8 -*-
"""
Created on Fri Jun  1 07:41:11 2018
@author: lpberg
Started from: https://mail.python.org/pipermail/python-list/2015-January/684996.html
"""
import csv

def column_index(row):
    for result, cell in enumerate(row, 0):
        if cell:
            return result
    raise ValueError

class Node:
    def __init__(self, name, level):
        self.name = name
        self.level = level
        self.children = []

    def append(self, child):
        self.children.append(child)

def read_tree(rows, levelnames):
    root = Node("#ROOT", "#ROOT")
    old_level = 0
    stack = [root]
    for i, row in enumerate(rows, 1):
        new_level = column_index(row)
        node = Node(row[new_level], levelnames[new_level])
        if new_level == old_level:
            stack[-1].append(node)
        elif new_level > old_level:
            if new_level - old_level != 1:
                raise ValueError
            stack.append(stack[-1].children[-1])
            stack[-1].append(node)
            old_level = new_level
        else:
            while new_level < old_level:
                stack.pop(-1)
                old_level -= 1
            stack[-1].append(node)
    return root

def getNodeStringWithChildren(level,name):
    return '''<div class="borderOn lvl'''+level+'''" data-toggle="collapse" data-target="#'''+name+level+'''">'''+name+'''</div>
                      <div style="margin-left:15px" id="'''+name+level+'''" class="collapse">'''
def getNodeStringWithoutChildren(level,name):
    return '''<div class="borderOn lvl'''+level+'''">'''+name+'''</div>'''

def getIntroCode(colors):
     return '''<!DOCTYPE html>
        <html>
        <head>
          <meta name="viewport" content="width=device-width, initial-scale=1">
          <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
          <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
          <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
          <style>
              div.lvl1:before, 
              div.lvl2:before,
              div.lvl3:before,
              div.lvl4:before,
              div.lvl5:before {
                  content: "";
                  display: inline-block;
                  width: 15px;
                  height: 15px;
                  margin-right: 5px;
                }
                div.lvl1:before {
                  background: '''+colors[0]+''';
                }
                div.lvl2:before {
                  background: '''+colors[1]+''';
                }
                div.lvl3:before {
                  background: '''+colors[2]+''';
                }
                div.lvl4:before {
                  background: '''+colors[3]+''';
                }
                div.lvl5:before {
                  background: '''+colors[4]+''';
                }
          </style>
        </head>
        <body>
        '''
        
def getClosingCode():
    return '''</body></html>'''

def traverseTreeDFS(node,outfile):
    if node.children:
        outfile.write(getNodeStringWithChildren(node.level,node.name))
        for child in node.children:
            traverseTreeDFS(child,outfile)
        outfile.write("</div>")
    else: 
        outfile.write(getNodeStringWithoutChildren(node.level,node.name))

def main(infile,outfile):
    colors = ["Red","Green","Blue","Orange","Black"]
    outfile = open(outfile,'w')
    outfile.write(getIntroCode(colors))
    with open(infile) as f:
        rows = csv.reader(f)
        levelnames = next(rows) # skip header
        tree = read_tree(rows, levelnames)
        for node in tree.children:
            traverseTreeDFS(node,outfile)
        outfile.write(getClosingCode())
        outfile.close()

if __name__ == "__main__":
    main("./tree.csv","./test.html")