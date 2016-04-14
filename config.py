from PySide import QtCore, QtGui

settings = QtCore.QSettings('Green Light Go', 'NASA-TLX')

if __name__ == '__main__':
	import sys
	app = QtGui.QApplication(sys.argv)

	if len(sys.argv) > 1 and 'clear' in sys.argv[1:]:
		settings.clear()
		QtGui.QMessageBox.information(None, 'NASA TLX Settings', 'Your settings have been cleared!')
		exit()
		
	currentFilename = settings.value('Output filename', 'nasa-tlx-output.csv')
	filename = QtGui.QFileDialog.getSaveFileName(None, 'Save file', currentFilename, 'Comma separated values (*.csv, *.txt);;All files (*)')[0]
	if filename != '':
		settings.setValue('Output filename', filename)
		QtGui.QMessageBox.information(None, 'NASA TLX Settings', 'Your settings have been saved!')
