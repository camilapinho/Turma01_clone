import sys
from PyQt5.QtWidgets import QApplication
from model.contamodel import ContaAtivo, ContaPassivo
from controller.contacontroller import ContaController
from view.contaview import MainView
    

def main():
    app = QApplication(sys.argv)
    view = MainView()
    controller = ContaController(view)
    view.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()



    