from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from sqlalchemy.exc import IntegrityError
from schemas.aluno import apresenta_aluno_lista
from model import Session, Aluno  
from logger import logger
from schemas import *
from flask_cors import CORS
from schemas.aluno import ListagemDeAlunosSchema, AlunoViewSchema

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app, origins="*")


home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
aluno_tag = Tag(name="Aluno", description="Cadastro de novo Aluno")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação."""
    return redirect('/openapi')



@app.post('/aluno', tags=[aluno_tag],
    responses={200: AlunoViewSchema, 409: ErrorSchema, 400: ErrorSchema})
def add_aluno(form: AlunoSchema):
    """Adiciona um novo aluno à base de dados"""
    aluno = Aluno(
        primeiro_nome=form.primeiro_nome,
        segundo_nome=form.segundo_nome,
        cpf=form.cpf,
        data_nascimento=form.data_nascimento
    )

    logger.debug(f"Adicionando aluno {aluno.primeiro_nome} {aluno.segundo_nome}, CPF {aluno.cpf}")

    try:
        session = Session()
        session.add(aluno)
        session.commit()
        return apresenta_aluno_lista([aluno]), 200

    except IntegrityError:
        session.rollback()
        return {"message": "CPF já cadastrado."}, 409

    except Exception as e:
        logger.error(f"Erro ao adicionar aluno: {str(e)}")
        return {"message": f"Erro inesperado: {str(e)}"}, 400
    
    
@app.delete('/del_aluno', tags=[aluno_tag],
    responses={"200": AlunoDelSchema, "404": ErrorSchema})
def del_aluno(query: AlunoBuscaSchema):
    """Deleta um aluno a partir do CPF informado
    Retorna uma mensagem de confirmação da remoção.
    """
    cpf_aluno = query.cpf
    logger.debug(f"Deletando aluno com CPF {cpf_aluno}")

    session = Session()
    count = session.query(Aluno).filter(Aluno.cpf == cpf_aluno).delete()
    session.commit()

    if count:
        logger.debug(f"Deletado aluno com CPF {cpf_aluno}")
        return {"message": "Aluno removido", "cpf": cpf_aluno}, 200
    else:
        error_msg = "Aluno não encontrado na base :/"
        logger.warning(f"Erro ao deletar aluno com CPF '{cpf_aluno}', {error_msg}")
        return {"message": error_msg}, 404
