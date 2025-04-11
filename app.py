from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from sqlalchemy.exc import IntegrityError
from schemas.processo import apresenta_processo
from model import Session, Processo  
from logger import logger
from schemas import *
from flask_cors import CORS
from schemas.processo import Apresenta_Processo_Lista, ProcessoViewSchema

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app, origins="*")


home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
processo_tag = Tag(name="Processo", description="Cadastro de número de processo")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação."""
    return redirect('/openapi')



@app.post('/processo', tags=[processo_tag], 
    responses={"200": ProcessoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_processo(form: ProcessoSchema):
    """Adiciona um novo número de processo à base de dados com datas obrigatórias"""
    processo = Processo(
        numero=form.numero,
        descricao=form.descricao,
        data_inicio=form.data_inicio,  
        data_fim=form.data_fim      
    )        
    logger.debug(f"Adicionando processo '{processo.numero}' com datas {processo.data_inicio} - {processo.data_fim}")
    
    try:
        session = Session()
        session.add(processo)
        session.commit()
        logger.debug(f"Adicionado processo: '{processo.numero}' com datas {processo.data_inicio} - {processo.data_fim}")
        return Apresenta_Processo_Lista([processo]), 200
    
    except IntegrityError:
        error_msg = "Número de processo já cadastrado na base :/"
        logger.warning(f"Erro ao adicionar processo '{processo.numero}', {error_msg}")
        return {"message": error_msg}, 409
    
    except Exception as e:
        error_msg = f"Não foi possível salvar o novo processo :/ Detalhes: {str(e)}"
        logger.warning(f"Erro ao adicionar processo '{processo.numero}', {error_msg}")
        return {"message": error_msg}, 400




@app.get('/processos', tags=[processo_tag],
         responses={"200": ListagemDeProcessosSchema, "404": ErrorSchema})
def get_processos():
    """Faz a busca por todos os Processos cadastrados

    Retorna uma representação da listagem de processos.
    """
    logger.debug("Coletando processos")
    session = Session()
    processos = session.query(Processo).all()

    if not processos:
        return {"processos": []}, 200
    else:
        logger.debug(f"{len(processos)} processos encontrados")
        return Apresenta_Processo_Lista(processos), 200




@app.get('/busca_processo', tags=[processo_tag],
         responses={"200": ProcessoViewSchema, "404": ErrorSchema})
def get_processo(query: ProcessoBuscaSchema):
    """Faz a busca por um Processo a partir do número

    Retorna uma representação do processo cadastrado.
    """
    numero_processo = query.numero
    logger.debug(f"Coletando dados sobre o processo #{numero_processo}")

    session = Session()
    processo = session.query(Processo).filter(Processo.numero == numero_processo).first()

    if not processo:
        error_msg = "Processo não encontrado na base :/"
        logger.warning(f"Erro ao buscar processo '{numero_processo}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Processo encontrado: '{processo.numero}'")
        return apresenta_processo(processo), 200




@app.delete('/del_processo', tags=[processo_tag],
            responses={"200": ProcessoDelSchema, "404": ErrorSchema})
def del_processo(query: ProcessoBuscaSchema):
    """Deleta um Processo a partir do número informado

    Retorna uma mensagem de confirmação da remoção.
    """
    numero_processo = query.numero
    logger.debug(f"Deletando processo #{numero_processo}")

    session = Session()
    count = session.query(Processo).filter(Processo.numero == numero_processo).delete()
    session.commit()

    if count:
        logger.debug(f"Deletado processo #{numero_processo}")
        return {"message": "Processo removido", "numero": numero_processo}, 200
    else:
        error_msg = "Processo não encontrado na base :/"
        logger.warning(f"Erro ao deletar processo '{numero_processo}', {error_msg}")
        return {"message": error_msg}, 404




@app.put('/processo/atualizar', tags=[processo_tag],
         responses={"200": ProcessoViewSchema, "404": ErrorSchema})
def update_processo(form: ProcessoSchema):
    """Atualiza um Processo existente na base de dados.

    Retorna a representação do processo atualizado.
    """
    logger.debug(f"Atualizando processo {form.numero}")

    session = Session()
    processo = session.query(Processo).filter(Processo.numero == form.numero).first()

    if not processo:
        error_msg = "Processo não encontrado na base :/"
        logger.warning(f"Erro ao atualizar processo '{form.numero}', {error_msg}")
        return {"message": error_msg}, 404

    processo.descricao = form.descricao
    processo.data_inicio = form.data_inicio
    processo.data_fim = form.data_fim

    session.commit()
    logger.debug(f"Processo atualizado: '{processo.numero}'")
    return apresenta_processo(processo), 200
    