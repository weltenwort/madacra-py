# vim: set fileencoding=utf-8 :
from socketio.namespace import BaseNamespace


class MadacraNamespace(BaseNamespace):
    def __init__(self, *args, **kwargs):
        super(MadacraNamespace, self).__init__(*args, **kwargs)

    @property
    def user(self):
        return self.session.get("user", None)

    @user.setter # noqa
    def user(self, value):
        self.session["user"] = value

    def process_packet(self, packet):
        with self.request.app_context():
            return super(MadacraNamespace, self).process_packet(packet)

    def add_job(self, job):
        self.jobs.append(job)
        return job
