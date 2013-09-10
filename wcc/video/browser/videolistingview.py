from five import grok
from Products.ATContentTypes.interfaces.folder import IATFolder
from Products.ATContentTypes.interfaces.topic import IATTopic
from wcc.featurable.interfaces import IFeaturableSettings, IFeaturable
from zope.component import getMultiAdapter, getUtility
from plone.registry.interfaces import IRegistry
from wcc.featurable.browser.featureimagelisting_view import FeatureImageListingView
from redturtle.video.interfaces import (
    IRTVideo, IRTInternalVideo,
    IRTRemoteVideo
)

grok.templatedir('templates')

class VideoListingView(FeatureImageListingView):
    grok.baseclass()
    grok.name('videolistingview')
    grok.require('zope2.View')
    grok.template('videolistingview')

    def limit_display(self):
        return int(self.request.get('limit_display', 0)) or 4

    def is_first_page(self):
        b_start = int(self.request.get('b_start', 0))
        if b_start == 0:
            return True
        return False

    def folderContents(self):
        contentFilter = self.request.get('contentFilter', {})
        contentFilter = dict(contentFilter)
        limit_display = self.limit_display()

        contentFilter['object_provides'] = IRTVideo.__identifier__

        if IATTopic.providedBy(self.context):
            return self.context.queryCatalog(batch=True, **contentFilter) 

        return self.context.getFolderContents(contentFilter, 
                batch=True, b_size=limit_display)

    def player_code(self, item):

        if not item:
            return u''

        if IRTInternalVideo.providedBy(item):
            view = item.unrestrictedTraverse('@@flowplayer')
            return view.getEmbedCode()

        if IRTRemoteVideo.providedBy(item):
            view = item.unrestrictedTraverse('@@flowplayer')
            return view.getPlayerCode()

        return u''

    
class FolderVideoListingView(VideoListingView):
    grok.context(IATFolder)

class TopicVideoListingView(VideoListingView):
    grok.context(IATTopic)
