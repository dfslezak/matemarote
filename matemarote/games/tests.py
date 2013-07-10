from django.utils import timezone
from django.test import TestCase
from models import *
import datetime

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

class GameFixtureLoadTest(TestCase):
    fixtures = ['user-testdata.json','games-testdata.json']
    
    def test_fixture_files(self):
        g = Game.objects.all()
        gr = GameRevision.objects.all()
        
        self.assertEqual(len(g), 2)
        self.assertEqual(len(gr), 3)
        self.assertEqual(gr[0].game, g[0])
        self.assertEqual(gr[1].game, g[1])
        self.assertNotEqual(gr[0].game, g[1])
        self.assertEqual(gr[2].game, g[1])
        self.assertEqual(gr[2].previous_version, gr[1])
        
class GameFlowFixtureLoadTest(TestCase):
    fixtures = ['user-testdata.json','games-testdata.json','gameflow-testdata.json']
    
    def test_fixture_files(self):
        g = Game.objects.all()
        gr = GameRevision.objects.all()
        gfn = GameFlowNode.objects.all()
        gf = GameFlow.objects.all()
        
        self.assertEqual(len(gfn), 3)
        self.assertEqual(gfn[0].game_revision, gr[0])
        self.assertEqual(gfn[1].game_revision, gr[1])
           
    #def test_list_games(self):
        #gf = GameFlow.objects.all()[0]
        #self.assertEqual(str(gf.list_games_per_skill(None)),'{1: [(1, True)], 2: [(2, True), (3, True)]}')

class GameFlowRulesTest(TestCase):
    fixtures = ['user-testdata.json','games-testdata.json','gameflow-testdata.json']
    
    def test_partial_completion(self):
        gf = GameFlow.objects.all()[0]
        gfn = GameFlowNode.objects.all()[2]
        gfr = GameFlowRule.objects.filter(gameflow_node=gfn).select_subclasses()
        self.assertEqual(str(gfr),'[<GameFlowRule_GamePartialCompletionDep: GameFlowRule_GamePartialCompletionDep object>]')

        gfn0 = GameFlowNode.objects.all()[0]
        gfs = GameFlowNodeStatus.objects.get(node=gfn0).gameflow_status
        self.assertEqual(gfr[0].lock_game(gfs),False)

class GameFlowTest(TestCase):
    fixtures = ['user-testdata.json']
    
    def test_game_creation(self):
        g1 = Game(name='game1')
        g2 = Game(name='game2')
        g1.save()
        g2.save()
        
        gr1 = GameRevision(game=g1,version='1.0.0.0',creation_date=timezone.now())
        gr2 = GameRevision(game=g2,version='1.0.0.0',creation_date=timezone.now())
        gr1.save()
        gr2.save()
    
        self.assertEqual(1 + 1, 2)

    def test_gameflow_node(self):
        g1 = Game(name='game1')
        g2 = Game(name='game2')
        g1.save()
        g2.save()
        
        gr1 = GameRevision(game=g1,version='1.0.0.0',creation_date=timezone.now())
        gr2 = GameRevision(game=g2,version='1.0.0.0',creation_date=timezone.now())
        gr1.save()
        gr2.save()
        
        gf = GameFlow()
        gf.save()
        
        gfn1 = GameFlowNode(game_revision=gr1,skill_level=1,gameflow=gf)
        gfn2 = GameFlowNode(game_revision=gr2,skill_level=2,gameflow=gf)
        gfn1.save()
        gfn2.save()

        gfr1 = GameFlowRule_GameFullDep(gameflow_node=gfn2)#,rule_type=GameFlowRule.DEPENDENCY)        
        gfr1.save()
        gfr1.previous_nodes.add(gfn1)
        gfr1.save()
       
        self.assertEqual(1 + 1, 2)
