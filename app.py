import json
from flask import Flask, request, Response
from sqlalchemy import select, func

from model import *

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


# @app.route('/admins', methods=['GET'])
# def ListAllAdmins():
#     try:
#         admin = select(Admin).select_from(Admin)
#         print(admin)
#         admin = db_session.execute(admin).scalars()
#         result = []
#         for consulta in admin:
#             result.append(consulta.serialize())
#         final = json.dumps(result)
#         return Response(
#             final,
#             status=200,
#             mimetype='application/json'
#         )
#     except Exception as e:
#         final = {
#             'status': 'error',
#             'message': str(e)
#         }
#         return Response(
#             response=json.dumps(final)
#         )
#
#
# @app.route('/admin/<int:id>', methods=['GET'])
# def listAdminById(id):
#     try:
#         admin_sql = select(Admin).where(Admin.id == id)
#         admin = db_session.execute(admin_sql).fetchone()
#         result = []
#         for consulta in admin:
#             result.append(consulta.serialize())
#         final = json.dumps(result)
#         return Response(
#             response=final,
#             status=200,
#             mimetype='application/json'
#         )
#     except Exception as e:
#         final = {
#             'status': 'error',
#             'message': str(e)
#         }
#         return Response(
#             response=json.dumps(final)
#         )
#
#
# @app.route('/admin', methods=['POST'])
# def createAdmin():
#     try:
#         admin = Admin(
#             nome=request.form['nome'],
#             email=request.form['email'],
#             senha=request.form['senha'],
#             cpf=request.form['cpf']
#         )
#         admin.save()
#         final = {
#             'status': 'success',
#             'message': 'Admin registrado com sucesso!',
#             'nome': admin.nome,
#             'email': admin.email,
#             'senha': admin.senha,
#             'cpf': admin.cpf,
#         }
#
#         return Response(
#             response=json.dumps(final),
#             status=201,
#             mimetype='application/json'
#         )
#     except Exception as e:
#         final = {
#             'status': 'error',
#             'message': str(e),
#         }
#         return Response(
#             response=json.dumps(final),
#         )
#
#
# @app.route('/admin/<int:id>', methods=['PUT'])
# def updateAdmin(id):
#     try:
#         admin = select(Admin).where(Admin.id == id)
#         admin = db_session.execute(admin).scalar()
#         if request.form['nome']:
#             admin.nome = request.form['nome']
#         if request.form['email']:
#             admin.email = request.form['email']
#         if request.form['senha']:
#             admin.senha = request.form['senha']
#         if request.form['cpf']:
#             admin.cpf = request.form['cpf']
#         admin.save()
#         final = {
#             'status': 'success',
#             'message': 'Admin atualizado com sucesso!',
#             'nome': admin.nome,
#             'email': admin.email,
#             'senha': admin.senha,
#             'cpf': admin.cpf
#         }
#         return Response(
#             response=json.dumps(final),
#             status=200,
#             mimetype='application/json'
#         )
#     except Exception as e:
#         final = {
#             'status': 'error',
#             'message': str(e)
#         }
#         return Response(
#             response=json.dumps(final)
#         )


@app.route('/categorias', methods=['GET'])
def ListAllCategorias():
    try:
        categoria = select(Categoria).select_from(Categoria)
        print(categoria)
        categoria = db_session.execute(categoria).scalars()
        result = []
        for consulta in categoria:
            result.append(consulta.serialize())
        final = json.dumps(result)
        return Response(
            final,
            status=200,
            mimetype='application/json'
        )
    except Exception as e:
        final = {
            'status': 'error',
            'message': str(e)
        }
        return Response(
            response=json.dumps(final)
        )


@app.route('/categoria/<int:id>', methods=['GET'])
def listCategoriaById(id):
    try:
        categoria_sql = select(Categoria).where(Categoria.id == id)
        categoria = db_session.execute(categoria_sql).fetchone()
        result = []
        for consulta in categoria:
            result.append(consulta.serialize())
        final = json.dumps(result)
        return Response(
            response=final,
            status=200,
            mimetype='application/json'
        )
    except Exception as e:
        final = {
            'status': 'error',
            'message': str(e)
        }
        return Response(
            response=json.dumps(final)
        )


@app.route('/categoria', methods=['POST'])
def createCategoria():
    try:
        categoria = Categoria(
            nome=request.form['nome'],
            icone=request.form['icone'],
        )
        categoria.save()
        final = {
            'status': 'success',
            'message': 'Categoria registrada com sucesso!',
            'nome': categoria.nome,
            'icone': categoria.icone,
        }

        return Response(
            response=json.dumps(final),
            status=201,
            mimetype='application/json'
        )
    except Exception as e:
        final = {
            'status': 'error',
            'message': str(e),
        }
        return Response(
            response=json.dumps(final),
        )


@app.route('/categoria/<int:id>', methods=['PUT'])
def updateCategoria(id):
    try:
        categoria = select(Categoria).where(Categoria.id == id)
        categoria = db_session.execute(categoria).scalar()
        if request.form['nome']:
            categoria.nome = request.form['nome']
        if request.form['icone']:
            categoria.email = request.form['icone']
        categoria.save()
        final = {
            'status': 'success',
            'message': 'Categoria atualizado com sucesso!',
            'nome': categoria.nome,
            'icone': categoria.icone,
        }
        return Response(
            response=json.dumps(final),
            status=200,
            mimetype='application/json'
        )
    except Exception as e:
        final = {
            'status': 'error',
            'message': str(e)
        }
        return Response(
            response=json.dumps(final)
        )


@app.route('/categoria/<int:id>', methods=['POST'])
def deleteCategoria(id):
    try:
        categoria = select(Categoria).where(Categoria.id == id)
        categoria = db_session.execute(categoria).scalar()
        final = {
            'status': 'sucess',
            'message': categoria.nome + 'foi excluida'
        }
        categoria.delete()
        return Response(
            response=json.dumps(final)
        )
    except Exception as e:
        final = {
            'status': 'error',
            'message': str(e)
        }
        return Response(
            response=json.dumps(final)
        )

#  pedro produto
@app.route('/produtos', methods=['GET'])
def listAllProdutos():
    try:
        produto = select(Produto).select_from(Produto)
        print(produto)
        produto = db_session.execute(produto).scalars()
        result = []
        for consulta in produto:
            result.append(consulta.serialize())
        final = json.dumps(result)
        return Response(
            final,
            status=200,
            mimetype='application/json'
        )
    except Exception as e:
        final = {
            'status': 'error',
            'message': str(e)
        }
        return Response(
            response=json.dumps(final)
        )


@app.route('/produto/<int:id>', methods=['GET'])
def listProdutoById(id):
    try:
        produto_sql = select(Produto).where(Produto.id == id)
        produto = db_session.execute(produto_sql).fetchone()
        result = []
        for consulta in produto:
            result.append(consulta.serialize())
        final = json.dumps(result)
        return Response(
            response=final,
            status=200,
            mimetype='application/json'
        )
    except Exception as e:
        final = {
            'status': 'error',
            'message': str(e)
        }
        return Response(
            response=json.dumps(final)
        )

@app.route('/produto', methods=['POST'])
def createProduto():
    try:
        produto = Produto(
            nome=request.form['nome'],
            preco=request.form['preco'],
            descricao=request.form['descricao'],
            imagem=request.form['imagem'],
            categoria_id=request.form['categoria_id']
        )
        produto.save()
        final = {
            'status': 'success',
            'message': 'Produto registrado com sucesso!',
            'nome': produto.nome,
            'descricao': produto.descricao,
            'preco': produto.preco,
            'categoria_id': produto.categoria_id,
            'imagem': produto.imagem
        }

        return Response(
            response=json.dumps(final),
            status=201,
            mimetype='application/json'
        )
    except Exception as e:
        final = {
            'status': 'error',
            'message': str(e),
        }
        return Response(
            response=json.dumps(final),
        )


@app.route('/produto/<int:id>', methods=['PUT'])
def updateProduto(id):
    try:
        produto = select(Produto).where(Produto.id == id)
        produto = db_session.execute(produto).scalar()
        if request.form['nome']:
            produto.nome = request.form['nome']
        if request.form['descricao']:
            produto.descricao = request.form['descricao']
        if request.form['imagem']:
            produto.imagem = request.form['imagem']
        if request.form['preco']:
            produto.preco = request.form['preco']
        produto.save()
        final = {
            'status': 'success',
            'message': 'Produto atualizado com sucesso!',
            'nome': produto.nome,
            'descricao': produto.descricao,
            'imagem': produto.imagem,
            'preco': produto.preco,
            'categoria_id': produto.categoria_id
        }
        return Response(
            response=json.dumps(final),
            status=200,
            mimetype='application/json'
        )
    except Exception as e:
        final = {
            'status': 'error',
            'message': str(e)
        }
    return Response(
        response=json.dumps(final)
    )

@app.route('/produto/<int:id>', methods=['POST'])
def deleteProduto(id):
    try:
        produto = select(Produto).where(Produto.id == id)
        produto = db_session.execute(produto).scalar()
        final = {
            'status': 'sucess',
            'message': produto.nome + 'foi excluida'
        }
        produto.delete()
        return Response(
            response=json.dumps(final)
        )
    except Exception as e:
        final = {
            'status': 'error',
            'message': str(e)
        }
        return Response(
            response=json.dumps(final)
        )


# VINICIUS HENRIQUE
@app.route('/funcionario', methods=['POST'])
def createFuncionario():
    try:
        funcionario = Funcionario(
            nome=request.form['nome'],
            email=request.form['email'],
            senha=request.form['senha'],
            telefone=request.form['telefone'],
        )
        funcionario.save()
        final = {
            'status': 'success',
            'message': 'Funcionario registrado com sucesso!',
            'nome': funcionario.nome,
            'email': funcionario.email,
            'senha': funcionario.senha,
            'telefone': funcionario.telefone,
        }

        return Response(
            response=json.dumps(final),
            status=201,
            mimetype='application/json'
        )
    except Exception as e:
        final = {
            'status': 'error',
            'message': str(e),
        }
        return Response(
            response=json.dumps(final),
        )


@app.route('/funcionario/<int:id>', methods=['PUT'])
def updateFuncionario(id):
    try:
        funcionario = select(Funcionario).where(Funcionario.id == id)
        funcionario = db_session.execute(funcionario).scalar()
        if request.form['nome']:
            funcionario.nome = request.form['nome']
        if request.form['email']:
            funcionario.email = request.form['email']
        if request.form['senha']:
            funcionario.senha = request.form['senha']
        if request.form['telefone']:
            funcionario.telefone = request.form['telefone']
        funcionario.save()
        final = {
            'status': 'success',
            'message': 'Funcionario atualizado com sucesso!',
            'nome': funcionario.nome,
            'email': funcionario.email,
            'senha': funcionario.senha,
            'telefone': funcionario.telefone
        }
        return Response(
            response=json.dumps(final),
            status=200,
            mimetype='application/json'
        )
    except Exception as e:
        final = {
            'status': 'error',
            'message': str(e)
        }
        return Response(
            response=json.dumps(final)
        )


@app.route('/funcionario', methods=['GET'])
def ListAllFuncionario():
    try:
        funcionario = select(Funcionario).select_from(Funcionario)
        print(Funcionario)
        funcionario = db_session.execute(funcionario).scalars()
        result = []
        for consulta in funcionario:
            result.append(consulta.serialize())
        final = json.dumps(result)
        return Response(
            final,
            status=200,
            mimetype='application/json'
        )
    except Exception as e:
        final = {
            'status': 'error',
            'message': str(e)
        }
        return Response(
            response=json.dumps(final)
        )


@app.route('/funcionario/<int:id>', methods=['GET'])
def listFuncionarioById(id):
    try:
        funcionario_sql = select(Funcionario).where(Funcionario.id == id)
        funcionario = db_session.execute(funcionario_sql).fetchone()
        result = []
        for consulta in funcionario:
            result.append(consulta.serialize())
        final = json.dumps(result)
        return Response(
            response=final,
            status=200,
            mimetype='application/json'
        )
    except Exception as e:
        final = {
            'status': 'error',
            'message': str(e)
        }
        return Response(
            response=json.dumps(final)
        )

@app.route('/funcionario/<int:id>', methods=['POST'])
def deleteFuncionario(id):
    try:
        funcionario = select(Funcionario).where(Funcionario.id == id)
        funcionario = db_session.execute(funcionario).scalar()
        final = {
            'status': 'sucess',
            'message': funcionario.nome + 'foi excluida'
        }
        funcionario.delete()
        return Response(
            response=json.dumps(final)
        )
    except Exception as e:
        final = {
            'status': 'error',
            'message': str(e)
        }
        return Response(
            response=json.dumps(final)
        )

@app.route('/ingrediente', methods=['POST'])
def createIngrediente():
    try:
        ingrediente = Ingrediente(
            nome=request.form['nome'],
            produto_id=request.form['produto_id'],
        )
        ingrediente.save()
        final = {
            'status': 'success',
            'message': 'Funcionario registrado com sucesso!',
            'nome': ingrediente.nome,
            'produto_id': ingrediente.produto_id,
        }
        return Response(
            response=json.dumps(final),
            status=201,
            mimetype='application/json'
        )
    except Exception as e:
        final = {
            'status': 'error',
            'message': str(e),
        }
        return Response(
            response=json.dumps(final),
        )

@app.route('/ingrediente/<int:id>', methods=['PUT'])
def updateIngrediente(id):
    try:
        ingrediente = select(Ingrediente).where(Ingrediente.id == id)
        ingrediente = db_session.execute(ingrediente).scalar()
        if request.form['nome']:
            ingrediente.nome = request.form['nome']
        if request.form['email']:
            ingrediente.produto_id = request.form['produto_id']
        final = {
            'status': 'success',
            'message': 'Funcionario atualizado com sucesso!',
            'nome': ingrediente.nome,
            'produto_id': ingrediente.produto_id,
        }
        return Response(
            response=json.dumps(final),
            status=200,
            mimetype='application/json'
        )
    except Exception as e:
        final = {
            'status': 'error',
            'message': str(e)
        }
        return Response(
            response=json.dumps(final)
        )

@app.route('/ingrediente', methods=['GET'])
def ListAllIngrediente():
    try:
        ingrediente = select(Ingrediente).select_from(Ingrediente)
        print(Ingrediente)
        ingrediente = db_session.execute(ingrediente).scalars()
        result = []
        for consulta in ingrediente:
            result.append(consulta.serialize())
        final = json.dumps(result)
        return Response(
            final,
            status=200,
            mimetype='application/json'
        )
    except Exception as e:
        final = {
            'status': 'error',
            'message': str(e)
        }
        return Response(
            response=json.dumps(final)
        )

@app.route('/ingrediente/<int:id>', methods=['GET'])
def listIngredienteById(id):
    try:
        ingrediente_sql = select(Ingrediente).where(Ingrediente.id == id)
        ingrediente = db_session.execute(ingrediente_sql).fetchone()
        result = []
        for consulta in ingrediente:
            result.append(consulta.serialize())
        final = json.dumps(result)
        return Response(
            response=final,
            status=200,
            mimetype='application/json'
        )
    except Exception as e:
        final = {
            'status': 'error',
            'message': str(e)
        }
        return Response(
            response=json.dumps(final)
        )

@app.route('/ingrediente/<int:id>', methods=['POST'])
def deleteIngrediente(id):
    try:
        ingrediente = select(Ingrediente).where(Ingrediente.id == id)
        ingrediente = db_session.execute(ingrediente).scalar()
        final = {
            'status': 'sucess',
            'message': ingrediente.nome + 'foi excluida'
        }
        ingrediente.delete()
        return Response(
            response=json.dumps(final)
        )
    except Exception as e:
        final = {
            'status': 'error',
            'message': str(e)
        }
        return Response(
            response=json.dumps(final)
        )

@app.route('/pedido', methods=['POST'])
def createPedido():
    try:
        pedido = Pedido(
            mesa=request.form['mesa'],
            status=request.form['status'],
            dataCriado=request.form['dataCriado'],
            funcionario_id=request.form['funcionario_id'],

        )
        pedido.save()
        final = {
            'status': 'success',
            'message': 'Pedido registrado com sucesso!',
            'mesa': pedido.mesa,
            'status': pedido.status,
            'dataCriado': pedido.dataCriado,
            'funcionario_id': pedido.funcionario_id
        }
        return Response(
            response=json.dumps(final),
            status=201,
            mimetype='application/json'
        )
    except Exception as e:
        final = {
            'status': 'error',
            'message': str(e),
        }
        return Response(
            response=json.dumps(final),
        )

@app.route('/pedido/<int:id>', methods=['PUT'])
def updatePedido(id):
    try:
        pedido = select(Pedido).where(Pedido.id == id)
        pedido = db_session.execute(pedido).scalar()
        if request.form['mesa']:
            pedido.mesa = request.form['mesa']
        if request.form['status']:
            pedido.status = request.form['status']
        if request.form['dataCriado']:
            pedido.dataCriado = request.form['dataCriado']
        if request.form['funcionario_id']:
            pedido.funcionario_id = request.form['funcionario_id']
        pedido.save()
        final = {
            'status': 'success',
            'message': 'Pedido atualizado com sucesso!',
            'mesa': pedido.mesa,
            'status': pedido.status,
            'dataCriado': pedido.dataCriado,
            'funcionario_id': pedido.funcionario_id
        }
        return Response(
            response=json.dumps(final),
            status=200,
            mimetype='application/json'
        )
    except Exception as e:
        final = {
            'status': 'error',
            'message': str(e)
        }
        return Response(
            response=json.dumps(final)
        )


@app.route('/pedido/<int:id>', methods=['GET'])
def listPedidoById(id):
    try:
        pedido_sql = select(Pedido).where(Pedido.id == id)
        pedido = db_session.execute(pedido_sql).fetchone()
        result = []
        for consulta in pedido:
            result.append(consulta.serialize())
        final = json.dumps(result)
        return Response(
            response=final,
            status=200,
            mimetype='application/json'
        )
    except Exception as e:
        final = {
            'status': 'error',
            'message': str(e)
        }
        return Response(
            response=json.dumps(final)
        )

@app.route('/pedido', methods=['GET'])
def ListAllPedido():
    try:
        pedido = select(Pedido).select_from(Pedido)
        print(Pedido)
        pedido = db_session.execute(pedido).scalars()
        result = []
        for consulta in pedido:
            result.append(consulta.serialize())
        final = json.dumps(result)
        return Response(
            final,
            status=200,
            mimetype='application/json'
        )
    except Exception as e:
        final = {
            'status': 'error',
            'message': str(e)
        }
        return Response(
            response=json.dumps(final)
        )





if __name__ == '__main__':
    app.run()
