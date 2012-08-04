# vim: set fileencoding=utf-8 :
from base import MadacraNamespace
from ..db.campaign import campaign_manager
from ..messaging import (
        message_hub,
        MessageReactor,
        )
from ..utils import validation as t


class CampaignNamespace(MadacraNamespace):
    def initialize(self):
        print("campaign namespace initialized", self.session)
        self.reactor = self.add_job(MessageReactor.from_hub(message_hub))
        self.reactor.start()

    def on_enumerate(self, data):
        if self.user:
            campaigns = campaign_manager.enumerate_campaigns(self.user["_id"])
            self.emit("enumerate", {
                "campaigns": t.List(campaign_manager.json_schema).check(campaigns),
                })
