from cx_Freeze import setup, Executable

setup(name="SoColors",version="0.1",description="converts colors.",executables=[Executable("V6_4GUI.py"), Executable("V6_2ListPDFColorMatrix.py"), Executable("QueuePDF.py"), Executable("Configurateur.py")])