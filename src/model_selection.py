from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
import lightgbm as lgb
import xgboost as xgb
from torch.utils.tensorboard import SummaryWriter
import pandas as pd
from config.paths_config import *
from src.logger import get_logger
from src.custom_exception import CustomException
import matplotlib.pyplot as plt
import time

logger = get_logger(__name__)

class ClassifierComparison:
    def __init__(self, data_path):
        self.data_path = data_path
        run_id = time.strftime("%Y%m%d-%H%M%S")
        self.writer = SummaryWriter(log_dir=f"tensorboard_logs/run_{run_id}")

        self.models = {
            'Logistic Regression': LogisticRegression(),
            'Random Forest': RandomForestClassifier(n_estimators=50, n_jobs=-1),
            'Gradient Boosting': GradientBoostingClassifier(n_estimators=50),
            'AdaBoost': AdaBoostClassifier(n_estimators=50),
            'Support Vector Classifier': SVC(),
            'K-Nearest Neighbors': KNeighborsClassifier(),
            'Naive Bayes': GaussianNB(),
            'Decision Tree': DecisionTreeClassifier(),
            'LightGBM': lgb.LGBMClassifier(),
            'XGBoost': xgb.XGBClassifier(eval_metric='mlogloss')
        }
        self.results = {}

    def load_data(self):
        try:
            logger.info("Loading data from CSV")
            df = pd.read_csv(self.data_path)
            df_sample = df.sample(frac=0.1, random_state=42)  # Sample 5% of the data
            X = df_sample.drop(columns='satisfaction')
            y = df_sample['satisfaction']
            logger.info("Data loaded and sampled successfully")
            return X, y
        except Exception as e:
            raise CustomException(f"Error loading data: {str(e)}")

    def split_data(self, X, y):
        try:
            logger.info("Splitting data into train and test sets")
            return train_test_split(X, y, test_size=0.2, random_state=42)
        except Exception as e:
            raise CustomException(f"Error splitting data: {str(e)}")

    def log_confusion_matrix(self, y_true, y_pred, step, model_name):
        cm = confusion_matrix(y_true, y_pred)
        fig, ax = plt.subplots(figsize=(5, 5))
        ax.matshow(cm, cmap=plt.cm.Blues, alpha=0.7)
        for i in range(cm.shape[0]):
            for j in range(cm.shape[1]):
                ax.text(x=j, y=i, s=cm[i, j], va='center', ha='center')

        plt.xlabel('Predicted Labels')
        plt.ylabel('True Labels')
        plt.title(f'Confusion Matrix: {model_name}')
        self.writer.add_figure(f'Confusion Matrix/{model_name}', fig, global_step=step)
        plt.close(fig)

    def train_and_evaluate(self, X_train, X_test, y_train, y_test):
        try:
            logger.info("Training and evaluating classifiers")
            for idx, (name, model) in enumerate(self.models.items()):
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)

                # Metrics
                accuracy = accuracy_score(y_test, y_pred)
                precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
                recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
                f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)

                # Log results
                self.results[name] = {
                    'accuracy': accuracy,
                    'precision': precision,
                    'recall': recall,
                    'f1_score': f1
                }
                logger.info(f"{name} trained successfully with metrics: "
                            f"Accuracy: {accuracy:.4f}, Precision: {precision:.4f}, Recall: {recall:.4f}, F1 Score: {f1:.4f}")

                # Log metrics to TensorBoard
                self.writer.add_scalar(f'Accuracy/{name}', accuracy, idx)
                self.writer.add_scalar(f'Precision/{name}', precision, idx)
                self.writer.add_scalar(f'Recall/{name}', recall, idx)
                self.writer.add_scalar(f'F1 Score/{name}', f1, idx)
                self.writer.add_text('Model Details', f"{name}: "
                                                      f"Accuracy: {accuracy:.4f}, "
                                                      f"Precision: {precision:.4f}, "
                                                      f"Recall: {recall:.4f}, "
                                                      f"F1 Score: {f1:.4f}", idx)

                # Log confusion matrix
                self.log_confusion_matrix(y_test, y_pred, idx, name)

            self.writer.close()
        except Exception as e:
            raise CustomException(f"Error during model training or evaluation: {str(e)}")

    def run(self):
        try:
            logger.info("Starting the classifier comparison pipeline")
            X, y = self.load_data()
            X_train, X_test, y_train, y_test = self.split_data(X, y)
            self.train_and_evaluate(X_train, X_test, y_train, y_test)
            logger.info("Classifier comparison completed successfully")
        except CustomException as ce:
            logger.error(f"Pipeline error: {str(ce)}")
            raise

if __name__ == "__main__":
    pipeline = ClassifierComparison(ENGINNERED_DATA)
    pipeline.run()

    print("To view results, run the following command in your terminal:")
    print("tensorboard --logdir=tensorboard_logs")
    print("Then open the displayed URL in your browser.")