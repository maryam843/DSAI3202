{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "7de9702f-52b3-4eda-a452-e4a1c50e4838",
   "metadata": {},
   "outputs": [],
   "source": [
    "from sklearn.metrics import classification_report\n",
    "\n",
    "def evaluate_model(model, X_test, y_test):\n",
    "    \"\"\"\n",
    "    Evaluates the trained model using test data and generates a classification report.\n",
    "\n",
    "    Args:\n",
    "        model (RandomForestClassifier): The trained machine learning model.\n",
    "        X_test (pandas.DataFrame): The test features.\n",
    "        y_test (pandas.Series): The test labels.\n",
    "\n",
    "    Returns:\n",
    "        str: A classification report as a string.\n",
    "    \"\"\"\n",
    "    predictions = model.predict(X_test)\n",
    "    return classification_report(y_test, predictions)"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
