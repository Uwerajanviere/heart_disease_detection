from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import joblib
import numpy as np

# Load trained model
model = joblib.load("heart_disease_model.pkl")

app = FastAPI()

# Serve static files like CSS
app.mount("/static", StaticFiles(directory="static"), name="static")

# Use Jinja2 templates
templates = Jinja2Templates(directory="static")

@app.get("/", response_class=HTMLResponse)
def read_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/predict", response_class=HTMLResponse)
def predict(request: Request,
            age: float = Form(...),
            sex: int = Form(...),
            cp: int = Form(...),
            trestbps: float = Form(...),
            chol: float = Form(...),
            fbs: int = Form(...),
            restecg: int = Form(...),
            thalach: float = Form(...),
            exang: int = Form(...),
            oldpeak: float = Form(...),
            slope: int = Form(...),
            ca: int = Form(...),
            thal: int = Form(...)):

    # Create input features in correct order (match the model)
    features = [age, sex, trestbps, chol, fbs, thalach, exang, oldpeak, slope, ca,
                cp == 1, cp == 2, cp == 3,
                restecg == 1, restecg == 2,
                thal == 1, thal == 2, thal == 3]

    features_array = np.array([features])
    prediction = model.predict(features_array)[0]

    result = "Heart Disease Detected" if prediction == 1 else "No Heart Disease"
    return templates.TemplateResponse("index.html", {
        "request": request,
        "result": result
    })
