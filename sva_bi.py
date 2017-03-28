@manager.command
def cliente_report_sva():

    import MySQLdb
    import MySQLdb.cursors
    import unicodecsv as csv
    import gzip
    import urlparse
    from datetime import datetime, timedelta

    from tcm import app

    uri = urlparse.urlparse(app.config['SQLALCHEMY_DATABASE_URI'])

    conn = MySQLdb.connect(host=uri.hostname,
                           port=uri.port or 3306,
                           user=uri.username,
                           passwd=uri.password,
                           db=uri.path.lstrip('/'),
                           cursorclass=MySQLdb.cursors.SSCursor)

    dt = datetime.today()
    td = datetime.today() - timedelta(days=1)
    c = conn.cursor()
    c.execute("""SELECT contract.id, 1, contract.msisdn
              FROM contract_manager.contract
              INNER JOIN product ON contract.id_product = product.id
              WHERE carrier='claro-br' and product.active is True
              and contract.created
              between '{}' and '{}';""".format(td, dt))

    date = td.strftime("%Y%m%d%H%M00")
    filename = 'SVA_10_CLIENTE_{date}.txt.gz'.format(date=date)
    with gzip.open(filename, 'w') as f:
        writer = csv.writer(f, delimiter='|')
        writer.writerow(["codigo_cliente", "tipo_chave", "Numero_telefone", "Numero_CPF",
                         "Numero_CNPJ", "Email_Cliente", "Nome_Cliente", "Sexo_Cliente",
                         "Data_Nascimento", "Estado_Civil", "CEP_Cliente", "Endereco_Cliente",
                         "Complemento_Cliente", "Bairro_Cliente", "Cidade_Cliente", "Estado_Cliente"])
        for i, row in enumerate(c.fetchall(), 1):
            writer.writerow(['%s' % row[0], '1', '%s' % row[2][2:],
                             '', '', '', '', '', '', '', '', '', '', '', '', ''])

    f.close()
    return {'total': i, 'filename': filename}


@manager.command
def claro_sva_start():

    import MySQLdb
    import MySQLdb.cursors
    import unicodecsv as csv
    import gzip
    import urlparse
    from datetime import datetime, timedelta

    from tcm import app

    uri = urlparse.urlparse(app.config['SQLALCHEMY_DATABASE_URI'])

    conn = MySQLdb.connect(host=uri.hostname,
                           port=uri.port or 3306,
                           user=uri.username,
                           passwd=uri.password,
                           db=uri.path.lstrip('/'),
                           cursorclass=MySQLdb.cursors.SSCursor)

    dt = datetime.today()
    td = datetime.today() - timedelta(days=1)
    c = conn.cursor()
    c.execute("""SELECT C.created, C.id_product, CH.msisdn, C.activated, C.medium,
              CH.charged, CH.value, C.cancelled, CH.charged, CH.updated, C.msisdn,
              C.id_package, CH.code
              FROM contract_manager.charge as CH
              JOIN contract_manager.contract as C ON C.id = CH.id_contract
              WHERE C.id_product in (44, 45, 52)
              and CH.charged between '{}' and '{}';""".format(td, dt))

    date = td.strftime("%Y%m%d%H%M00")
    filename = 'SVA_10_CLARO_START_{date}.txt.gz'.format(date=date)
    with gzip.open(filename, 'w') as f:
        writer = csv.writer(f, delimiter='|')
        writer.writerow(["Data_Criacao_Registro_Origem", "Hora_Criacao_Registro_Origem",
                         "Codigo_servico", "Codigo_Categoria", "Numero_telefone",
                         "Data_Ativacao", "Hora_Ativacao", "Codigo_canal", "Comando",
                         "Data_Tarifacao", "Hora_Tarifacao", "Valor_Tarifacao",
                         "codigo_assinatura", "Data_Cancelamento", "Hora_Cancelamento",
                         "Data_Tentativa", "Hora_Tentativa", "Codigo_Status",
                         "Data_Estimada_Churn", "Hora_Estimada_Churn", "Valor_Repasse_Parceiro",
                         "Valor_Repasse_Claro", "Valor_Imposto", "Codigo_Parceiro",
                         "codigo_cliente", "tipo_chave", "Codigo_Tipo_Serviço", "Duracao_Servico",
                         "Codigo_detalhe_produto", "Codigo_Sharecode"])

        for i, row in enumerate(c.fetchall(), 1):
            writer.writerow(['%s' % row[0].strftime("%Y%m%d %H:%M:%S"), '', '%s' % row[1], '',
                             '%s' % row[2][2:], '%s' % row[3].strftime("%Y%m%d %H:%M:%S"), '',
                             '%s' % row[4], '', '%s' % row[5].strftime("%Y%m%d %H:%M:%S"),
                             '', '%s' % str(round(row[6], 2)).replace('.', ','), '',
                             '%s' % row[7].strftime("%Y%m%d %H:%M:%S") if row[7] else '', '',
                             '%s' % row[8].strftime("%Y%m%d %H:%M:%S") if row[8] else '',
                             '%s' % row[9].strftime("%Y%m%d %H:%M:%S"), '', '', '',
                             '40', '60', '', '10', '%s' % row[10][2:], '1', 'e', '',
                             '%s' % row[11], '%s' % row[12]])

    f.close()
    return {'total': i, 'filename': filename}


@manager.command
def claro_sva_sync():

    import MySQLdb
    import MySQLdb.cursors
    import unicodecsv as csv
    import gzip
    import urlparse
    from datetime import datetime, timedelta

    from tcm import app

    uri = urlparse.urlparse(app.config['SQLALCHEMY_DATABASE_URI'])

    conn = MySQLdb.connect(host=uri.hostname,
                           port=uri.port or 3306,
                           user=uri.username,
                           passwd=uri.password,
                           db=uri.path.lstrip('/'),
                           cursorclass=MySQLdb.cursors.SSCursor)

    dt = datetime.today()
    td = datetime.today() - timedelta(days=1)
    c = conn.cursor()
    c.execute("""SELECT C.created, C.id_product, CH.msisdn, C.activated,
              C.medium, CH.charged, CH.value, C.cancelled, CH.charged,
              CH.updated, C.msisdn, C.id_package, CH.code
              FROM contract_manager.charge as CH
              JOIN contract_manager.contract as C ON C.id = CH.id_contract
              WHERE C.id_product = 51
              and CH.charged between '{}' and '{}' limit 11;""".format(td, dt))

    date = td.strftime("%Y%m%d%H%M00")
    filename = 'SVA_10_CLARO_SYNC_{date}.txt.gz'.format(date=date)
    with gzip.open(filename, 'w') as f:
        writer = csv.writer(f, delimiter='|')
        writer.writerow(["Data_Criacao_Registro_Origem", "Hora_Criacao_Registro_Origem",
                         "Codigo_servico", "Codigo_Categoria", "Numero_telefone",
                         "Data_Ativacao", "Hora_Ativacao", "Codigo_canal", "Comando",
                         "Data_Tarifacao", "Hora_Tarifacao", "Valor_Tarifacao",
                         "codigo_assinatura", "Data_Cancelamento", "Hora_Cancelamento",
                         "Data_Tentativa", "Hora_Tentativa", "Codigo_Status",
                         "Data_Estimada_Churn", "Hora_Estimada_Churn", "Valor_Repasse_Parceiro",
                         "Valor_Repasse_Claro", "Valor_Imposto", "Codigo_Parceiro",
                         "codigo_cliente", "tipo_chave", "Codigo_Tipo_Serviço", "Duracao_Servico",
                         "Codigo_detalhe_produto", "Codigo_Sharecode"])

        for i, row in enumerate(c.fetchall(), 1):
            writer.writerow(['%s' % row[0].strftime("%Y%m%d %H:%M:%S"), '', '%s' % row[1], '',
                             '%s' % row[2][2:], '%s' % row[3].strftime("%Y%m%d %H:%M:%S") if row[3] else '',
                             '', '%s' % row[4] if row[4] else '', '',
                             '%s' % row[5].strftime("%Y%m%d %H:%M:%S"), '',
                             '%s' % str(round(row[6], 2)).replace('.', ',') if row[6] else '',
                             '', '%s' % row[7].strftime("%Y%m%d %H:%M:%S") if row[7] else '', '',
                             '%s' % row[8].strftime("%Y%m%d %H:%M:%S") if row[8] else '',
                             '%s' % row[9].strftime("%Y%m%d %H:%M:%S"),
                             '', '', '', '40', '60', '', '10', '%s' % row[10][2:], '1', 'e', '',
                             '%s' % row[11], '%s' % row[12]])

    f.close()
    return {'total': i, 'filename': filename}


@manager.command
def claro_sva_cpf():

    import MySQLdb
    import MySQLdb.cursors
    import unicodecsv as csv
    import gzip
    import urlparse
    from datetime import datetime, timedelta

    from tcm import app

    uri = urlparse.urlparse(app.config['SQLALCHEMY_DATABASE_URI'])

    conn = MySQLdb.connect(host=uri.hostname,
                           port=uri.port or 3306,
                           user=uri.username,
                           passwd=uri.password,
                           db=uri.path.lstrip('/'),
                           cursorclass=MySQLdb.cursors.SSCursor)

    dt = datetime.today()
    td = datetime.today() - timedelta(days=1)
    c = conn.cursor()
    c.execute("""SELECT C.created, C.id_product, CH.msisdn, C.activated, C.medium,
              CH.charged, CH.value, C.cancelled, CH.charged, CH.updated, C.msisdn,
              C.id_package, CH.code
              FROM contract_manager.charge as CH
              JOIN contract_manager.contract as C ON C.id = CH.id_contract
              WHERE C.id_product = 54
              and CH.charged between '{}' and '{}';""".format(td, dt))

    date = td.strftime("%Y%m%d%H%M00")
    filename = 'SVA_10_CLARO_CPF_{date}.txt.gz'.format(date=date)
    with gzip.open(filename, 'w') as f:
        writer = csv.writer(f, delimiter='|')
        writer.writerow(["Data_Criacao_Registro_Origem", "Hora_Criacao_Registro_Origem",
                         "Codigo_servico", "Codigo_Categoria", "Numero_telefone",
                         "Data_Ativacao", "Hora_Ativacao", "Codigo_canal", "Comando",
                         "Data_Tarifacao", "Hora_Tarifacao", "Valor_Tarifacao",
                         "codigo_assinatura", "Data_Cancelamento", "Hora_Cancelamento",
                         "Data_Tentativa", "Hora_Tentativa", "Codigo_Status",
                         "Data_Estimada_Churn", "Hora_Estimada_Churn", "Valor_Repasse_Parceiro",
                         "Valor_Repasse_Claro", "Valor_Imposto", "Codigo_Parceiro",
                         "codigo_cliente", "tipo_chave", "Codigo_Tipo_Serviço", "Duracao_Servico",
                         "Codigo_detalhe_produto", "Codigo_Sharecode"])

        for i, row in enumerate(c.fetchall(), 1):
            writer.writerow(['%s' % row[0].strftime("%Y%m%d %H:%M:%S"), '', '%s' % row[1], '',
                             '%s' % row[2][2:], '%s' % row[3].strftime("%Y%m%d %H:%M:%S"), '',
                             '%s' % row[4], '', '%s' % row[5].strftime("%Y%m%d %H:%M:%S"),
                             '', '%s' % str(round(row[6], 2)).replace('.', ','), '',
                             '%s' % row[7].strftime("%Y%m%d %H:%M:%S") if row[7] else '', '',
                             '%s' % row[8].strftime("%Y%m%d %H:%M:%S") if row[8] else '',
                             '%s' % row[9].strftime("%Y%m%d %H:%M:%S"),
                             '', '', '', '40', '60', '', '10', '%s' % row[10][2:],
                             '1', 'e', '', '%s' % row[11], '%s' % row[12]])

    f.close()
    return {'total': i, 'filename': filename}


@manager.command
def claro_sva_feel_safe():

    import MySQLdb
    import MySQLdb.cursors
    import unicodecsv as csv
    import gzip
    import urlparse
    from datetime import datetime, timedelta

    from tcm import app

    uri = urlparse.urlparse(app.config['SQLALCHEMY_DATABASE_URI'])

    conn = MySQLdb.connect(host=uri.hostname,
                           port=uri.port or 3306,
                           user=uri.username,
                           passwd=uri.password,
                           db=uri.path.lstrip('/'),
                           cursorclass=MySQLdb.cursors.SSCursor)

    dt = datetime.today()
    td = datetime.today() - timedelta(days=1)
    c = conn.cursor()
    c.execute("""SELECT C.created, C.id_product, CH.msisdn, C.activated, C.medium,
              CH.charged, CH.value, C.cancelled, CH.charged, CH.updated, C.msisdn,
              C.id_package, CH.code
              FROM contract_manager.charge as CH
              JOIN contract_manager.contract as C ON C.id = CH.id_contract
              WHERE C.id_product in (55, 56, 57, 72, 128, 129)
              and CH.charged between '{}' and '{}';""".format(td, dt))

    date = td.strftime("%Y%m%d%H%M00")
    filename = 'SVA_10_CLARO_FEEL_SAFE_{date}.txt.gz'.format(date=date)
    with gzip.open(filename, 'w') as f:
        writer = csv.writer(f, delimiter='|')
        writer.writerow(["Data_Criacao_Registro_Origem", "Hora_Criacao_Registro_Origem",
                         "Codigo_servico", "Codigo_Categoria", "Numero_telefone",
                         "Data_Ativacao", "Hora_Ativacao", "Codigo_canal", "Comando",
                         "Data_Tarifacao", "Hora_Tarifacao", "Valor_Tarifacao",
                         "codigo_assinatura", "Data_Cancelamento", "Hora_Cancelamento",
                         "Data_Tentativa", "Hora_Tentativa", "Codigo_Status",
                         "Data_Estimada_Churn", "Hora_Estimada_Churn", "Valor_Repasse_Parceiro",
                         "Valor_Repasse_Claro", "Valor_Imposto", "Codigo_Parceiro",
                         "codigo_cliente", "tipo_chave", "Codigo_Tipo_Serviço", "Duracao_Servico",
                         "Codigo_detalhe_produto", "Codigo_Sharecode"])

        for i, row in enumerate(c.fetchall(), 1):
            writer.writerow(['%s' % row[0].strftime("%Y%m%d %H:%M:%S"), '', '%s' % row[1], '',
                             '%s' % row[2][2:], '%s' % row[3].strftime("%Y%m%d %H:%M:%S"), '',
                             '%s' % row[4], '', '%s' % row[5].strftime("%Y%m%d %H:%M:%S"),
                             '', '%s' % str(round(row[6], 2)).replace('.', ','), '',
                             '%s' % row[7].strftime("%Y%m%d %H%M%S") if row[7] else '', '',
                             '%s' % row[8].strftime("%Y%m%d %H:%M:%S") if row[8] else '',
                             '%s' % row[9].strftime("%Y%m%d %H:%M:%S"), '', '', '',
                             '40', '60', '', '10', '%s' % row[10][2:], '1', 'e', '',
                             '%s' % row[11], '%s' % row[12]])

    f.close()
    return {'total': i, 'filename': filename}


@manager.command
def claro_sva_neymar():

    import MySQLdb
    import MySQLdb.cursors
    import unicodecsv as csv
    import gzip
    import urlparse
    from datetime import datetime, timedelta

    from tcm import app

    uri = urlparse.urlparse(app.config['SQLALCHEMY_DATABASE_URI'])

    conn = MySQLdb.connect(host=uri.hostname,
                           port=uri.port or 3306,
                           user=uri.username,
                           passwd=uri.password,
                           db=uri.path.lstrip('/'),
                           cursorclass=MySQLdb.cursors.SSCursor)

    dt = datetime.today()
    td = datetime.today() - timedelta(days=1)
    c = conn.cursor()
    c.execute("""SELECT C.created, C.id_product, CH.msisdn, C.activated, C.medium,
              CH.charged, CH.value, C.cancelled, CH.charged, CH.updated, C.msisdn,
              C.id_package, CH.code
              FROM contract_manager.charge as CH
              JOIN contract_manager.contract as C ON C.id = CH.id_contract
              WHERE C.id_product = 126

              and CH.charged between '{}' and '{}';""".format(td, dt))

    date = td.strftime("%Y%m%d%H%M00")
    filename = 'SVA_10_CLARO_NEYMAR_{date}.txt.gz'.format(date=date)
    with gzip.open(filename, 'w') as f:
        writer = csv.writer(f, delimiter='|')
        writer.writerow(["Data_Criacao_Registro_Origem", "Hora_Criacao_Registro_Origem",
                         "Codigo_servico", "Codigo_Categoria", "Numero_telefone",
                         "Data_Ativacao", "Hora_Ativacao", "Codigo_canal", "Comando",
                         "Data_Tarifacao", "Hora_Tarifacao", "Valor_Tarifacao",
                         "codigo_assinatura", "Data_Cancelamento", "Hora_Cancelamento",
                         "Data_Tentativa", "Hora_Tentativa", "Codigo_Status",
                         "Data_Estimada_Churn", "Hora_Estimada_Churn", "Valor_Repasse_Parceiro",
                         "Valor_Repasse_Claro", "Valor_Imposto", "Codigo_Parceiro",
                         "codigo_cliente", "tipo_chave", "Codigo_Tipo_Serviço", "Duracao_Servico",
                         "Codigo_detalhe_produto", "Codigo_Sharecode"])

        for i, row in enumerate(c.fetchall(), 1):
            writer.writerow(['%s' % row[0].strftime("%Y%m%d %H:%M:%S"), '', '%s' % row[1], '',
                             '%s' % row[2][2:], '%s' % row[3].strftime("%Y%m%d %H:%M:%S"), '',
                             '%s' % row[4], '', '%s' % row[5].strftime("%Y%m%d %H:%M:%S"),
                             '', '%s' % str(round(row[6], 2)).replace('.', ','), '',
                             '%s' % row[7].strftime("%Y%m%d %H:%M:%S") if row[7] else '', '',
                             '%s' % row[8].strftime("%Y%m%d %H:%M:%S") if row[8] else '',
                             '%s' % row[9].strftime("%Y%m%d %H:%M:%S"), '', '', '',
                             '40', '60', '', '10', '%s' % row[10][2:], '1', 'e', '',
                             '%s' % row[11], '%s' % row[12]])

    f.close()
    return {'total': i, 'filename': filename}


@manager.command
def claro_controle_arquivo():

    import unicodecsv as csv
    import gzip
    from datetime import datetime, timedelta

    array_temp = []
    array_temp.append(cliente_report_sva())
    array_temp.append(claro_sva_start())
    array_temp.append(claro_sva_cpf())
    array_temp.append(claro_sva_feel_safe())
    array_temp.append(claro_sva_neymar())

    date_time = datetime.today() - timedelta(days=1)
    file_name = 'SVA_10_LST_CTRL_ARQUIVO_{date}.txt.gz'.format(date=date_time.strftime("%Y%m%d%H%M00"))
    with gzip.open(file_name, 'w') as f:
        writer = csv.writer(f, delimiter='|')
        writer.writerow(["Data_movimento", "Codigo_parceiro", "Descricao_Nome_Arquivo",
                         "Descricao_Tipo_Arquivo", "Quantidade_Linha_Arquivo"])

        for row in array_temp:
            writer.writerow(['%s' % date_time.strftime("%Y%m%d %H:%M:%S"),
                             '10', '%s' % row.get('filename'), '', '%s' % row.get('total')])
    f.close()