from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost:3306/pokedex_andrei'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)

class Pokemon(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    nombre=db.Column(db.String(30), nullable=False)
    tipo=db.Column(db.String(15), nullable=True)
    edad=db.Column(db.Integer, nullable=False)
    fecha_nacimiento=db.Column(db.String(10), nullable=False)
    ataque_principal=db.Column(db.String(100), nullable=False)
    foto=db.Column(db.String(255), nullable=True)
    
    def __repr__(self) :
        return "[Pokemon %s]" % str(self.id)
db.create_all()

class IndexRoute(Resource):
    def get(self):
        return {'response': 'Pokedeeeeeeeeeeeeeeeeeeeex'},200

class IndexRoutePokemon(Resource):
    def get(self):
        pokemones= Pokemon.query.all()
        response=[]
        if pokemones:
            for pokemon in pokemones:
                response.append({
                    "Id":pokemon.id,
                    "Nombre":pokemon.nombre,
                    "Tipo":pokemon.tipo,
                    "Edad":pokemon.edad,
                    "Fecha de Nacimiento":pokemon.fecha_nacimiento,
                    "Ataque Principal":pokemon.ataque_principal,
                    "Foto":pokemon.foto
                })
        return {'response':response},200

    def post(self):
        pokemon_crear=request.get_json()
        if pokemon_crear is None:
            return "Los campos no estan completos", 404
        if 'Nombre' not in pokemon_crear:
            return 'Nombre no registrado',404
        if 'Edad' not in pokemon_crear:
            return 'Edad no registrada', 404 
        if 'FechadeNacimiento' not in pokemon_crear:
            return "Fecha de nacimiento no registrada",404
        if "AtaquePrincipal" not in pokemon_crear:
            return "Ataque no registrado",404
        else:
            pokemon = Pokemon(nombre=pokemon_crear['Nombre'], tipo=pokemon_crear['Tipo'], edad=pokemon_crear['Edad'], fecha_nacimiento=pokemon_crear['FechadeNacimiento'],ataque_principal=pokemon_crear['AtaquePrincipal'],foto=pokemon_crear['Foto'] )
            db.session.add(pokemon)
            db.session.commit()
        return {"response":"¡Pokemon registrado exitosamente!"}, 200

class PokemonbyID(Resource):
    def get(self,id):
        pokemon=Pokemon.query.filter_by(id=id).first()
        if pokemon:
            return{'response':{
                "Id":pokemon.id,
                "Nombre":pokemon.nombre,
                "Tipo":pokemon.tipo,
                "Edad":pokemon.edad,
                "Fecha de Nacimiento":pokemon.fecha_nacimiento,
                "Ataque Principal":pokemon.ataque_principal,
                "Foto":pokemon.foto
            }},200
        else:
            return{"response":"Id de Pokemon no registrada"},404
    
    def put(self,id):
        pokemon=Pokemon.query.filter_by(id=id).first()
        if pokemon:
            datos = request.get_json()
            pokemon.nombre = datos['Nombre']
            pokemon.tipo = datos['Tipo']
            pokemon.edad = datos['Edad']
            pokemon.fechadenacimiento = datos['FechadeNacimiento']
            pokemon.ataque =  datos['AtaquePrincipal']
            pokemon.foto = datos['Foto']
            db.session.commit()
            return {"response": "¡Pokemon actualizado con exito!"}
        else:
            return{"response":"Datos no validos"},404


    def delete(self,id):
        pokemon=Pokemon.query.filter_by(id=id).first()
        db.session.delete(pokemon)
        db.session.commit()
        if pokemon:
            return { "response": "Pokemon con Id: {pokemon}. Borrado exitosamente.".format(pokemon=id)}, 200
        else:
            return{"response":"Id de Pokemon no registrada, no se puede borrar"},

api.add_resource(IndexRoute,'/')
api.add_resource(IndexRoutePokemon,'/pokemon')
api.add_resource(PokemonbyID,'/pokemon/<int:id>')