from glob import globs

def outputTriangulation(TypeId, neighbors, triangle_dir, operator):

    filename =  triangle_dir + "Triangulation-" + operator + TypeId
    f = open(filename, "w")
    l = len(neighbors)
    l -= 2
    if globs["qcnNo"] <= 9:
        no_str = "00" + str(globs["qcnNo"])
    elif globs["qcnNo"] <=99:
        no_str = "0" + str(globs["qcnNo"])
    else:
        no_str = str(globs["qcnNo"])
    new_typeid = "" + TypeId
    new_typeid = new_typeid.replace("P10-RandomConstraints", "R0.00-D11.00-IA-")
    new_typeid = new_typeid + no_str

    print(l, new_typeid, file=f)
    for i in range(len(neighbors)-1):
        for j in neighbors[i]:
            if i < j:
                print("%d %d" % (i, j), file = f)
    print(".", file = f)
    f.close()
