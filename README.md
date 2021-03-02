# Imposto é Robô!

## Requisitos

- Scrapear os PDFs (local na mesma passa)
- Padrão de PDF é o da Rico
- Pega os dados importantes (Compra/Venda, Papel, Quantidade, ...)
- Confirma ou edita dados scaneados junto com PDF (esquerdo vs. direito)
- De acordo com as regras computa a declaração
    - Operações financeiras: se o valor na venda for maior que 20k em ações
- Mostrar resultados separados por Seção
    - Bens (Quantidade, preço médio de compra, Total, Ação, CNPJ)
    - Operações financeiras (Lucro/Prejuizo mensal) se o valor na venda for maior que 20k em ações
    - Aba do lucro sem imposto (Rendimentos não tributados)

## Tarefas

- [x] Extrair texto
- [x] Transformar o texto extraído em objetos
- [ ] Transformar as notas em objetos
- [ ] Verifcar se emolumentos e taxa de liquidação batem
- [ ] Carteira mantém registro das operações abertas
