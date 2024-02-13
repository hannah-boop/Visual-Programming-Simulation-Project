import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import plot_tree

root = tk.Tk()
root.title("Evaluation Metrics Simulation")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

center_x = int(screen_width/2 - 800 / 2)
center_y = int(screen_height/2 - 600 / 2)

root.geometry(f'800x600+{center_x}+{center_y}')
root.resizable(False, False)

dataset_string = tk.StringVar()
dataset_combo = ttk.Combobox(root, textvariable=dataset_string)
dataset_combo['values'] = ('Iris', 'Diabetes')
dataset_combo['state'] = 'readonly'
dataset_combo.set('Sample datasets')

root.columnconfigure(0, weight=2)
root.columnconfigure(1, weight=1)

dataset_label = tk.Label(root, text="Pick a sample Dataset:")
dataset_label.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)
dataset_combo.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)

evalmetrics_label = tk.Label(root, text="Evaluation Metrics")
evalmetrics_label.grid(column=0, row=6, sticky=tk.W, padx=5, pady=5)

def load_dataset(dataset_name):
    if dataset_name == 'Iris':
        return datasets.load_iris(), 'classification'
    elif dataset_name == 'Diabetes':
        return datasets.load_diabetes(), 'regression'
    else:
        return None, None

def calculate_metrics():
    dataset_name_var = dataset_string.get()
    dataset, problem_type = load_dataset(dataset_name_var)
    if dataset is None:
        return

    # Update labels for dataset title and data model used
    dataset_title_label.config(text=f"Dataset Title: {dataset_name_var}")
    datamodel_used_label.config(text=f"Data Model Used: {'Decision Tree' if problem_type == 'classification' else 'Linear Regression'}")

    # Update evaluation metrics type label
    evalmetrics_type_label.config(text=f"Evaluation Metrics Type: {problem_type.capitalize()}")

    # Sample evaluation metrics
    y_true = dataset.target
    y_pred = np.random.randint(0, high=np.max(y_true), size=len(y_true))

    if problem_type == 'classification':
        accuracy = accuracy_score(y_true, y_pred)
        precision = precision_score(y_true, y_pred, average='weighted', zero_division=1)
        recall = recall_score(y_true, y_pred, average='weighted')
        f1 = f1_score(y_true, y_pred, average='weighted')

        accuracy_label.config(text=f"Accuracy: {accuracy:.2f}")
        precision_label.config(text=f"Precision: {precision:.2f}")
        recall_label.config(text=f"Recall: {recall:.2f}")
        f1_label.config(text=f"F1 Score: {f1:.2f}")

        mse_label.config(text="")
        rmse_label.config(text="")
        mae_label.config(text="")
        r2_label.config(text="")

        # Display data visualization for decision tree
        plot_decision_tree(dataset)

    elif problem_type == 'regression':
        mse = mean_squared_error(y_true, y_pred)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(y_true, y_pred)
        r2 = r2_score(y_true, y_pred)

        accuracy_label.config(text="")
        precision_label.config(text="")
        recall_label.config(text="")
        f1_label.config(text="")

        mse_label.config(text=f"Mean Squared Error: {mse:.2f}")
        rmse_label.config(text=f"Root Mean Squared Error: {rmse:.2f}")
        mae_label.config(text=f"Mean Absolute Error: {mae:.2f}")
        r2_label.config(text=f"R2 Score: {r2:.2f}")

        # Display data visualization for linear regression
        plot_linear_regression(dataset)

def plot_decision_tree(dataset):
    X = dataset.data
    y = dataset.target

    model = DecisionTreeClassifier()
    model.fit(X, y)

    plt.figure(figsize=(10, 7))
    plot_tree(model, filled=True, feature_names=dataset.feature_names, class_names=dataset.target_names)
    plt.title('Decision Tree Visualization')
    plt.show()

def plot_linear_regression(dataset):
    X = dataset.data[:, np.newaxis, 2]
    y = dataset.target

    model = LinearRegression()
    model.fit(X, y)

    plt.scatter(X, y, color='black')
    plt.plot(X, model.predict(X), color='blue', linewidth=3)
    plt.xlabel('Feature')
    plt.ylabel('Target')
    plt.title('Linear Regression')
    plt.show()

calculate_button = ttk.Button(root, text="Calculate Metrics", command=calculate_metrics)
calculate_button.grid(column=0, row=7, sticky=tk.W, padx=5, pady=5)

def clear_all():
    dataset_combo.set('Sample datasets')
    dataset_title_label.config(text="")
    datamodel_used_label.config(text="")
    evalmetrics_type_label.config(text="")
    accuracy_label.config(text="")
    precision_label.config(text="")
    recall_label.config(text="")
    f1_label.config(text="")
    mse_label.config(text="")
    rmse_label.config(text="")
    mae_label.config(text="")
    r2_label.config(text="")

clear_button = ttk.Button(root, text="Clear All", command=clear_all)
clear_button.grid(column=1, row=7, sticky=tk.W, padx=5, pady=5)

dataset_title_label = tk.Label(root, text="")
dataset_title_label.grid(column=0, row=8, sticky=tk.W, padx=5, pady=5)

evalmetrics_type_label = tk.Label(root, text="")
evalmetrics_type_label.grid(column=0, row=9, sticky=tk.W, padx=5, pady=5)

datamodel_used_label = tk.Label(root, text="")
datamodel_used_label.grid(column=0, row=10, sticky=tk.W, padx=5, pady=5)

accuracy_label = tk.Label(root, text="Accuracy: ")
accuracy_label.grid(column=1, row=8, sticky=tk.W, padx=5, pady=5)

precision_label = tk.Label(root, text="Precision: ")
precision_label.grid(column=1, row=9, sticky=tk.W, padx=5, pady=5)

recall_label = tk.Label(root, text="Recall: ")
recall_label.grid(column=1, row=10, sticky=tk.W, padx=5, pady=5)

f1_label = tk.Label(root, text="F1 Score: ")
f1_label.grid(column=1, row=11, sticky=tk.W, padx=5, pady=5)

mse_label = tk.Label(root, text="Mean Squared Error: ")
mse_label.grid(column=1, row=12, sticky=tk.W, padx=5, pady=5)

rmse_label = tk.Label(root, text="Root Mean Squared Error: ")
rmse_label.grid(column=1, row=13, sticky=tk.W, padx=5, pady=5)

mae_label = tk.Label(root, text="Mean Absolute Error: ")
mae_label.grid(column=1, row=14, sticky=tk.W, padx=5, pady=5)

r2_label = tk.Label(root, text="R2 Score: ")
r2_label.grid(column=1, row=15, sticky=tk.W, padx=5, pady=5)

def update_data_models(event):
    pass

dataset_combo.bind("<<ComboboxSelected>>", update_data_models)

root.mainloop()
