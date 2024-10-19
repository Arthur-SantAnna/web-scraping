import PySimpleGUI as sg


def main():
    # All the stuff inside your window.
    layout = [
        [sg.Text("Título do produto:")],
        [sg.InputText(key='-TITULO-')],
        [sg.Text("Link do produto:")],
        [sg.InputText(key='-LINK-')],
        [sg.Text("Preço alvo:")],
        [sg.InputText(key='-PRECOALVO-')],
        [sg.Text("", size=(30, 1), key='-ERROR-', text_color='red')],
        [sg.Button('Enviar'), sg.Button('Cancelar')]
    ]

    # Create the Window
    window = sg.Window('Web Scraping', layout)

    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()

        # if user closes window or clicks cancel
        if event == sg.WIN_CLOSED or event == 'Cancelar':
            break

        if event == 'Enviar':
            if values['-LINK-'].strip() and values['-PRECOALVO-'].strip():
                print('Link: ', values['-LINK-'])
                print('Preço alvo:', values['-PRECOALVO-'])
                # Clear input fields
                window['-LINK-'].update('')
                window['-PRECOALVO-'].update('')
                # Clear error message
                window['-ERROR-'].update('')
            else:
                # Show error message
                window['-ERROR-'].update('Por favor, preencha todos os campos!')

    window.close()


if __name__ == '__main__':
    main()
