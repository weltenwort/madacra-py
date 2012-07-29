# vim: set fileencoding=utf-8 :
import datetime

from ..utils import validation as t

from . import db_manager


class CampaignManager(db_manager.CollectionManager):
    name = "campaign"
    indices = [
            db_manager.CollectionIndex("name"),
            ]

    db_schema = t.Dict({
        t.Key("_id", optional=True): t.ObjectId,
        t.Key("closed", default=False): t.Bool,
        t.Key("creation_datetime", default=datetime.datetime.now): t.DateTime,
        t.Key("creation_user_id"): t.ObjectId,
        t.Key("name"): t.String,
        t.Key("parent_campaign_id", default=None): t.ObjectId,
        t.Key("players"): t.List(t.Dict({
            t.Key("name"): t.String,
            t.Key("user_ids"): t.List(t.ObjectId),
            }), min_length=1),
        })

    json_schema = t.Dict({
        t.Key("_id"): t.ObjectId.serialized(),
        t.Key("closed"): t.Bool,
        t.Key("creation_datetime"): t.DateTime.serialized(),
        t.Key("creation_user_id"): t.ObjectId.serialized(),
        t.Key("name"): t.String,
        t.Key("parent_campaign_id"): t.ObjectId.serialized(),
        t.Key("players"): t.List(t.Dict({
            t.Key("name"): t.String,
            t.Key("user_ids"): t.List(t.ObjectId.serialized()),
            }), min_length=1),
        })

    CREATION_USER_PLAYER_NAME = "Game Master"

    def enumerate_campaigns(self, user_id=None, include_closed=False):
        query = {
                "closed": include_closed,
                }
        if user_id is not None:
            query["players.user_ids"] = user_id
        campaigns = t.List(self.db_schema).check(list(self.collection.find(query)))
        return campaigns

    def create_campaign(self, name, creation_user_id):
        campaign = self.db_schema.check({
            "creation_user_id": creation_user_id,
            "name": name,
            "players": [
                {
                    "name": self.CREATION_USER_PLAYER_NAME,
                    "user_ids": [creation_user_id, ],
                    },
                ],
            })
        return self.collection.insert(campaign)


campaign_manager = CampaignManager()
