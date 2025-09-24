
# Credit Card Fraud Detection API 

Este proyecto es una **API en FastAPI** que permite predecir fraudes en transacciones con tarjetas de crédito usando un **modelo de machine learning entrenado con XGBoost**. Incluye procesamiento de datos (ETL) y escalado de features para garantizar que las predicciones sean consistentes con el modelo entrenado.

---

## Estructura del proyecto

```graphql
├── etl/
│   └── process.py            # Función de transformación de datos (ETL)
├── ml\_models/
│   ├── model\_fraud.pkl       # Modelo XGBoost entrenado
│   └── scaler\_fraud.pkl      # StandardScaler para Amount y Time
├── schema/
│   └── input.py              # Modelo Pydantic para validación de input
├── main.py                   # Archivo principal de la API FastAPI
├── requirements.txt          # Librerías necesarias

````

---

## Librerías utilizadas

- [FastAPI](https://fastapi.tiangolo.com/) - Framework web para crear la API.  
- [uvicorn](https://www.uvicorn.org/) - Servidor ASGI para correr la API.  
- [pickle](https://docs.python.org/3/library/pickle.html) - Para serializar y cargar el modelo.  
- [pandas](https://pandas.pydata.org/) - Para manipulación de datos.  
- [xgboost](https://xgboost.readthedocs.io/) - Modelo de machine learning para clasificación.

---

## Instalación

1. Clonar el repositorio:

```bash
git clone https://github.com/CesarAAR/api_ml_models.git
cd creditcard-fraud-api
````

2. Crear entorno virtual e instalar dependencias:

```bash
python -m venv venv
source venv/bin/activate  # Linux / Mac
venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

3. Ejecutar la API:

```bash
uvicorn main:app --reload
```

La API estará disponible en `http://127.0.0.1:8000`.

---

## Endpoints

### 1️⃣ `/api/etl` - Transformación de datos

* **Método:** POST
* **Descripción:** Aplica el ETL (transformaciones y escalado) a los datos de entrada y devuelve el DataFrame procesado.
* **Input:** JSON con los campos `Time`, `Amount`, `V1`…`V28`.

**Ejemplo de JSON:**

```json
{
  "Time": 1,
  "V1": -1.358354062,
  "V2": -1.340163075,
  "V3": 1.773209343,
  ...
  "V28": -0.059751841,
  "Amount": 378.66,
}
```

* **Output:** JSON con los datos transformados:

```json
{
  "data": [
    {
      "Time": 0.002,
      "V1": -1.358,
      ...
    }
  ]
}
```

### 2️⃣ `/api/predict` - Predicción de fraude

* **Método:** POST
* **Descripción:** Recibe una transacción, aplica ETL, y devuelve si es fraude y la probabilidad asociada.
* **Input:** Igual que `/api/etl`.
* **Output:**

```json
{
  "prediction": 1,        # 0 = No fraude, 1 = Fraude
  "probability": 0.92     # Probabilidad de fraude
}
```

---

## ⚡ Notas importantes

* El **pipeline de ETL** incluye escalado de `Amount` y `Time` usando el `StandardScaler` entrenado.
* El **orden de las columnas** debe coincidir con el usado en el entrenamiento:

```
['Time', 'V1', 'V2', ..., 'V28', 'Amount']
```

* El modelo fue entrenado con XGBoost, y se ha ajustado un **umbral para optimizar precisión y recall**.

---

## 💡 Contribuciones

Este proyecto puede expandirse para incluir:

* Predicción de múltiples transacciones a la vez.
* Registro de transacciones y resultados en base de datos.
* Endpoint con autenticación y control de usuarios.

---

##  Licencia

MIT License

## Json de Ejemplo:

```
{
  "Time":472,
  "V1": -3.043540624,
  "V2": -3.157307121,
  "V3": 1.08846278,
  "V4": 2.288643618,
  "V5": 1.35980513,
  "V6": -1.064822523,
  "V7": 0.325574266,
  "V8": -0.067793653,
  "V9": -0.270952836,
  "V10": -0.838586565,
  "V11": -0.414575448,
  "V12": -0.50314086,
  "V13": 0.676501545,
  "V14": -1.692028933,
  "V15": 2.000634839,
  "V16": 0.666779696,
  "V17": 0.599717414,
  "V18": 1.725321007,
  "V19": 0.28334483,
  "V20": 2.102338793,
  "V21": 0.661695925,
  "V22": 0.435477209,
  "V23": 1.375965743,
  "V24": -0.293803153,
  "V25": 0.279798032,
  "V26": -0.145361715,
  "V27": -0.252773123,
  "V28": 0.035764225,
  "Amount":529
}
```
```
{
  "Time":1,
  "V1": -1.358354062,
  "V2": -1.340163075,
  "V3": 1.773209343,
  "V4": 0.379779593,
  "V5": -0.503198133,
  "V6": 1.800499381,
  "V7": 0.791460956,
  "V8": 0.247675787,
  "V9": -1.514654323,
  "V10": 0.207642865,
  "V11": 0.624501459,
  "V12": 0.066083685,
  "V13": 0.717292731,
  "V14": -0.165945923,
  "V15": 2.345864949,
  "V16": -2.890083194,
  "V17": 1.109969379,
  "V18": -0.121359313,
  "V19": -2.261857095,
  "V20": 0.524979725,
  "V21": 0.247998153,
  "V22": 0.771679402,
  "V23": 0.909412262,
  "V24": -0.689280956,
  "V25": -0.327641834,
  "V26": -0.139096572,
  "V27": -0.055352794,
  "V28": -0.059751841,
  "Amount":378.66
}
```

La información la pueden tomar del siguiente dataset: 
- [Kaggle](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud/data) - Credit Card Fraud Detection
