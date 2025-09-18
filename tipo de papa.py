import sys
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QMessageBox,
    QGroupBox,
    QRadioButton,
    QButtonGroup,
)
from PySide6.QtCore import Qt


class SistemaVentaPapas(QMainWindow):
    def __init__(self):
        super().__init__()

        # Constantes del negocio (mismo que tu código original)
        self.PASTUSA_1 = 2000
        self.PASTUSA_2 = 3000
        self.SABANERA_1 = 4000
        self.SABANERA_2 = 5000

        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Sistema de Venta de Papas - Fedepapa")
        self.setGeometry(200, 200, 600, 500)

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Título principal
        titulo = QLabel("🥔 Sistema de Venta de Papas")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet(
            """
            font-size: 24px; 
            font-weight: bold; 
            color: #2c3e50; 
            margin: 10px;
            background-color: #ecf0f1;
            padding: 15px;
            border-radius: 10px;
        """
        )
        layout.addWidget(titulo)

        # Sección 1: Selección de tipo de papa
        self.setup_tipo_papa_section(layout)

        # Sección 2: Datos de venta
        self.setup_datos_venta_section(layout)

        # Sección 3: Selección de tamaño
        self.setup_tamano_section(layout)

        # Botones de acción
        self.setup_buttons(layout)

        # Área de resultados
        self.setup_resultado_section(layout)

        # Aplicar estilos globales
        self.apply_styles()

    def setup_tipo_papa_section(self, layout):
        # Grupo para tipo de papa
        grupo_tipo = QGroupBox("1. Seleccione el tipo de papa")
        grupo_tipo.setStyleSheet("QGroupBox { font-weight: bold; }")
        layout_tipo = QVBoxLayout()

        # Radio buttons para tipo de papa
        self.tipo_papa_group = QButtonGroup()

        self.radio_pastusa = QRadioButton("Pastusa")
        self.radio_sabanera = QRadioButton("Sabanera")

        self.tipo_papa_group.addButton(self.radio_pastusa, 1)
        self.tipo_papa_group.addButton(self.radio_sabanera, 2)

        layout_tipo.addWidget(self.radio_pastusa)
        layout_tipo.addWidget(self.radio_sabanera)

        grupo_tipo.setLayout(layout_tipo)
        layout.addWidget(grupo_tipo)

    def setup_datos_venta_section(self, layout):
        # Grupo para datos de venta
        grupo_venta = QGroupBox("2. Datos de la venta")
        grupo_venta.setStyleSheet("QGroupBox { font-weight: bold; }")
        layout_venta = QVBoxLayout()

        # Valor por kilo
        layout_valor = QHBoxLayout()
        layout_valor.addWidget(QLabel("Valor por kilo ($):"))
        self.entry_valor_kilo = QLineEdit()
        self.entry_valor_kilo.setPlaceholderText("Ej: 1500")
        layout_valor.addWidget(self.entry_valor_kilo)
        layout_venta.addLayout(layout_valor)

        # Kilos vendidos
        layout_kilos = QHBoxLayout()
        layout_kilos.addWidget(QLabel("Kilos vendidos:"))
        self.entry_kilos = QLineEdit()
        self.entry_kilos.setPlaceholderText("Ej: 50")
        layout_kilos.addWidget(self.entry_kilos)
        layout_venta.addLayout(layout_kilos)

        grupo_venta.setLayout(layout_venta)
        layout.addWidget(grupo_venta)

    def setup_tamano_section(self, layout):
        # Grupo para tamaño
        grupo_tamano = QGroupBox("3. Seleccione el tamaño")
        grupo_tamano.setStyleSheet("QGroupBox { font-weight: bold; }")
        layout_tamano = QVBoxLayout()

        # Radio buttons para tamaño
        self.tamano_group = QButtonGroup()

        self.radio_tamano_1 = QRadioButton("Tamaño 1")
        self.radio_tamano_2 = QRadioButton("Tamaño 2")

        self.tamano_group.addButton(self.radio_tamano_1, 1)
        self.tamano_group.addButton(self.radio_tamano_2, 2)

        layout_tamano.addWidget(self.radio_tamano_1)
        layout_tamano.addWidget(self.radio_tamano_2)

        grupo_tamano.setLayout(layout_tamano)
        layout.addWidget(grupo_tamano)

    def setup_buttons(self, layout):
        # Layout para botones
        button_layout = QHBoxLayout()

        self.btn_calcular = QPushButton("💰 Calcular Total")
        self.btn_calcular.clicked.connect(self.calcular_total)

        self.btn_limpiar = QPushButton("🗑️ Limpiar")
        self.btn_limpiar.clicked.connect(self.limpiar_campos)

        button_layout.addWidget(self.btn_calcular)
        button_layout.addWidget(self.btn_limpiar)

        layout.addLayout(button_layout)

    def setup_resultado_section(self, layout):
        # Área de resultados
        resultado_label = QLabel("Resultado del cálculo:")
        resultado_label.setStyleSheet("font-weight: bold; margin-top: 20px;")
        layout.addWidget(resultado_label)

        self.text_resultado = QTextEdit()
        self.text_resultado.setMaximumHeight(150)
        self.text_resultado.setStyleSheet(
            """
            QTextEdit {
                background-color: #f8f9fa;
                border: 2px solid #dee2e6;
                border-radius: 8px;
                padding: 10px;
                font-family: 'Courier New', monospace;
            }
        """
        )
        layout.addWidget(self.text_resultado)

    def calcular_total(self):
        try:
            # Validar selección de tipo de papa
            tipo_seleccionado = self.tipo_papa_group.checkedId()
            if tipo_seleccionado == -1:
                QMessageBox.warning(
                    self, "Error", "Por favor seleccione un tipo de papa"
                )
                return

            # Validar selección de tamaño
            tamano_seleccionado = self.tamano_group.checkedId()
            if tamano_seleccionado == -1:
                QMessageBox.warning(self, "Error", "Por favor seleccione un tamaño")
                return

            # Validar valor por kilo
            try:
                valor_kilo = float(self.entry_valor_kilo.text())
                if valor_kilo <= 0:
                    raise ValueError()
            except ValueError:
                QMessageBox.critical(
                    self, "Error", "Ingrese un valor por kilo válido (mayor a 0)"
                )
                return

            # Validar kilos vendidos
            try:
                kilos_vendidos = float(self.entry_kilos.text())
                if kilos_vendidos <= 0:
                    raise ValueError()
            except ValueError:
                QMessageBox.critical(
                    self, "Error", "Ingrese una cantidad de kilos válida (mayor a 0)"
                )
                return

            # Realizar cálculos (misma lógica que tu código original)
            valor_neto = valor_kilo * kilos_vendidos

            # Determinar tipo de papa seleccionado
            nombre_tipo = "Pastusa" if tipo_seleccionado == 1 else "Sabanera"

            # Calcular ajuste según tipo y tamaño
            ajuste = 0
            descripcion_ajuste = ""

            if tipo_seleccionado == 1:  # Pastusa
                if tamano_seleccionado == 1:
                    ajuste = self.PASTUSA_1
                    descripcion_ajuste = f"Recargo Pastusa Tamaño 1: +${ajuste:,.0f}"
                else:
                    ajuste = self.PASTUSA_2
                    descripcion_ajuste = f"Recargo Pastusa Tamaño 2: +${ajuste:,.0f}"
                valor_final = valor_neto + ajuste
            else:  # Sabanera
                if tamano_seleccionado == 1:
                    ajuste = self.SABANERA_1
                    descripcion_ajuste = f"Descuento Sabanera Tamaño 1: -${ajuste:,.0f}"
                else:
                    ajuste = self.SABANERA_2
                    descripcion_ajuste = f"Descuento Sabanera Tamaño 2: -${ajuste:,.0f}"
                valor_final = valor_neto - ajuste

            # Mostrar resultado detallado
            resultado = f"""
=== RESUMEN DE VENTA ===
Tipo de papa: {nombre_tipo}
Tamaño: {tamano_seleccionado}
Valor por kilo: ${valor_kilo:,.0f}
Kilos vendidos: {kilos_vendidos:,.2f} kg

Valor base: ${valor_neto:,.0f}
{descripcion_ajuste}

💰 TOTAL A PAGAR: ${valor_final:,.0f}
===============================
            """.strip()

            self.text_resultado.clear()
            self.text_resultado.append(resultado)

            # Mensaje de confirmación
            QMessageBox.information(
                self, "Cálculo Completado", f"Total calculado: ${valor_final:,.0f}"
            )

        except Exception as e:
            QMessageBox.critical(
                self, "Error inesperado", f"Ha ocurrido un error: {str(e)}"
            )

    def limpiar_campos(self):
        # Limpiar todos los campos
        self.entry_valor_kilo.clear()
        self.entry_kilos.clear()
        self.text_resultado.clear()

        # Deseleccionar radio buttons
        self.tipo_papa_group.setExclusive(False)
        self.radio_pastusa.setChecked(False)
        self.radio_sabanera.setChecked(False)
        self.tipo_papa_group.setExclusive(True)

        self.tamano_group.setExclusive(False)
        self.radio_tamano_1.setChecked(False)
        self.radio_tamano_2.setChecked(False)
        self.tamano_group.setExclusive(True)

        QMessageBox.information(self, "Limpiar", "Todos los campos han sido limpiados")

    def apply_styles(self):
        self.setStyleSheet(
            """
            QMainWindow {
                background-color: #ffffff;
            }
            QGroupBox {
                font-size: 14px;
                border: 2px solid #bdc3c7;
                border-radius: 10px;
                margin: 10px 0px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #2c3e50;
            }
            QLabel {
                color: #2c3e50;
                font-size: 12px;
            }
            QLineEdit {
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                padding: 8px;
                font-size: 12px;
                margin: 2px;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
            QRadioButton {
                color: #2c3e50;
                font-size: 12px;
                margin: 5px;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 12px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
        """
        )


def main():
    app = QApplication(sys.argv)

    # Configurar la aplicación
    app.setApplicationName("Sistema Fedepapa")
    app.setApplicationVersion("1.0")

    ventana = SistemaVentaPapas()
    ventana.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
