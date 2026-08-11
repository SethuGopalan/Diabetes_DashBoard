# Diabetes Dashboard

## 1. Project Overview

This project is a Python Dash dashboard for analyzing diabetes-related health data.  
The dashboard helps explore how health factors such as age, BMI, glucose, triceps thickness, insulin, and pregnancy count relate to diabetes risk.  
The goal is to turn notebook analysis into an interactive web application.

## 2. Dataset

The dataset contains health information related to diabetes prediction.  
Main columns include pregnancies, glucose, diastolic blood pressure, triceps skinfold thickness, insulin, BMI, diabetes pedigree function, age, and diabetes status.  
The `diabetes` column is the target variable, where `1` means diabetic and `0` means non-diabetic.

## 3. Main Analysis

The dashboard includes descriptive statistics, histograms, boxplots, correlation heatmaps, and grouped analysis.  
Special focus is given to high-risk factors such as age, BMI, and triceps thickness.  
The project also analyzes how the number of high-risk factors affects diabetes likelihood.

## 4. Dashboard Features

- View diabetes data summary
- Explore glucose, BMI, insulin, and age distributions
- Compare diabetes rate by age and pregnancy groups
- Analyze combined risk factors
- Visualize diabetes likelihood using charts

## 5. Technologies Used

- Python
- Pandas
- Matplotlib / Plotly
- Dash
- Scikit-learn
- Google Cloud Platform planned for deployment

## 6. Project Structure

```text
diabetes_dashboard/
│
├── app.py
├── data/
│   └── diabetes.csv
├── assets/
│   └── style.css
├── notebooks/
│   └── diabetes_analysis.ipynb
├── requirements.txt
└── README.md
