#! /usr/bin/env python

###############################################################################
##  DendroPy Phylogenetic Computing Library.
##
##  Copyright 2009 Jeet Sukumaran and Mark T. Holder.
##
##  This program is free software; you can redistribute it and/or modify
##  it under the terms of the GNU General Public License as published by
##  the Free Software Foundation; either version 3 of the License, or
##  (at your option) any later version.
##
##  This program is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##  GNU General Public License for more details.
##
##  You should have received a copy of the GNU General Public License along
##  with this program. If not, see <http://www.gnu.org/licenses/>.
##
###############################################################################

"""
Tests of tree metrics.
"""

import random
import unittest
import math
from cStringIO import StringIO

import dendropy
from dendropy.treesplit import encode_splits
from dendropy import treecalc

class TreeEuclideanDistTest(unittest.TestCase):

    def runTest(self):
         tree_list = dendropy.TreeList(
            stream=StringIO("""((t5:0.161175,t6:0.161175):0.392293,((t4:0.104381,(t2:0.075411,t1:0.075411):1):0.065840,t3:0.170221):0.383247);
                        ((t5:2.161175,t6:0.161175):0.392293,((t4:0.104381,(t2:0.075411,t1:0.075411):1):0.065840,t3:0.170221):0.383247);
                        ((t5:0.161175,t6:0.161175):0.392293,((t2:0.075411,(t4:0.104381,t1:0.075411):1):0.065840,t3:0.170221):0.383247);
                        ((t5:0.161175,t6:0.161175):0.392293,((t4:0.104381,(t2:0.075411,t1:0.075411):0.028969):0.065840,t3:0.170221):0.383247);
                        """),
            format="newick")
         for i in tree_list:
             encode_splits(i)
         self.assertAlmostEqual(treecalc.euclidean_distance(tree_list[0], tree_list[1]), 2.0)
         self.assertAlmostEqual(treecalc.euclidean_distance(tree_list[0], tree_list[2]), math.sqrt(2.0))
         self.assertAlmostEqual(treecalc.euclidean_distance(tree_list[0], tree_list[3]), 0.97103099999999998)
         self.assertAlmostEqual(treecalc.euclidean_distance(tree_list[1], tree_list[2]), math.sqrt(6.0))
         self.assertAlmostEqual(treecalc.euclidean_distance(tree_list[1], tree_list[3]), 2.2232636377544162)
         self.assertAlmostEqual(treecalc.euclidean_distance(tree_list[2], tree_list[3]), 1.000419513484718)

class TreeSymmetricDistTest(unittest.TestCase):

    def runTest(self):
         ref = dendropy.Tree(stream=StringIO("((t5,t6),((t4,(t2,t1)),t3));"), format="newick")
         taxon_set = ref.taxon_set
         encode_splits(ref)
         o_tree = dendropy.Tree(stream=StringIO("((t1,t2),((t4,(t5,t6)),t3));"), format="newick", taxon_set=taxon_set)
         encode_splits(o_tree)
         self.assertEqual(treecalc.symmetric_difference(o_tree, ref), 2)

class TreePatristicDistTest(unittest.TestCase):

    def setUp(self):
        self.tree = dendropy.Tree.get_from_string("(((a:1, b:1):1, c:2):1, (d:2, (e:1,f:1):1):1):0;", format="newick")

    def testPatDistMatrix(self):
        pdm = treecalc.PatristicDistanceMatrix(self.tree)
        def _chk_distance(pdm, t1, t2, exp_distance):
            tax1 = self.tree.taxon_set.require_taxon(label=t1)
            tax2 = self.tree.taxon_set.require_taxon(label=t2)
            pd = pdm(tax1, tax2)
            self.assertEqual(pd, exp_distance)
        _chk_distance(pdm, "a", "b", 2)
        _chk_distance(pdm, "a", "c", 4)
        _chk_distance(pdm, "b", "c", 4)
        _chk_distance(pdm, "a", "d", 6)
        _chk_distance(pdm, "f", "d", 4)
        _chk_distance(pdm, "c", "d", 6)

    def testPatDistFunc(self):
        encode_splits(self.tree)
        def _chk_distance(t1, t2, exp_distance):
            tax1 = self.tree.taxon_set.get_taxon(label=t1)
            tax2 = self.tree.taxon_set.get_taxon(label=t2)
            pd = treecalc.patristic_distance(self.tree, tax1, tax2)
            self.assertEqual(pd, exp_distance)
        _chk_distance("a", "b", 2)
        _chk_distance("a", "c", 4)
        _chk_distance("b", "c", 4)
        _chk_distance("a", "d", 6)
        _chk_distance("f", "d", 4)
        _chk_distance("c", "d", 6)

if __name__ == "__main__":
    unittest.main()
