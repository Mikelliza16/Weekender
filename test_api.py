import requests

def test_ingest_endpoint():
    url = 'http://localhost:8000/ingest'  
    data = {'data': [[100, 100, 200, 3000]]}
    response = requests.post(url, json=data)
    assert response.status_code == 200
    assert response.json() == {'message': 'Datos ingresados correctamente'}

def test_predict_endpoint():
    url = 'http://localhost:8000/predict'  
    # Enviamos datos compatibles con el modelo dummy (array de arrays)
    data = {'data': [[100], [200]]} 
    response = requests.get(url, json=data)
    assert response.status_code == 200
    # Verificamos que devuelve una lista
    json_data = response.json()
    assert 'prediction' in json_data
    print(f"Predicción recibida: {json_data['prediction']}")

def test_retrain_endpoint():
    url = 'http://localhost:8000/retrain'  
    response = requests.post(url)
    assert response.status_code == 200
    assert response.json() == {'message': 'Modelo reentrenado correctamente.'}

if __name__ == "__main__":
    try:
        print("⏳ Ejecutando tests...")
        test_ingest_endpoint()
        test_predict_endpoint()
        test_retrain_endpoint()
        print("✅ TODOS LOS TESTS HAN PASADO CORRECTAMENTE")
    except Exception as e:
        print(f"❌ ERROR: {e}")