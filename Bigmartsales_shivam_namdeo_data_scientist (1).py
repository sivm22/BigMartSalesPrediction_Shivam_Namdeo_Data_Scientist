# -*- coding: utf-8 -*-
"""BigMartSales_Shivam_Namdeo_Data_Scientist.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1INjrAQmf_Sn0Sb1gn-v7zNgiwgUx0wQm

**BigMart Sales Prediction!**

Sales Prediction for Big Mart Outlets

Problem Statement:

The data scientists at BigMart have collected 2013 sales data for 1559 products across 10 stores in different cities. Also, certain attributes of each product and store have been defined. The aim is to build a predictive model and predict the sales of each product at a particular outlet.

Using this model, BigMart will try to understand the properties of products and outlets which play a key role in increasing sales.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df=pd.read_csv('/content/train_v9rqX0R.csv')

df.head()

df.info()

df.isna().sum()

"""Dataset Overview

- The dataset contains 8,523 rows and 12 columns.
- The dataset is structured with both categorical and numerical
  variables.

Key Observations
Missing Values:
- Item_Weight: 1,463 missing values
- Outlet_Size: 2,410 missing values

These missing values will need to be handled appropriately (imputation or removal).

Column Breakdown:

- Categorical Variables: Item_Identifier, Item_Fat_Content, Item_Type, Outlet_Identifier, Outlet_Size, Outlet_Location_Type, Outlet_Type
Numerical Variables: Item_Weight, Item_Visibility, Item_MRP, Outlet_Establishment_Year, Item_Outlet_Sales
Potential Data Cleaning Needs:

- Inconsistent categorical values: Item_Fat_Content might have inconsistencies (e.g., "Low Fat" vs. "low fat").

- Handling missing values in Item_Weight and Outlet_Size.
Checking for outliers in numerical columns such as Item_Visibility and Item_Outlet_Sales.
"""

print(df.isnull().sum())

"""Approach to Fix Missing Values
- For Item_Weight: We will fill missing values with the mean weight of the respective Item_Identifier. If an item's weight is missing, we will use the average weight of that item from the dataset.

- For Outlet_Size: Since outlet sizes are categorical (Small, Medium, High), we will fill missing values with the most frequent (mode) outlet size of the respective Outlet_Type.
"""

# missing Item_Weight by filling with the mean weight of the respective Item_Identifier
df['Item_Weight'] = df.groupby('Item_Identifier')['Item_Weight'].transform(lambda x: x.fillna(x.mean()))

# remaining Item_Weight missing values with overall mean (if any group had all NaN)
df['Item_Weight'] = df['Item_Weight'].fillna(df['Item_Weight'].mean())

# missing Outlet_Size by filling with the most frequent size for each Outlet_Type
mode_outlet_size = df.groupby('Outlet_Type')['Outlet_Size'].agg(lambda x: x.mode()[0])  # Find mode for each type
df['Outlet_Size'] = df['Outlet_Size'].fillna(df['Outlet_Type'].map(mode_outlet_size))

# Verifying if all missing values are handled
print("\nMissing Values after fixing:")
print(df.isnull().sum())

"""### Exploratory Data Analysis (EDA)

In this step, we will:

- Summarize the dataset
- Visualize key relationships
- Detect any anomalies or outliers.


"""

# Summary statistics of numerical features
print("\nSummary Statistics:")
print(df.describe())

# unique values in categorical columns
categorical_cols = ['Item_Fat_Content', 'Item_Type', 'Outlet_Identifier',
                    'Outlet_Size', 'Outlet_Location_Type', 'Outlet_Type']
print("\nUnique Values in Categorical Columns:")
for col in categorical_cols:
    print(f"{col}: {df[col].unique()}")

"""#### Observations from Numerical Data
Item Visibility:
- The minimum value is 0, which doesn't make sense (a product must have some visibility).
For this we should replace 0 values with the mean or median visibility.

Item Outlet Sales:
- The average sales is ₹2181, but it varies significantly (std = ₹1706).
The max sale is ₹13,086, while the min is just ₹33.
Indicating high sales variation among products.

#### Observations from Categorical Data

Item_Fat_Content has inconsistent labels:

- low fat, LF, and Low Fat all mean Low Fat.
reg and Regular both mean Regular.
- For this we should standardize these categories.

Outlet Size has only 3 values:

- Small, Medium, High - No missing categories.

Outlet Type:

-There are 4 different types of stores, which may impact sales.
"""

# inconsistent categories in Item_Fat_Content
df['Item_Fat_Content'] = df['Item_Fat_Content'].replace({
    'LF': 'Low Fat',
    'low fat': 'Low Fat',
    'reg': 'Regular'
})

# Replacing zero Item Visibility with median
visibility_median = df[df['Item_Visibility'] > 0]['Item_Visibility'].median()
df.loc[df['Item_Visibility'] == 0, 'Item_Visibility'] = visibility_median

# Verifing changes
print("\n Unique Values After Cleaning:")
print(df['Item_Fat_Content'].unique())
print("\n Summary of Item Visibility After Fixing:")
print(df['Item_Visibility'].describe())

"""#### Data Visualization

Now, let's look into sales trends & relationships using Matplotlib & Seaborn.
"""

# Set plot style
sns.set_style("whitegrid")

"""Sales Distribution → Understanding the sales range"""

# 1. Distribution of Item Outlet Sales
plt.figure(figsize=(10, 5))
sns.histplot(df['Item_Outlet_Sales'], bins=30, kde=True)
plt.title("Distribution of Sales", fontsize=14)
plt.xlabel("Item Outlet Sales", fontsize=12)
plt.ylabel("Frequency", fontsize=12)
plt.show()

"""Brief observation of distribution of Item Outlet Sales

- This histogram with a KDE curve shows the distribution of sales
  across all items and outlets.
- The sales data is right-skewed, meaning most products have lower
  sales, while a few have very high sales.

Item Type vs. Sales → Which items sell more?
"""

# 2. Sales by Item Type
plt.figure(figsize=(12, 6))
sns.boxplot(x='Item_Type', y='Item_Outlet_Sales', data=df)
plt.xticks(rotation=90)
plt.title("📦 Sales by Item Type", fontsize=14)
plt.xlabel("Item Type", fontsize=12)
plt.ylabel("Sales", fontsize=12)
plt.show()

"""Sales by Item Type

- A box plot comparing sales across different item categories.
Most categories have a similar median sales value, but some categories (like Starchy Foods and Seafood) have higher upper ranges.
- There are many outliers, indicating that certain products within each category perform significantly better than others.

Outlet Type vs. Sales → Which store type sells more?
"""

# 3. Sales by Outlet Type
plt.figure(figsize=(8, 5))
sns.boxplot(x='Outlet_Type', y='Item_Outlet_Sales', data=df)
plt.title("🏪 Sales by Outlet Type", fontsize=14)
plt.xlabel("Outlet Type", fontsize=12)
plt.ylabel("Sales", fontsize=12)
plt.show()

"""Sales by Outlet Type

- Another box plot illustrating sales across different outlet types.
Supermarket Type 3 has the highest median and overall sales compared to other outlets.
- Grocery stores tend to have lower sales overall, with minimal variance.

Item MRP vs. Sales → How pricing affects sales?
"""

# 4. Item MRP vs. Sales
plt.figure(figsize=(10, 5))
sns.scatterplot(x='Item_MRP', y='Item_Outlet_Sales', data=df, alpha=0.5)
plt.title("💰 Item MRP vs. Sales", fontsize=14)
plt.xlabel("Item MRP", fontsize=12)
plt.ylabel("Sales", fontsize=12)
plt.show()

"""Item MRP vs. Sales

- A scatter plot showing the relationship between Maximum Retail Price (MRP) and sales.
- A positive correlation is evident—higher MRP items tend to have higher sales, but there are distinct price bands where sales tend to cluster.
- Certain price ranges (e.g., below 50 and between 100-150 MRP) show dense clustering, indicating popular pricing strategies.

#### Deeper Insights from the Visualizations

**Distribution of Item Outlet Sales (Right-Skewed Sales Pattern)**

*   **Key Takeaway:** Most items have relatively low sales, while a small number of products contribute significantly to overall revenue.
*   **Implication:**
    *   **Product Bundling:** Retailers can bundle low-sales items with high-selling ones to increase their movement.
    *   **Inventory Management:** Products with extremely high sales may experience stock shortages if not replenished efficiently.

**Sales by Item Type (Category-Level Trends & Outliers)**

*   **Key Takeaway:**
    *   Most item categories have similar median sales, but certain categories (like Starchy Foods & Seafood) show greater variation in performance.
    *   The presence of many outliers suggests that individual products within a category can have highly variable sales.
*   **Implication:**
    *   **High-Performance Products:** Identifying these outliers can help in targeted promotions to maximize sales.
    *   **Diversification Strategy:** Categories with low median sales but high variability could benefit from better marketing and shelf placement.

**Sales by Outlet Type (Supermarkets vs. Grocery Stores Performance)**

*   **Key Takeaway:**
    *   Supermarket Type 3 significantly outperforms other outlet types in terms of sales.
    *   Grocery stores have the lowest sales, with minimal variation, indicating a more consistent but lower revenue generation.
*   **Implication:**
    *   **Expansion Strategy:** Investing in Supermarket Type 3-like stores could maximize revenue potential.
    *   **Grocery Store Optimization:** Grocery stores should focus on high-margin items to counteract their lower sales volume.

**Item MRP vs. Sales (Pricing Strategy & Consumer Behavior)**

*   **Key Takeaway:**
    *   Sales increase with price, but there are distinct MRP bands where items sell more (e.g., 100-150 MRP).
    *   The clustering at specific price ranges suggests that consumers tend to purchase within familiar pricing brackets.
*   **Implication:**
    *   **Pricing Strategy:** Introduce more products in the high-demand MRP bands to align with consumer spending habits.
    *   **Promotional Planning:** Items in lower-selling MRP bands may require discounts or value-added promotions to increase sales.

### Overall Business Recommendations : 🚀

*  **Invest in High-Performing Outlets:** Focus on expanding Supermarket Type 3, as it generates the highest sales.

*  **Optimize Pricing Strategy:** Try to align new product pricing within the 100-150 MRP range, as it shows the highest consumer engagement.

*  **Improve Inventory Planning:** Identify fast-moving and low-selling products to balance stock levels and avoid over/under-stocking.

*  **Category-Specific Promotions:** Outlier products in various categories should be promoted aggressively to maximize profitability.

### Feature Engineering & Data Preparation for Modeling

Now that we have cleaned and explored the dataset, the next step is Feature Engineering, where we create new variables or modify existing ones to improve our predictive model's performance.

Key Feature Engineering Steps:

- Convert categorical variables into numerical representations (One-Hot Encoding / Label Encoding).
- Create new meaningful features (Outlet Age, Item Visibility Adjustments, etc.).
- Handle skewness and outliers in numerical features.
- Normalize/Scale numerical features for better model performance.

#### Encoding Categorical Features
We have several categorical features (Item_Fat_Content, Item_Type, Outlet_Identifier, Outlet_Size, Outlet_Location_Type, Outlet_Type). These need to be converted into a numerical format before feeding them into a machine learning model.

#### Creating New Features

Outlet Age:

- Instead of using Outlet_Establishment_Year directly, we convert it into Outlet_Age = Current Year - Establishment Year.

Item Visibility Correction

- Some products have Item_Visibility = 0, which isn't realistic. We will replace these zero values with the mean visibility of that item category.

Item Category Extraction

- Extracting the first few letters of Item_Identifier to group similar products (e.g., FD for food, DR for drinks, NC for non-consumables).

Feature Engineering
- New features (Outlet_Age, Item_Category).
- Zero values in Item_Visibility.
- Encode categorical variables.
"""

# Creating Outlet_Age Feature (Using 2025 as the current year)
df['Outlet_Age'] = 2025 - df['Outlet_Establishment_Year']

# Extracting Item Category from Item Identifier
df['Item_Category'] = df['Item_Identifier'].apply(lambda x: x[:2])
df['Item_Category'] = df['Item_Category'].replace({'FD': 'Food', 'DR': 'Drinks', 'NC': 'Non-Consumable'})

# Checking the first few rows
print(df[['Outlet_Establishment_Year', 'Outlet_Age', 'Item_Identifier', 'Item_Category']].head())

"""Assessing the impact of Outlet Age and Item Category on sales using box plots:"""

import matplotlib.pyplot as plt
import seaborn as sns

# Set figure size for better readability
plt.figure(figsize=(14, 6))

# 📊 1. Outlet Age vs. Sales
plt.subplot(1, 2, 1)
sns.boxplot(x='Outlet_Age', y='Item_Outlet_Sales', data=df, palette='viridis')
plt.xticks(rotation=45)
plt.title('Outlet Age vs. Sales')
plt.xlabel('Outlet Age (Years)')
plt.ylabel('Item Outlet Sales')

# 📊 2. Item Category vs. Sales
plt.subplot(1, 2, 2)
sns.boxplot(x='Item_Category', y='Item_Outlet_Sales', data=df, palette='Set2')
plt.title('Item Category vs. Sales')
plt.xlabel('Item Category')
plt.ylabel('Item Outlet Sales')

# Show plots
plt.tight_layout()
plt.show()

"""Insights from Outlet Age & Item Category vs. Sales

1️⃣ Outlet Age vs. Sales

- Older outlets (25+ years) tend to have higher median sales but more variability.

-  Newer outlets (less than 20 years old) show a more consistent sales pattern with fewer extreme outliers.

- There's no clear linear trend—some mid-aged outlets still perform well, indicating that store management & location matter more than just age.

2️⃣ Item Category vs. Sales

- Food items generally have higher sales compared to Drinks & Non-Consumables.

- Drinks show a slightly lower sales range, meaning they may not be primary revenue drivers.

- Non-Consumable items have the lowest median sales, but they exhibit some high-value outliers, possibly specialty or luxury items.

**Key Business Takeaways**

- Older stores are still competitive if well-located & managed.

- Food products are the strongest sales driver, so promotions should focus on
them.

- Non-consumables have some high-value sales → Need targeted marketing.

- Outlet renovation & modernization for mid-aged stores may boost sales.

We will now create interaction features or transformations to improve model performance.

✅ Feature Engineering Plan
We will introduce:

 1️⃣ Price per Unit Weight → Item_MRP / Item_Weight (Identifies high-value or bulk items).

2️⃣ Visibility Score → Log transformation of Item_Visibility to handle skewness.

3️⃣ Outlet Type Encoding → Convert categorical values into numerical (One-Hot Encoding or Label Encoding).

4️⃣ Outlet Age Category → Group outlets into Young (≤15 yrs), Mid (16-25 yrs), and Old (26+ yrs).

5️⃣ Item Category Type → Flag Non-Consumables separately.
"""

import numpy as np

#  1. Price per Unit Weight (Avoid division errors)
df['Price_per_Unit_Weight'] = df['Item_MRP'] / df['Item_Weight']

#  2. Log Transformation of Item Visibility (Handling Skewness)
df['Item_Visibility_Log'] = np.log1p(df['Item_Visibility'])  # log1p to avoid log(0) issues

#  3. Encoding Outlet Type (One-Hot Encoding)
df = pd.get_dummies(df, columns=['Outlet_Type'], drop_first=True)

#  4. Creating Outlet Age Category
df['Outlet_Age_Category'] = pd.cut(df['Outlet_Age'], bins=[0, 15, 25, 100], labels=['Young', 'Mid', 'Old'])

#  5. Non-Consumable Item Flag (Binary Feature)
df['Non_Consumable'] = df['Item_Category'].apply(lambda x: 1 if x == 'Non-Consumable' else 0)

#  Checking new features
print(df[['Price_per_Unit_Weight', 'Item_Visibility_Log', 'Outlet_Age_Category', 'Non_Consumable']].head())

"""Observation:

- Price_per_Unit_Weight: Varies significantly, capturing differences in pricing relative to weight.
- Item_Visibility_Log: Values are now better scaled, reducing the impact of skewness.
- Outlet_Age_Category: Correctly classifies stores as Young, Mid, or Old.
- Non_Consumable: Accurately flags non-consumable items as 1, ensuring differentiation.
"""

# Set visualization style
sns.set_style("whitegrid")

# 📊 1️⃣ Price per Unit Weight vs. Sales (Scatter Plot)
plt.figure(figsize=(8, 5))
sns.scatterplot(x=df["Price_per_Unit_Weight"], y=df["Item_Outlet_Sales"], alpha=0.5)
plt.title("Price per Unit Weight vs. Sales")
plt.xlabel("Price per Unit Weight")
plt.ylabel("Item Outlet Sales")
plt.show()

"""1️⃣ Price per Unit Weight vs. Sales (Scatter Plot)

- No clear linear relationship between price per unit weight and sales.
- Indicates that pricing alone might not be a dominant factor in
  influencing sales.
"""

# 📊 2️⃣ Item Visibility Log vs. Sales (Scatter Plot)
plt.figure(figsize=(8, 5))
sns.scatterplot(x=df["Item_Visibility_Log"], y=df["Item_Outlet_Sales"], alpha=0.5)
plt.title("Item Visibility Log vs. Sales")
plt.xlabel("Log of Item Visibility")
plt.ylabel("Item Outlet Sales")
plt.show()

"""2️⃣ Item Visibility Log vs. Sales (Scatter Plot)

- Items with very low visibility still have strong sales, suggesting that shelf placement might not significantly impact sales.
- Higher visibility doesn't guarantee higher sales.
"""

# 📊 3️⃣ Outlet Age Category vs. Sales (Box Plot)
plt.figure(figsize=(8, 5))
sns.boxplot(x=df["Outlet_Age_Category"], y=df["Item_Outlet_Sales"])
plt.title("Outlet Age Category vs. Sales")
plt.xlabel("Outlet Age Category")
plt.ylabel("Item Outlet Sales")
plt.show()

"""3️⃣ Outlet Age Category vs. Sales (Box Plot)

- Older outlets have a slightly wider range of sales distribution.
- Mid-aged and old outlets show similar median sales, meaning outlet
  establishment year might not be a strong predictor.
"""

# 📊 4️⃣ Non-Consumables vs. Sales (Bar Chart)
plt.figure(figsize=(8, 5))
sns.barplot(x=df["Non_Consumable"], y=df["Item_Outlet_Sales"])
plt.xticks(ticks=[0, 1], labels=["Consumables", "Non-Consumables"])
plt.title("Non-Consumables vs. Sales")
plt.xlabel("Product Type")
plt.ylabel("Item Outlet Sales")
plt.show()

"""4️⃣ Non-Consumables vs. Sales (Bar Chart)

- Non-consumables and consumables have nearly identical sales patterns.
- Indicates that product type (food, drinks, or non-consumables) alone
  does not impact overall sales significantly.
"""

'''
 Next Step: Preparing Data for Machine Learning!

 ✅ Step: Preparing Data for Machine Learning! 🚀
Now, we will prepare our dataset to be model-ready by performing the following key steps:

🔹 Steps in Data Preparation:
1️⃣ Encoding Categorical Variables

Convert text-based categorical columns into numerical format for machine learning algorithms.
2️⃣ Feature Scaling for Numerical Variables

Standardize numerical features to ensure they have the same scale.
3️⃣ Splitting the Data (Train-Test Split)

Since we already have a separate test dataset, we'll only split the training dataset into:
Training set → For model learning
Validation set → For model evaluation before making final predictions

'''

"""Encoding Categorical Variables
- We will encode categorical features using OneHotEncoder for nominal variables and LabelEncoder for ordinal variables where applicable.
"""

# Print all column names in the dataframe
print("🔍 Available Columns in Dataset:")
print(df.columns.tolist())

# Check which categorical columns are missing
missing_cols = [col for col in categorical_cols if col not in df.columns]
if missing_cols:
    print(f"⚠️ Missing Columns: {missing_cols}")
else:
    print("✅ All categorical columns are present.")

"""It looks like 'Outlet_Type' has already been one-hot encoded into:

- 'Outlet_Type_Supermarket Type1'
- 'Outlet_Type_Supermarket Type2'
- 'Outlet_Type_Supermarket Type3'

Since these new columns represent the original 'Outlet_Type', we no longer need 'Outlet_Type' in our encoding process.
"""

from sklearn.preprocessing import OneHotEncoder, LabelEncoder

# Select categorical columns excluding 'Outlet_Type' since it's already encoded
categorical_cols = ["Item_Fat_Content", "Outlet_Size", "Outlet_Location_Type", "Item_Category", "Outlet_Age_Category"]

# Apply One-Hot Encoding for categorical variables
df_encoded = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

# Apply Label Encoding for binary categorical variables if needed
label_encoder = LabelEncoder()
df_encoded["Outlet_Identifier"] = label_encoder.fit_transform(df["Outlet_Identifier"])

# Display the first few rows of the transformed dataset
print(df_encoded.head())

# Save the processed data for the next step
df_encoded.to_csv("encoded_data.csv", index=False)

"""Quick Summary of Encoded Data:
- Categorical variables successfully one-hot encoded, e.g.:
  Outlet_Size_Medium, Outlet_Size_Small, Item_Category_Food, etc.
- Binary categorical variables properly label encoded, e.g.:
Outlet_Identifier converted to numerical labels.
- Newly engineered features retained, e.g.:
Price_per_Unit_Weight, Item_Visibility_Log, Outlet_Age_Category_Mid, etc.

Now that we have cleaned and encoded our dataset, the next step is to select relevant features and prepare the data for modeling.

- Identify important features for predicting Item_Outlet_Sales.
Drop unnecessary columns (like Item_Identifier, redundant encodings, etc.).

Since we have separate train and test datasets, we must ensure proper alignment of feature columns.
We will split the train dataset into training & validation sets for model evaluation.
- Standardization & Scaling:

Numerical features will be scaled for better model performance.
Features like Item_MRP, Price_per_Unit_Weight, Item_Visibility_Log, etc., will be transformed.
"""

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Load the processed dataset
df = pd.read_csv("/content/encoded_data.csv")

#  Drop unnecessary columns
df.drop(["Item_Identifier", "Outlet_Establishment_Year"], axis=1, inplace=True)

#  Separate Features (X) and Target (y)
X = df.drop("Item_Outlet_Sales", axis=1)  # Features
y = df["Item_Outlet_Sales"]  # Target Variable

#  Split into Train and Validation Set (80% Training, 20% Validation)
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

#  Scale Numerical Features
num_cols = ["Item_Weight", "Item_Visibility", "Item_MRP", "Price_per_Unit_Weight", "Item_Visibility_Log"]

scaler = StandardScaler()
X_train[num_cols] = scaler.fit_transform(X_train[num_cols])
X_val[num_cols] = scaler.transform(X_val[num_cols])

#  Save Processed Data for Model Training
X_train.to_csv("X_train.csv", index=False)
X_val.to_csv("X_val.csv", index=False)
y_train.to_csv("y_train.csv", index=False)
y_val.to_csv("y_val.csv", index=False)

#  Display Final Processed Data Shape
print("X_train Shape:", X_train.shape)
print("X_val Shape:", X_val.shape)
print("y_train Shape:", y_train.shape)
print("y_val Shape:", y_val.shape)

"""Next Step: Model Training & Evaluation! 🎯
We'll now train multiple regression models and evaluate their performance.

1️⃣ Train Multiple Models

- Linear Regression
- Decision Tree Regressor
- Random Forest Regressor
- Gradient Boosting Regressor

2️⃣ Evaluate Model Performance

Using Root Mean Squared Error (RMSE) as the evaluation metric.

3️⃣ Compare Models & Select the Best One
"""

print("🔍 Checking Data Types in X_train:")
print(X_train.dtypes.value_counts())

print("\n🔍 Checking Unique Values in Categorical Columns:")
for col in X_train.select_dtypes(include=["object"]).columns:
    print(f"{col}: {X_train[col].unique()}")

from sklearn.preprocessing import OneHotEncoder

# Define categorical column to encode
categorical_col = ["Item_Type"]

# Initialize One-Hot Encoder
encoder = OneHotEncoder(drop="first", sparse_output=False, handle_unknown="ignore")

# Fit and transform `Item_Type`
X_train_encoded = pd.DataFrame(encoder.fit_transform(X_train[categorical_col]))
X_val_encoded = pd.DataFrame(encoder.transform(X_val[categorical_col]))

# Assign proper column names
X_train_encoded.columns = encoder.get_feature_names_out(categorical_col)
X_val_encoded.columns = encoder.get_feature_names_out(categorical_col)

# Reset index to match original DataFrame
X_train_encoded.index = X_train.index
X_val_encoded.index = X_val.index

# Drop original `Item_Type` column & concatenate encoded data
X_train = X_train.drop(columns=categorical_col).join(X_train_encoded)
X_val = X_val.drop(columns=categorical_col).join(X_val_encoded)

# Ensure all columns are now numeric
print("\n✅ Final Data Types After Encoding:")
print(X_train.dtypes.value_counts())

print("\n🔍 Checking Data Types After Encoding:")
print(X_train.dtypes.value_counts())  # Should no longer have 'object' types

print("\n🔍 Checking First Few Rows After Encoding:")
print(X_train.head())

from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error
import numpy as np

# Initialize models
models = {
    "Linear Regression": LinearRegression(),
    "Decision Tree": DecisionTreeRegressor(random_state=42),
    "Random Forest": RandomForestRegressor(n_estimators=100, random_state=42),
    "Gradient Boosting": GradientBoostingRegressor(n_estimators=100, random_state=42)
}

# Train and evaluate each model
results = {}

for name, model in models.items():
    print(f"🔄 Training {name}...")

    # Train the model
    model.fit(X_train, y_train)

    # Predictions
    y_pred_train = model.predict(X_train)
    y_pred_val = model.predict(X_val)

    # Compute RMSE
    train_rmse = np.sqrt(mean_squared_error(y_train, y_pred_train))
    val_rmse = np.sqrt(mean_squared_error(y_val, y_pred_val))

    # Store results
    results[name] = {"Train RMSE": train_rmse, "Validation RMSE": val_rmse}

    print(f"✅ {name} - Train RMSE: {train_rmse:.2f}, Validation RMSE: {val_rmse:.2f}\n")

# Convert results to DataFrame
results_df = pd.DataFrame(results).T

# Display Model Performance Summary
print("\n📊 Model Performance Summary:")
print(results_df)

# Save the results for future reference
results_df.to_csv("model_performance.csv", index=True)

"""Key Insights from Model Performance

1️⃣ Linear Regression: Performs reasonably well, with a Validation RMSE of 1068.91.

2️⃣ Decision Tree: Overfits heavily (Train RMSE = 0.00, Validation RMSE = 1499.10), indicating it's memorizing the training data.

3️⃣ Random Forest: Has the lowest Train RMSE (434.18) but a slightly higher Validation RMSE (1091.85) than Linear Regression, suggesting some overfitting.

4️⃣ Gradient Boosting: Best performing model, with the lowest Validation RMSE (1040.11), indicating it generalizes better than others.

#### Hyperparameter Tuning
Now that we have a baseline performance, let's fine-tune the best model (Gradient Boosting) using Random Search to optimize its performance.
"""

from sklearn.model_selection import RandomizedSearchCV
from sklearn.ensemble import GradientBoostingRegressor
import numpy as np

# Define parameter distribution
param_dist = {
    "n_estimators": [50, 100, 200, 300],
    "learning_rate": [0.01, 0.05, 0.1, 0.2],
    "max_depth": [3, 5, 7, 9],
    "subsample": [0.7, 0.8, 0.9, 1.0]
}

# Initialize Gradient Boosting Regressor
gb = GradientBoostingRegressor(random_state=42)

# Set up RandomizedSearchCV
random_search = RandomizedSearchCV(
    estimator=gb,
    param_distributions=param_dist,
    n_iter=15,  # Number of random combinations to try
    scoring="neg_root_mean_squared_error",  # Minimize RMSE
    cv=3,  # 3-fold cross-validation
    verbose=2,
    n_jobs=-1,  # Use all available CPU cores
    random_state=42  # Ensures reproducibility
)

# Run Randomized Search
print("🔄 Running Randomized Search... This should be faster! ⏳")
random_search.fit(X_train, y_train)

# Best hyperparameters
best_params = random_search.best_params_
print("\n✅ Best Hyperparameters Found:", best_params)

# Evaluate on Validation Set
best_gb = random_search.best_estimator_
y_pred_val = best_gb.predict(X_val)
val_rmse = np.sqrt(mean_squared_error(y_val, y_pred_val))
print(f"\n📊 Final Optimized Gradient Boosting RMSE on Validation Set: {val_rmse:.2f}")

"""### Results Analysis
Best Hyperparameters Found:

subsample: 0.9 → Uses 90% of data in each boosting round.

n_estimators: 300 → More trees improve learning, but at a higher cost.

max_depth: 5 → Balanced depth to avoid overfitting.

learning_rate: 0.01 → A smaller step size ensures stable learning.

📊 Final RMSE on Validation Set: 1030.01

It suggests that parameter tuning improved the model, but there might still be room for further optimization.
"""

# Merge Train + Validation for final training
X_final_train = pd.concat([X_train, X_val], axis=0)
y_final_train = pd.concat([y_train, y_val], axis=0)

print(f"✅ Final Training Dataset Shape: {X_final_train.shape}, Labels Shape: {y_final_train.shape}")

"""Now lets do the same above processes for the Test dataset"""

test_df = pd.read_csv("/content/test_AbJTz2l.csv")

# Ensure test set has the same feature engineering steps applied
test_df["Outlet_Age"] = 2025 - test_df["Outlet_Establishment_Year"]

# **Recreate Item_Category from Item_Identifier**
test_df["Item_Category"] = test_df["Item_Identifier"].apply(lambda x:
    "Food" if x[0] == "F" else "Drinks" if x[0] == "D" else "Non-Consumable")

# **Recreate Outlet_Age_Category**
def categorize_outlet_age(age):
    if age > 25:
        return "Old"
    elif age > 15:
        return "Mid"
    else:
        return "New"

test_df["Outlet_Age_Category"] = test_df["Outlet_Age"].apply(categorize_outlet_age)

# Apply the same feature engineering as train data
test_df["Price_per_Unit_Weight"] = test_df["Item_MRP"] / test_df["Item_Weight"]
test_df["Item_Visibility_Log"] = np.log1p(test_df["Item_Visibility"])
test_df["Non_Consumable"] = (test_df["Item_Category"] == "Non-Consumable").astype(int)

# Apply the same categorical encoding as train data
test_df = pd.get_dummies(test_df, columns=categorical_cols, drop_first=True)

# Ensure all feature columns match between train & test
missing_cols = set(X_final_train.columns) - set(test_df.columns)
for col in missing_cols:
    test_df[col] = 0  # Add missing columns with default value 0

# Ensure correct column order
test_df = test_df[X_final_train.columns]

print(f"✅ Final Test Dataset Shape: {test_df.shape}")

"""Generating Predictions Using the Best Model

Since Gradient Boosting with RandomizedSearchCV gave us the best RMSE (1030.01), we will use it to predict the sales for the test data.

Next:

1️⃣ Loading the best model (Gradient Boosting with tuned hyperparameters).

2️⃣ Making predictions on test_df.

3️⃣ Preparing a submission file

4️⃣ Saving the results as a CSV file.
"""

print("🔍 Checking Test Data Types:\n", test_df.dtypes.value_counts())
print("\n🔍 Checking First Few Rows of Test Data:\n", test_df.head())

# Convert categorical variable 'Outlet_Identifier' using Label Encoding (same as training)
test_df["Outlet_Identifier"] = label_encoder.transform(test_df["Outlet_Identifier"])

# Verify that `Outlet_Identifier` is now numerical
print("✅ Checking Test Data Types After Encoding:\n", test_df.dtypes.value_counts())

# Ensure all features in test match train dataset
missing_cols = set(X_final_train.columns) - set(test_df.columns)
for col in missing_cols:
    test_df[col] = 0  # Add missing columns as zeros

# Ensure correct column order
test_df = test_df[X_final_train.columns]

# Check for missing values in test dataset
missing_values_test = test_df.isnull().sum()
missing_values_test = missing_values_test[missing_values_test > 0]
print("🔍 Missing Values in Test Data:\n", missing_values_test)

# Fill missing Item_Weight values with the mean (same as train set)
test_df["Item_Weight"].fillna(test_df["Item_Weight"].mean(), inplace=True)

# Fill missing Item_Weight values explicitly (avoid inplace warning)
test_df = test_df.copy()  # Ensure we're modifying a copy of the original DataFrame
test_df["Item_Weight"] = test_df["Item_Weight"].fillna(test_df["Item_Weight"].mean())

# Recalculate Price_per_Unit_Weight after fixing Item_Weight
test_df["Price_per_Unit_Weight"] = test_df["Item_MRP"] / test_df["Item_Weight"]

# Recalculate Price_per_Unit_Weight after fixing Item_Weight
test_df["Price_per_Unit_Weight"] = test_df["Item_MRP"] / test_df["Item_Weight"]

# Verify that no missing values remain
print("✅ Missing Values After Fixing:\n", test_df.isnull().sum().sum())

#  Predict Sales for Test Data
test_predictions = final_model.predict(test_df)

#  Create Submission DataFrame
submission_df = pd.DataFrame({
    "Item_Identifier": pd.read_csv("/content/test_AbJTz2l.csv")["Item_Identifier"],
    "Outlet_Identifier": pd.read_csv("/content/test_AbJTz2l.csv")["Outlet_Identifier"],
    "Item_Outlet_Sales": test_predictions
})

#  Save Predictions to CSV
submission_file_path = "bigmart_sales_predictions.csv"
submission_df.to_csv(submission_file_path, index=False)

print(f"✅ Predictions saved successfully! Download your file here: {submission_file_path}")

"""Model Performance Metrics on Validation Set
Since we have already computed RMSE for different models, let's now compute additional performance metrics to better evaluate our best model.

We will calculate:

Mean Absolute Error (MAE) → Measures average absolute errors.
Mean Squared Error (MSE) → Measures average squared errors.
Root Mean Squared Error (RMSE) → Measures standard deviation of residuals.
R² Score (Coefficient of Determination) → Measures how well the model explains variance.
"""

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

# Make predictions on validation set
y_pred_val = final_model.predict(X_val)

# Compute performance metrics
mae = mean_absolute_error(y_val, y_pred_val)
mse = mean_squared_error(y_val, y_pred_val)
rmse = np.sqrt(mse)
r2 = r2_score(y_val, y_pred_val)

# Print metrics
print("📊 **Validation Set Performance Metrics:**")
print(f"✅ Mean Absolute Error (MAE): {mae:.2f}")
print(f"✅ Mean Squared Error (MSE): {mse:.2f}")
print(f"✅ Root Mean Squared Error (RMSE): {rmse:.2f}")
print(f"✅ R² Score: {r2:.4f}")

# Save metrics for future reference
metrics_dict = {
    "Mean Absolute Error (MAE)": mae,
    "Mean Squared Error (MSE)": mse,
    "Root Mean Squared Error (RMSE)": rmse,
    "R² Score": r2
}

import pandas as pd
metrics_df = pd.DataFrame([metrics_dict])
metrics_df.to_csv("model_performance_metrics.csv", index=False)

print("\n✅ Performance Metrics saved successfully! Download: model_performance_metrics.csv")

"""Model Performance Metrics

The validation performance metrics indicate how well the model predicts sales:

✅ Mean Absolute Error (MAE) → 727.33

The model's predictions, on average, deviate by 727.33 sales units from the actual values.

✅ Mean Squared Error (MSE) → 1,060,921.07

The squared average error indicates how large the variance in prediction errors is. A lower MSE is preferred.

✅ Root Mean Squared Error (RMSE) → 1,030.01

RMSE gives an error estimate in the same units as sales. The lower, the better!
This tells us that most predictions deviate by about 1,030 sales units.

✅ R² Score → 0.6097

~61% of the variance in sales is explained by the model.
There's room for improvement, but it's performing reasonably well.

Trying XGBoost and LightGBM if they provide better results
"""

from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np
import pandas as pd

# Define the models
advanced_models = {
    "XGBoost": XGBRegressor(n_estimators=300, learning_rate=0.05, max_depth=5, random_state=42),
    "LightGBM": LGBMRegressor(n_estimators=300, learning_rate=0.05, max_depth=5, random_state=42)
}

# Dictionary to store results
advanced_results = {}

# Train and evaluate each model
for name, model in advanced_models.items():
    print(f"🔄 Training {name}...")

    # Train the model
    model.fit(X_train, y_train)

    # Predictions
    y_pred_train = model.predict(X_train)
    y_pred_val = model.predict(X_val)

    # Compute RMSE and R² score
    train_rmse = np.sqrt(mean_squared_error(y_train, y_pred_train))
    val_rmse = np.sqrt(mean_squared_error(y_val, y_pred_val))
    r2 = r2_score(y_val, y_pred_val)

    # Store results
    advanced_results[name] = {
        "Train RMSE": train_rmse,
        "Validation RMSE": val_rmse,
        "R² Score": r2
    }

    print(f"✅ {name} - Train RMSE: {train_rmse:.2f}, Validation RMSE: {val_rmse:.2f}, R² Score: {r2:.4f}\n")

# Convert results to DataFrame for easy comparison
advanced_results_df = pd.DataFrame(advanced_results).T

# Save the results
advanced_results_df.to_csv("advanced_model_performance.csv", index=True)

# Display final results
print("📊 **Advanced Model Performance Summary:**")
print(advanced_results_df)

"""# Final Comparison:

Both **XGBoost** and **LightGBM** performed well, with **LightGBM achieving the best validation RMSE of 1045.83** and the highest **R² score of 0.5976**, indicating slightly better generalization.

##  Model Performance Summary:

| Model                     | Train RMSE | Validation RMSE | R² Score |
|---------------------------|------------|----------------|----------|
| **XGBoost**              | 890.15     | 1061.97        | 0.5851   |
| **LightGBM**             | 944.81     | 1045.83        | 0.5976   |
| **Gradient Boosting** (Prev. Best) | 1035.67  | 1040.11 | 0.6097 |

 **Gradient Boosting still has the best R² score (0.6097), but LightGBM achieves slightly better RMSE.**  
 **Decision Tree severely overfits with a validation RMSE of 1499.10.**  
 **Random Forest performed worse than expected with an RMSE of 1091.85.**

"""

# The Best Model from Advanced Models (LightGBM)
best_model = advanced_models["LightGBM"]

# Predict Sales for Test Data
test_predictions = best_model.predict(test_df)

# Create Submission DataFrame
submission_df = pd.DataFrame({
    "Item_Identifier": pd.read_csv("/content/test_AbJTz2l.csv")["Item_Identifier"],
    "Outlet_Identifier": pd.read_csv("/content/test_AbJTz2l.csv")["Outlet_Identifier"],
    "Item_Outlet_Sales": test_predictions
})

# Save Predictions to CSV with a New Name
final_submission_file_path = "bigmart_sales_final_predictions.csv"
submission_df.to_csv(final_submission_file_path, index=False)

print(f"✅ Predictions saved successfully! Download your file here: {final_submission_file_path}")