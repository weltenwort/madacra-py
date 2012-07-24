# vim: set fileencoding=utf-8 :
from socketio.namespace import BaseNamespace


class MadacraNamespace(BaseNamespace):
    def __init__(self, *args, **kwargs):
        super(MadacraNamespace, self).__init__(*args, **kwargs)
        if "user_id" not in self.session:
            self.session["user_id"] = None

    def process_packet(self, packet):
        with self.request.app_context():
            return super(MadacraNamespace, self).process_packet(packet)

    def add_job(self, job):
        self.jobs.append(job)
        return job
