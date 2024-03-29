from evolution.interpreter import evaluate_tree
from utils.tree_builder import TreeBuilder, regenerate_ids
from treelib import Tree
from settings.nodes import terminals, numbers
from settings.variables import TREE_MAX_DEPTH
import uuid
import random

class Individual:
  
  def __init__(self, tree):
    self.fitness = 0
    self.id = str(uuid.uuid4())
    self.tree = tree
    self.eval = evaluate_tree(tree)


  def __gt__(self,other):
    return self.fitness > other.fitness

  def __lt__(self,other):
    return self.fitness < other.fitness

  def __eq__(self,other):
    return self.fitness == other.fitness

class IndividualFactory:
  @staticmethod
  
  def prototype():
    builder = TreeBuilder()
    tree = builder.halfAndHalf()
    return Individual(tree)

  @staticmethod
  def fromTree(tree):
    return Individual(tree)

  
  @staticmethod
  def crossOver(individualA, individualB):
    tree = None

    while tree is None or tree.depth(tree.get_node(tree.root)) > TREE_MAX_DEPTH:
      treeA = Tree(tree = individualA.tree, deep=True)
      treeB = Tree(tree = individualB.tree, deep=True)
      regenerate_ids(treeA)
      regenerate_ids(treeB)
      removedNode = random.choice(treeA.all_nodes())
      addedNode = random.choice(treeB.all_nodes())

      addedSubtree = Tree(tree = treeB.subtree(addedNode.identifier), deep=True)

      if treeA.root == removedNode.identifier:
        tree = addedSubtree

      else:
        parent = treeA.parent(removedNode.identifier)
        treeA.remove_subtree(removedNode.identifier)
        treeA.paste(parent.identifier, addedSubtree)
        tree = treeA

    return Individual(tree)


  @staticmethod
  def mutate(individual):
    aTerminal = random.choice(list(terminals.keys() ) + numbers)
    tree = individual.tree
    leaf = random.choice(tree.leaves())
    tree.get_node(leaf.identifier).tag = aTerminal

    return Individual(tree)

  @staticmethod
  def elitism(individual):
      eliteTree = Tree(tree = individual.tree, deep=True)
      regenerate_ids(tree = eliteTree)
      elite = Individual(eliteTree)
      elite.id = individual.id
      return elite
