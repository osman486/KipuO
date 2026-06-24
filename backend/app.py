from flask import Flask, jsonify, request
from flask_cors import CORS
from db import get_connection
import psycopg2

app = Flask(__name__)
CORS(app)

# ==================== ЗАПОВЕДНИКИ ====================

@app.route('/reserves', methods=['GET'])
def get_reserves():
    region = request.args.get('region')
    climate = request.args.get('climate')
    
    conn = get_connection()
    cursor = conn.cursor()
    
    query = 'SELECT * FROM reserves WHERE 1=1'
    params = []
    
    if region:
        query += ' AND region = %s'
        params.append(region)
    if climate:
        query += ' AND climate = %s'
        params.append(climate)
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    reserves = []
    for row in rows:
        reserves.append({
            'id': row[0],
            'name': row[1],
            'region': row[2],
            'climate': row[3],
            'area': row[4],
            'description': row[5],
            'latitude': row[6] if len(row) > 6 else None,
            'longitude': row[7] if len(row) > 7 else None,
            'image_url': row[8] if len(row) > 8 else None,
            'established_date': row[9] if len(row) > 9 else None
        })
    conn.close()
    return jsonify(reserves)

@app.route('/reserves/<int:id>', methods=['GET'])
def get_reserve(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM reserves WHERE id = %s', (id,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return jsonify({'error': 'Заповедник не найден'}), 404
    
    return jsonify({
        'id': row[0],
        'name': row[1],
        'region': row[2],
        'climate': row[3],
        'area': row[4],
        'description': row[5],
        'latitude': row[6] if len(row) > 6 else None,
        'longitude': row[7] if len(row) > 7 else None,
        'image_url': row[8] if len(row) > 8 else None,
        'established_date': row[9] if len(row) > 9 else None
    })

@app.route('/reserves', methods=['POST'])
def add_reserve():
    data = request.json
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO reserves (name, region, climate, area, description, latitude, longitude, image_url, established_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
    ''', (data['name'], data.get('region'), data.get('climate'), data.get('area'),
          data.get('description'), data.get('latitude'), data.get('longitude'),
          data.get('image_url'), data.get('established_date')))
    reserve_id = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return jsonify({'id': reserve_id, 'message': 'Заповедник добавлен'}), 201

@app.route('/reserves/<int:id>', methods=['PUT'])
def update_reserve(id):
    data = request.json
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE reserves 
        SET name=%s, region=%s, climate=%s, area=%s, description=%s, 
            latitude=%s, longitude=%s, image_url=%s, established_date=%s
        WHERE id=%s
    ''', (data['name'], data.get('region'), data.get('climate'), data.get('area'),
          data.get('description'), data.get('latitude'), data.get('longitude'),
          data.get('image_url'), data.get('established_date'), id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Заповедник обновлен'})

@app.route('/reserves/<int:id>', methods=['DELETE'])
def delete_reserve(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM reserves WHERE id = %s', (id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Заповедник удален'})

# ==================== ЖИВОТНЫЕ ====================

@app.route('/animals', methods=['GET'])
def get_animals():
    reserve_id = request.args.get('reserve_id')
    conn = get_connection()
    cursor = conn.cursor()
    
    if reserve_id:
        cursor.execute('SELECT * FROM animals WHERE reserve_id = %s', (reserve_id,))
    else:
        cursor.execute('SELECT * FROM animals')
    
    rows = cursor.fetchall()
    animals = []
    for row in rows:
        animals.append({
            'id': row[0],
            'name': row[1],
            'species': row[2],
            'rarity': row[3],
            'reserve_id': row[4],
            'description': row[5],
            'image_url': row[6] if len(row) > 6 else None
        })
    conn.close()
    return jsonify(animals)

@app.route('/animals', methods=['POST'])
def add_animal():
    data = request.json
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO animals (name, species, rarity, reserve_id, description, image_url)
        VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
    ''', (data['name'], data.get('species'), data.get('rarity'),
          data.get('reserve_id'), data.get('description'), data.get('image_url')))
    animal_id = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return jsonify({'id': animal_id, 'message': 'Животное добавлено'}), 201

@app.route('/animals/<int:id>', methods=['PUT'])
def update_animal(id):
    data = request.json
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE animals 
        SET name=%s, species=%s, rarity=%s, reserve_id=%s, description=%s, image_url=%s
        WHERE id=%s
    ''', (data['name'], data.get('species'), data.get('rarity'),
          data.get('reserve_id'), data.get('description'), data.get('image_url'), id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Животное обновлено'})

@app.route('/animals/<int:id>', methods=['DELETE'])
def delete_animal(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM animals WHERE id = %s', (id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Животное удалено'})

# ==================== ОТЗЫВЫ ====================

@app.route('/reviews', methods=['GET'])
def get_reviews():
    reserve_id = request.args.get('reserve_id')
    conn = get_connection()
    cursor = conn.cursor()
    
    if reserve_id:
        cursor.execute('SELECT * FROM reviews WHERE reserve_id = %s ORDER BY created_at DESC', (reserve_id,))
    else:
        cursor.execute('SELECT * FROM reviews ORDER BY created_at DESC')
    
    rows = cursor.fetchall()
    reviews = []
    for row in rows:
        reviews.append({
            'id': row[0],
            'reserve_id': row[1],
            'author': row[2],
            'rating': row[3],
            'comment': row[4],
            'created_at': row[5].isoformat() if row[5] else None
        })
    conn.close()
    return jsonify(reviews)

@app.route('/reviews', methods=['POST'])
def add_review():
    data = request.json
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO reviews (reserve_id, author, rating, comment)
        VALUES (%s, %s, %s, %s) RETURNING id
    ''', (data['reserve_id'], data.get('author', 'Аноним'), data['rating'], data['comment']))
    review_id = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return jsonify({'id': review_id, 'message': 'Отзыв добавлен'}), 201

@app.route('/stats', methods=['GET'])
def get_stats():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM reserves')
    reserves_count = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM animals')
    animals_count = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM animals WHERE rarity = \'Краснокнижный\'')
    redbook_count = cursor.fetchone()[0]
    
    conn.close()
    
    return jsonify({
        'reserves_count': reserves_count,
        'animals_count': animals_count,
        'redbook_count': redbook_count
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)