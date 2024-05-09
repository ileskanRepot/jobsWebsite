from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Depends, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from typing import Annotated
import starlette.status as status

from controller import controller

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

def error(request: Request, errorTxt: str):
	return templates.TemplateResponse(
		name="error.html",
		request=request,
		context={"errorTxt": errorTxt}
	)

def success(request: Request, successTxt: str):
	return templates.TemplateResponse(
		name="success.html",
		request=request,
		context={"successTxt": successTxt}
	)



class Applicatoin(BaseModel):
	# position: int
	name: str = ""
	email: str = ""
	cl: str = ""

class Destiny(BaseModel):
	# position: int
	id: int = ""
	destiny: str = ""

# HTML
@app.get("/")
async def root(request: Request):
	jobs = controller.getJobs()
	return templates.TemplateResponse(
		name="index.html",
		request=request,
		context={"jobs": jobs}
	)


# @app.get("/api/jobs")
# async def jobsJson(request: Request):
# 	return {"job1": "title1", "job2": "title2"}

@app.get("/sendApplication/{name}")
async def sendApplication(request: Request, name: int):
	job = controller.getJob(name)
	if job == None:
		return error(request, "Wrong id")
	return templates.TemplateResponse(
		name="sendApplication.html",
		request=request,
		context={"job": job}
	)

@app.post("/sendApplication/{link}")
async def sendApplication(request: Request, link:str, name: Annotated[str, Form()], email: Annotated[str, Form()], cl: Annotated[str, Form()]):
	ret = controller.addApplication(link, name, email, cl, 0)

	if ret["error"]:
		return error(request, ret["msg"])
	
	return RedirectResponse("/successGetApplication", status_code=status.HTTP_302_FOUND)

@app.get("/successGetApplication")
async def successGetApplication(request: Request):
	return success(request, "Application received successfully")

@app.get("/applications")
async def applications(request: Request):
	applications = controller.getApplications()
	return templates.TemplateResponse(
		name="applications.html",
		request=request,
		context={ "applications": applications }
	)

@app.post("/applications/{id}")
async def applications(request: Request, id:int, destiny: Annotated[str, Form()]):
	controller.desideDestiny(id, destiny)
	return destiny

@app.get("/{full_path:path}")
async def captureRoutes(request: Request, full_path: str):
	return templates.TemplateResponse(
		name="notFound.html",
		request=request,
	)