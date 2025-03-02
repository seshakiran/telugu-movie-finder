from flask import Flask, request, jsonify
import sys
import os
import datetime
from dotenv import load_dotenv

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the function from surabhi.py
from surabhi import get_movies_for_date_or_month

# Load environment variables
load_dotenv()

app = Flask(__name__)

@app.route('/api/movies', methods=['GET'])
def get_movies():
    date_str = request.args.get('date')
    
    if not date_str:
        return jsonify({"error": "Date parameter is required"}), 400
    
    try:
        target_date = datetime.datetime.strptime(date_str, "%m/%d/%Y").date()
    except ValueError:
        return jsonify({"error": "Invalid date format. Please use mm/dd/yyyy."}), 400
    
    try:
        movies = get_movies_for_date_or_month(target_date)
        
        # Format the response
        response = {
            "date": date_str,
            "formatted_date": target_date.strftime("%B %d, %Y"),
            "movies": [],
            "found_exact_date": False
        }
        
        if movies:
            # Check if any movies were found on the exact date
            response["found_exact_date"] = any(
                movie["release_date"].day == target_date.day and 
                movie["release_date"].month == target_date.month 
                for movie in movies
            )
            
            # Format movie data for JSON response
            for movie in movies:
                response["movies"].append({
                    "title": movie["title"],
                    "release_date": movie["release_date"].strftime("%B %d, %Y"),
                    "url": movie["url"],
                    "summary": movie.get("Summary", "Not available")
                })
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# This is used when running the Flask app directly
if __name__ == '__main__':
    app.run(debug=True, port=5003)
