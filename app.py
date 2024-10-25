from flask import Flask, render_template, request, jsonify
import logging

app = Flask(__name__)

# Enable logging
logging.basicConfig(level=logging.DEBUG)

# Home route that renders the chatbot page
@app.route('/')
def home():
    app.logger.debug("Loading chatbot frontend.")
    return render_template('index.html')

# Function to simulate a healthcare chatbot response
def chatbot_response(user_message):
    app.logger.debug(f"User message received: {user_message}")
    
    # Convert user message to lowercase for case-insensitive matching
    user_message_lower = user_message.lower().strip()
    
    # Dictionary mapping conditions to responses
    responses = {
        "common cold": "Symptoms: Runny nose, sore throat, cough, congestion; Advice: Rest, fluids, avoid crowds; Medications: Decongestants, Acetaminophen; Home Remedies: Honey, steam inhalation.",
        "covid-19": "Symptoms: Fever, cough, loss of taste/smell, fatigue; Advice: Isolate, get tested, rest; Medications: Antivirals, fever reducers; Home Remedies: Rest, fluids, vitamin C.",
        "strep throat": "Symptoms: Sore throat, swollen glands, fever, headache; Advice: Avoid sharing utensils, rest; Medications: Antibiotics, pain relievers; Home Remedies: Saltwater gargle, warm tea.",
        "pneumonia": "Symptoms: Chest pain, cough, fever, shortness of breath; Advice: Seek medical care, rest; Medications: Antibiotics, antivirals; Home Remedies: Warm fluids, humidifier.",
        "bronchitis": "Symptoms: Persistent cough, mucus, chest discomfort; Advice: Avoid smoking, rest; Medications: Cough suppressants, bronchodilators; Home Remedies: Steam inhalation, honey.",
        "asthma": "Symptoms: Wheezing, shortness of breath, chest tightness; Advice: Avoid triggers, use inhaler; Medications: Inhalers, corticosteroids; Home Remedies: Breathing exercises, avoid allergens.",
        "tuberculosis": "Symptoms: Persistent cough, weight loss, night sweats; Advice: Avoid close contact, follow treatment; Medications: Antibiotics (Rifampicin); Home Remedies: Nutrient-rich diet, fresh air.",
        "allergies": "Symptoms: Sneezing, runny nose, itchy eyes, rash; Advice: Avoid allergens, use antihistamines; Medications: Antihistamines, decongestants; Home Remedies: Saline rinses, avoiding triggers.",
        "sinusitis": "Symptoms: Facial pain, congestion, thick nasal mucus; Advice: Rest, stay hydrated; Medications: Decongestants, nasal sprays; Home Remedies: Steam, warm compress.",
        "flu": "Symptoms: Fever, body aches, fatigue, cough; Advice: Rest, isolate, hydrate; Medications: Oseltamivir, Acetaminophen; Home Remedies: Chicken soup, humidifier.",
        "chickenpox": "Symptoms: Itchy rash, fever, fatigue; Advice: Isolate, avoid scratching; Medications: Antihistamines, Acetaminophen; Home Remedies: Oatmeal baths, calamine lotion.",
        "measles": "Symptoms: Rash, fever, cough, conjunctivitis; Advice: Isolate, rest; Medications: Fever reducers, vitamin A; Home Remedies: Hydration, rest, dark room for eye sensitivity.",
        "endometriosis": "Symptoms: Pelvic pain, heavy periods, infertility; Advice: Follow treatment, manage pain; Medications: Hormonal therapy, NSAIDs; Home Remedies: Heat therapy, dietary changes.",
        "mumps": "Symptoms: Swollen salivary glands, fever, headache; Advice: Isolate, avoid sharing items; Medications: Pain relievers, fever reducers; Home Remedies: Warm compress, rest.",
        "rubella": "Symptoms: Rash, low-grade fever, swollen lymph nodes; Advice: Isolate, avoid pregnant women; Medications: Pain relievers, fever reducers; Home Remedies: Rest, fluids.",
        "hiv": "Symptoms: Fatigue, weight loss, frequent infections; Advice: Follow treatment, avoid unprotected sex; Medications: Antiretrovirals (ARVs); Home Remedies: Healthy diet, exercise.",
        "hepatitis a": "Symptoms: Jaundice, fatigue, abdominal pain, nausea; Advice: Avoid alcohol, rest; Medications: Symptom relief, hydration; Home Remedies: Hydrate, small frequent meals.",
        "hepatitis b": "Symptoms: Jaundice, dark urine, fatigue, abdominal pain; Advice: Avoid alcohol, get vaccinated; Medications: Antivirals, pain relievers; Home Remedies: Rest, low-fat diet.",
        "hepatitis c": "Symptoms: Fatigue, jaundice, dark urine, joint pain; Advice: Avoid alcohol, follow treatment; Medications: Antivirals, interferons; Home Remedies: Hydrate, healthy diet.",
        "dengue": "Symptoms: High fever, rash, joint pain, headache; Advice: Prevent mosquito bites, rest; Medications: Pain relievers (avoid NSAIDs); Home Remedies: Papaya leaf juice, hydration.",
        "malaria": "Symptoms: Fever, chills, sweating, fatigue; Advice: Use mosquito nets, seek treatment; Medications: Antimalarials (Chloroquine); Home Remedies: Hydration, avoid mosquito exposure.",
        "zika": "Symptoms: Mild fever, rash, joint pain, red eyes; Advice: Avoid mosquito bites, rest; Medications: Symptom relief, acetaminophen; Home Remedies: Hydrate, rest.",
        "lyme disease": "Symptoms: Rash, fever, fatigue, joint pain; Advice: Check for ticks, seek treatment early; Medications: Antibiotics (Doxycycline); Home Remedies: Rest, pain relief.",
        "chikungunya": "Symptoms: Fever, joint pain, rash, muscle pain; Advice: Prevent mosquito bites, rest; Medications: Pain relievers (Acetaminophen); Home Remedies: Hydration, rest.",
        "typhoid": "Symptoms: High fever, abdominal pain, diarrhea; Advice: Stay hydrated, seek treatment; Medications: Antibiotics, hydration therapy; Home Remedies: Oral rehydration, small meals.",
        "tetanus": "Symptoms: Muscle stiffness, jaw lock, spasms; Advice: Seek urgent medical care, vaccination; Medications: Tetanus immunoglobulin, antibiotics; Home Remedies: None, seek medical help.",
        "cholera": "Symptoms: Severe diarrhea, dehydration, vomiting; Advice: Hydrate, seek treatment; Medications: Oral rehydration salts (ORS), antibiotics; Home Remedies: Coconut water, rehydration.",
        "ebola": "Symptoms: Fever, bleeding, vomiting, diarrhea; Advice: Isolate, seek immediate care; Medications: Antivirals, supportive care; Home Remedies: None, immediate medical attention.",
        "yellow fever": "Symptoms: Fever, chills, jaundice, muscle pain; Advice: Vaccinate, prevent mosquito bites; Medications: Supportive care; Home Remedies: Hydrate, rest.",
        "polio": "Symptoms: Paralysis, fever, muscle weakness; Advice: Vaccinate, seek rehab; Medications: Pain relievers, physiotherapy; Home Remedies: Physical therapy, supportive care.",
        "rabies": "Symptoms: Fever, headache, confusion, paralysis; Advice: Get vaccinated, seek urgent care; Medications: Rabies vaccine, immunoglobulin; Home Remedies: None, immediate medical care.",
        "plague": "Symptoms: Swollen lymph nodes, fever, chills; Advice: Avoid contact with rodents, seek care; Medications: Antibiotics (Streptomycin); Home Remedies: None, medical treatment required.",
        "leprosy": "Symptoms: Skin lesions, numbness, muscle weakness; Advice: Early treatment, avoid close contact; Medications: Antibiotics (Dapsone); Home Remedies: Nutrient-rich diet, avoid exposure.",
        "anthrax": "Symptoms: Skin sores, fever, chest pain (inhalation); Advice: Avoid contact with infected animals, seek care; Medications: Antibiotics (Ciprofloxacin); Home Remedies: None, seek medical help.",
        "e coli": "Symptoms: Severe diarrhea, abdominal cramps, nausea; Advice: Stay hydrated, avoid contaminated food; Medications: Rehydration, antibiotics in severe cases; Home Remedies: Hydration, probiotics.",
        "salmonella": "Symptoms: Diarrhea, fever, abdominal pain; Advice: Avoid raw/contaminated food, hydrate; Medications: Rehydration therapy, antibiotics if needed; Home Remedies: Hydrate, bland diet.",
        "norovirus": "Symptoms: Vomiting, diarrhea, stomach cramps; Advice: Isolate, hydrate, rest; Medications: Rehydration therapy; Home Remedies: Oral rehydration salts, hydration.",
        "shingles": "Symptoms: Painful rash, itching, fever; Advice: Avoid contact with vulnerable people; Medications: Antivirals (Acyclovir); Home Remedies: Cool baths, calamine lotion.",
        "psoriasis": "Symptoms: Red, scaly skin patches, itching; Advice: Avoid triggers, moisturize; Medications: Corticosteroids, immunosuppressants; Home Remedies: Moisturizers, oatmeal baths.",
        "eczema": "Symptoms: Itchy, inflamed skin, redness; Advice: Avoid triggers, moisturize; Medications: Corticosteroids, antihistamines; Home Remedies: Coconut oil, oatmeal baths.",
        "gout": "Symptoms: Joint pain, swelling, redness; Advice: Avoid purine-rich foods, stay hydrated; Medications: NSAIDs, corticosteroids; Home Remedies: Cherry juice, hydration.",
        "osteoarthritis": "Symptoms: Joint pain, stiffness, swelling; Advice: Stay active, manage weight; Medications: NSAIDs, pain relievers; Home Remedies: Warm baths, physical therapy.",
        "rheumatoid arthritis": "Symptoms: Joint pain, swelling, fatigue; Advice: Follow treatment, stay active; Medications: DMARDs, corticosteroids; Home Remedies: Fish oil, warm compress.",
        "lupus": "Symptoms: Fatigue, joint pain, rash, fever; Advice: Avoid sun, follow treatment; Medications: Immunosuppressants, NSAIDs; Home Remedies: Aloe vera, turmeric.",
        "celiac": "Symptoms: Diarrhea, weight loss, bloating; Advice: Follow gluten-free diet, avoid triggers; Medications: Symptom relief; Home Remedies: Gluten-free diet, probiotics.",
        "crohn": "Symptoms: Abdominal pain, diarrhea, weight loss; Advice: Follow treatment, avoid trigger foods; Medications: Immunosuppressants, corticosteroids; Home Remedies: Low-fiber diet, probiotics.",
        "ibs": "Symptoms: Abdominal pain, bloating, diarrhea/constipation; Advice: Manage stress, follow diet plan; Medications: Antispasmodics, fiber supplements; Home Remedies: Peppermint oil, probiotics.",
        "gallstones": "Symptoms: Abdominal pain, nausea, vomiting; Advice: Avoid fatty foods, stay active; Medications: Pain relievers, bile acids; Home Remedies: Apple cider vinegar, lemon juice.",
        "kidney stones": "Symptoms: Severe back pain, nausea, blood in urine; Advice: Hydrate, avoid salty foods; Medications: Pain relievers, alpha-blockers; Home Remedies: Lemon juice, plenty of water.",
        "uti": "Symptoms: Painful urination, frequent urge, cloudy urine; Advice: Hydrate, practice good hygiene; Medications: Antibiotics; Home Remedies: Cranberry juice, hydration.",
        "hypertension": "Symptoms: Often none, headache, dizziness; Advice: Reduce salt, exercise; Medications: ACE inhibitors, beta-blockers; Home Remedies: Garlic, exercise.",
        "diabetes": "Symptoms: Frequent urination, fatigue, thirst; Advice: Follow diet, exercise; Medications: Metformin, insulin; Home Remedies: Cinnamon, low-carb diet.",
        "hypothyroidism": "Symptoms: Fatigue, weight gain, cold intolerance; Advice: Regular testing, take meds; Medications: Levothyroxine; Home Remedies: Iodine-rich foods, avoid goitrogens.",
        "hyperthyroidism": "Symptoms: Weight loss, anxiety, sweating; Advice: Follow treatment, avoid triggers; Medications: Antithyroid drugs, beta-blockers; Home Remedies: Stress management, low-iodine diet.",
        "anemia": "Symptoms: Fatigue, pale skin, shortness of breath; Advice: Eat iron-rich foods, rest; Medications: Iron supplements; Home Remedies: Spinach, beetroot juice.",
        "migraine": "Symptoms: Severe headache, nausea, light sensitivity; Advice: Avoid triggers, rest; Medications: Triptans, pain relievers; Home Remedies: Caffeine, cold compress.",
        "glaucoma": "Symptoms: Blurred vision, eye pain, halos around lights; Advice: Regular eye exams, follow treatment; Medications: Eye drops, beta-blockers; Home Remedies: Omega-3 rich foods, hydration.",
        "cataracts": "Symptoms: Blurry vision, glare, faded colors; Advice: Wear sunglasses, follow treatment; Medications: Surgery for severe cases; Home Remedies: Leafy greens, vitamin C.",
        "tinnitus": "Symptoms: Ringing in the ears, hearing loss; Advice: Avoid loud noises, manage stress; Medications: Antidepressants (for severe cases); Home Remedies: Ginkgo biloba, white noise.",
        "herniated disc": "Symptoms: Back pain, leg numbness, weakness; Advice: Avoid heavy lifting, follow therapy; Medications: NSAIDs, muscle relaxants; Home Remedies: Ice packs, stretching exercises.",
        "sciatica": "Symptoms: Leg pain, lower back pain, tingling; Advice: Avoid prolonged sitting, stretch; Medications: Pain relievers, physical therapy; Home Remedies: Hot/cold packs, yoga.",
        "fibromyalgia": "Symptoms: Widespread pain, fatigue, sleep problems; Advice: Manage stress, regular exercise; Medications: Pain relievers, antidepressants; Home Remedies: Yoga, warm baths.",
        "osteoporosis": "Symptoms: Bone fractures, back pain, stooped posture; Advice: Weight-bearing exercise, calcium intake; Medications: Bisphosphonates, calcium supplements; Home Remedies: Dairy, vitamin D.",
        "Scoliosis":" Symptoms: Curved spine, uneven shoulders, back pain; Advice: Wear brace, follow treatment; Medications: Pain relievers, physical therapy; Home Remedies: Yoga, stretching exercises.",
        "Varicose Veins":" Symptoms: Swollen, twisted veins, leg pain; Advice: Avoid standing long, elevate legs; Medications: Compression stockings, sclerotherapy; Home Remedies: Exercise, leg elevation."
       }
    
    # First try exact matches
    for condition, response in responses.items():
        if condition in user_message_lower:
            app.logger.debug(f"Exact match found for condition: {condition}")
            return response
            
    # If no exact match, try partial matches
    for condition, response in responses.items():
        if any(word in user_message_lower for word in condition.split()):
            app.logger.debug(f"Partial match found for condition: {condition}")
            return response
    
    # Default response if no match is found
    return "I understand you have a health-related query. Could you please be more specific about your symptoms or the condition you'd like to know about?"

# Backend route to handle user input and return bot response
@app.route('/get_response', methods=['POST'])
def get_bot_response():
    user_message = request.form.get('message')
    app.logger.debug(f"Message received: {user_message}")
    
    if user_message:
        response = chatbot_response(user_message)
        app.logger.debug(f"Response sent: {response}")
        return jsonify({"response": response})
    else:
        return jsonify({"response": "No message received"}), 400

if __name__ == "__main__":
    app.run(debug=True, port=5001)