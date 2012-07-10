# -*- encoding:utf-8 -*-
from flask.ext.script import Manager, Shell
from flask.ext.assets import ManageAssets
from flask.ext.zen import Test, ZenTest

from madacraserver import create_app
from server import RunSocketIOServer

manager = Manager(create_app(), with_default_commands=False)
manager.add_command("assets", ManageAssets())
manager.add_command("shell", Shell())
manager.add_command("test", Test())
manager.add_command("zen", ZenTest())
manager.add_command("runserver", RunSocketIOServer())


if __name__ == "__main__":
    manager.run()
