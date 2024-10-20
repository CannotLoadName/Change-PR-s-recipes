from os.path import split, splitext, join, isdir
from json import loads, dumps
from os import listdir
from sys import argv

original = {"type": "forge:ore_dict", "ore": "enderpearl"}
replacement = {"type": "minecraft:item", "item": "projectred-core:resource_item", "data": 402}


def handle(fname):
    if splitext(split(fname)[1])[1] == ".json":
        fd = loads(open(fname, "r").read())
        if "key" in fd:
            for i in fd["key"]:
                if fd["key"][i] == original:
                    fd["key"][i] = replacement
        elif "ingredients" in fd:
            for i in range(len(fd["ingredients"])):
                if fd["ingredients"][i] == original:
                    fd["ingredients"][i] = replacement
        fl = open(fname, "w")
        fl.write(dumps(fd, indent=2))
        fl.close()


def handlePath(dname, act=False):
    for i in listdir(dname):
        j = join(dname, i)
        if isdir(j):
            handlePath(j, act or i == "recipes")
        elif act:
            handle(j)


for pth in argv[1:]:
    handlePath(pth)
