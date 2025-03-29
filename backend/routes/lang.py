from backend import app, db
from backend.models import Language, Word, Lesson
from backend.routes import build_error
from flask import jsonify, request
from flask_login import login_required

@app.route('/lang', methods=['GET'])
def list_languages():
    langs = Language.query.all()
    
    return jsonify([{"id": l.id, 'name': l.name} for l in langs])

@app.route('/lang/create', methods=['POST'])
@login_required
def create_language():
    body = request.get_json()
    if body == None:
        return build_error("No JSON body provided", 400)
    if 'name' not in body:
        return build_error("Name of language must be provided", 400)
    
    name = body['name']
    if Language.query.filter_by(name=name).first():
        return build_error("Language with name already exists", 400)
    
    new_language = Language(name=name)
    db.session.add(new_language)
    db.session.commit()
    return jsonify({"id": new_language.id, "name": new_language.name})


@app.route('/lang/<int:lang_id>/import', methods=['POST'])
@login_required
def import_words(lang_id: int):
    body = request.get_json()
    if body == None:
        return build_error("No JSON body provided", 400)
    if 'words' not in body:
        return build_error("words must be provided", 400)
    
    words = body['words']
    
    lang = Language.query.filter_by(id=lang_id).first()
    
    if not lang:
        return build_error(f'Language with id {lang_id} doesn\'t exist', 400)
    
    for word in words:
        if 'english' not in word or 'translation' not in word:
            return build_error('Word missing required attributes', 400)
        
        new_word = Word(lang_id=lang.id, english=word['english'], translation=word['translation'], definition=(word['definition'] if 'definition' in word else None))
        db.session.add(new_word)
    
    # this will only commit the words to DB if all of them were successful
    db.session.commit()
    return '', 201

@app.route('/lang/<int:lang_id>')
def retrieve_lang(lang_id: int):
    lang = Language.query.filter_by(id=lang_id).first()
    
    if not lang:
        return build_error(f'Language with id {lang_id} doesn\'t exist', 400)
    
    words = [{
        "english": word.english,
        "translation": word.translation,
        "definition": word.definition,
        "id": word.id
    } for word in lang.words]
    
    lessons = [{
        'title': lesson.title,
        'id': lesson.id
    } for lesson in lang.lessons]
    
    response = {
        "language": {
            'id': lang.id,
            'name': lang.name
        },
        'words': words,
        'lessons': lessons
    }
    
    return jsonify(response)

@app.route('/lang/<int:lang_id>/lesson', methods=['POST'])
@login_required
def create_lesson(lang_id: int):
    body = request.get_json()
    if body == None:
        return build_error("No JSON body provided", 400)
    if 'title' not in body or 'text' not in body:
        return build_error("'title' and 'text' must be provided", 400)
    lang = Language.query.filter_by(id=lang_id).first()

    if not lang:
        return build_error(f'Language with id {lang_id} doesn\'t exist', 400)
        
    title = body['title']
    text = body['text']
        
    new_lesson = Lesson(lang_id=lang.id, title=title, text=text)
    db.session.add(new_lesson)
    
    # this will only commit the words to DB if all of them were successful
    db.session.commit()
    return jsonify({
        'id': new_lesson.id
    }), 201

@app.route('/lang/<int:lang_id>/lesson/<int:lesson_id>', methods=['GET'])
def fetch_lesson(lang_id: int, lesson_id: int):
    lesson = Lesson.query.filter_by(id=lesson_id, lang_id=lang_id).first()
    
    if not lesson:
        return build_error(f'Lesson doesn\'t exist', 400)
    
    
    response = {
        'title': lesson.title,
        'text': lesson.text
    }
    
    return jsonify(response)

@app.route('/lang/<int:lang_id>/lesson/<int:lesson_id>', methods=['POST'])
@login_required
def update_lesson(lang_id: int, lesson_id: int):
    body = request.get_json()
    if body == None:
        return build_error("No JSON body provided", 400)
    if 'title' not in body or 'text' not in body:
        return build_error("'title' and 'text' must be provided", 400)

    lesson = Lesson.query.filter_by(id=lesson_id, lang_id=lang_id).first()
    
    if not lesson:
        return build_error(f'Lesson doesn\'t exist', 400)
    
    lesson.text = body['text']
    lesson.title = body['title']
    
    db.session.commit()
    
    return '', 200

@app.route('/lang/<int:lang_id>/word/<int:word_id>', methods=['DELETE'])
@login_required
def delete_word(lang_id: int, word_id: int):
    word = Word.query.filter_by(id=word_id, lang_id=lang_id).first()
    
    if not word:
        return build_error(f'Word can\'t be found', 404)
    
    db.session.delete(word)
    db.session.commit()
    
    return '', 200