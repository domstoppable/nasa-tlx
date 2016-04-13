import random

from PySide import QtGui, QtCore

factors = [
	{
		"name": "Mental Demand",
		"description": '''
			How much mental and perceptual activity was required?
			Was the task easy or demanding, simple or complex?'''
	},{
		"name": "Physical Demand",
		"description": '''
			How much physical activity was required?
			Was the task easy or demanding, slack or strenuous?'''
	}, {
		"name": "Temporal Demand",
		"description": '''
			How much time pressure did you feel due to the pace at which
			the tasks or task elements occurred? Was the pace slow or rapid?'''
	}, {
		"name": "Performance",
		"description": '''
			How successful were you in performing the task?
			How satisfied were you with your performance?'''
	}, {
		"name": "Frustration",
		"description": '''
			How irritated, stressed, and annoyed versus
			content, relaxed, and complacent did you feel during the task?'''
	}, {
		"name": "Effort",
		"description": '''
			How hard did you have to work (mentally and physically)
			to accomplish your level of performance?'''
	},
]

class DemandSlider(QtGui.QWidget):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setLayout(QtGui.QVBoxLayout())
		
		slider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
		slider.setRange(1, 21)
		slider.setTickInterval(1)
		slider.setValue(11)
		slider.setTickPosition(slider.TicksBothSides)
		
		self.layout().addWidget(slider)
		
		labels = QtGui.QWidget(self)
		labels.setLayout(QtGui.QHBoxLayout())
		labels.layout().addWidget(QtGui.QLabel('Low'))
		label = QtGui.QLabel('High')
		label.setAlignment(QtCore.Qt.AlignRight)
		labels.layout().addWidget(label)
		self.layout().addWidget(labels)

class ComparisonPage(QtGui.QWidget):
	chosen = QtCore.Signal(str, object)
	cleared = QtCore.Signal(object)

	def __init__(self, options):
		super().__init__()
		self.setLayout(QtGui.QHBoxLayout())
		self.options = options
		self.buttons = []
		for o in self.options:
			b = QtGui.QPushButton(o)
			b.setCheckable(True)
			b.clicked.connect(self.onChoose)
			b.setAutoExclusive(True)
			self.buttons.append(b)
			self.layout().addWidget(b)
			
	def getChoice(self):
		for b in self.buttons:
			if b.isChecked():
				return b.text()

	def onChoose(self):
		for b in self.buttons:
			if b.isChecked():
				self.chosen.emit(b.text(), self.options)
				return
		self.cleared.emit(self.options)
		
class TLXWindow(QtGui.QWidget):
	def __init__(self):
		super().__init__()
		
		self.setWindowTitle('NASA TLX')
		font = self.font()
		font.setPointSize(14)
		self.setFont(font)
		self.setLayout(QtGui.QVBoxLayout())
		
		self.createTabs()
		self.createNavigation()
		
	def createTabs(self):
		self.tabs = QtGui.QTabWidget(self)
		
		self.createParticipantPage()
		self.createFactorsPage()
		self.createComparisonPages()
		self.layout().addWidget(self.tabs)
		
	def createNavigation(self):
		container = QtGui.QWidget(self)
		container.setLayout(QtGui.QHBoxLayout())
		
		self.previousButton = QtGui.QPushButton(' Previous')
		self.previousButton.clicked.connect(self.gotoPreviousPage)
		self.previousButton.setDisabled(True)
		container.layout().addWidget(self.previousButton)
		
		container.layout().addWidget(QtGui.QLabel(''))
		container.layout().addWidget(QtGui.QLabel(''))
		
		self.nextButton = QtGui.QPushButton('Next ')
		self.nextButton.clicked.connect(self.gotoNextPage)
		container.layout().addWidget(self.nextButton)
		
		self.layout().addWidget(container)
		
	def createParticipantPage(self):
		container = QtGui.QWidget()
		container.setLayout(QtGui.QVBoxLayout())
		container.layout().setAlignment(QtCore.Qt.AlignVCenter)
		container.layout().addWidget(QtGui.QLabel('<b>Participant ID</b>'))
		container.layout().addWidget(QtGui.QLineEdit())
		
		self.tabs.addTab(container, 'Participant Info')
		
	def createFactorsPage(self):
		w = QtGui.QWidget()
		layout = QtGui.QFormLayout()
		for f in factors:
			slider = DemandSlider()
			layout.addRow('<br><b>%s</b>' % f['name'], None)
			description = '<i>%s</i>' % f['description'].strip().replace('\n', '<br>')
			layout.addRow(description, slider)
			
		w.setLayout(layout)
		self.tabs.addTab(w, 'Factors')
		
	def createComparisonPages(self):
		self.comparisonPages = []
		comparisons = []
		for i, f1 in enumerate(factors):
			for j in range(i+1, len(factors)):
				f2 = factors[j]
				pair = [f1['name'], f2['name']]
				random.shuffle(pair)
				comparisons.append(pair)
				
		random.shuffle(comparisons)
		for c in comparisons:
			page = ComparisonPage(c)
			self.tabs.addTab(page, '%s vs %s' % (c[0], c[1]))
			page.chosen.connect(self.onComparisonPicked)
			self.comparisonPages.append(page)
	
	def onComparisonPicked(self, choice, options):
		print(choice, ' from ', options)
		self.gotoNextPage()
		
	def gotoNextPage(self):
		current = self.tabs.currentIndex()
		if current < self.tabs.count():
			self.tabs.setCurrentIndex(current+1)
			self.previousButton.setDisabled(False)
			if current == self.tabs.count() - 2:
				self.nextButton.setDisabled(True)
		
	def gotoPreviousPage(self):
		current = self.tabs.currentIndex()
		if current > -1:
			self.tabs.setCurrentIndex(current-1)
			self.nextButton.setDisabled(False)
			if current == 1:
				self.previousButton.setDisabled(True)
		


if __name__ == '__main__':
	import sys

	app = QtGui.QApplication(sys.argv)
	appWindow = TLXWindow()
	appWindow.show()
	sys.exit(app.exec_())
