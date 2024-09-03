from flask import request
from models.empresa import db, Empresa
from flask import Blueprint
from flask_restx import Api, Resource, fields, marshal

empresa_blueprint = Blueprint('empresa', __name__)
empresa_api = Api(empresa_blueprint, doc='/docs', title='Empresa API', description='API para CRUD de empresas.')

empresa_model = empresa_api.model('Empresa', {
    'id': fields.Integer(readOnly=True, description='O identificador único da empresa'),
    'cnpj': fields.String(required=True, description='CNPJ da empresa'),
    'nome_razao': fields.String(required=True, description='Nome da razão social da empresa'),
    'nome_fantasia': fields.String(description='Nome fantasia da empresa'),
    'cnae': fields.String(description='CNAE da empresa'),
})


pagination_model = empresa_api.model('Pagination', {
    'total': fields.Integer(description='Número total de empresas'),
    'pages': fields.Integer(description='Número total de páginas'),
    'current_page': fields.Integer(description='Número da página atual'),
    'per_page': fields.Integer(description='Número de empresas por página'),
    'has_next': fields.Boolean(description='Indica se há uma próxima página'),
    'has_prev': fields.Boolean(description='Indica se há uma página anterior'),
    'companies': fields.List(fields.Nested(empresa_model), description='Lista de empresas na página atual'),
})


@empresa_api.route('/empresa')
class CompanyResource(Resource):
    @empresa_api.marshal_with(pagination_model)
    def get(self):
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        paginated_companies = Empresa.query.paginate(page=page, per_page=per_page, error_out=False)
        response = {
            'total': paginated_companies.total,
            'pages': paginated_companies.pages,
            'current_page': paginated_companies.page,
            'per_page': paginated_companies.per_page,
            'has_next': paginated_companies.has_next,
            'has_prev': paginated_companies.has_prev,
            'companies': paginated_companies.items
        }

        return response, 200

    @empresa_api.expect(empresa_model)
    @empresa_api.response(201, 'Empresa criada com sucesso.', empresa_model)
    def post(self):
        data = request.get_json()
        if Empresa.query.filter_by(cnpj=data.get('cnpj')).first():
            return "Empresa com esse cnpj ja cadastrada", 403
        new_company = Empresa(
            cnpj=data.get('cnpj'),
            nome_razao=data.get('nome_razao'),
            nome_fantasia=data.get('nome_fantasia'),
            cnae=data.get('cnae')
        )
        db.session.add(new_company)
        db.session.commit()
        return data, 201


@empresa_api.route('/empresa/<string:cnpj>')
@empresa_api.param('cnpj')
class CompanyDetailResource(Resource):
    @empresa_api.marshal_with(empresa_model)
    def get(self, cnpj):
        company = Empresa.query.filter_by(cnpj=cnpj).first()
        if not company:
            return f"Empresa de cnpj {cnpj} não encontrada.", 404
        return company, 200

    @empresa_api.expect(empresa_model)
    @empresa_api.marshal_with(empresa_model)
    def patch(self, cnpj):
        company = Empresa.query.filter_by(cnpj=cnpj).first()
        if not company:
            return f"Empresa de cnpj {cnpj} não encontrada.", 404

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
    def delete(self, cnpj):
        company = Empresa.query.filter_by(cnpj=cnpj).first()
        if not company:
            return f"Empresa de cnpj {cnpj} não encontrada.", 403

        db.session.delete(company)
        db.session.commit()
        return "", 204
