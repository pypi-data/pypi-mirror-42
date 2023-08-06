#!/usr/bin/env python

"""
A newick/nexus file/string parser based on the ete3.parser.newick
"""

import os
import re


# Regular expressions used for reading newick format
_ILEGAL_NEWICK_CHARS = r":;(),\[\]\t\n\r="
_NON_PRINTABLE_CHARS_RE = r"[\x00-\x1f]+"
_FLOAT_RE = r"\s*[+-]?\d+\.?\d*(?:[eE][-+]\d+)?\s*"
_NAME_RE = r"[^():,;]+?"
_NHX_RE = r"\[&&NHX:[^\]]*\]"

# clear mrbayes stuff from newick that's not quite NHX compatible, e.g.,
# "((a[&Z=1,Y=2], b[&Z=1,Y=2]):1.0[&L=1,W=0], c[&Z=1,Y=2]):2.0[&L=1,W=1];"
_MB_RE = r"\[(.*?)\]"



class NewickError(Exception):
    """Exception class designed for NewickIO errors."""
    def __init__(self, value):
        Exception.__init__(self, value)

class NexusError(Exception):
    """Exception class designed for NewickIO errors."""
    def __init__(self, value):
        Exception.__init__(self, value)



NW_FORMAT = {
    # flexible with support
    # Format 0 = (A:0.35,(B:0.72,(D:0.60,G:0.12)1.00:0.64)1.00:0.56);
    0: [
        ('name', str, True),
        ('dist', float, True),
        ('support', float, True),
        ('dist', float, True),
    ],

    # flexible with internal node names
    # Format 1 = (A:0.35,(B:0.72,(D:0.60,G:0.12)E:0.64)C:0.56);
    1: [
        ('name', str, True),
        ('dist', float, True),
        ('name', str, True),
        ('dist', float, True),      
    ],

    # strict with support values
    # Format 2 = (A:0.35,(B:0.72,(D:0.60,G:0.12)1.00:0.64)1.00:0.56);
    2: [
        ('name', str, False),
        ('dist', float, False),
        ('support', str, False),
        ('dist', float, False),      
    ],

    # strict with internal node names
    # Format 3 = (A:0.35,(B:0.72,(D:0.60,G:0.12)E:0.64)C:0.56);
    3: [
        ('name', str, False),
        ('dist', float, False),
        ('name', str, False),
        ('dist', float, False),      
    ],

    # strict with internal node names
    # Format 4 = (A:0.35,(B:0.72,(D:0.60,G:0.12)));
    4: [
        ('name', str, False),
        ('dist', float, False),
        (None, None, False),
        (None, None, False),      
    ],

    # Format 5 = (A:0.35,(B:0.72,(D:0.60,G:0.12):0.64):0.56);
    5: [
        ('name', str, False),
        ('dist', float, False),
        (None, None, False),
        ('dist', float, False),      
    ],

    # Format 6 = (A:0.35,(B:0.72,(D:0.60,G:0.12)E)C);
    6: [
        ('name', str, False),
        (None, None, False),
        (None, None, False),        
        ('dist', float, False),      
    ],    

    # Format 7 = (A,(B,(D,G)E)C);
    7: [
        ('name', str, False),
        ('dist', float, False),
        ('name', str, False),        
        (None, None, False),        
    ],    


    # Format 8 = (A,(B,(D,G)));
    8: [
        ('name', str, False),
        (None, None, False),
        ('name', str, False),        
        (None, None, False),
    ],

    # Format 9 = (,(,(,)));
    9: [
        ('name', str, False),
        (None, None, False),
        (None, None, False),
        (None, None, False),
    ],    

    # Format 10 = ((a[&Z=1,Y=2], b[&Z=1,Y=2]):1.0[&L=1,W=0], c[&Z=1,Y=2]):2.0[%L=1,W=1];"

}




# re matchers should all be compiled on toytree init
class Matchers:
    def __init__(self):
        self.matcher = {}

        for node_type in ["leaf", "single", "internal"]:
            if node_type == "leaf" or node_type == "single":
                container1 = NW_FORMAT[formatcode][0][0]
                container2 = NW_FORMAT[formatcode][1][0]
                converterFn1 = NW_FORMAT[formatcode][0][1]
                converterFn2 = NW_FORMAT[formatcode][1][1]
                flexible1 = NW_FORMAT[formatcode][0][2]
                flexible2 = NW_FORMAT[formatcode][1][2]

            else:
                container1 = NW_FORMAT[formatcode][2][0]
                container2 = NW_FORMAT[formatcode][3][0]
                converterFn1 = NW_FORMAT[formatcode][2][1]
                converterFn2 = NW_FORMAT[formatcode][3][1]
                flexible1 = NW_FORMAT[formatcode][2][2]
                flexible2 = NW_FORMAT[formatcode][3][2]



        if converterFn1 == str:
            FIRST_MATCH = "("+_NAME_RE+")"
        elif converterFn1 == float:
            FIRST_MATCH = "("+_FLOAT_RE+")"
        elif converterFn1 is None:
            FIRST_MATCH = '()'

        if converterFn2 == str:
            SECOND_MATCH = "(:"+_NAME_RE+")"
        elif converterFn2 == float:
            SECOND_MATCH = "(:"+_FLOAT_RE+")"
        elif converterFn2 is None:
            SECOND_MATCH = '()'

        if flexible1 and node_type != 'leaf':
            FIRST_MATCH += "?"
        if flexible2:
            SECOND_MATCH += "?"

        matcher_str= '^\s*%s\s*%s\s*(%s)?\s*$' % (FIRST_MATCH, SECOND_MATCH, _NHX_RE)
        compiled_matcher = re.compile(matcher_str)
        matchers[node_type] = [container1, container2, converterFn1, converterFn2, compiled_matcher]

    return matchers



class NewickParser:
    "Parse newick file/str formatted data to extract tree data and features"    
    def __init__(self, newick):
        pass



    def newick_from_string(nw, root, matcher, fmt):
        """ Reads a newick string in the New Hampshire format. """

        # check parentheses
        if nw.count('(') != nw.count(')'):
            raise NewickError('Parentheses do not match. Broken tree data.')

        # remove white spaces and separators 
        nw = re.sub("[\n\r\t]+", "", nw)

        # focal parent node
        unode = None

        # splits on nodes start
        for chunk in nw.split("(")[1:]:

            # add child to make this node a parent.
            unode = (root if not unode else unode.add_child())

            # get all parenth endings from this parenth start
            subchunks = [ch.strip() for ch in chunk.split(",")]
            ending = subchunks[-1]
            if ending and (not ending.endswith(';')):
                raise NewickError('Broken newick structure at: %s' % chunk)

            # Every closing parenthesis closes a node and goes up one level.
            endlen = len(subchunks) - 1
            for idx, leaf in enumerate(subchunks):

                # bail out if empty
                if (not leaf) & (idx == endlen):
                    continue

                # if ending then get closer
                subnws = leaf.split(")")

                # parse features and apply to the unode object
                self.read_node_data(subnws[0], unode, matcher, fmt)

                # next contain closing nodes and data about the internal nodes.
                if len(closing_nodes) > 1:
                    for closing_internal in closing_nodes[1:]:
                        closing_internal =  closing_internal.rstrip(";")

                        # read internal node data and go up one level
                        _read_node_data(closing_internal, current_parent, "internal", matcher, formatcode)
                        current_parent = current_parent.up
        return root_node


    def apply_node_data(self, subnw, unode, matcher, fmt):

        node = unode.add_child()
        
        # if no feature data
        if not subnw:
            return 

        # load matcher junk
        c1, c2, cv1, cv2, match = matcher['node']

        # look for junk
        data = re.match(matcher, subnw)

        # 
        if data:
            data = data.groups()

            # data should not be empty
            if all([i is None for i in data]):
                raise NewickError(
                    "Unexpected newick format {}".format(subnw[:50]))

            # node has a name
            if data[0]:  # is not None and data[0] != '':
                node.add_feature(c1, converterFn1(data[0]))

            if data[1]:  # is not None and data[1] != '':
                node.add_feature(c2, converterFn2(data[1][1:]))

            if data[2] & data[2].startswith("[&&NHX"):
                pass  # _parse_extra_features(node, data[2])

        else:
            raise NewickError("Unexpected newick format {}".format(subnw[:50]))





    def apply_edge_data(self):
        pass


    # being replaced by node and edge funcs
    def read_node_data(subnw, current_node, node_type, matcher, formatcode):
        "Reads a leaf node from a subpart of the original newicktree"

        # ..
        if node_type == "leaf" or node_type == "single":
            if node_type == "leaf":
                node = current_node.add_child()
            else:
                node = current_node
        else:
            node = current_node

        # ...
        subnw = subnw.strip()
        
        # ...
        if not subnw and node_type == 'leaf' and formatcode != 100:
            raise NewickError('Empty leaf node found')
        elif not subnw:
            return

        container1, container2, converterFn1, converterFn2, compiled_matcher = matcher[node_type]
        data = re.match(compiled_matcher, subnw)
        if data:
            data = data.groups()
            # This prevents ignoring errors even in flexible nodes:
            if subnw and data[0] is None and data[1] is None and data[2] is None:
                raise NewickError("Unexpected newick format '%s'" %subnw)

            if data[0] is not None and data[0] != '':
                node.add_feature(container1, converterFn1(data[0].strip()))

            if data[1] is not None and data[1] != '':
                node.add_feature(container2, converterFn2(data[1][1:].strip()))

            if data[2] is not None \
                    and data[2].startswith("[&&NHX"):
                _parse_extra_features(node, data[2])
        else:
            raise NewickError("Unexpected newick format '%s' " %subnw[0:50])
        return




class NexusParser:
    "Parse nexus file/str formatted data to extract tree data and features"
    def __init__(self, nexus):



class TreeParser:
    def __init__(self, intree, tree_format=0):
        """
        Reads tree input as string or file, figures out format and parses it.
        Formats 0-10 are newick formats supported by ete3. 
        Format 11 is nexus format from mrbayes.
        """
        self.intree = intree
        self.fmt = tree_format
        self.data = None
        
        self.get_tree_data()
        self.check_format()
        

    def get_tree_data(self):
        "load data from a file or string"
        if isinstance(self.intree, (str, bytes)):
            # load from a file
            if os.path.exists(self.intree):
                with open(self.intree, 'rU') as indata:
                    self.data = indata.read()
            else:
                self.data = self.intree

    def check_format(self):
        "test format of intree nex/nwk, extra features"
                
        # get compiled re matcher to test 
