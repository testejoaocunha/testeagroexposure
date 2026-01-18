# --- CALCULADORA DE SOJA ---

# 1. ENTRADA DE DADOS
print("Digite os valores abaixo para calcular o preço por saca:")

cbot = float(input("CBOT (Bushel): "))
premio = float(input("Prêmio (Cents/Bushel): "))
cambio = float(input("Câmbio (Dólar): "))
frete = float(input("Frete por saca (R$): "))

# 2. LÓGICA DE CÁLCULO
# Somamos CBOT + Prêmio e dividimos por 100 (pois são cents)
# Multiplicamos por 0.60 (fator de conversão bushel para saca de 60kg)
preco_em_dolar = ((cbot + premio) / 100) * 0.60

# Converte para Real e subtrai o frete
preco_bruto_real = preco_em_dolar * cambio
preco_final_liquido = preco_bruto_real - frete

# 3. RESULTADO
print("-" * 30)
print(f"Resultado Bruto: R$ {preco_bruto_real:.2f}")
print(f"Resultado Líquido (com frete): R$ {preco_final_liquido:.2f}")
print("-" * 30)