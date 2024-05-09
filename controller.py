from db import db
from exception import UnknownIdException, UnknownDestiny


class Controller():
    def __init__(self):
        pass

    def addApplication(self, link, name, email, cl, status):
        applicationIds = [link[0] for link in db.getAdvertisementLinks()]
        if not (int(link) in applicationIds):
            raise UnknownIdException("Wrong application id") 
            # return {"error": True, "msg": "Wrong application id"}
        print(applicationIds)
        db.addApplication(link, name, email, cl, status)
        return

    def getJobs(self):
        jobs = db.getAdvertisements()
        jobsDict = {job[0]:{"title":job[2], "desc":job[3], "loc":job[4]} for job in jobs}
        return jobsDict

    def getJob(self, num: int):
        filteredJobs = db.getAdvertisement(num)
        if len(filteredJobs) == 0:
            raise UnknownIdException("Wrong application id") 
        job = filteredJobs[0]
        return {"title":job[2], "desc":job[3], "loc":job[4]}

    def getApplications(self, id):
        applications = None
        if id == -1:
            applications = db.getApplications()
        elif not (id in db.getStatusIds()):
            raise UnknownIdException("Wrond Id")
        else:
            applications = db.getApplicationsWithStatus(id)
        ads = {ad[0]:ad[1] for ad in db.linkAddToName()}
        print(applications)
        for ii in range(len(applications)):
            applications[ii]["position"] = ads[applications[ii]["position"]]
            applications[ii]["status"] = db.statusIdToStr(applications[ii]["status"])

        return applications

    def reject(self, id):
        db.disqualifyApplication(id)

    def toInterview(self, id):
        db.qualifyApplication(id)

    def desideDestiny(self, id, destiny):
        applicationIds = None
        if destiny == "delete":
            applicationIds = db.getAllApplicationIds()
        else:
            applicationIds = db.getApplicationIds(0)
        print(applicationIds)
        print(type(id))

        if not (id in applicationIds):
            raise UnknownIdException("Wrong Id")

        if destiny == "reject":
            self.reject(id)
            return
        if destiny == "toInterview":
            self.toInterview(id)
            return
        if destiny == "delete":
            db.deleteApplication(id)
            return

        raise UnknownDestiny

controller = Controller()