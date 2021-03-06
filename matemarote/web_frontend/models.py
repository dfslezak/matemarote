from django.utils.translation import ugettext as _
from django.db import models
from django.forms import Form,ModelForm, Textarea,FileField
from games.models import Game, GameRevision,GameFlowNode
from django.conf import settings
import os

WEBGAMES_DIR = 'games'
WEBGAMES_RES_DIR = 'res'
WEBGAMES_GAMEFILES_DIR = 'game_files'
WEBGAMES_SCREENSHOTS_DIR = 'screenshots'

TOOLTIP_TEMPLATE = "<h2>%s</h2><p class='text'>%s</p>"

class GameForm(ModelForm):
    class Meta:
        model = Game
        fields = ['name','description']
        widgets = {'description': Textarea}

class GameRevisionForm(ModelForm):
    class Meta:
        model = GameRevision
        fields = ['version','previous_version']
    #def __init__(self, *args, **kwargs):
        #super(GameRevisionForm, self).__init__(*args, **kwargs)
        #self.fields['previous_version'].queryset = GameRevision.objects.filter(game=self.instance.game)

class UploadGameRevisionForm(Form):
    upload_file = FileField(label=_('Select a zip file'))

class GameRevisionWebPackage(models.Model):
    class Meta:
        abstract = True

    @staticmethod
    def static_dir(game_revision):
        return os.path.join(settings.MEDIA_ROOT,WEBGAMES_DIR,game_revision.game.name,"v%s" % game_revision.version)

    @staticmethod
    def checkPackageNamelist(namelist):
        all_present = 'res/' in namelist and 'pages/' in namelist and 'gamefiles/' in namelist and 'screenshots' in namelist
        return all_present

class WebGameFlowNode(models.Model):
    gameflow_node = models.OneToOneField(GameFlowNode)
    created = models.DateTimeField(auto_now_add=True)
    
    display_name = models.CharField(max_length=255)
    tooltip_description = models.TextField()
    
    def get_tooltip(self,gameflow_status):
        tooltip =  TOOLTIP_TEMPLATE % (self.display_name, self.tooltip_description)
        
        return tooltip
        
    @property
    def static_dir(self):
        return GameRevisionWebPackage.static_dir(self.gameflow_node.game_revision)
    
    @property
    def resource_path(self):
        return os.path.join(self.static_dir, WEBGAMES_RES_DIR)

    # @property
    #def page_path(self):
    #    return os.path.join(self.static_dir, WEBGAMES_PAGES_DIR)

    @property
    def game_file_path(self):
        return os.path.join(self.static_dir, WEBGAMES_GAMEFILES_DIR)
    
    @property
    def screenshots_path(self):
        return os.path.join(self.static_dir, WEBGAMES_SCREENSHOTS_DIR)
                    
    def _flatten_walk(self, subdir, include_dirs = False):
        '''Returns a flat list of file paths for all files in the given subdir, all relative to subdir'''
        paths = []
        for dirpath, dirnames, filenames in os.walk(path.join(settings.MEDIA_ROOT, subdir)):
            if '/.' in dirpath: continue
            curdir = dirpath[len(self.abspath)+1:]
            if include_dirs and curdir:
                paths.append(curdir)
            paths += [path.join(curdir,f) for f in filenames if not f.startswith('.')]
        return paths
    
    @property
    def files(self):
        '''All files related to this game'''
        return self._flatten_walk(self.static_dir)
    
    @property
    def files_and_dirs(self):
        return self._flatten_walk(self.static_dir, True)
        
    @property
    def game_files(self):
        '''All game_files related to this game'''
        return self._flatten_walk(self.game_file_path)
    
    @property
    def image_url(self):
        try:
            screenshots = [x for x in os.listdir(self.abs_screenshots_path)
                                if x[-4:].lower() in ('.png', '.gif','.jpg')]
        except OSError:
            return ''
        
        if screenshots:
            return path.join(settings.MEDIA_URL, self.screenshots_path, screenshots[0])
        return ''
            
    def create_directory_structure(self):
        #for dirname in self.resource_path, self.page_path, self.game_file_path, self.screenshots_path:
        for dirname in self.resource_path, self.game_file_path, self.screenshots_path:
            d = os.path.join(settings.MEDIA_ROOT, dirname)
            if not os.path.exists(d): os.makedirs(d)
