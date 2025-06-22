# 🚗 Car Dekho – Used Car Price Prediction

# Hello everyone,

This is my machine learning project where I worked on predicting the price of used cars. The goal was to create a model that can tell us how much a car is worth, based on its features like year, fuel type, kilometers driven, transmission type, and more.

# 🧩 Step-by-Step Process I Followed:

# 1. Collected the Data

I started by using a dataset that had details about used cars – like car name, how many kilometers it had run, fuel type, price, and other information.

# 2. Cleaned the Data

The data wasn't clean, so I had to fix it.
For example:

I removed unwanted text from columns like “km driven” (e.g., removed ‘km’).

I converted text into numbers where needed, so the model could understand it.

I dropped unnecessary columns that were not helpful for prediction (like car name).

# 3. Understood the Data (EDA)

I then explored the data to understand:

Which features affect the price the most.

How things like year, fuel type, or km driven impact the price.
I used graphs and charts to see patterns and spot any outliers or strange values.

# 4. Converted Categorical Values

Some columns had words like “Petrol”, “Diesel”, “Manual”, “Automatic”, etc.
I converted them into numbers using encoding so that the machine learning model could work with them.

# 5. Trained the Models

I selected useful columns and split the data into two parts:

Training Data: to train the model.

Testing Data: to check how well the model performs.

Then, I trained different models like:

Linear Regression

Lasso Regression

Ridge Regression

Random Forest

Among all, Random Forest performed the best because it combines multiple decision trees and gives better accuracy.

# 6. Tested the Model

I gave some new inputs (like car year, fuel type, transmission, etc.) and checked what price the model predicted. It worked well and gave results close to the actual price.

# ✅ Why I Did Each Step:

 1.Cleaning  was important to remove messy or incorrect values.

2.EDA helped me understand how features affect price.

3.Encoding was needed because ML models can’t work with text.

4.Training and Testing helped in making sure the model works well on new data.

# 🎯 Final Output

In the end, I got a working model that can predict the price of a used car based on its details. This can help car buyers and sellers make better decisions.

