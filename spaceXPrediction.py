{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "<p style=\"text-align:center\">\n",
    "    <a href=\"https://skills.network/?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMDS0321ENSkillsNetwork26802033-2022-01-01\" target=\"_blank\">\n",
    "    <img src=\"https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/assets/logos/SN_web_lightmode.png\" width=\"200\" alt=\"Skills Network Logo\"  />\n",
    "    </a>\n",
    "</p>\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# **Space X  Falcon 9 First Stage Landing Prediction**\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Assignment:  Machine Learning Prediction\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Estimated time needed: **60** minutes\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Space X advertises Falcon 9 rocket launches on its website with a cost of 62 million dollars; other providers cost upward of 165 million dollars each, much of the savings is because Space X can reuse the first stage. Therefore if we can determine if the first stage will land, we can determine the cost of a launch. This information can be used if an alternate company wants to bid against space X for a rocket launch.   In this lab, you will create a machine learning pipeline  to predict if the first stage will land given the data from the preceding labs.\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "![](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DS0701EN-SkillsNetwork/api/Images/landing\\_1.gif)\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Several examples of an unsuccessful landing are shown here:\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "![](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DS0701EN-SkillsNetwork/api/Images/crash.gif)\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Most unsuccessful landings are planed. Space X; performs a controlled landing in the oceans.\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Objectives\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Perform exploratory  Data Analysis and determine Training Labels\n",
    "\n",
    "*   create a column for the class\n",
    "*   Standardize the data\n",
    "*   Split into training data and test data\n",
    "\n",
    "\\-Find best Hyperparameter for SVM, Classification Trees and Logistic Regression\n",
    "\n",
    "*   Find the method performs best using test data\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": []
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "***\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Import Libraries and Define Auxiliary Functions\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "We will import the following libraries for the lab\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Pandas is a software library written for the Python programming language for data manipulation and analysis.\n",
    "import pandas as pd\n",
    "# NumPy is a library for the Python programming language, adding support for large, multi-dimensional arrays and matrices, along with a large collection of high-level mathematical functions to operate on these arrays\n",
    "import numpy as np\n",
    "# Matplotlib is a plotting library for python and pyplot gives us a MatLab like plotting framework. We will use this in our plotter function to plot data.\n",
    "import matplotlib.pyplot as plt\n",
    "#Seaborn is a Python data visualization library based on matplotlib. It provides a high-level interface for drawing attractive and informative statistical graphics\n",
    "import seaborn as sns\n",
    "# Preprocessing allows us to standarsize our data\n",
    "from sklearn import preprocessing\n",
    "# Allows us to split our data into training and testing data\n",
    "from sklearn.model_selection import train_test_split\n",
    "# Allows us to test parameters of classification algorithms and find the best one\n",
    "from sklearn.model_selection import GridSearchCV\n",
    "# Logistic Regression classification algorithm\n",
    "from sklearn.linear_model import LogisticRegression\n",
    "# Support Vector Machine classification algorithm\n",
    "from sklearn.svm import SVC\n",
    "# Decision Tree classification algorithm\n",
    "from sklearn.tree import DecisionTreeClassifier\n",
    "# K Nearest Neighbors classification algorithm\n",
    "from sklearn.neighbors import KNeighborsClassifier"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "This function is to plot the confusion matrix.\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [],
   "source": [
    "def plot_confusion_matrix(y,y_predict):\n",
    "    \"this function plots the confusion matrix\"\n",
    "    from sklearn.metrics import confusion_matrix\n",
    "\n",
    "    cm = confusion_matrix(y, y_predict)\n",
    "    ax= plt.subplot()\n",
    "    sns.heatmap(cm, annot=True, ax = ax); #annot=True to annotate cells\n",
    "    ax.set_xlabel('Predicted labels')\n",
    "    ax.set_ylabel('True labels')\n",
    "    ax.set_title('Confusion Matrix'); \n",
    "    ax.xaxis.set_ticklabels(['did not land', 'land']); ax.yaxis.set_ticklabels(['did not land', 'landed'])"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Load the dataframe\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Load the data\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>FlightNumber</th>\n",
       "      <th>Date</th>\n",
       "      <th>BoosterVersion</th>\n",
       "      <th>PayloadMass</th>\n",
       "      <th>Orbit</th>\n",
       "      <th>LaunchSite</th>\n",
       "      <th>Outcome</th>\n",
       "      <th>Flights</th>\n",
       "      <th>GridFins</th>\n",
       "      <th>Reused</th>\n",
       "      <th>Legs</th>\n",
       "      <th>LandingPad</th>\n",
       "      <th>Block</th>\n",
       "      <th>ReusedCount</th>\n",
       "      <th>Serial</th>\n",
       "      <th>Longitude</th>\n",
       "      <th>Latitude</th>\n",
       "      <th>Class</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>1</td>\n",
       "      <td>2010-06-04</td>\n",
       "      <td>Falcon 9</td>\n",
       "      <td>6104.959412</td>\n",
       "      <td>LEO</td>\n",
       "      <td>CCAFS SLC 40</td>\n",
       "      <td>None None</td>\n",
       "      <td>1</td>\n",
       "      <td>False</td>\n",
       "      <td>False</td>\n",
       "      <td>False</td>\n",
       "      <td>NaN</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0</td>\n",
       "      <td>B0003</td>\n",
       "      <td>-80.577366</td>\n",
       "      <td>28.561857</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>2</td>\n",
       "      <td>2012-05-22</td>\n",
       "      <td>Falcon 9</td>\n",
       "      <td>525.000000</td>\n",
       "      <td>LEO</td>\n",
       "      <td>CCAFS SLC 40</td>\n",
       "      <td>None None</td>\n",
       "      <td>1</td>\n",
       "      <td>False</td>\n",
       "      <td>False</td>\n",
       "      <td>False</td>\n",
       "      <td>NaN</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0</td>\n",
       "      <td>B0005</td>\n",
       "      <td>-80.577366</td>\n",
       "      <td>28.561857</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>3</td>\n",
       "      <td>2013-03-01</td>\n",
       "      <td>Falcon 9</td>\n",
       "      <td>677.000000</td>\n",
       "      <td>ISS</td>\n",
       "      <td>CCAFS SLC 40</td>\n",
       "      <td>None None</td>\n",
       "      <td>1</td>\n",
       "      <td>False</td>\n",
       "      <td>False</td>\n",
       "      <td>False</td>\n",
       "      <td>NaN</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0</td>\n",
       "      <td>B0007</td>\n",
       "      <td>-80.577366</td>\n",
       "      <td>28.561857</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>4</td>\n",
       "      <td>2013-09-29</td>\n",
       "      <td>Falcon 9</td>\n",
       "      <td>500.000000</td>\n",
       "      <td>PO</td>\n",
       "      <td>VAFB SLC 4E</td>\n",
       "      <td>False Ocean</td>\n",
       "      <td>1</td>\n",
       "      <td>False</td>\n",
       "      <td>False</td>\n",
       "      <td>False</td>\n",
       "      <td>NaN</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0</td>\n",
       "      <td>B1003</td>\n",
       "      <td>-120.610829</td>\n",
       "      <td>34.632093</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>5</td>\n",
       "      <td>2013-12-03</td>\n",
       "      <td>Falcon 9</td>\n",
       "      <td>3170.000000</td>\n",
       "      <td>GTO</td>\n",
       "      <td>CCAFS SLC 40</td>\n",
       "      <td>None None</td>\n",
       "      <td>1</td>\n",
       "      <td>False</td>\n",
       "      <td>False</td>\n",
       "      <td>False</td>\n",
       "      <td>NaN</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0</td>\n",
       "      <td>B1004</td>\n",
       "      <td>-80.577366</td>\n",
       "      <td>28.561857</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "   FlightNumber        Date BoosterVersion  PayloadMass Orbit    LaunchSite  \\\n",
       "0             1  2010-06-04       Falcon 9  6104.959412   LEO  CCAFS SLC 40   \n",
       "1             2  2012-05-22       Falcon 9   525.000000   LEO  CCAFS SLC 40   \n",
       "2             3  2013-03-01       Falcon 9   677.000000   ISS  CCAFS SLC 40   \n",
       "3             4  2013-09-29       Falcon 9   500.000000    PO   VAFB SLC 4E   \n",
       "4             5  2013-12-03       Falcon 9  3170.000000   GTO  CCAFS SLC 40   \n",
       "\n",
       "       Outcome  Flights  GridFins  Reused   Legs LandingPad  Block  \\\n",
       "0    None None        1     False   False  False        NaN    1.0   \n",
       "1    None None        1     False   False  False        NaN    1.0   \n",
       "2    None None        1     False   False  False        NaN    1.0   \n",
       "3  False Ocean        1     False   False  False        NaN    1.0   \n",
       "4    None None        1     False   False  False        NaN    1.0   \n",
       "\n",
       "   ReusedCount Serial   Longitude   Latitude  Class  \n",
       "0            0  B0003  -80.577366  28.561857      0  \n",
       "1            0  B0005  -80.577366  28.561857      0  \n",
       "2            0  B0007  -80.577366  28.561857      0  \n",
       "3            0  B1003 -120.610829  34.632093      0  \n",
       "4            0  B1004  -80.577366  28.561857      0  "
      ]
     },
     "execution_count": 7,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "data = pd.read_csv(\"https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_2.csv\")\n",
    "\n",
    "# If you were unable to complete the previous lab correctly you can uncomment and load this csv\n",
    "\n",
    "# data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DS0701EN-SkillsNetwork/api/dataset_part_2.csv')\n",
    "\n",
    "data.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>FlightNumber</th>\n",
       "      <th>PayloadMass</th>\n",
       "      <th>Flights</th>\n",
       "      <th>Block</th>\n",
       "      <th>ReusedCount</th>\n",
       "      <th>Orbit_ES-L1</th>\n",
       "      <th>Orbit_GEO</th>\n",
       "      <th>Orbit_GTO</th>\n",
       "      <th>Orbit_HEO</th>\n",
       "      <th>Orbit_ISS</th>\n",
       "      <th>...</th>\n",
       "      <th>Serial_B1058</th>\n",
       "      <th>Serial_B1059</th>\n",
       "      <th>Serial_B1060</th>\n",
       "      <th>Serial_B1062</th>\n",
       "      <th>GridFins_False</th>\n",
       "      <th>GridFins_True</th>\n",
       "      <th>Reused_False</th>\n",
       "      <th>Reused_True</th>\n",
       "      <th>Legs_False</th>\n",
       "      <th>Legs_True</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>1.0</td>\n",
       "      <td>6104.959412</td>\n",
       "      <td>1.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>...</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0.0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>2.0</td>\n",
       "      <td>525.000000</td>\n",
       "      <td>1.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>...</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0.0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>3.0</td>\n",
       "      <td>677.000000</td>\n",
       "      <td>1.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>...</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0.0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>4.0</td>\n",
       "      <td>500.000000</td>\n",
       "      <td>1.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>...</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0.0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>5.0</td>\n",
       "      <td>3170.000000</td>\n",
       "      <td>1.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>...</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0.0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>...</th>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>85</th>\n",
       "      <td>86.0</td>\n",
       "      <td>15400.000000</td>\n",
       "      <td>2.0</td>\n",
       "      <td>5.0</td>\n",
       "      <td>2.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>...</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>1.0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>86</th>\n",
       "      <td>87.0</td>\n",
       "      <td>15400.000000</td>\n",
       "      <td>3.0</td>\n",
       "      <td>5.0</td>\n",
       "      <td>2.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>...</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>1.0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>87</th>\n",
       "      <td>88.0</td>\n",
       "      <td>15400.000000</td>\n",
       "      <td>6.0</td>\n",
       "      <td>5.0</td>\n",
       "      <td>5.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>...</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>1.0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>88</th>\n",
       "      <td>89.0</td>\n",
       "      <td>15400.000000</td>\n",
       "      <td>3.0</td>\n",
       "      <td>5.0</td>\n",
       "      <td>2.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>...</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>1.0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>89</th>\n",
       "      <td>90.0</td>\n",
       "      <td>3681.000000</td>\n",
       "      <td>1.0</td>\n",
       "      <td>5.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>...</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>1.0</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "<p>90 rows × 83 columns</p>\n",
       "</div>"
      ],
      "text/plain": [
       "    FlightNumber   PayloadMass  Flights  Block  ReusedCount  Orbit_ES-L1  \\\n",
       "0            1.0   6104.959412      1.0    1.0          0.0          0.0   \n",
       "1            2.0    525.000000      1.0    1.0          0.0          0.0   \n",
       "2            3.0    677.000000      1.0    1.0          0.0          0.0   \n",
       "3            4.0    500.000000      1.0    1.0          0.0          0.0   \n",
       "4            5.0   3170.000000      1.0    1.0          0.0          0.0   \n",
       "..           ...           ...      ...    ...          ...          ...   \n",
       "85          86.0  15400.000000      2.0    5.0          2.0          0.0   \n",
       "86          87.0  15400.000000      3.0    5.0          2.0          0.0   \n",
       "87          88.0  15400.000000      6.0    5.0          5.0          0.0   \n",
       "88          89.0  15400.000000      3.0    5.0          2.0          0.0   \n",
       "89          90.0   3681.000000      1.0    5.0          0.0          0.0   \n",
       "\n",
       "    Orbit_GEO  Orbit_GTO  Orbit_HEO  Orbit_ISS  ...  Serial_B1058  \\\n",
       "0         0.0        0.0        0.0        0.0  ...           0.0   \n",
       "1         0.0        0.0        0.0        0.0  ...           0.0   \n",
       "2         0.0        0.0        0.0        1.0  ...           0.0   \n",
       "3         0.0        0.0        0.0        0.0  ...           0.0   \n",
       "4         0.0        1.0        0.0        0.0  ...           0.0   \n",
       "..        ...        ...        ...        ...  ...           ...   \n",
       "85        0.0        0.0        0.0        0.0  ...           0.0   \n",
       "86        0.0        0.0        0.0        0.0  ...           1.0   \n",
       "87        0.0        0.0        0.0        0.0  ...           0.0   \n",
       "88        0.0        0.0        0.0        0.0  ...           0.0   \n",
       "89        0.0        0.0        0.0        0.0  ...           0.0   \n",
       "\n",
       "    Serial_B1059  Serial_B1060  Serial_B1062  GridFins_False  GridFins_True  \\\n",
       "0            0.0           0.0           0.0             1.0            0.0   \n",
       "1            0.0           0.0           0.0             1.0            0.0   \n",
       "2            0.0           0.0           0.0             1.0            0.0   \n",
       "3            0.0           0.0           0.0             1.0            0.0   \n",
       "4            0.0           0.0           0.0             1.0            0.0   \n",
       "..           ...           ...           ...             ...            ...   \n",
       "85           0.0           1.0           0.0             0.0            1.0   \n",
       "86           0.0           0.0           0.0             0.0            1.0   \n",
       "87           0.0           0.0           0.0             0.0            1.0   \n",
       "88           0.0           1.0           0.0             0.0            1.0   \n",
       "89           0.0           0.0           1.0             0.0            1.0   \n",
       "\n",
       "    Reused_False  Reused_True  Legs_False  Legs_True  \n",
       "0            1.0          0.0         1.0        0.0  \n",
       "1            1.0          0.0         1.0        0.0  \n",
       "2            1.0          0.0         1.0        0.0  \n",
       "3            1.0          0.0         1.0        0.0  \n",
       "4            1.0          0.0         1.0        0.0  \n",
       "..           ...          ...         ...        ...  \n",
       "85           0.0          1.0         0.0        1.0  \n",
       "86           0.0          1.0         0.0        1.0  \n",
       "87           0.0          1.0         0.0        1.0  \n",
       "88           0.0          1.0         0.0        1.0  \n",
       "89           1.0          0.0         0.0        1.0  \n",
       "\n",
       "[90 rows x 83 columns]"
      ]
     },
     "execution_count": 8,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "X = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_3.csv')\n",
    "\n",
    "# If you were unable to complete the previous lab correctly you can uncomment and load this csv\n",
    "\n",
    "# X = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DS0701EN-SkillsNetwork/api/dataset_part_3.csv')\n",
    "\n",
    "X.head(100)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## TASK  1\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Create a NumPy array from the column <code>Class</code> in <code>data</code>, by applying the method <code>to_numpy()</code>  then\n",
    "assign it  to the variable <code>Y</code>,make sure the output is a  Pandas series (only one bracket df\\['name of  column']).\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "array([0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1,\n",
       "       1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1,\n",
       "       1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1,\n",
       "       1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,\n",
       "       1, 1], dtype=int64)"
      ]
     },
     "execution_count": 9,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "Y = data[\"Class\"].to_numpy()\n",
    "Y"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## TASK  2\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Standardize the data in <code>X</code> then reassign it to the variable  <code>X</code> using the transform provided below.\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# students get this \n",
    "transform = preprocessing.StandardScaler()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "array([[-1.71291154e+00, -1.94814463e-16, -6.53912840e-01, ...,\n",
       "        -8.35531692e-01,  1.93309133e+00, -1.93309133e+00],\n",
       "       [-1.67441914e+00, -1.19523159e+00, -6.53912840e-01, ...,\n",
       "        -8.35531692e-01,  1.93309133e+00, -1.93309133e+00],\n",
       "       [-1.63592675e+00, -1.16267307e+00, -6.53912840e-01, ...,\n",
       "        -8.35531692e-01,  1.93309133e+00, -1.93309133e+00],\n",
       "       ...,\n",
       "       [ 1.63592675e+00,  1.99100483e+00,  3.49060516e+00, ...,\n",
       "         1.19684269e+00, -5.17306132e-01,  5.17306132e-01],\n",
       "       [ 1.67441914e+00,  1.99100483e+00,  1.00389436e+00, ...,\n",
       "         1.19684269e+00, -5.17306132e-01,  5.17306132e-01],\n",
       "       [ 1.71291154e+00, -5.19213966e-01, -6.53912840e-01, ...,\n",
       "        -8.35531692e-01, -5.17306132e-01,  5.17306132e-01]])"
      ]
     },
     "execution_count": 11,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "X = transform.fit_transform(X) \n",
    "X"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "We split the data into training and testing data using the  function  <code>train_test_split</code>.   The training data is divided into validation data, a second set used for training  data; then the models are trained and hyperparameters are selected using the function <code>GridSearchCV</code>.\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## TASK  3\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Use the function train_test_split to split the data X and Y into training and test data. Set the parameter test_size to  0.2 and random_state to 2. The training data and test data should be assigned to the following labels.\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "<code>X_train, X_test, Y_train, Y_test</code>\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "metadata": {},
   "outputs": [],
   "source": [
    "X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=2)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "we can see we only have 18 test samples.\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "(18,)"
      ]
     },
     "execution_count": 13,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "Y_test.shape"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## TASK  4\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Create a logistic regression object  then create a  GridSearchCV object  <code>logreg_cv</code> with cv = 10.  Fit the object to find the best parameters from the dictionary <code>parameters</code>.\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 14,
   "metadata": {},
   "outputs": [],
   "source": [
    "parameters ={'C':[0.01,0.1,1],\n",
    "             'penalty':['l2'],\n",
    "             'solver':['lbfgs']}"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 17,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "GridSearchCV(cv=10, estimator=LogisticRegression(),\n",
       "             param_grid={'C': [0.01, 0.1, 1], 'penalty': ['l2'],\n",
       "                         'solver': ['lbfgs']})"
      ]
     },
     "execution_count": 17,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "parameters ={\"C\":[0.01,0.1,1],'penalty':['l2'], 'solver':['lbfgs']}# l1 lasso l2 ridge\n",
    "lr=LogisticRegression()\n",
    "\n",
    "logreg_cv = GridSearchCV(lr, parameters, cv=10)\n",
    "\n",
    "logreg_cv.fit(X_train, Y_train)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "We output the <code>GridSearchCV</code> object for logistic regression. We display the best parameters using the data attribute <code>best_params\\_</code> and the accuracy on the validation data using the data attribute <code>best_score\\_</code>.\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 18,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "tuned hpyerparameters :(best parameters)  {'C': 0.01, 'penalty': 'l2', 'solver': 'lbfgs'}\n",
      "accuracy : 0.8464285714285713\n"
     ]
    }
   ],
   "source": [
    "print(\"tuned hpyerparameters :(best parameters) \",logreg_cv.best_params_)\n",
    "print(\"accuracy :\",logreg_cv.best_score_)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## TASK  5\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Calculate the accuracy on the test data using the method <code>score</code>:\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 19,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "0.8333333333333334"
      ]
     },
     "execution_count": 19,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "logreg_cv.score(X_test, Y_test)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Lets look at the confusion matrix:\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 20,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 432x288 with 2 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "yhat=logreg_cv.predict(X_test)\n",
    "plot_confusion_matrix(Y_test,yhat)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Examining the confusion matrix, we see that logistic regression can distinguish between the different classes.  We see that the major problem is false positives.\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## TASK  6\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Create a support vector machine object then  create a  <code>GridSearchCV</code> object  <code>svm_cv</code> with cv - 10.  Fit the object to find the best parameters from the dictionary <code>parameters</code>.\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 21,
   "metadata": {},
   "outputs": [],
   "source": [
    "parameters = {'kernel':('linear', 'rbf','poly','rbf', 'sigmoid'),\n",
    "              'C': np.logspace(-3, 3, 5),\n",
    "              'gamma':np.logspace(-3, 3, 5)}\n",
    "svm = SVC()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 22,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "GridSearchCV(cv=10, estimator=SVC(),\n",
       "             param_grid={'C': array([1.00000000e-03, 3.16227766e-02, 1.00000000e+00, 3.16227766e+01,\n",
       "       1.00000000e+03]),\n",
       "                         'gamma': array([1.00000000e-03, 3.16227766e-02, 1.00000000e+00, 3.16227766e+01,\n",
       "       1.00000000e+03]),\n",
       "                         'kernel': ('linear', 'rbf', 'poly', 'rbf', 'sigmoid')})"
      ]
     },
     "execution_count": 22,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "svm_cv = GridSearchCV(svm, parameters, cv=10)\n",
    "\n",
    "svm_cv.fit(X_train, Y_train)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 23,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "tuned hpyerparameters :(best parameters)  {'C': 1.0, 'gamma': 0.03162277660168379, 'kernel': 'sigmoid'}\n",
      "accuracy : 0.8482142857142856\n"
     ]
    }
   ],
   "source": [
    "print(\"tuned hpyerparameters :(best parameters) \",svm_cv.best_params_)\n",
    "print(\"accuracy :\",svm_cv.best_score_)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## TASK  7\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Calculate the accuracy on the test data using the method <code>score</code>:\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 24,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "0.8333333333333334"
      ]
     },
     "execution_count": 24,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "svm_cv.score(X_test, Y_test)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "We can plot the confusion matrix\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 25,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 432x288 with 2 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "yhat=svm_cv.predict(X_test)\n",
    "plot_confusion_matrix(Y_test,yhat)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## TASK  8\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Create a decision tree classifier object then  create a  <code>GridSearchCV</code> object  <code>tree_cv</code> with cv = 10.  Fit the object to find the best parameters from the dictionary <code>parameters</code>.\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 26,
   "metadata": {},
   "outputs": [],
   "source": [
    "parameters = {'criterion': ['gini', 'entropy'],\n",
    "     'splitter': ['best', 'random'],\n",
    "     'max_depth': [2*n for n in range(1,10)],\n",
    "     'max_features': ['auto', 'sqrt'],\n",
    "     'min_samples_leaf': [1, 2, 4],\n",
    "     'min_samples_split': [2, 5, 10]}\n",
    "\n",
    "tree = DecisionTreeClassifier()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 27,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "GridSearchCV(cv=10, estimator=DecisionTreeClassifier(),\n",
       "             param_grid={'criterion': ['gini', 'entropy'],\n",
       "                         'max_depth': [2, 4, 6, 8, 10, 12, 14, 16, 18],\n",
       "                         'max_features': ['auto', 'sqrt'],\n",
       "                         'min_samples_leaf': [1, 2, 4],\n",
       "                         'min_samples_split': [2, 5, 10],\n",
       "                         'splitter': ['best', 'random']})"
      ]
     },
     "execution_count": 27,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "tree_cv = GridSearchCV(tree, parameters, cv=10)\n",
    "\n",
    "tree_cv.fit(X_train, Y_train)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 28,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "tuned hpyerparameters :(best parameters)  {'criterion': 'gini', 'max_depth': 16, 'max_features': 'auto', 'min_samples_leaf': 1, 'min_samples_split': 2, 'splitter': 'best'}\n",
      "accuracy : 0.8767857142857143\n"
     ]
    }
   ],
   "source": [
    "print(\"tuned hpyerparameters :(best parameters) \",tree_cv.best_params_)\n",
    "print(\"accuracy :\",tree_cv.best_score_)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## TASK  9\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Calculate the accuracy of tree_cv on the test data using the method <code>score</code>:\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 29,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "0.9444444444444444"
      ]
     },
     "execution_count": 29,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "tree_cv.score(X_test, Y_test)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "We can plot the confusion matrix\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 30,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 432x288 with 2 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "yhat = svm_cv.predict(X_test)\n",
    "plot_confusion_matrix(Y_test,yhat)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## TASK  10\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Create a k nearest neighbors object then  create a  <code>GridSearchCV</code> object  <code>knn_cv</code> with cv = 10.  Fit the object to find the best parameters from the dictionary <code>parameters</code>.\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 31,
   "metadata": {},
   "outputs": [],
   "source": [
    "parameters = {'n_neighbors': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],\n",
    "              'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute'],\n",
    "              'p': [1,2]}\n",
    "\n",
    "KNN = KNeighborsClassifier()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 32,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "GridSearchCV(cv=10, estimator=KNeighborsClassifier(),\n",
       "             param_grid={'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute'],\n",
       "                         'n_neighbors': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],\n",
       "                         'p': [1, 2]})"
      ]
     },
     "execution_count": 32,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "knn_cv = GridSearchCV(KNN, parameters, cv=10)\n",
    "\n",
    "knn_cv.fit(X_train, Y_train)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 33,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "tuned hpyerparameters :(best parameters)  {'algorithm': 'auto', 'n_neighbors': 10, 'p': 1}\n",
      "accuracy : 0.8482142857142858\n"
     ]
    }
   ],
   "source": [
    "print(\"tuned hpyerparameters :(best parameters) \",knn_cv.best_params_)\n",
    "print(\"accuracy :\",knn_cv.best_score_)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## TASK  11\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Calculate the accuracy of tree_cv on the test data using the method <code>score</code>:\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 34,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "0.8333333333333334"
      ]
     },
     "execution_count": 34,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "knn_cv.score(X_test, Y_test)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "We can plot the confusion matrix\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 35,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 432x288 with 2 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "yhat = knn_cv.predict(X_test)\n",
    "plot_confusion_matrix(Y_test,yhat)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## TASK  12\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Find the method performs best:\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 52,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "GridSearchCV(cv=10, estimator=DecisionTreeClassifier(),\n",
      "             param_grid={'criterion': ['gini', 'entropy'],\n",
      "                         'max_depth': [2, 4, 6, 8, 10, 12, 14, 16, 18],\n",
      "                         'max_features': ['auto', 'sqrt'],\n",
      "                         'min_samples_leaf': [1, 2, 4],\n",
      "                         'min_samples_split': [2, 5, 10],\n",
      "                         'splitter': ['best', 'random']})\n"
     ]
    }
   ],
   "source": [
    "predictors = [knn_cv, svm_cv, logreg_cv, tree_cv]\n",
    "best_predictor = {}\n",
    "best_result = 0\n",
    "for predictor in predictors: \n",
    "     best_predictor.update({predictor:predictor.score(X_test, Y_test)})\n",
    "\n",
    "max_value = max(best_predictor, key=best_predictor.get)\n",
    "print(max_value)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Authors\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "<a href=\"https://www.linkedin.com/in/joseph-s-50398b136/?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMDS0321ENSkillsNetwork26802033-2022-01-01\">Joseph Santarcangelo</a> has a PhD in Electrical Engineering, his research focused on using machine learning, signal processing, and computer vision to determine how videos impact human cognition. Joseph has been working for IBM since he completed his PhD.\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Change Log\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "| Date (YYYY-MM-DD) | Version | Changed By    | Change Description      |\n",
    "| ----------------- | ------- | ------------- | ----------------------- |\n",
    "| 2021-08-31        | 1.1     | Lakshmi Holla | Modified markdown       |\n",
    "| 2020-09-20        | 1.0     | Joseph        | Modified Multiple Areas |\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Copyright © 2020 IBM Corporation. All rights reserved.\n"
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
   "version": "3.9.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
