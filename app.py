from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

app = Flask(__name__)
CORS(app)  # Kích hoạt CORS

# Tải và chuẩn bị dữ liệu
movies_df = pd.read_csv('movies.csv')
ratings_df = pd.read_csv('ratings.csv')
tags_df = pd.read_csv('tags.csv')

# Kết hợp các thẻ và thể loại
tags_combined = tags_df.groupby('movieId')['tag'].apply(lambda x: ' '.join(x)).reset_index()
movies_with_tags = pd.merge(movies_df, tags_combined, on='movieId', how='left')
movies_with_tags['tag'] = movies_with_tags['tag'].fillna('')
movies_with_tags['metadata'] = movies_with_tags['genres'].apply(lambda x: x.replace('|', ' ')) + ' ' + movies_with_tags['tag']

# Vector hóa TF-IDF
tfidf_vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf_vectorizer.fit_transform(movies_with_tags['metadata'])

# Tính độ tương tự cosine
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

# Hàm trợ giúp để lấy đề xuất theo tên film
def get_recommendations(title):
    try:
        idx = movies_with_tags.loc[movies_with_tags['title'].str.lower() == title.lower()].index[0]
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:11]  # Lấy top 10
        movie_indices = [i[0] for i in sim_scores]
        recommended_movies = movies_with_tags['title'].iloc[movie_indices].tolist()
        reasons = [f"Có thể loại và thẻ tương tự với {title}" for _ in movie_indices]
        return {'movies': recommended_movies, 'reasons': reasons}
    except IndexError:
        return {'movies': [], 'reasons': ['Không tìm thấy tiêu đề phim.']}

@app.route('/movies', methods=['GET'])
def movies():
    danh_sach_phim = movies_df['title'].tolist()
    return jsonify(danh_sach_phim)

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json
    ten_phim = data['title']
    recommendations = get_recommendations(ten_phim)
    return jsonify(recommendations)

@app.route('/feedback', methods=['POST'])
def feedback():
    data = request.json
    liked_movies = data['liked_movies']
    # Xử lý và lưu trữ phản hồi
    print("Phản hồi đã nhận:", liked_movies)
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)
