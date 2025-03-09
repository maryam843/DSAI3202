{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "055c289e-38c2-4d3b-a598-14683c2e5cfe",
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "\n",
    "def load_data():\n",
    "    \"\"\"\n",
    "    Loads the Iris dataset from an online source.\n",
    "\n",
    "    Returns:\n",
    "        pandas.DataFrame: The loaded dataset containing features and labels.\n",
    "    \"\"\"\n",
    "    url = \"https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv\"\n",
    "    data = pd.read_csv(url)\n",
    "    return data"
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
