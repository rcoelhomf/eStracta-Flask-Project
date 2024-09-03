from flask import request
from models.empresa import db, Empresa
from flask import Blueprint
from flask_restx import Api, Resource, fields

empresa_blueprint = Blueprint('empresa', __name__)
empresa_api = Api(empresa_blueprint, doc='/docs', title='Empresa API', description='API para CRUD de empresas.')

empresa_model = empresa_api.model('Empresa', {
    'id': fields.Integer(readOnly=True, description='O identificador único da empresa'),
    'cnpj': fields.String(required=True, description='CNPJ da empresa'),
    'nome_razao': fields.String(required=True, description='Nome da razão social da empresa'),
    'nome_fantasia': fields.String(description='Nome fantasia da empresa'),
    'cnae': fields.String(description='CNAE da empresa'),
})


@empresa_api.route('/empresa')
class CompanyResource(Resource):
    @empresa_api.marshal_list_with(empresa_model)
    def get(self):
        company_list = Empresa.query.all()

        return company_list, 200

    @empresa_api.expect(empresa_model)
    @empresa_api.response(201, 'Empresa criada com sucesso.', empresa_model)
    def post(self):
        data = request.get_json()
        new_company = Empresa(
            cnpj=data.get('cnpj'),
            nome_razao=data.get('nome_razao'),
            nome_fantasia=data.get('nome_fantasia'),
            cnae=data.get('cnae')
        )
        db.session.add(new_company)
        db.session.commit()
        return data, 201


@empresa_api.route('/empresa/<int:id>')
@empresa_api.param('id')
class CompanyDetailResource(Resource):
    @empresa_api.marshal_with(empresa_model)
    def get(self, id):
        company = Empresa.query.get(id)
        if not company:
            return f"Empresa de id {id} não encontrada.", 404
        return company, 200

    @empresa_api.expect(empresa_model)
    @empresa_api.marshal_with(empresa_model)
    def patch(self, id):
        company = Empresa.query.get(id)
        if not company:
            return f"Empresa de id {id} não encontrada.", 404

        data = request.get_json()
        if data.get('cnpj') or data.get('nome_razao'):
            return 'Campo de atualização não autorizado.', 403
        company.nome_fantasia = data.get('nome_fantasia', company.nome_fantasia)
        company.cnae = data.get('cnae', company.cnae)
        db.session.commit()

        return {
            'id': company.id,
            'cnpj': company.cnpj,
            'nome_razao': company.nome_razao,
            'nome_fantasia': company.nome_fantasia,
            'cnae': company.cnae
        }

    @empresa_api.response(204, 'Empresa deletada com sucesso.')
    def delete(self, id):
        company = Empresa.query.get(id)
        if not company:
            return f"Empresa de id {id} não encontrada.", 403

        db.session.delete(company)
        db.session.commit()
        return "", 204
