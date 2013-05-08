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
        
        
class GameFlowTest(TestCase):
    fixtures = ['user-testdata.json']
    
    def test_game_creation(self):
        g1 = Game()
        g2 = Game()
        g1.save()
        g2.save()
        
        gr1 = GameRevision(game=g1,version='1.0.0.0',creation_date=timezone.now())
        gr2 = GameRevision(game=g2,version='1.0.0.0',creation_date=timezone.now())
        gr1.save()
        gr2.save()
    
        self.assertEqual(1 + 1, 2)

    def test_game_flow_node(self):
        g1 = Game()
        g2 = Game()
        g1.save()
        g2.save()
        
        gr1 = GameRevision(game=g1,version='1.0.0.0',creation_date=timezone.now())
        gr2 = GameRevision(game=g2,version='1.0.0.0',creation_date=timezone.now())
        gr1.save()
        gr2.save()
        
        gfn1 = GameFlowNode(game_revision=gr1,skill_level=1)
        gfn2 = GameFlowNode(game_revision=gr2,skill_level=2)
        gfn1.save()
        gfn2.save()

        gfr1 = GameFlowRule_GameFullDep(game_revision=gr2)#,rule_type=GameFlowRule.DEPENDENCY)        
        gfr1.save()
        gfr1.previous_nodes.add(gfn1)
        gfr1.save()

        print "Number of rules %s" % (str(GameFlowRule.objects.count()), )
        #gfn2.rules.add(gfr1)
        
        #print serializers.serialize("xml", GameFlowNode.objects.all())
        
        gf = GameFlow()
        gf.save()
        gf.nodes.add(gfn1)
        gf.nodes.add(gfn2)
        #gf.verify_level_dependency(gfn2)        
        print gfn2.id
        
        self.assertEqual(1 + 1, 2)
