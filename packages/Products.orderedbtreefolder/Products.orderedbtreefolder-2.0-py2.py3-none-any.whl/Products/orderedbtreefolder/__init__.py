# Initialize OrderedBTreeFolder and CMFOrderedBTreeFolder
from . import orderedbtreefolder as obt


def initialize(context):

    context.registerClass(
        obt.OrderedBTreeFolder,
        constructors=(obt.manage_addOrderedBTreeFolderForm,
                      obt.manage_addOrderedBTreeFolder),
        icon='orderedbtreefolder.gif',
    )
