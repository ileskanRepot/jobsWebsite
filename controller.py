from db import db


class Controller():
    def __init__(self):
        pass
    def addApplication(self, link, name, email, cl, status):
        applicationIds = [link[0] for link in db.getAdvertisementLinks()]
        if not (int(link) in applicationIds):
            return {"error": True, "msg": "Wrong application id"}
        print(applicationIds)
        db.addApplication(link, name, email, cl, status)
        return {"error": False, "msg": "Everything good"}

    def getJobs(self):
        jobs = db.getAdvertisements()
        jobsDict = {job[0]:{"title":job[2], "desc":job[3], "loc":job[4]} for job in jobs}
        return jobsDict

    def getJob(self, num: int):
        filteredJobs = db.getAdvertisement(num)
        if len(filteredJobs) == 0:
            return None
        job = filteredJobs[0]
        return {"title":job[2], "desc":job[3], "loc":job[4]}

    def getApplications(self):
        applications = db.getApplications(0)
        ads = {ad[0]:ad[1] for ad in db.linkAddToName()}
        print(applications)
        for ii, apply in enumerate(applications):
            print(apply)
            print("WEE")
            print(applications[ii]["position"])
            applications[ii]["position"] = ads[applications[ii]["position"]]

        return applications

    def desideDestiny(self, id, destiny):
        applicationIds = db.getApplicationIds(0)
        print(applicationIds)
        print(type(id))

        if destiny == "reject":
            pass
        elif destiny == "toInterview":
            pass

        return None

controller = Controller()