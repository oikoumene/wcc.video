from collective.grok import gs
from wcc.video import MessageFactory as _

@gs.importstep(
    name=u'wcc.video', 
    title=_('wcc.video import handler'),
    description=_(''))
def setupVarious(context):
    if context.readDataFile('wcc.video.marker.txt') is None:
        return
    portal = context.getSite()

    # do anything here
