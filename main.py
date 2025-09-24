from fastapi import FastAPI
from etl.process import elt_transform
from schema.input import InputSchema
import pickle

from fastapi import FastAPI
import pickle
from schema.input import InputSchema
from etl.process import elt_transform

app = FastAPI(
    title="Credit Card Fraud Detection API",
    description="""
API para predecir fraudes en transacciones de tarjetas de crédito usando un modelo XGBoost entrenado.
Incluye ETL para transformación y escalado de features, y predicción de fraude con probabilidad.
""",
    version="1.0.0",
    contact={
        "name": "César Álvarez",
        "email": "cealalvarezr@gmail.com",
    },
)

# Cargar modelo entrenado
with open("ml_models\\model_fraud.pkl","rb") as f:
    fraud_predict_model = pickle.load(f)

@app.get("/", summary="Prueba de disponibilidad de la API")
def test_api():
    """
    Endpoint de prueba para verificar que la API está corriendo correctamente.

    Returns:
        dict: Mensaje de estado con código HTTP 200
    """
    return {
        "status": 200,
        "detail": "API funcionando correctamente"
    }

@app.post("/api/etl", summary="Transformación ETL de datos")
def etl_process(input_user: InputSchema):
    """
    Aplica el pipeline de ETL a los datos de entrada.

    Args:
        input_user (InputSchema): Transacción con campos Time, Amount, V1...V28

    Returns:
        dict: Contiene:
            - status (int): Código HTTP
            - data (list of dict): DataFrame transformado como lista de diccionarios
    """
    try:
        user_dict = input_user.model_dump()
        df = elt_transform(user_dict)
        return {
            "status": 200,
            "data": df.to_dict(orient="records")
        }
    except Exception as e:
        return {
            "status": 500,
            "detail": str(e)
        }

@app.post("/api/predict", summary="Predicción de fraude")
def predict_fraud(input_user: InputSchema):
    """
    Realiza la predicción de fraude en una transacción.

    Args:
        input_user (InputSchema): Transacción con campos Time, Amount, V1...V28

    Returns:
        dict: Contiene:
            - status (int): Código HTTP
            - prediction (str): "Fraude" o "No Fraude"
            - probability (float): Probabilidad de que la transacción sea fraudulenta
    """
    try:
        user_dict = input_user.model_dump()
        df = elt_transform(user_dict)

        # Predicción
        prediction = fraud_predict_model.predict(df)
        probability = fraud_predict_model.predict_proba(df)[:,1][0]

        result = "Fraude" if int(prediction[0]) == 1 else "No Fraude"

        return {
            "status": 200,
            "prediction": result,
            "probability": float(probability)
        }
    except Exception as e:
        return {
            "status": 500,
            "detail": str(e)
        }
