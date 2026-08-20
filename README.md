# Diabetes Dashboard

## 1. Project Overview

The Diabetes Dashboard is an end-to-end data science and MLOps project for analyzing diabetes-related health data and building predictive machine learning models.

The project goes beyond a traditional dashboard. Data is stored in a MinIO-based Terrafox Data Lake, processed through a PySpark data pipeline, written to PostgreSQL, exposed through FastAPI, and visualized using Dash.

The long-term goal is to use Ray with multiple NVIDIA Jetson devices to train and compare machine learning models, track experiments through MLflow, select the best-performing model, and expose the final prediction through the dashboard.
## Dashboard Preview

![Diabetes Analytics Dashboard](/home/coder/workspace/.dvenv/docs/images/Diabetic-Dashboard.png)
## 2. Project Architecture

```text
                 Terrafox Data Lake
                       MinIO
                         │
                         ▼
                terrafox_datalake
                         │
                         ▼
                 PySpark Data Loader
                         │
                         ▼
                    Data Cleaner
                         │
                         ▼
                    PostgreSQL
                         │
              ┌──────────┴──────────┐
              │                     │
              ▼                     ▼
           FastAPI              ML Workflow
              │                     │
              ▼                     ▼
        Dash Dashboard          Ray Cluster
                                    │
                       ┌────────────┼────────────┐
                       ▼            ▼            ▼
                   Jetson 1     Jetson 2     Jetson 3
                       │            │            │
                       └────────────┼────────────┘
                                    ▼
                            Model Evaluation
                                    │
                                    ▼
                              Best Model
                                    │
                                    ▼
                                 MLflow
                                    │
                                    ▼
                             Prediction API
                                    │
                                    ▼
                              Dash Dashboard
```

## 3. Dataset

The dataset contains health information related to diabetes prediction.

Main columns include:

- pregnancies
- glucose
- diastolic blood pressure
- triceps skinfold thickness
- insulin
- BMI
- diabetes pedigree function
- age
- diabetes status

The `diabetes` column is the target variable:

- `1` = diabetic
- `0` = non-diabetic

## 4. Data Pipeline

The project uses a structured ETL pipeline instead of reading a local CSV directly from the dashboard.

```text
MinIO Data Lake
      ↓
datalake_reader.py
      ↓
data_loader.py
      ↓
PySpark
      ↓
data_cleaner.py
      ↓
database_writer.py
      ↓
PostgreSQL
```

### Pipeline Responsibilities

**Data Lake Reader**
- Connects to the Terrafox MinIO Data Lake
- Locates the source dataset
- Provides the dataset to Spark

**Data Loader**
- Creates the PySpark environment
- Loads raw data from the Data Lake

**Data Cleaner**
- Removes duplicate records
- Handles invalid or missing values
- Applies data transformations
- Prepares clean data for analysis and ML

**Database Writer**
- Writes the cleaned Spark DataFrame to PostgreSQL
- Maintains the `diabetes_clean` table used by the application

## 5. Analysis and Visualization

The analysis layer studies relationships between patient characteristics and diabetes outcomes.

Planned and implemented analysis includes:

- Descriptive statistics
- Histograms
- Boxplots
- Correlation analysis
- Age-based analysis
- BMI analysis
- Glucose analysis
- Insulin analysis
- Pregnancy-group analysis
- Combined risk-factor analysis
- Diabetes vs non-diabetes comparison

The analysis results are exposed through FastAPI and visualized using Dash and Plotly.

## 6. Machine Learning Workflow

The next stage of the project introduces a complete machine learning workflow.

The workflow will:

1. Retrieve cleaned data from PostgreSQL/Data Lake
2. Prepare model features and target data
3. Train multiple candidate models
4. Distribute training workloads using Ray
5. Execute workloads across NVIDIA Jetson workers
6. Track experiments using MLflow
7. Compare model performance
8. Select the best-performing model
9. Store the selected model
10. Expose predictions through FastAPI
11. Display prediction results in the Dash application

## 7. Distributed Model Training

Ray will coordinate distributed machine learning jobs across the AI lab.

```text
                 Ray Head Node
                      │
        ┌─────────────┼─────────────┐
        │             │             │
        ▼             ▼             ▼
   NVIDIA Jetson 1  Jetson 2     Jetson 3
        │             │             │
        ▼             ▼             ▼
    Training A     Training B     Training C
        │             │             │
        └─────────────┼─────────────┘
                      ▼
                Compare Results
                      ▼
                  Best Model
```

The three training paths can be used to compare different model types, hyperparameters, or training strategies.

For example:

```text
Jetson 1 → Logistic Regression
Jetson 2 → Random Forest
Jetson 3 → Neural Network
```

The final architecture is designed so that the training strategy can be changed without changing the dashboard or data pipeline.

## 8. MLflow Experiment Tracking

MLflow will be used to track the machine learning lifecycle.

It will record information such as:

- Model type
- Training parameters
- Hyperparameters
- Accuracy
- Precision
- Recall
- F1 score
- ROC-AUC
- Training time
- Model artifacts

The experiment results can then be compared to determine which model should be used for prediction.

## 9. Best Model Selection

After all candidate models are trained, their evaluation metrics will be compared.

```text
Model A ─┐
Model B ─┼─→ Evaluation → Best Model → Prediction API
Model C ─┘
```

The selected model will become the model used by the prediction section of the Diabetes Dashboard.

## 10. Dashboard Features

### Statistics

- Dataset information
- Column information
- Data types
- Total rows
- Head rows
- Tail rows

### Analysis & Visualization

- Distribution analysis
- Risk-factor analysis
- Correlation analysis
- Diabetes group comparisons
- Interactive Plotly visualizations

### Prediction

- Patient health inputs
- Machine learning prediction
- Diabetes risk probability
- Selected model information

## 11. Technologies Used

### Data Engineering
- MinIO
- Terrafox Data Lake
- PySpark
- Pandas
- PostgreSQL

### Backend
- Python
- FastAPI

### Frontend
- Dash
- Plotly
- HTML / CSS

### Machine Learning
- Scikit-learn
- Machine learning classification models

### MLOps
- MLflow
- Ray

### Distributed / Edge AI
- NVIDIA Jetson
- Ray workers

### Infrastructure
- Linux / Fedora
- Coder
- Cloudflare
- Git / GitHub

## 12. Project Structure

```text
diabetes-dashboard/
│
├── src/
│   │
│   ├── api/
│   │   ├── main.py
│   │   ├── info.py
│   │   └── analysis.py
│   │
│   ├── dashboard/
│   │   ├── app.py
│   │   └── assets/
│   │       ├── style.css
│   │       └── images/
│   │
│   ├── data_pipeline/
│   │   ├── datalake_reader.py
│   │   ├── data_loader.py
│   │   ├── data_cleaner.py
│   │   └── database_writer.py
│   │
│   ├── database/
│   │
│   └── ml/
│       ├── training/
│       ├── evaluation/
│       └── prediction/
│
├── notebooks/
│
├── models/
│
├── tests/
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## 13. Current Project Status

### Completed

- MinIO Data Lake connection
- Terrafox Data Lake integration
- PySpark data loading
- Data cleaning pipeline
- PostgreSQL database writing
- FastAPI connection
- Dash Statistics interface
- Data Lake → PySpark → PostgreSQL → FastAPI → Dash integration

### In Progress

- Analysis API
- Interactive visualizations

### Planned

- Feature engineering
- Machine learning training
- Ray distributed training
- NVIDIA Jetson workers
- MLflow experiment tracking
- Model comparison
- Best-model selection
- Prediction API
- Dashboard prediction interface

## 14. Final Project Goal

The final objective is to build a complete reusable machine learning architecture:

```text
Data Lake
   ↓
Data Engineering
   ↓
Database
   ↓
Analysis
   ↓
Distributed Model Training
   ↓
Experiment Tracking
   ↓
Best Model Selection
   ↓
Prediction API
   ↓
Interactive Dashboard
```

The Diabetes dataset acts as the first use case for developing and testing this larger Data Science, MLOps, and distributed AI architecture.
