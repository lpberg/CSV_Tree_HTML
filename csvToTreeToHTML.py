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

def dfs(node):
    if node.children:
        outfile.write('''<div class="borderOn lvl'''+node.level+'''" data-toggle="collapse" data-target="#'''+node.name+node.level+'''">'''+node.name+'''</div>
                      <div style="margin-left:15px" id="'''+node.name+node.level+'''" class="collapse">''')
        for child in node.children:
            dfs(child)
        outfile.write("</div>")
    else: 
        outfile.write('''<div class="borderOn lvl'''+node.level+'''">'''+node.name+'''</div>''')

    
outfile = open("./test.html",'w')

def main():
    colors = ["#4c4cc9","#6666d0","#7f7fd8","#9999e0","#b2b2e7","#ccccef","#e5e5f7","#ffffff"]
    outfile.write('''<!DOCTYPE html>
        <html>
        <head>
          <meta name="viewport" content="width=device-width, initial-scale=1">
          <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
          <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
          <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
          <style>
              div { margin: 0; padding: 0; margin-bottom:10px;}
              body {color:white;}
              .borderOn {border-style: solid; border-color:gray; border-width:thin;}
              .lvl1 {border-style: solid; background-color:'''+colors[0]+''';}
              .lvl2 {border-style: solid; background-color:'''+colors[1]+''';}
              .lvl3 {border-style: solid; background-color:'''+colors[2]+''';}
              .lvl4 {border-style: solid; background-color:'''+colors[3]+''';}
              .lvl5 {border-style: solid; background-color:'''+colors[4]+''';}
              .lvl6 {border-style: solid; background-color:'''+colors[5]+''';}
          </style>
        </head>
        <body>
        ''')
    infile = "./tree.csv"
    with open(infile) as f:
        rows = csv.reader(f)
        levelnames = next(rows) # skip header
        tree = read_tree(rows, levelnames)
        for node in tree.children:
            dfs(node)
        outfile.write('''</body></html>''')
        outfile.close()

if __name__ == "__main__":
    main()