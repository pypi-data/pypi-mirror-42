# Pickle model with joblib
import joblib

from sklearn import datasets, model_selection, neighbors

diabetes = datasets.load_diabetes()

x_train, x_test, y_train, y_test = model_selection.train_test_split(
    diabetes.data, diabetes.target, test_size=0.33, random_state=42)

knn = neighbors.KNeighborsRegressor().fit(x_train, y_train)

joblib.dump(knn, 'src/persis/models/knn.pkl')
