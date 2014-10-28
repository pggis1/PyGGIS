import psycopg2

class DXFParser:

    def __init__(self, filename):
        raw_dxf = open(filename, "r").read()
        raw_dxf = raw_dxf.replace(" ", "")
        raw_dxf = raw_dxf.splitlines()

        self.structured_dxf = []
        self.lines = []
        self.polylines = []
        self.KEY = 0
        self.VALUE = 1

        i = 0
        while i < len(raw_dxf):
            if i % 2 == 0:
                self.structured_dxf.append([raw_dxf[i], raw_dxf[i+1].strip("\n")])
            i += 1

    def get_lines(self):
        """get all LINE records as tuple from dxf-file"""
        current_record = 0

        while current_record < len(self.structured_dxf):
            if self.structured_dxf[current_record][self.VALUE] == "LINE":
                line = {'8': 0, '10': 0, '20': 0, '30': 0, '11': 0, '21': 0, '31': 0}

                itr = 1
                while self.structured_dxf[current_record + itr][self.KEY] != "0":
                    if self.structured_dxf[current_record + itr][self.KEY] in line.keys():
                        line[self.structured_dxf[current_record + itr][self.KEY]] = \
                            self.structured_dxf[current_record + itr][self.VALUE]
                    itr += 1
                if 0 not in line.values():
                    self.lines.append(line)
                else:
                    print ("ERROR: Line %i. Corrupted record." % current_record)

            current_record += 1
        return tuple(self.lines)

    def get_ln_crd(self, n, point='0x', scale=1):
        points = {'0x': '10', '0y': '20', '0z': '30', 'x': '11', 'y': '21', 'z': '31'}
        try:
            return float(self.lines[n][points[point]])/scale
        except IndexError:
            print("No such line %i" % n)
        except KeyError:
            print("No such point %s" % point)
        return 0

    def get_ln_layer(self, n):
        try:
            return self.lines[n]['8']
        except IndexError:
            print("No such line %i" % n)
        return 0

    def get_polylines(self):
        """get all POLYLINE records as tuple from dxf-file"""
        current_record = 0

        while current_record < len(self.structured_dxf):

            if self.structured_dxf[current_record][self.VALUE] == "POLYLINE":
                polyline = {'8': 0, '62': 0, '10': 0, '20': 0, '30': 0, '39': '0', '70': '0', 'VERTICES': '0'}

                itr = 1
                while self.structured_dxf[current_record + itr][self.KEY] != "0":
                    if self.structured_dxf[current_record + itr][self.KEY] in polyline.keys():
                        polyline[self.structured_dxf[current_record + itr][self.KEY]] = \
                            self.structured_dxf[current_record + itr][self.VALUE]
                    itr += 1
                vertices = self.get_vertices(current_record + itr)
                polyline['VERTICES'] = vertices
                if (polyline['70'] == '9' or polyline['70'] == '1') and polyline['VERTICES']:
                    polyline['VERTICES'].append(polyline['VERTICES'][0])

                if 0 not in polyline.values():
                    self.polylines.append(polyline)
                else:
                    print ("ERROR: Polyline %i. Corrupted record." % current_record)

            current_record += 1

        return tuple(self.polylines)

    def get_vertices(self, itr):
        """get all VERTEX records as tuple from POLYLINE block"""
        vertices = []
        current_record = itr

        vertex = {'10': 0, '20': 0, '30': 0}
        while current_record < len(self.structured_dxf):
            if self.structured_dxf[current_record][self.VALUE] == "SEQEND":
                if 0 not in vertex.values():
                    vertices.append(vertex)
                break
            if self.structured_dxf[current_record][self.VALUE] != "VERTEX":
                if self.structured_dxf[current_record][self.KEY] in vertex.keys():
                    vertex[self.structured_dxf[current_record][self.KEY]] = \
                        self.structured_dxf[current_record][self.VALUE]
            else:
                if 0 not in vertex.values():
                    vertices.append(vertex)
                vertex = {'10': 0, '20': 0, '30': 0}

            current_record += 1

        return vertices

    def get_pl_hght(self, n):
        try:
            return float(self.polylines[n]['39'])
        except IndexError:
            print("No such polyline %i" % n)
        return 0

    def get_pl_vrtcs(self, n):
        try:
            return self.polylines[n]['VERTICES']
        except IndexError:
            print("No such polyline %i" % n)

    def get_pl_layer(self, n):
        try:
            return self.polylines[n]['8']
        except IndexError:
            print("No such polyline %i" % n)
        return 0

    def get_pl_color(self, n):
        try:
            return int(self.polylines[n]['62'])
        except IndexError:
            print("No such polyline %i" % n)
        return 0

    def is_pl_closed(self, n):
        try:
            if self.polylines[n]['70'] == "9" or self.polylines[n]['70'] == "1":
                return True
        except IndexError:
            print("No such polyline %i" % n)
        return False