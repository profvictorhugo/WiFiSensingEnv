import argparse
import os
import sys
from pathlib import Path
import json

def gerar_amostras(n):
        return [num for num in range(n)]


def salvar_em_arquivo(amostras, path, filename):

        os.makedirs(path, exist_ok=True)
        caminho_completo = os.path.join(path, filename)

        with open(caminho_completo, 'w') as f:
                for valor in amostras:
                        f.write(f"{valor}\n")
    
        return str(Path(caminho_completo).resolve())


def main():
    
        parser = argparse.ArgumentParser(description="Gera amostras e salva em arquivo.")
        
        parser.add_argument('-n', type=int, required=True, help='Número de amostras')
        parser.add_argument('-p', type=str, required=True, help='Caminho da pasta para salvar')
        parser.add_argument('-f', type=str, required=True, help='Nome do arquivo')

        args = parser.parse_args()

        try:
                desktop_path = Path.home() / 'Desktop'
                destino = os.path.join(desktop_path, args.p)
                
                amostras = gerar_amostras(args.n)
                caminho = salvar_em_arquivo(amostras, destino, args.f)
                
                print(json.dumps({
                    'quantidade': args.n,
                    'arquivo': caminho,
                    'mensagem': f'{args.n} amostras salvas com sucesso.'
                }))
                
        except Exception as e:
                print(f"Erro ao gerar/salvar amostras: {str(e)}", file=sys.stderr)
                sys.exit(1)


if __name__ == '__main__':
        main()