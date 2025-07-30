# Projeto-Orientado-a-Objeto
Para a materia de projeto de software

DESCRIÇÃO DE GERENCIAMENTO DE PORTFÓLIO

Este módulo é uma das funcionalidade do projeto de Sistema de Negociação Automatizada. 
Ele permite o controle e acompanhamento de carteiras de investimento, incluindo adição de ativos, cálculo do valor total investido e visualização da carteira.

CLASSE: Portfolio 
        |--> Representa uma carteira de investimentos de um usuario. Será responsável para guardar ativos comprados, calcular o valor total investido
        e exibir os ativos da carteira.

OBEJTO: user_portfolio.
        |--> Representa uma carteira de investimento individual. 

ATRIBUTO DE OBJETO
       ATIVOS (do tipo list) > Lista que armazena todos os ativos adicionados à carteira. Cada ativo é um dicionário contendo nome, quantidade e preço.
       SALDO (do tipo float) > 	Representa o saldo disponível do usuário (pode ser usado futuramente). Inicialmente é 0.0.

AÇÕES DO OBJETO
       adicionar_ativo() > adiciona um ativo à carteira
       calcular_valor_total() > soma o valor total investido
       listar_carteira() > exibe os ativos na tela


