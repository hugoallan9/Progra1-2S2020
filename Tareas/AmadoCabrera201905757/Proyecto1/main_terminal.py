from listas_reproduccion import *
import os
import subprocess
import time

run = True

# Main loop
directorio_csvs()
directorio_repor()
while run:
    subprocess.run('clear' ,shell=True)
    print(header)
    print(instrucciones)
    ans1 = input(pregunta)
    ans1 = ans1.strip()
    ans1 = ans1.replace('\ ', ' ')
    if ans1 == 'quit()' or ans1 == 'Quit()' or ans1 == 'QUIT()':
        run = False
        subprocess.run('clear' ,shell=True)
    else:
        try:
            os.chdir(ans1)
        except:
            print('\nSu entrada no es válida')
            time.sleep(1)
            continue
        print('\nBuscando listas de reproducción en')
        print(ans1)
        time.sleep(2)
        subprocess.run('clear' ,shell=True)
        print(cabecera_documentos)
        i1 = 0
        lista_docs = []
        for f in os.listdir():
            file_name, file_ext = os.path.splitext(f)
            if file_ext == '.xml':
                doc = Documento(f)
                doc.probability_playlist()
                if doc.posible_playlist:
                    print(f'  {i1+1})', end=' ')
                    press(f, bt_color='green')
                else:
                    print(f'  {i1+1})', end=' ')
                    press(f, bt_color='red')
                lista_docs.append(f)
                i1 += 1
        print(mensaje_documentos)
        print("Seleccione por indice el documento que desea parsear")
        try:
            ans2 = int(input(pregunta))
            musica_principal = Documento(lista_docs[ans2-1])
            musica_principal.nombre_playlist()
        except:
            print("Parece que hubo un error, reinicie proceso")
            time.sleep(1)
            continue
        print('\nRevisando el documento:', end=' ')
        print(lista_docs[ans2-1])
        time.sleep(2)
        subprocess.run('clear', shell=True)
        try:
            barra_carga(musica_principal)
            musica_principal.make_report()
        except:
            subprocess.run('clear', shell=True)
            print('Hubo un error')
            time.sleep(1)
            continue
        correcto1 = False
        while not correcto1:
            print('\n¿Desea elevorar una gráfica? [y/n]')
            ans3 = input(pregunta)
            ans3 = ans3.lower().strip()
            if ans3 == 'y':
                try:
                    print('Selecione la cantidad de columnas')
                    ans4 = int(input(pregunta))
                    print('(Cierre la imagen para que el programa pueda continuar)')
                    musica_principal.make_histogram(ans4)
                    correcto1 = True
                except Exception as e:
                    print(e)
                    time.sleep(5)
                    pass
            elif ans3 == 'n':
                correcto1 = True
            subprocess.run('clear', shell=True)
            musica_principal.make_report()
        correcto2 = False
        while not correcto2:
            print('\n¿Desea guardar el reporte? [y/n]')
            ans5 = input(pregunta)
            ans5 = ans5.lower().strip()
            if ans5 == 'y':
                print('Desea imprimir en:')
                print('  1) LaTeX\n  2) Markdown\n  3) Pdf')
                print('Seleccione el indice')
                try:
                    ans6 = int(input(pregunta))
                    if ans6 == 1:
                        musica_principal.report = 'LaTeX'
                    elif ans6 == 2:
                        musica_principal.report = 'Markdown'
                    elif ans6 == 3:
                        musica_principal.report = 'Pdf'
                    else:
                        pass
                    correcto2 = True
                except:
                    pass
            elif ans5 == 'n':
                correcto2 = True
            musica_principal.save_report()
            subprocess.run('clear', shell=True)
            musica_principal.make_report()
        print('\nSe creará un reporte en CSV de la lista de reproducción')
        musica_principal.write_csv()
        loquesea = input('\nPresione (Enter) para continuar')
        musica_principal.restart()

#