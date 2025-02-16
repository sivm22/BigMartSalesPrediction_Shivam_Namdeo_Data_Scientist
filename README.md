# 📊 BigMart Sales Prediction - Machine Learning Model

## 🏬 Project Overview
This project aims to predict sales for BigMart outlets using historical data from 2013. The dataset consists of sales data for 1559 products across 10 stores. The objective is to understand the key factors influencing sales and build a machine learning model that accurately predicts sales for each product.

---

## 📂 Dataset Overview

The dataset consists of **8,523** training samples and **5,681** test samples with the following features:

- **Item Features**: `Item_Identifier`, `Item_Weight`, `Item_Fat_Content`, `Item_Visibility`, `Item_Type`, `Item_MRP`
- **Outlet Features**: `Outlet_Identifier`, `Outlet_Establishment_Year`, `Outlet_Size`, `Outlet_Location_Type`, `Outlet_Type`
- **Target Variable**: `Item_Outlet_Sales` (Total sales for a particular item at a store)

### 🔍 Data Preprocessing
- **Handling Missing Values**: Imputed missing values in `Item_Weight` with the mean and `Outlet_Size` using the mode.
- **Feature Engineering**:
  - `Outlet_Age`: Created using `2025 - Outlet_Establishment_Year`.
  - `Item_Category`: Extracted from `Item_Identifier` (Food, Drinks, Non-Consumables).
  - `Price_per_Unit_Weight`: `Item_MRP / Item_Weight`.
  - `Item_Visibility_Log`: Log transformation applied to reduce skewness.
  - `Outlet_Age_Category`: Categorized outlets into `Young`, `Mid`, `Old`.
  - `Non_Consumable`: Binary flag for Non-Consumable items.
- **Encoding Categorical Variables**: Applied One-Hot Encoding and Label Encoding where necessary.
- **Feature Scaling**: Standardized numerical features (`Item_Weight`, `Item_Visibility`, `Item_MRP`, etc.) using `StandardScaler`.

---

## 📈 Exploratory Data Analysis (EDA)
To better understand sales patterns, we visualized:
1. **Item Outlet Sales Distribution** - Right-skewed pattern with most products having low sales.
2. **Sales by Item Type** - Certain categories (like Starchy Foods, Seafood) have high variability.
3. **Sales by Outlet Type** - `Supermarket Type 3` has the highest median sales.
4. **Item MRP vs Sales** - Positive correlation, showing pricing influences sales.

---

## 🤖 Model Building & Training

### 🚀 Models Evaluated
1️⃣ **Linear Regression**  
2️⃣ **Decision Tree Regressor**  
3️⃣ **Random Forest Regressor**  
4️⃣ **Gradient Boosting Regressor**  

📊 **Initial Model Performance Summary:**
| Model               | Train RMSE | Validation RMSE |
|---------------------|------------|-----------------|
| **Linear Regression** | 1141.31 | 1068.91 |
| **Decision Tree** | 0.00 | 1499.10 (Overfitting) |
| **Random Forest** | 434.18 | 1091.85 |
| **Gradient Boosting** | 1035.67 | **1040.11** |

✅ **Gradient Boosting was selected as the best-performing model.**

---

## 🔧 Hyperparameter Tuning

To further improve **Gradient Boosting**, we performed **Randomized Search** for hyperparameter tuning.

🔍 **Best Hyperparameters Found:**
- **n_estimators**: 300
- **learning_rate**: 0.01
- **max_depth**: 5
- **subsample**: 0.9

📊 **Optimized Gradient Boosting Performance:**
- **Final RMSE on Validation Set**: **1030.01**  

---

## 🏆 Advanced Model Comparison (XGBoost vs LightGBM)

After tuning Gradient Boosting, we tested **XGBoost** and **LightGBM** to explore further improvements.

📊 **Advanced Model Performance Summary:**
| Model           | Train RMSE | Validation RMSE | R² Score |
|----------------|------------|-----------------|----------|
| **XGBoost**    | 890.15 | 1061.97 | 0.5851 |
| **LightGBM**   | 944.81 | 1045.83 | 0.5976 |
| **Gradient Boosting** (Prev. Best) | 1035.67 | **1040.11** | **0.6097** |

✅ **Gradient Boosting achieved the best R² score (0.6097), while LightGBM had slightly better RMSE.**

---

## 🔮 Final Sales Predictions

Using the best model (**Gradient Boosting with tuned hyperparameters**), we predicted sales for the **test dataset** and created the final submission file.

📂 **Final Predictions File**: [`bigmart_final_predictions.csv`](#) (Download)

---

## 📌 Key Takeaways & Business Insights

1️⃣ **Older Outlets** tend to have higher variability in sales but can still perform well.  
2️⃣ **Supermarkets (Type 3)** generate the highest revenue, indicating expansion potential.  
3️⃣ **Certain item categories** (e.g., Seafood, Starchy Foods) show high variability, indicating product-level optimizations.  
4️⃣ **Pricing Strategy**: Certain MRP bands (100-150) see high sales; strategic pricing can boost revenue.  
5️⃣ **Gradient Boosting performed best**, but **LightGBM** also showed competitive performance.  

---

## 🔧 Future Improvements

🔹 **Further Feature Engineering**: Introduce more interaction features to capture hidden patterns.  
🔹 **Hyperparameter Optimization**: Try **Bayesian Optimization** for further fine-tuning.  
🔹 **Stacking Models**: Experiment with model stacking (combining multiple models for better accuracy).  
🔹 **Real-Time Sales Forecasting**: Deploy the model using Flask or FastAPI for live predictions.  

---

Author:
Shivam Namdeo


