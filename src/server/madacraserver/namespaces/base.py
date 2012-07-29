# vim: set fileencoding=utf-8 :
from socketio.namespace import BaseNamespace


class MadacraNamespace(BaseNamespace):
    def __init__(self, *args, **kwargs):
        super(MadacraNamespace, self).__init__(*args, **kwargs)

    @property
    def user_id(self):
        return self.session.get("user_id", None)

    @user_id.setter # noqa
    def user_id(self, value):
        self.session["user_id"] = value

    def process_packet(self, packet):
        with self.request.app_context():
            return super(MadacraNamespace, self).process_packet(packet)

    def add_job(self, job):
        self.jobs.append(job)
        return job
