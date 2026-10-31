import os
import joblib
from flask import Flask, request, render_template
import pymongo
# MONGODB_URI="mongodb+srv://nzapadiya288_db_user:P9nIF1PZnWJe9x8u@my-cluster.ynapcpn.mongodb.net"

mongo_client = pymongo.MongoClient("mongodb+srv://nzapadiya288_db_user:P9nIF1PZnWJe9x8u@my-cluster.ynapcpn.mongodb.net")

db = mongo_client["farm_yield_db"]
collection = db["farm_yield_collection"]


app = Flask(__name__)

# Resolve absolute path to the model relative to this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "nandanamodel.joblib")

# Load model into memory
model = joblib.load(MODEL_PATH)


@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        name = request.form.get("fullname")
        mob = request.form.get("mob")
        state_code = request.form.get("state_code")
        agro_climatic_zone_code = request.form.get("agro_climatic_zone_code")
        season_code = request.form.get("season_code")
        crop_code = request.form.get("crop_code")
        soil_type_code = request.form.get("soil_type_code")
        irrigation_type_code = request.form.get("irrigation_type_code")
        seed_type_code = request.form.get("seed_type_code")
        mechanization_code = request.form.get("mechanization_code")
        farm_size_ha = request.form.get("farm_size_ha")
        soil_ph = request.form.get("soil_ph")
        organic_carbon_pct = request.form.get("organic_carbon_pct")
        nitrogen_kg_ha = request.form.get("nitrogen_kg_ha")
        phosphorus_kg_ha = request.form.get("phosphorus_kg_ha")
        potassium_kg_ha = request.form.get("potassium_kg_ha")
        soil_moisture_pct = request.form.get("soil_moisture_pct")
        avg_temp_c = request.form.get("avg_temp_c")
        rainfall_mm = request.form.get("rainfall_mm")
        humidity_pct = request.form.get("humidity_pct")
        sunshine_hours = request.form.get("sunshine_hours")
        sowing_month = request.form.get("sowing_month")
        crop_duration_days = request.form.get("crop_duration_days")
        seed_rate_kg_ha = request.form.get("seed_rate_kg_ha")
        fertilizer_kg_ha = request.form.get("fertilizer_kg_ha")
        organic_manure_t_ha = request.form.get("organic_manure_t_ha")
        pesticide_l_ha = request.form.get("pesticide_l_ha")
        num_irrigations = request.form.get("num_irrigations")
        labour_days_ha = request.form.get("labour_days_ha")
        pest_disease_code = request.form.get("pest_disease_code")

        data = [[state_code,agro_climatic_zone_code,season_code,crop_code,soil_type_code,irrigation_type_code,seed_type_code,mechanization_code,farm_size_ha,soil_ph,organic_carbon_pct,nitrogen_kg_ha,phosphorus_kg_ha,potassium_kg_ha,soil_moisture_pct,avg_temp_c,rainfall_mm,humidity_pct,sunshine_hours,sowing_month,crop_duration_days,seed_rate_kg_ha,fertilizer_kg_ha,organic_manure_t_ha,pesticide_l_ha,num_irrigations,labour_days_ha,pest_disease_code]]
        result = model.predict(data)

        submitdata = {
            "name": name,
            "mob": mob,
            "state_code": state_code,
            "agro_climatic_zone_code": agro_climatic_zone_code,
            "season_code": season_code,
            "crop_code": crop_code,
            "soil_type_code": soil_type_code,
            "irrigation_type_code": irrigation_type_code,
            "seed_type_code": seed_type_code,
            "mechanization_code": mechanization_code,
            "farm_size_ha": farm_size_ha,
            "soil_ph": soil_ph,
            "organic_carbon_pct": organic_carbon_pct,
            "nitrogen_kg_ha": nitrogen_kg_ha,
            "phosphorus_kg_ha": phosphorus_kg_ha,
            "potassium_kg_ha": potassium_kg_ha,
            "soil_moisture_pct": soil_moisture_pct,
            "avg_temp_c": avg_temp_c,
            "rainfall_mm": rainfall_mm,
            "humidity_pct": humidity_pct,
            "sunshine_hours": sunshine_hours,
            "sowing_month": sowing_month,
            "crop_duration_days": crop_duration_days,
            "seed_rate_kg_ha": seed_rate_kg_ha,
            "fertilizer_kg_ha": fertilizer_kg_ha,
            "organic_manure_t_ha": organic_manure_t_ha,
            "pesticide_l_ha": pesticide_l_ha,
            "num_irrigations": num_irrigations,
            "labour_days_ha": labour_days_ha,
            "pest_disease_code": pest_disease_code,
            "predicted_yield": float(result[0])}

        collection.insert_one(submitdata)


        print(result)
        return render_template('index.html',result=result)


    else:
        return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)