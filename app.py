import json
import jwt
from datetime import datetime, timedelta, timezone
from flask import Flask, request, Response
from sqlalchemy import select
from werkzeug.security import check_password_hash
from flask_cors import CORS
from model import *

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "https://localhost:5173/", "methods": ["GET", "POST", "PUT", "DELETE"], "allow_headers": ["Content-Type"], "supports_credentials": True}})


SECRET_KEY = 'your_secret_key'

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/admins', methods=['GET'])
def ListAllAdmins():
    try:
        admin_query = select(Admin).select_from(Admin)
        admins = db_session.execute(admin_query).scalars()
        result = [admin.serialize() for admin in admins]
        return Response(
            json.dumps(result),
            status=200,
            mimetype='application/json'
        )
    except Exception as e:
        return Response(
            response=json.dumps({'status': 'error', 'message': str(e)}),
            status=500,
            mimetype='application/json'
        )


@app.route('/admin/<int:id>', methods=['GET'])
def listAdminById(id):
    try:
        admin_query = select(Admin).where(Admin.id == id)
        admin_result = db_session.execute(admin_query).fetchone()

        # Verifica se o resultado está vazio
        if not admin_result:
            return Response(
                response=json.dumps({'status': 'error', 'message': 'Admin not found'}),
                status=404,
                mimetype='application/json'
            )

        # Extrai a instância do admin do resultado
        admin = admin_result[0]

        return Response(
            response=json.dumps({
                'status': 'success',
                'message': 'Admin encontrado',
                'id': admin.id,
                'nome': admin.nome,
                'email': admin.email,
                'senha': admin.senha,
                'cpf': admin.cpf,
            }),
            status=200,
            mimetype='application/json'
        )
    except Exception as e:
        return Response(
            response=json.dumps({'status': 'error', 'message': str(e)}),
            status=500,
            mimetype='application/json'
        )


@app.route('/admin', methods=['POST'])
def createAdmin():
    try:
        admin_data = request.form
        admin = Admin(
            nome=admin_data['nome'],
            email=admin_data['email'],
            senha=admin_data['senha'],
            cpf=admin_data['cpf']
        )
        admin.save()
        return Response(
            response=json.dumps({
                'status': 'success',
                'message': 'Admin registrado com sucesso!',
                'nome': admin.nome,
                'email': admin.email,
                'cpf': admin.cpf
            }),
            status=201,
            mimetype='application/json'
        )
    except Exception as e:
        return Response(
            response=json.dumps({'status': 'error', 'message': str(e)}),
            status=500,
            mimetype='application/json'
        )


@app.route('/admin/<int:id>', methods=['PUT'])
def updateAdmin(id):
    try:
        admin_query = select(Admin).where(Admin.id == id)
        admin = db_session.execute(admin_query).scalar()
        if not admin:
            return Response(
                response=json.dumps({'status': 'error', 'message': 'Admin not found'}),
                status=404,
                mimetype='application/json'
            )

        admin_data = request.form
        if admin_data.get('nome'):
            admin.nome = admin_data['nome']
        if admin_data.get('email'):
            admin.email = admin_data['email']
        if admin_data.get('senha'):
            admin.senha = admin_data['senha']
        if admin_data.get('cpf'):
            admin.cpf = admin_data['cpf']
        admin.save()

        return Response(
            response=json.dumps({
                'status': 'success',
                'message': 'Admin atualizado com sucesso!',
                'nome': admin.nome,
                'email': admin.email,
                'cpf': admin.cpf
            }),
            status=200,
            mimetype='application/json'
        )
    except Exception as e:
        return Response(
            response=json.dumps({'status': 'error', 'message': str(e)}),
            status=500,
            mimetype='application/json'
        )


@app.route('/admin/login', methods=['POST'])
def loginAdmin():
    try:
        # Captura o e-mail e senha enviados pelo front-end
        login_data = request.json
        email = login_data['email']
        senha = login_data['senha']

        # Verificar se o admin existe
        admin = db_session.execute(select(Admin).where(Admin.email == email)).scalar()
        if not admin:
            return Response(
                response=json.dumps({'status': 'error', 'message': 'Admin not found'}),
                status=404,
                mimetype='application/json'
            )

        # Verificar a senha
        if admin.senha != senha:
            return Response(
                response=json.dumps({'status': 'error', 'message': 'Invalid credentials'}),
                status=401,
                mimetype='application/json'
            )

        # Gerar o token JWT
        payload = {
            'admin_id': admin.id,
            'exp': datetime.now(timezone.utc) + timedelta(days=1)  # Agora usando datetime correto
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return Response(
            response=json.dumps({'status': 'success', 'token': token}),
            status=200,
            mimetype='application/json'
        )

    except Exception as e:
        return Response(
            response=json.dumps({'status': 'error', 'message': str(e)}),
            status=500,
            mimetype='application/json'
        )


@app.route('/categorias/<int:id>', methods=['GET'])
def ListAllCategoriaByAdmin(id):
    try:
        # Consulta para buscar as categorias associadas ao admin pelo 'id'
        categorias_query = select(Categoria).where(Categoria.admin_id == id)
        categorias = db_session.execute(categorias_query).scalars().all()

        # Se não encontrar nenhuma categoria
        if not categorias:
            return Response(
                response=json.dumps({'status': 'error', 'message': 'Não tem categorias nesse admin'}),
                status=404,
                mimetype='application/json'
            )

        # Serializando as categorias para retornar como JSON
        result = [categoria.serialize() for categoria in categorias]

        return Response(
            json.dumps(result),
            status=200,
            mimetype='application/json'
        )
    except Exception as e:
        return Response(
            json.dumps({'status': 'error', 'message': str(e)}),
            status=500,
            mimetype='application/json'
        )

@app.route('/categoria/<int:id>', methods=['GET'])
def listCategoriaById(id):
    try:
        categoria_sql = select(Categoria).where(Categoria.id == id)
        categoria = db_session.execute(categoria_sql).scalar()
        if categoria:
            return Response(
                json.dumps(categoria.serialize()),
                status=200,
                mimetype='application/json'
            )
        else:
            return Response(
                json.dumps({'status': 'error', 'message': 'Categoria não encontrada'}),
                status=404,
                mimetype='application/json'
            )
    except Exception as e:
        return Response(
            json.dumps({'status': 'error', 'message': str(e)}),
            status=500,
            mimetype='application/json'
        )
@app.route('/categoria', methods=['POST'])
def createCategoria():
    try:
        nome = request.form['nome']
        icone = request.form['icone']
        admin_id = request.form['admin_id']

        # Verificar se o admin_id existe
        admin = db_session.query(Admin).filter_by(id=admin_id).first()
        if not admin:
            return Response(
                json.dumps({'status': 'error', 'message': 'admin_id não encontrado'}),
                status=404,
                mimetype='application/json'
            )

        categoria = Categoria(nome=nome, icone=icone, admin_id=int(admin_id))
        categoria.save()

        return Response(
            json.dumps({
                'status': 'success',
                'message': 'Categoria registrada com sucesso!',
                'categoria': categoria.serialize()
            }),
            status=201,
            mimetype='application/json'
        )
    except KeyError as e:
        return Response(
            json.dumps({'status': 'error', 'message': f"Campo faltando: {str(e)}"}),
            status=400,
            mimetype='application/json'
        )
    except Exception as e:
        return Response(
            json.dumps({'status': 'error', 'message': str(e)}),
            status=500,
            mimetype='application/json'
        )


@app.route('/categoria/<int:id>', methods=['PUT'])
def updateCategoria(id):
    try:
        categoria_sql = select(Categoria).where(Categoria.id == id)
        categoria = db_session.execute(categoria_sql).scalar()
        if not categoria:
            return Response(
                json.dumps({'status': 'error', 'message': 'Categoria não encontrada'}),
                status=404,
                mimetype='application/json'
            )

        if 'nome' in request.form:
            categoria.nome = request.form['nome']
        if 'icone' in request.form:
            categoria.icone = request.form['icone']

        categoria.save()

        return Response(
            json.dumps({
                'status': 'success',
                'message': 'Categoria atualizada com sucesso!',
                'categoria': categoria.serialize()
            }),
            status=200,
            mimetype='application/json'
        )
    except Exception as e:
        return Response(
            json.dumps({'status': 'error', 'message': str(e)}),
            status=500,
            mimetype='application/json'
        )


@app.route('/categoria/delete/<int:id>', methods=['POST'])
def deleteCategoria(id):
    try:
        # Seleciona a categoria com base no ID
        categoria_sql = select(Categoria).where(Categoria.id == id)
        categoria = db_session.execute(categoria_sql).scalar()

        # Verifica se a categoria foi encontrada
        if not categoria:
            return Response(
                json.dumps({'status': 'error', 'message': 'Categoria não encontrada'}),
                status=404,
                mimetype='application/json'
            )

        # Exclui a categoria
        categoria.delete()

        # Retorna a resposta de sucesso
        final = {
            'status': 'success',
            'message': f'{categoria.nome} foi excluída com sucesso!'
        }
        return Response(
            response=json.dumps(final),
            status=200,
            mimetype='application/json'
        )

    except Exception as e:
        # Caso ocorra um erro, retorna uma resposta com o erro
        final = {
            'status': 'error',
            'message': str(e)
        }
        return Response(
            response=json.dumps(final),
            status=500,
            mimetype='application/json'
        )

@app.route('/funcionarios/<int:id>', methods=['GET'])
def ListAllFuncionarioByAdmin(id):
    try:
        # Consulta para buscar os funcionários associados ao admin pelo 'id'
        funcionario_sql = select(Funcionario).where(Funcionario.admin_id == id)
        funcionarios = db_session.execute(funcionario_sql).scalars().all()

        # Verifica se há funcionários associados ao admin
        if not funcionarios:
            return Response(
                json.dumps({'status': 'error', 'message': 'Não existe funcionarios nesse admin'}),
                status=404,
                mimetype='application/json'
            )

        # Serializa os dados dos funcionários
        result = [funcionario.serialize() for funcionario in funcionarios]

        # Resposta com a lista de funcionários
        final = json.dumps(result)
        return Response(
            response=final,
            status=200,
            mimetype='application/json'
        )

    except Exception as e:
        # Trata exceções e retorna erro
        return Response(
            json.dumps({'status': 'error', 'message': str(e)}),
            status=500,
            mimetype='application/json'
        )

@app.route('/funcionario/<int:id>', methods=['GET'])
def listFuncionarioById(id):
    try:
        # Busca o funcionário pelo ID usando SQLAlchemy
        funcionario = db_session.query(Funcionario).filter(Funcionario.id == id).first()

        # Verifica se o funcionário foi encontrado
        if not funcionario:
            return Response(
                json.dumps({'status': 'error', 'message': 'Funcionário não encontrado'}),
                status=404,
                mimetype='application/json'
            )

        # Serializa os dados do funcionário
        final = json.dumps(funcionario.serialize())  # Serialize o objeto diretamente
        return Response(
            response=final,
            status=200,
            mimetype='application/json'
        )

    except Exception as e:
        return Response(
            json.dumps({'status': 'error', 'message': str(e)}),
            status=500,
            mimetype='application/json'
        )

@app.route('/funcionario', methods=['POST'])
def createFuncionario():
    try:
        # Criação do novo funcionário
        funcionario = Funcionario(
            nome=request.form['nome'],
            email=request.form['email'],
            senha=request.form['senha'],
            telefone=request.form['telefone'],
            admin_id=int(request.form['admin_id'])
        )
        funcionario.save()

        # Resposta de sucesso
        final = {
            'status': 'success',
            'message': 'Funcionário registrado com sucesso!',
            'nome': funcionario.nome,
            'email': funcionario.email,
            'telefone': funcionario.telefone,
            'admin_id': funcionario.admin_id
        }

        return Response(
            response=json.dumps(final),
            status=201,
            mimetype='application/json'
        )

    except Exception as e:
        return Response(
            json.dumps({'status': 'error', 'message': str(e)}),
            status=500,
            mimetype='application/json'
        )


@app.route('/funcionario/<int:id>', methods=['PUT'])
def updateFuncionario(id):
    try:
        # Busca o funcionário
        funcionario_sql = select(Funcionario).where(Funcionario.id == id)
        funcionario = db_session.execute(funcionario_sql).scalar()

        # Verifica se o funcionário existe
        if not funcionario:
            return Response(
                json.dumps({'status': 'error', 'message': 'Funcionário não encontrado'}),
                status=404,
                mimetype='application/json'
            )

        # Atualiza os dados do funcionário
        if request.form['nome']:
            funcionario.nome = request.form['nome']
        if request.form['email']:
            funcionario.email = request.form['email']
        if request.form['senha']:
            funcionario.senha = request.form['senha']
        if request.form['telefone']:
            funcionario.telefone = request.form['telefone']

        funcionario.save()

        # Resposta de sucesso
        final = {
            'status': 'success',
            'message': 'Funcionário atualizado com sucesso!',
            'nome': funcionario.nome,
            'email': funcionario.email,
            'telefone': funcionario.telefone
        }

        return Response(
            response=json.dumps(final),
            status=200,
            mimetype='application/json'
        )

    except Exception as e:
        return Response(
            json.dumps({'status': 'error', 'message': str(e)}),
            status=500,
            mimetype='application/json'
        )

@app.route('/funcionario/delete/<int:id>', methods=['POST'])
def deleteFuncionario(id):
    try:
        # Busca o funcionário
        funcionario_sql = select(Funcionario).where(Funcionario.id == id)
        funcionario = db_session.execute(funcionario_sql).scalar()

        # Verifica se o funcionário foi encontrado
        if not funcionario:
            return Response(
                json.dumps({'status': 'error', 'message': 'Funcionário não encontrado'}),
                status=404,
                mimetype='application/json'
            )

        # Exclui o funcionário
        funcionario.delete()

        # Resposta de sucesso
        final = {
            'status': 'success',
            'message': f'{funcionario.nome} foi excluído com sucesso!'
        }

        return Response(
            response=json.dumps(final),
            status=200,
            mimetype='application/json'
        )

    except Exception as e:
        return Response(
            json.dumps({'status': 'error', 'message': str(e)}),
            status=500,
            mimetype='application/json'
        )

@app.route('/funcionario/login', methods=['POST'])
def loginFuncionario():
    try:
        # Recebe os dados enviados na requisição (email e senha)
        email = request.json.get('email')
        senha = request.json.get('senha')

        # Verifica se o email e senha foram informados
        if not email or not senha:
            return Response(
                json.dumps({'status': 'error', 'message': 'Email e senha são obrigatórios'}),
                status=400,
                mimetype='application/json'
            )

        # Consulta o funcionário pelo email
        funcionario_sql = select(Funcionario).where(Funcionario.email == email)
        funcionario = db_session.execute(funcionario_sql).scalar()

        # Verifica se o funcionário existe
        if not funcionario:
            return Response(
                json.dumps({'status': 'error', 'message': 'Funcionário não encontrado'}),
                status=404,
                mimetype='application/json'
            )

            # Verificar a senha
        if funcionario.senha != senha:
            return Response(
                response=json.dumps({'status': 'error', 'message': 'Invalid credentials'}),
                status=401,
                mimetype='application/json'
            )

        # Gerar o token JWT
        payload = {
            'admin_id': funcionario.id,
            'exp': datetime.now(timezone.utc) + timedelta(days=1)  # Agora usando datetime correto
        }

        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        # Se o login for bem-sucedido, retorna os dados do funcionário e o token
        final = {
            'status': 'success',
            'message': 'Login bem-sucedido',
            'funcionario': funcionario.serialize(),
            'token': token  # Inclui o token no retorno
        }

        return Response(
            response=json.dumps(final),
            status=200,
            mimetype='application/json'
        )

    except Exception as e:
        # Se houver qualquer erro, retorna uma resposta com o erro
        return Response(
            json.dumps({'status': 'error', 'message': str(e)}),
            status=500,
            mimetype='application/json'
        )


@app.route('/produtos/<int:id>', methods=['GET'])
def listAllProdutoByAdmin(id):
    try:
        # Consulta todos os produtos do admin, considerando a relação com Categoria
        produto_sql = select(Produto).join(Categoria).where(Categoria.admin_id == id)
        produtos = db_session.execute(produto_sql).scalars().all()

        # Verifica se há produtos
        if not produtos:
            return Response(
                json.dumps({'status': 'error', 'message': 'Nenhum produto encontrado para este admin'}),
                status=404,
                mimetype='application/json'
            )

        # Serializa todos os produtos
        result = [produto.serialize() for produto in produtos]

        # Retorna os produtos
        return Response(
            json.dumps(result),
            status=200,
            mimetype='application/json'
        )
    except Exception as e:
        # Retorna uma resposta de erro genérica
        return Response(
            json.dumps({'status': 'error', 'message': f'Erro ao listar produtos: {str(e)}'}),
            status=500,
            mimetype='application/json'
        )

@app.route('/produto/<int:id>', methods=['GET'])
def listProdutoById(id):
    try:
        # Consulta o produto pelo ID
        produto_sql = select(Produto).where(Produto.id == id)
        produto_result = db_session.execute(produto_sql).fetchone()

        # Verifica se o produto existe
        if not produto_result:
            return Response(
                json.dumps({'status': 'error', 'message': 'Produto não encontrado'}),
                status=404,
                mimetype='application/json'
            )

        produto = produto_result[0]

        # Serializa o produto
        return Response(
            json.dumps({
                'status': 'success',
                'message': 'Produto encontrado',
                'id': produto.id,
                'nome': produto.nome,
                'preco': produto.preco,
                'descricao': produto.descricao,
                'image': produto.imagem,
                'categoria_id': produto.categoria_id
            }),
            status=200,
            mimetype='application/json'
        )
    except Exception as e:
        # Retorna uma resposta de erro genérica
        return Response(
            json.dumps({'status': 'error', 'message': f'Erro ao buscar produto: {str(e)}'}),
            status=500,
            mimetype='application/json'
        )


@app.route('/produto', methods=['POST'])
def createProduto():
    try:
        # Verifica se todos os campos foram passados
        if not request.form.get('nome') or not request.form.get('preco') or not request.form.get(
                'descricao') or not request.form.get('imagem') or not request.form.get('categoria_id'):
            return Response(
                json.dumps({'status': 'error', 'message': 'Todos os campos são obrigatórios'}),
                status=400,
                mimetype='application/json'
            )

        # Cria o novo produto
        produto = Produto(
            nome=request.form['nome'],
            preco=float(request.form['preco']),
            descricao=request.form['descricao'],
            imagem=request.form['imagem'],
            categoria_id=int(request.form['categoria_id'])
        )
        produto.save()  # Salva o produto no banco de dados

        # Retorna sucesso
        return Response(
            json.dumps({
                'status': 'success',
                'message': 'Produto registrado com sucesso!',
                'produto': produto.serialize()
            }),
            status=201,
            mimetype='application/json'
        )
    except Exception as e:
        # Retorna erro genérico
        return Response(
            json.dumps({'status': 'error', 'message': f'Erro ao criar produto: {str(e)}'}),
            status=500,
            mimetype='application/json'
        )


@app.route('/produto/<int:id>', methods=['PUT'])
def updateProduto(id):
    try:
        # Consulta o produto pelo ID
        produto_sql = select(Produto).where(Produto.id == id)
        produto = db_session.execute(produto_sql).scalar()

        # Verifica se o produto existe
        if not produto:
            return Response(
                json.dumps({'status': 'error', 'message': 'Produto não encontrado'}),
                status=404,
                mimetype='application/json'
            )

        # Atualiza os campos, caso sejam informados
        if request.form.get('nome'):
            produto.nome = request.form['nome']
        if request.form.get('preco'):
            produto.preco = float(request.form['preco'])
        if request.form.get('descricao'):
            produto.descricao = request.form['descricao']
        if request.form.get('imagem'):
            produto.imagem = request.form['imagem']
        if request.form.get('categoria_id'):
            produto.categoria_id = request.form['categoria_id']

        # Salva as alterações
        produto.save()

        # Retorna sucesso
        return Response(
            json.dumps({
                'status': 'success',
                'message': 'Produto atualizado com sucesso!',
                'produto': produto.serialize()
            }),
            status=200,
            mimetype='application/json'
        )
    except Exception as e:
        # Retorna erro genérico
        return Response(
            json.dumps({'status': 'error', 'message': f'Erro ao atualizar produto: {str(e)}'}),
            status=500,
            mimetype='application/json'
        )


@app.route('/produto/delete/<int:id>', methods=['POST'])
def deleteProduto(id):
    try:
        # Verifica se o produto existe
        produto_sql = select(Produto).where(Produto.id == id)
        produto = db_session.execute(produto_sql).scalar()

        # Se o produto não for encontrado, retorna um erro
        if not produto:
            return Response(
                response=json.dumps({
                    'status': 'error',
                    'message': f'Produto com ID {id} não encontrado.'
                }),
                status=404,
                mimetype='application/json'
            )

        # Deleta o produto
        produto.delete()

        # Retorna resposta de sucesso após exclusão
        final = {
            'status': 'success',
            'message': f'O produto "{produto.nome}" foi excluído com sucesso.'
        }
        return Response(
            response=json.dumps(final),
            status=200,
            mimetype='application/json'
        )

    except Exception as e:
        # Trata exceções e retorna mensagem de erro
        return Response(
            response=json.dumps({
                'status': 'error',
                'message': f'Erro ao excluir o produto: {str(e)}'
            }),
            status=500,
            mimetype='application/json'
        )


# @app.route('/ingredientes', methods=['GET'])
# def ListAllIngrediente():
#     try:
#         ingredientes_sql = select(Ingrediente).select_from(Ingrediente)
#         ingredientes = db_session.execute(ingredientes_sql).scalars()
#
#         if not ingredientes:
#             return Response(
#                 response=json.dumps({
#                     'status': 'error',
#                     'message': 'Nenhum ingrediente encontrado.'
#                 }),
#                 status=404,
#                 mimetype='application/json'
#             )
#
#         result = [ingrediente.serialize() for ingrediente in ingredientes]
#         return Response(
#             response=json.dumps(result),
#             status=200,
#             mimetype='application/json'
#         )
#     except Exception as e:
#         return Response(
#             response=json.dumps({
#                 'status': 'error',
#                 'message': f'Erro ao listar os ingredientes: {str(e)}'
#             }),
#             status=500,
#             mimetype='application/json'
#         )
#
#
# @app.route('/ingrediente/<int:id>', methods=['GET'])
# def listIngredienteById(id):
#     try:
#         ingrediente_sql = select(Ingrediente).where(Ingrediente.id == id)
#         ingrediente = db_session.execute(ingrediente_sql).fetchone()
#
#         if not ingrediente:
#             return Response(
#                 response=json.dumps({
#                     'status': 'error',
#                     'message': f'Ingrediente com ID {id} não encontrado.'
#                 }),
#                 status=404,
#                 mimetype='application/json'
#             )
#
#         result = [ingrediente.serialize()]
#         return Response(
#             response=json.dumps(result),
#             status=200,
#             mimetype='application/json'
#         )
#     except Exception as e:
#         return Response(
#             response=json.dumps({
#                 'status': 'error',
#                 'message': f'Erro ao buscar ingrediente: {str(e)}'
#             }),
#             status=500,
#             mimetype='application/json'
#         )
#
#
# @app.route('/ingrediente', methods=['POST'])
# def createIngrediente():
#     try:
#         nome = request.form['nome']
#         produto_id = int(request.form['produto_id'])
#
#         ingrediente = Ingrediente(
#             nome=nome,
#             produto_id=produto_id,
#         )
#         ingrediente.save()
#
#         final = {
#             'status': 'success',
#             'message': 'Ingrediente registrado com sucesso!',
#             'nome': ingrediente.nome,
#             'produto_id': ingrediente.produto_id,
#         }
#         return Response(
#             response=json.dumps(final),
#             status=201,
#             mimetype='application/json'
#         )
#     except Exception as e:
#         return Response(
#             response=json.dumps({
#                 'status': 'error',
#                 'message': f'Erro ao criar ingrediente: {str(e)}'
#             }),
#             status=500,
#             mimetype='application/json'
#         )
#
#
# @app.route('/ingrediente/<int:id>', methods=['PUT'])
# def updateIngrediente(id):
#     try:
#         ingrediente_sql = select(Ingrediente).where(Ingrediente.id == id)
#         ingrediente = db_session.execute(ingrediente_sql).scalar()
#
#         if not ingrediente:
#             return Response(
#                 response=json.dumps({
#                     'status': 'error',
#                     'message': f'Ingrediente com ID {id} não encontrado.'
#                 }),
#                 status=404,
#                 mimetype='application/json'
#             )
#
#         if 'nome' in request.form:
#             ingrediente.nome = request.form['nome']
#         if 'produto_id' in request.form:
#             ingrediente.produto_id = int(request.form['produto_id'])
#
#         ingrediente.save()
#
#         final = {
#             'status': 'success',
#             'message': 'Ingrediente atualizado com sucesso!',
#             'nome': ingrediente.nome,
#             'produto_id': ingrediente.produto_id,
#         }
#         return Response(
#             response=json.dumps(final),
#             status=200,
#             mimetype='application/json'
#         )
#     except Exception as e:
#         return Response(
#             response=json.dumps({
#                 'status': 'error',
#                 'message': f'Erro ao atualizar ingrediente: {str(e)}'
#             }),
#             status=500,
#             mimetype='application/json'
#         )
#
#
# @app.route('/ingrediente/<int:id>', methods=['POST'])
# def deleteIngrediente(id):
#     try:
#         ingrediente_sql = select(Ingrediente).where(Ingrediente.id == id)
#         ingrediente = db_session.execute(ingrediente_sql).scalar()
#
#         if not ingrediente:
#             return Response(
#                 response=json.dumps({
#                     'status': 'error',
#                     'message': f'Ingrediente com ID {id} não encontrado.'
#                 }),
#                 status=404,
#                 mimetype='application/json'
#             )
#
#         ingrediente.delete()
#         final = {
#             'status': 'success',
#             'message': f'O ingrediente "{ingrediente.nome}" foi excluído com sucesso.'
#         }
#         return Response(
#             response=json.dumps(final),
#             status=200,
#             mimetype='application/json'
#         )
#     except Exception as e:
#         return Response(
#             response=json.dumps({
#                 'status': 'error',
#                 'message': f'Erro ao excluir ingrediente: {str(e)}'
#             }),
#             status=500,
#             mimetype='application/json'
#         )

@app.route('/pedido/<int:pedido_id>', methods=['GET'])
def listPedidoById(pedido_id):
    try:
        # Buscar o pedido pelo ID, incluindo os produtos associados
        pedido = db_session.query(Pedido).filter(Pedido.id == pedido_id).first()

        # Verificar se o pedido existe
        if not pedido:
            return Response(
                response=json.dumps({'status': 'erro', 'message': 'Pedido não encontrado'}),
                status=404,
                mimetype='application/json'
            )

        # Buscar os produtos associados ao pedido
        produtos = db_session.query(PedidoProduto).filter(PedidoProduto.pedido_id == pedido_id).all()

        # Serializar os produtos
        produtos_serializados = [produto.serialize() for produto in produtos]

        # Retornar o pedido com os produtos
        return Response(
            response=json.dumps({
                'status': 'sucesso',
                'pedido': pedido.serialize(),
                'produtos': produtos_serializados
            }),
            status=200,
            mimetype='application/json'
        )

    except Exception as e:
        return Response(
            response=json.dumps({'status': 'erro', 'message': str(e)}),
            status=500,
            mimetype='application/json'
        )

@app.route('/pedidos/admin/<int:admin_id>', methods=['GET'])
def listAllPedidoByAdmin(admin_id):
    try:
        # 1. Busca todos os funcionários que pertencem ao admin (com base no admin_id)
        funcionarios = db_session.query(Funcionario).filter(Funcionario.admin_id == admin_id).all()

        if not funcionarios:
            return Response(
                response=json.dumps({'status': 'erro', 'message': f'Nenhum funcionário encontrado para o admin com ID {admin_id}'}),
                status=404,
                mimetype='application/json'
            )

        # 2. Coleta todos os IDs dos funcionários encontrados
        funcionario_ids = [funcionario.id for funcionario in funcionarios]

        # 3. Busca todos os pedidos que pertencem a esses funcionários
        pedidos = db_session.query(Pedido).filter(Pedido.funcionario_id.in_(funcionario_ids)).all()

        if not pedidos:
            return Response(
                response=json.dumps({'status': 'erro', 'message': f'Não há pedidos associados aos funcionários do admin com ID {admin_id}'}),
                status=404,
                mimetype='application/json'
            )

        # 4. Serializa os pedidos
        pedidos_serializados = [pedido.serialize() for pedido in pedidos]

        return Response(
            response=json.dumps({
                'status': 'sucesso',
                'pedidos': pedidos_serializados
            }),
            status=200,
            mimetype='application/json'
        )

    except Exception as e:
        return Response(
            response=json.dumps({'status': 'erro', 'message': str(e)}),
            status=500,
            mimetype='application/json'
        )


@app.route('/pedido/produtos/<int:pedido_id>', methods=['GET'])
def listAllProdutoByPedido(pedido_id):
    try:
        # Busca o pedido no banco de dados
        pedido = db_session.query(Pedido).filter(Pedido.id == pedido_id).first()
        if not pedido:
            return Response(
                response=json.dumps({'status': 'erro', 'message': 'Pedido não encontrado'}),
                status=404,
                mimetype='application/json'
            )

        # Busca todos os produtos associados ao pedido através da tabela PedidoProduto
        produtos_do_pedido = db_session.query(Produto, PedidoProduto.quantidade).join(PedidoProduto).filter(PedidoProduto.pedido_id == pedido_id).all()

        # Verifica se existem produtos associados ao pedido
        if not produtos_do_pedido:
            return Response(
                response=json.dumps({'status': 'sucesso', 'message': 'Nenhum produto associado a este pedido'}),
                status=200,
                mimetype='application/json'
            )

        # Serializa os produtos e retorna como resposta, incluindo a quantidade dentro do produto
        produtos_serializados = [
            {
                **produto.serialize(),  # Inclui todos os dados do produto
                'quantidade': quantidade  # Adiciona a quantidade do produto
            }
            for produto, quantidade in produtos_do_pedido
        ]

        return Response(
            response=json.dumps({
                'status': 'sucesso',
                'message': 'Produtos associados ao pedido recuperados com sucesso',
                'pedido': pedido.serialize(),
                'produtos': produtos_serializados
            }),
            status=200,
            mimetype='application/json'
        )

    except Exception as e:
        return Response(
            response=json.dumps({'status': 'erro', 'message': str(e)}),
            status=500,
            mimetype='application/json'
        )

@app.route('/pedidos/status/<int:admin_id>/<string:status>', methods=['GET'])
def listarPedidosPorStatus(admin_id, status):
    try:
        # Verifica se o status é válido
        valid_status = ['PENDENTE', 'EM_ESPERA', 'EM_PRODUCAO', 'FINALIZADO']
        if status not in valid_status:
            return Response(
                response=json.dumps({'status': 'erro', 'message': f'Status inválido. Valores permitidos: {", ".join(valid_status)}'}),
                status=400,
                mimetype='application/json'
            )

        # 1. Busca todos os funcionários que pertencem ao admin (com base no admin_id)
        funcionarios = db_session.query(Funcionario).filter(Funcionario.admin_id == admin_id).all()

        if not funcionarios:
            return Response(
                response=json.dumps({'status': 'erro', 'message': f'Nenhum funcionário encontrado para o admin com ID {admin_id}'}),
                status=404,
                mimetype='application/json'
            )

        # 2. Coleta todos os IDs dos funcionários encontrados
        funcionario_ids = [funcionario.id for funcionario in funcionarios]

        # 3. Busca todos os pedidos que pertencem a esses funcionários e têm o status especificado
        pedidos = db_session.query(Pedido).filter(Pedido.funcionario_id.in_(funcionario_ids), Pedido.status == status).all()

        # Verifica se não encontrou pedidos
        if not pedidos:
            return Response(
                response=json.dumps({'status': 'erro', 'message': f'Não há pedidos com o status {status} para o admin com ID {admin_id}'}),
                status=404,
                mimetype='application/json'
            )

        # Serializa os pedidos
        pedidos_serializados = [pedido.serialize() for pedido in pedidos]

        return Response(
            response=json.dumps({
                'status': 'sucesso',
                'pedidos': pedidos_serializados
            }),
            status=200,
            mimetype='application/json'
        )

    except Exception as e:
        return Response(
            response=json.dumps({'status': 'erro', 'message': str(e)}),
            status=500,
            mimetype='application/json'
        )

@app.route('/pedido', methods=['POST'])
def criarPedido():
    try:
        mesa = request.form.get('mesa')
        funcionario_id = request.form.get('funcionario_id')

        if not mesa or not funcionario_id:
            return Response(
                response=json.dumps({'status': 'erro', 'message': 'Mesa e funcionario_id são obrigatórios'}),
                status=400,
                mimetype='application/json'
            )

        # Criar pedido sem status e dataCriado
        pedido = Pedido(
            mesa=mesa,
            status=StatusPedido.PENDENTE,  # Status temporário ou 'pendente' até a finalização
            funcionario_id=int(funcionario_id),
        )

        db_session.add(pedido)
        db_session.commit()  # O pedido é persistido no banco de dados, mas sem status definitivo.

        return Response(
            response=json.dumps({
                'status': 'sucesso',
                'message': 'Pedido criado com sucesso!',
                'pedido': pedido.serialize()  # Retorna o pedido criado
            }),
            status=200,
            mimetype='application/json'
        )
    except Exception as e:
        return Response(
            response=json.dumps({'status': 'erro', 'message': str(e)}),
            status=500,
            mimetype='application/json'
        )

VALID_STATUSES = ['PENDENTE', 'EM_ESPERA', 'EM_PRODUCAO', 'FINALIZADO']

@app.route('/pedido/update-status/<int:pedido_id>', methods=['PUT'])
def updatePedido(pedido_id):
    try:
        status = request.form.get('status')  # Ou request.json.get('status')

        if not status or status not in VALID_STATUSES:
            return Response(
                response=json.dumps({'status': 'erro', 'message': 'Status inválido. Valores permitidos: PENDENTE, EM_ESPERA, EM_PRODUCAO, FINALIZADO'}),
                status=400,
                mimetype='application/json'
            )

        # Busca o pedido no banco de dados
        pedido = db_session.query(Pedido).filter(Pedido.id == pedido_id).first()

        if not pedido:
            return Response(
                response=json.dumps({'status': 'erro', 'message': 'Pedido não encontrado'}),
                status=404,
                mimetype='application/json'
            )

        # Atualiza o status do pedido
        pedido.status = status
        db_session.commit()

        return Response(
            response=json.dumps({
                'status': 'sucesso',
                'message': 'Status do pedido atualizado com sucesso!',
                'pedido': pedido.serialize()
            }),
            status=200,
            mimetype='application/json'
        )

    except Exception as e:
        return Response(
            response=json.dumps({'status': 'erro', 'message': str(e)}),
            status=500,
            mimetype='application/json'
        )

@app.route('/pedido/adicionar-produto', methods=['POST'])
def adicionarProduto():
    try:
        pedido_id = request.form.get('pedido_id')
        produto_id = request.form.get('produto_id')
        quantidade = request.form.get('quantidade')

        # Verifica se todos os dados obrigatórios foram passados
        if not pedido_id or not produto_id or not quantidade:
            return Response(
                response=json.dumps(
                    {'status': 'erro', 'message': 'Pedido ID, Produto ID e Quantidade são obrigatórios'}
                ),
                status=400,
                mimetype='application/json'
            )

        # Busca o pedido no banco de dados
        pedido = db_session.query(Pedido).filter(Pedido.id == pedido_id).first()
        if not pedido:
            return Response(
                response=json.dumps({'status': 'erro', 'message': 'Pedido não encontrado'}),
                status=404,
                mimetype='application/json'
            )

        # Busca o produto no banco de dados
        produto = db_session.query(Produto).filter(Produto.id == produto_id).first()
        if not produto:
            return Response(
                response=json.dumps({'status': 'erro', 'message': 'Produto não encontrado'}),
                status=404,
                mimetype='application/json'
            )

        # Verifica se o produto já foi adicionado ao pedido
        pedido_produto = db_session.query(PedidoProduto).filter_by(pedido_id=pedido.id, produto_id=produto.id).first()
        if pedido_produto:
            # Se já existe, atualiza a quantidade
            pedido_produto.quantidade += int(quantidade)
        else:
            # Caso contrário, cria uma nova associação
            pedido_produto = PedidoProduto(
                pedido_id=int(pedido.id),
                produto_id=int(produto.id),
                quantidade=int(quantidade)
            )
            db_session.add(pedido_produto)

        db_session.commit()  # Salva a associação no banco de dados

        # Busca os produtos relacionados ao pedido com a quantidade
        produtos_do_pedido = db_session.query(PedidoProduto, Produto).join(Produto).filter(PedidoProduto.pedido_id == pedido.id).all()

        # Formata os produtos para incluir a quantidade
        produtos_com_quantidade = [
            {
                'id': produto.id,
                'nome': produto.nome,
                'preco': produto.preco,
                'quantidade': pedido_produto.quantidade
            } for pedido_produto, produto in produtos_do_pedido
        ]

        # Retorna a resposta com o pedido e seus produtos atualizados
        return Response(
            response=json.dumps({
                'status': 'sucesso',
                'message': 'Produto adicionado ao pedido!',
                'pedido': pedido.serialize(),  # Retorna o pedido atualizado
                'produtos': produtos_com_quantidade  # Retorna os produtos com quantidade
            }),
            status=200,
            mimetype='application/json'
        )
    except Exception as e:
        return Response(
            response=json.dumps({'status': 'erro', 'message': str(e)}),
            status=500,
            mimetype='application/json'
        )


@app.route('/pedido/finalizar', methods=['POST'])
def finalizarPedido():
    try:
        pedido_id = request.form.get('pedido_id')  # O pedido a ser finalizado

        if not pedido_id:
            return Response(
                response=json.dumps({'status': 'erro', 'message': 'Pedido ID é obrigatório'}),
                status=400,
                mimetype='application/json'
            )

        # Buscar o pedido pelo ID
        pedido = db_session.query(Pedido).filter(Pedido.id == pedido_id).first()
        if not pedido:
            return Response(
                response=json.dumps({'status': 'erro', 'message': 'Pedido não encontrado'}),
                status=404,
                mimetype='application/json'
            )

        # Verificar se o pedido tem pelo menos um produto associado
        produtos_associados = db_session.query(PedidoProduto).filter_by(pedido_id=pedido_id).all()
        if not produtos_associados:
            return Response(
                response=json.dumps({'status': 'erro', 'message': 'Pedido não pode ser finalizado sem produtos'}),
                status=400,
                mimetype='application/json'
            )

        # Atualizar o status do pedido para "EM_ESPERA" e adicionar a data de criação
        pedido.status = StatusPedido.EM_ESPERA
        pedido.dataCriado = datetime.now()  # Atribui a data atual
        db_session.commit()  # Commit para salvar as alterações

        return Response(
            response=json.dumps({
                'status': 'sucesso',
                'message': 'Pedido finalizado com sucesso!',
                'pedido': pedido.serialize()
            }),
            status=200,
            mimetype='application/json'
        )

    except Exception as e:
        return Response(
            response=json.dumps({'status': 'erro', 'message': str(e)}),
            status=500,
            mimetype='application/json'
        )

@app.route('/pedido/<int:pedido_id>/produto/<int:produto_id>', methods=['POST'])
def removerProduto(pedido_id, produto_id):
    try:
        # Busca a associação entre pedido e produto
        pedido_produto = db_session.query(PedidoProduto).filter_by(pedido_id=pedido_id, produto_id=produto_id).first()

        if not pedido_produto:
            return Response(
                response=json.dumps({'status': 'erro', 'message': 'Produto não encontrado no pedido'}),
                status=404,
                mimetype='application/json'
            )

        # Remove a associação do produto com o pedido
        db_session.delete(pedido_produto)
        db_session.commit()

        return Response(
            response=json.dumps({'status': 'sucesso', 'message': 'Produto removido do pedido'}),
            status=200,
            mimetype='application/json'
        )
    except Exception as e:
        return Response(
            response=json.dumps({'status': 'erro', 'message': str(e)}),
            status=500,
            mimetype='application/json'
        )



if __name__ == '__main__':
    app.run()
