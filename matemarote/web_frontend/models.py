from django.db import models
from games.models import GameRevision,GameFlowNode
from django.conf import settings
import os

WEBGAMES_DIR = '/games'
WEBGAMES_RES_DIR = 'res'
WEBGAMES_GAMEFILES_DIR = 'game_files'
WEBGAMES_SCREENSHOTS_DIR = 'screenshots'

TOOLTIP_TEMPLATE = "<h2>%s</h2><p class='text'>%s</p>"


class WebGameFlowNode(models.Model):
    game_flow_node = models.OneToOneField(GameFlowNode)
    created = models.DateTimeField(auto_now_add=True)
    
    display_name = models.CharField(max_length=255)
    tooltip_description = models.TextField()
    
    def get_tooltip(self,game_flow_status):
        tooltip =  TOOLTIP_TEMPLATE % (self.display_name, self.tooltip_description)
        
        return tooltip
        
    @property
    def static_dir(self):
        return os.path.join(WEBGAMES_DIR,self.game_flow_node.game_revision.game.name,self.game_flow_node.game_revision.version)
    
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
