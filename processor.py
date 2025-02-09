import pandas as pd
import re

def process_csv(input_file_path):
    # Detectar delimitador automaticamente
    with open(input_file_path, "r", encoding="utf-8") as file:
        first_line = file.readline()
        detected_delimiter = "," if "," in first_line else ";"

    # Carregar o DataFrame original exatamente como no local
    try:
        df_original = pd.read_csv(input_file_path, sep=detected_delimiter, encoding="utf-8", dtype=str)
    except Exception as e:
        print(f"Erro ao carregar o arquivo: {e}")
        return None

    # Criar uma cópia para aplicar as correções
    df_corrected_final = df_original.copy()

    # Definir padrões para detectar colunas que precisam ser corrigidas
    patterns = [
        r"^\d+-.*-.*KC",
        r"^\d+-.*-.*Lab",
        r"^Atividade\s*[:|]\s*.+",
    ]

    # Identificar colunas alvo
    target_columns = [
        col for col in df_corrected_final.columns
        if any(re.match(pattern, col, re.IGNORECASE) for pattern in patterns)
    ]

    # Contar quantos alunos têm notas em cada coluna relevante
    column_counts = {col: df_corrected_final[col].notna().sum() for col in target_columns}

    # Aplicar a correção: Preencher valores vazios com "0,00" somente se houver pelo menos 3 notas na coluna
    for col in target_columns:
        if column_counts[col] >= 5:
            df_corrected_final[col] = df_corrected_final[col].fillna("0,00")

    # Converter valores para numéricos corretamente
    def convert_to_numeric(value):
        if isinstance(value, str):
            value = value.replace(',', '.').strip()  # Remove espaços e troca vírgula por ponto
        try:
            return float(value)
        except ValueError:
            return 0.0

    for col in target_columns:
        df_corrected_final[col] = df_corrected_final[col].apply(convert_to_numeric)

    # Remover a linha "Points Possible" para evitar interferências
    mask_points_possible = df_corrected_final.iloc[:, 0].astype(str).str.contains("Points Possible", na=False)
    df_corrected_final = df_corrected_final[~mask_points_possible].copy()

    # Criar colunas KC Count e Lab Count
    kc_columns = [col for col in target_columns if re.match(r"^\d+-.*-.*KC", col, re.IGNORECASE) or re.match(r"^Atividade\s*[:|]\s*.+", col, re.IGNORECASE)]
    #lab_columns = [col for col in target_columns if re.match(r"^\d+-.*-.*Lab", col, re.IGNORECASE)]
    lab_columns = [col for col in target_columns if re.search(r"\bLab\b", col, re.IGNORECASE)]


    # Aplicar a condição para ajustar notas de "Lab" se forem > 1.0
    for col in lab_columns:
        df_corrected_final[col] = df_corrected_final[col].apply(lambda x: 1.0 if x > 1.0 else x)

    # Contagem de notas preenchidas
    kc_count_series = df_corrected_final[kc_columns].notna().sum(axis=1)
    lab_count_series = df_corrected_final[lab_columns].notna().sum(axis=1)

    # Soma das notas
    kc_total_sums = df_corrected_final[kc_columns].sum(axis=1)
    lab_total_sums = df_corrected_final[lab_columns].sum(axis=1)

    # Calcular as médias de "KC Count" e "Lab Count" total ####################################################
    kc_mean_total = int(kc_count_series.mean())  # Média total das entradas de KC Count (agora convertendo para inteiro)
    lab_mean_total = int(lab_count_series.mean())  # Média total das entradas de Lab Count (agora convertendo para inteiro)


    # Calcular as médias e garantir que valores nulos sejam substituídos por 0
    kc_scores = (kc_total_sums / kc_count_series).fillna(0)
    lab_scores = ((lab_total_sums / lab_count_series) * 100).fillna(0)  # Multiplicado por 100

    # Calcular o Current Score como a média de Knowledge Checks e Labs
    current_score = ((kc_scores + lab_scores) / 2).fillna(0)


    # Garantir que não existam colunas duplicadas antes da concatenação
    df_corrected_final.drop(columns=["KC Count", "Knowledge Checks Current Score", "Lab Count", "Labs Current Score", "Current Score"], errors='ignore', inplace=True)

    # Atualizar os valores no DataFrame sem fragmentação
    df_corrected_final = pd.concat([
        df_corrected_final,
        kc_count_series.rename("KC Count"),
        kc_scores.rename("Knowledge Checks Current Score").round(2),
        lab_count_series.rename("Lab Count"),
        lab_scores.rename("Labs Current Score").round(2),
        current_score.rename("Current Score").round(2)
    ], axis=1)

    # Adicionar as colunas com a média total fixa, agora com valor inteiro ####################################################
    df_corrected_final["Média KC Count"] = kc_mean_total
    df_corrected_final["Média Lab Count"] = lab_mean_total

# Função para contar atividades feitas
    def count_activities(row):
        count = 0
        for col in target_columns:
            if column_counts[col] >= 5:  # Verifica se pelo menos 5 alunos têm nota nessa coluna
                value = row[col]
                if pd.notna(value) and value != 0 and value / value == 1:  # Verifica se a divisão é 1
                    count += 1
        return count

    # Criar a nova coluna "realizado_aluno" com a contagem correta de atividades feitas
    df_corrected_final["realizado_aluno"] = df_corrected_final.apply(count_activities, axis=1)

    #desempenho em relação as entregas
    # Evitar divisão por zero
    total_mean = kc_mean_total + lab_mean_total if (kc_mean_total + lab_mean_total) > 0 else 1

    # Calcular desempenho das entregas
    df_corrected_final["desempenho_das_entregas"] = df_corrected_final["realizado_aluno"].astype(float) / total_mean

    # Criar a coluna "Unposted Current Score" com os valores de "Current Score" convertidos para inteiro
    df_corrected_final["Unposted Current Score"] = current_score.astype(int)

    # Alterar os valores de "Current Score" para substituir o ponto por vírgula
    #importante para o ranking funcionar
    df_corrected_final["Current Score"] = df_corrected_final["Current Score"].apply(lambda x: str(x).replace('.', ','))

    # Identificar a posição da coluna "Final Points"
    #importante para o ranking funcionar
    final_points_index = df_corrected_final.columns.get_loc("Final Points")

    #importante para o ranking funcionar
    #colocar "Current Score" após "Final Points" e "Unposted Current Score" após "Current Score"
    columns_order = list(df_corrected_final.columns[:final_points_index + 1]) + ['Current Score', 'Unposted Current Score'] + list(df_corrected_final.columns[final_points_index + 1:])
    df_corrected_final = df_corrected_final[columns_order]


    # Caminho do novo arquivo corrigido (usando /tmp/ no Render)
    corrected_file_path_final = "/tmp/corrigido.csv"

    # Salvar o arquivo corrigido mantendo o delimitador correto
    df_corrected_final.to_csv(corrected_file_path_final, sep=detected_delimiter, index=False, encoding='utf-8')

    return corrected_file_path_final