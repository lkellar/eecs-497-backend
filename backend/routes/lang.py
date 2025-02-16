from backend import app, db
from backend.models import Language, Word
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

@app.route('/lang/import', methods=['POST'])
@login_required
def import_words():
    body = request.get_json()
    if body == None:
        return build_error("No JSON body provided", 400)
    if 'lang_id' not in body or 'words' not in body:
        return build_error("lang_id and words must be provided", 400)
    
    words = body['words']
    lang_id = body['lang_id']
    
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

@app.route('/lang/words/<int:lang_id>')
def retrieve_words(lang_id: int):
    words = Word.query.filter_by(lang_id=lang_id).all()
    
    words = [{
        "english": word.english,
        "translation": word.translation,
        "definition": word.definition
    } for word in words]
    
    return words