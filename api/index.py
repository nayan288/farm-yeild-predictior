import os
import joblib
import pymongo
from flask import Flask, request, render_template

# MongoDB connection
MONGO_URI = os.getenv("MONGODB_URI", "mongodb+srv://nzapadiya288_db_user:P9nIF1PZnWJe9x8u@my-cluster.ynapcpn.mongodb.net")
mongo_client = pymongo.MongoClient(MONGO_URI)
db = mongo_client["farm_yield_db"]
collection = db["farm_yield_collection"]

app = Flask(__name__)

# Absolute path resolution for model
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "nandanamodel.joblib")

# Load model
model = joblib.load(MODEL_PATH)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get("fullname")
        mob = request.form.get("mob")

        # Convert form string inputs to float for model prediction
        fields = [
            "state_code", "agro_climatic_zone_code", "season_code", "crop_code",
            "soil_type_code", "irrigation_type_code", "seed_type_code", "mechanization_code",
            "farm_size_ha", "soil_ph", "organic_carbon_pct", "nitrogen_kg_ha",
            "phosphorus_kg_ha", "potassium_kg_ha", "soil_moisture_pct", "avg_temp_c",
            "rainfall_mm", "humidity_pct", "sunshine_hours", "sowing_month",
            "crop_duration_days", "seed_rate_kg_ha", "fertilizer_kg_ha",
            "organic_manure_t_ha", "pesticide_l_ha", "num_irrigations",
            "labour_days_ha", "pest_disease_code"
        ]

        # Convert values to floats
        data_dict = {field: float(request.form.get(field, 0)) for field in fields}
        input_features = [[data_dict[field] for field in fields]]

        # Run prediction
        result = model.predict(input_features)
        predicted_yield = float(result[0])

        # Prepare payload for MongoDB
        submitdata = {
            "name": name,
            "mob": mob,
            **data_dict,
            "predicted_yield": predicted_yield
        }
        
        try:
            collection.insert_one(submitdata)
        except Exception as e:
            print("Database Error:", e)

        return render_template('index.html', result=round(predicted_yield, 2))

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)