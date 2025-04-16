from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'a'  # Change this to a random secret key

# Configure MySQL connection
db_config = {
    'host': 'localhost',
    'user': 'root',  # Replace with your MySQL username
    'password': 'aditi',  # Replace with your MySQL password
    'database': 'recipe'  # Replace with your MySQL database name
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recipes')
def recipes():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        
        # Fetch the id along with other fields
        cursor.execute('SELECT id, DishName, Spice, DietaryInfo FROM recipes')
        results = cursor.fetchall()
        
        return render_template('recipes.html', recipes=results)
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)})
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        dish_name = request.form['DishName']
        description = request.form['Description']
        spice = request.form['Spice']
        prep_time = request.form['PrepTime']
        cook_time = request.form['CookTime']
        serves = request.form['Serves']
        dietary_info = request.form['DietaryInfo']
        ingredients = request.form['Ingredients']
        instructions = request.form['Instructions']

        try:
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()
            cursor.execute('INSERT INTO recipes (DishName, Description, Spice, PrepTime, CookTime, Serves, DietaryInfo, Ingredients, Instructions) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                           (dish_name, description, spice, prep_time, cook_time, serves, dietary_info, ingredients, instructions))
            connection.commit()
            return redirect(url_for('recipes'))
        except mysql.connector.Error as err:
            return jsonify({'error': str(err)})
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    else:
        return render_template('submit.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        
        # Ensure the id field is included in the SELECT statement
        cursor.execute('SELECT id, DishName, Spice, DietaryInfo FROM recipes WHERE DishName LIKE %s OR Ingredients LIKE %s', 
                       ('%' + query + '%', '%' + query + '%'))
        results = cursor.fetchall()
        
        return render_template('recipes.html', recipes=results)
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)})
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

            
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        try:
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()
            cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, hashed_password))
            connection.commit()
            return redirect(url_for('login'))
        except mysql.connector.Error as err:
            return jsonify({'error': str(err)})
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor(dictionary=True)
            cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
            user = cursor.fetchone()

            if user and check_password_hash(user['password'], password):
                session['user_id'] = user['id']
                return redirect(url_for('recipes'))
            else:
                return "Invalid username or password"
        except mysql.connector.Error as err:
            return jsonify({'error': str(err)})
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    return render_template('login.html')

@app.route('/recipe/<int:recipe_id>')
def recipe_detail(recipe_id):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute('SELECT * FROM recipes WHERE id = %s', (recipe_id,))
        recipe = cursor.fetchone()
        
        if recipe:
            return render_template('recipe_detail.html', recipe=recipe)
        else:
            return "Recipe not found", 404
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)})
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)