# vim: set fileencoding=utf-8 :
from . import db_manager


class CampaignManager(db_manager.CollectionManager):
    name = "campaign"
    indices = [
            db_manager.CollectionIndex("name"),
            ]


campaign_manager = CampaignManager()
